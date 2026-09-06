import json
import time
import tkinter as tk
from types import SimpleNamespace

import pytest

from fca import config as C
from fca import secrets
from fca.app import App, TAB_SPECS


@pytest.fixture(scope="module")
def app():
    try: instance = App()
    except tk.TclError: pytest.skip("No Windows display")
    instance.withdraw(); instance.update(); yield instance; instance.on_close()


def test_window_opens_and_all_tabs_build(app):
    assert len(app._tabs) == len(TAB_SPECS) == 18
    for key, _cls, _icon, _group in TAB_SPECS:
        app.select(key); app.update(); assert app.current_page().winfo_exists()


def test_language_switch_is_immediate_and_persistent(app):
    app.select("tab.study"); app.set_ui_language("en"); app.update()
    assert app.page_title.cget("text") == "Spaced Review" and app.language_var.get() == "English"
    assert C.load_settings()["ui_lang"] == "en"
    app.set_ui_language("fr"); app.update()
    assert app.page_title.cget("text") == "Révision espacée" and app.language_var.get() == "Français"


def test_card_session_can_complete(app):
    app.set_ui_language("tr"); app.select("tab.study"); tab = app.current_page(); tab.limit.set(5); tab.start("new")
    assert len(tab.session) == 5
    for _ in range(5): tab.reveal(); tab.grade(4); app.update()
    assert tab.session == []


def test_exam_can_generate_and_finish(app):
    app.select("tab.exam"); tab = app.current_page(); tab.count.set(5); tab.start(); assert len(tab.questions) == 5
    while tab.idx < len(tab.questions):
        tab.choice.set(tab.questions[tab.idx].answer); tab.submit(); app.update()
    row = app.repos.db.one("SELECT score FROM exams WHERE id=?", (tab.exam_id,)); assert row["score"] == 100.0


def test_ai_offline_page_does_not_crash(app):
    app.settings["ai_enabled"] = False; app.select("tab.ai"); tab = app.current_page(); tab.input.insert("1.0", "Test"); tab.send(); app.update()
    assert app.t("ai.status_off") in tab.output.get("1.0", "end")


def _pump(app, predicate, timeout=10.0):
    """Run the Tk event loop until ``predicate()`` holds (background AI work lands via app.run_async)."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.update()
        if predicate(): return True
        time.sleep(0.05)
    return False


def _ai_rows(tab):
    return [i for i in tab.tree.get_children() if tab.tree.set(i, "src") == tab.t("dict.ai_source")]


def test_dictionary_falls_back_to_ai_and_caches_results(app, mock_ai):
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "local", "dict_ai_autosave": True}); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    assert tab.policy.get() == app.t("dict.ai_local")
    tab.query.set("zzqqxxgrignotage"); tab.search()
    assert app.t("dict.ai_asking") in tab.ai_out.get("1.0", "end")
    assert _pump(app, lambda: _ai_rows(tab)), "AI results did not arrive"
    entry = tab.current(); sample = mock_ai.sample[0]
    assert entry is not None and entry.source == "ai" and entry.headword == sample["headword"]
    assert sample["translation"].split("; ")[0] in tab.w_trans.cget("text") and sample["example"] in tab.w_example.cget("text")
    assert tab.w_note.cget("text") == sample["note"] and app.t("dict.ai_source") in tab.w_meta.cget("text")
    out = tab.ai_out.get("1.0", "end")
    assert app.t("dict.answered_by") in out and mock_ai.MODEL in out and app.t("dict.ai_local") in out and sample["headword"] in out
    assert mock_ai.count("/chat/completions") == 1 and mock_ai.chats[-1]["auth"] == ""
    assert not tab.save_btn.winfo_manager()                                          # autosaved -> no extra button
    # cached: persisted with source "ai", instantly found offline next time, no second request
    assert app.repos.dictionary.count("ai") >= 1 and any(r["source"] == "ai" and r["example"] == sample["example"] for r in app.repos.dictionary.all())
    tab.query.set(sample["headword"]); tab.search(); app.update()
    assert tab.current().source == "ai" and mock_ai.count("/chat/completions") == 1
    assert _pump(app, lambda: tab.ai_state.cget("text") == app.t("dict.state_local"), 5)
    # "Ask AI" merges AI entries on top of local hits and works for word-bank export with the example sentence
    tab.query.set({"de": "Haus", "fr": "maison", "en": "house"}[C.TARGET_LANG]); tab.search(); app.update()
    assert tab.current().source == "builtin"
    tab.ask_ai(); assert _pump(app, lambda: mock_ai.count("/chat/completions") == 2 and _ai_rows(tab))
    assert tab.tree.get_children()[0] in _ai_rows(tab) and len(tab.results) > len(mock_ai.sample)
    tab.add_to_bank(); word = app.repos.words.search(sample["headword"])[0]
    assert word["example_target"] == sample["example"]


def test_dictionary_policy_off_makes_no_ai_request(app, mock_ai):
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "off"}); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    assert tab.policy.get() == app.t("dict.ai_off") and tab.ai_state.cget("text") == app.t("dict.state_off")
    tab.query.set("qqzzxxnothing"); tab.search()
    _pump(app, lambda: False, 1.0)
    assert mock_ai.count("/chat/completions") == 0 and tab.tree.get_children() == ()
    assert app.t("dict.no_result") in tab.ai_out.get("1.0", "end")
    tab.ask_ai(); app.update()
    assert app.t("ai.status_off") in tab.ai_out.get("1.0", "end") and mock_ai.count() == 0
    # unreachable local provider: offline text, no crash, no hang
    app.settings.update({"dict_ai": "local", "ai_base": "http://127.0.0.1:9"}); app.refresh_ai_clients()
    tab.query.set("qqzzxxnothing"); tab.search()
    assert _pump(app, lambda: app.t("ai.status_off") in tab.ai_out.get("1.0", "end"), 5)
    tab.policy.set(app.t("dict.ai_auto")); tab._policy_changed()
    assert C.load_settings()["dict_ai"] == "auto"


def test_dictionary_key_release_without_a_text_change_keeps_the_pending_ai_answer(app, mock_ai):
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "local", "dict_ai_autosave": False}); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    answer = '```json\n[{"headword": "Qqzzslow", "pos": "n", "extra": "m", "translation": "slow-thing", "example": "", "note": ""}]\n```'
    def slow(_body): time.sleep(0.5); return answer
    mock_ai.content = slow
    tab.query.set("qqzzslow"); tab.search()
    for keysym in ("Shift_L", "Control_L", "Left", "Escape", "Caps_Lock", "Return"): tab._on_key(SimpleNamespace(keysym=keysym))
    assert app.t("dict.ai_asking") in tab.ai_out.get("1.0", "end")
    assert _pump(app, lambda: _ai_rows(tab)), "answer discarded after a key release that did not change the query"
    assert tab.current().headword == "Qqzzslow" and mock_ai.count("/chat/completions") == 1
    # a different query does supersede the pending answer - and takes the progress text with it
    tab.query.set("qqzzslow2"); tab.search()
    assert app.t("dict.ai_asking") in tab.ai_out.get("1.0", "end") and app.status.get() == app.t("dict.ai_asking")
    tab.query.set("maison"); tab._on_key(SimpleNamespace(keysym="n"))
    assert app.t("dict.ai_asking") not in tab.ai_out.get("1.0", "end") and app.status.get() == app.t("g.ready")
    assert _pump(app, lambda: mock_ai.count("/chat/completions") == 2); _pump(app, lambda: False, 1.2)    # let the late answer land
    heads = [tab.tree.set(i, "head") for i in tab.tree.get_children()]
    assert "maison" in heads and "Qqzzslow" not in heads and app.t("dict.ai_asking") not in tab.ai_out.get("1.0", "end")


def test_settings_page_follows_the_policy_chosen_in_the_dictionary_toolbar(app):
    app.select("tab.settings"); stab = app.current_page(); stab.dict_ai.set(app.t("dict.ai_auto")); stab.save(); app.update()
    app.select("tab.dictionary"); dtab = app.current_page(); dtab.policy.set(app.t("dict.ai_off")); dtab._policy_changed(); app.update()
    assert app.settings["dict_ai"] == "off" and C.load_settings()["dict_ai"] == "off"
    app.settings["alt_model"] = "qqzz/model"; C.save_settings(app.settings)                       # any setting changed elsewhere
    app.select("tab.settings"); stab = app.current_page(); app.update()
    assert stab.dict_ai.get() == app.t("dict.ai_off") and stab.alt_model.get() == "qqzz/model"     # the form shows the live settings
    stab.goal.set(33); stab.save(); app.update()                                                   # saving an unrelated change keeps the toolbar choice
    assert app.settings["dict_ai"] == "off" and C.load_settings()["dict_ai"] == "off" and C.load_settings()["daily_goal"] == 33
    app.select("tab.dictionary"); assert app.current_page().policy.get() == app.t("dict.ai_off")
    app.settings.update({"dict_ai": "auto", "daily_goal": C.DEFAULT_SETTINGS["daily_goal"], "alt_model": C.ALT_MODEL_DEFAULT}); C.save_settings(app.settings)


def test_settings_alt_endpoint_keeps_key_out_of_settings_and_drives_dictionary(app, mock_ai):
    app.select("tab.settings"); tab = app.current_page(); app.update()
    assert tab.key_state.cget("text") == app.t("settings.alt_key_none")
    tab.alt_enabled.set(True); tab.alt_base.set(mock_ai.base); tab.alt_model.set(mock_ai.MODEL); tab.alt_key.set("nvapi-ui-secret")
    tab.dict_ai.set(app.t("dict.ai_alt")); tab.dict_autosave.set(False); tab.save(); app.update()
    assert "nvapi-ui-secret" not in C.SETTINGS_PATH.read_text(encoding="utf-8")
    assert secrets.get_secret("alt_api_key") == "nvapi-ui-secret" and tab.alt_key.get() == ""
    assert tab.key_state.cget("text") == app.t("settings.alt_key_saved")
    assert app.ai_alt.api_key == "nvapi-ui-secret" and app.ai_alt.base == mock_ai.base and app.ai_alt.model == mock_ai.MODEL
    assert C.load_settings()["dict_ai"] == "alt" and C.load_settings()["alt_enabled"] is True
    tab.test_alt(); assert _pump(app, lambda: app.t("settings.alt_ok") in tab.alt_result.cget("text"), 5)
    assert mock_ai.requests[-1]["auth"] == "Bearer nvapi-ui-secret"
    # dictionary now answers through the alternative client with the bearer key; autosave off -> "Save" button
    app.select("tab.dictionary"); dtab = app.current_page(); app.update()
    assert dtab.policy.get() == app.t("dict.ai_alt")
    mock_ai.content = '```json\n[{"headword": "Qqzzalt", "pos": "n", "extra": "", "translation": "alt-thing", "example": "Qqzzalt!", "note": ""}]\n```'
    dtab.query.set("qqzzalt"); dtab.search()
    assert _pump(app, lambda: _ai_rows(dtab))
    assert mock_ai.chats[-1]["auth"] == "Bearer nvapi-ui-secret" and mock_ai.chats[-1]["body"]["model"] == mock_ai.MODEL
    assert dtab.current().headword == "Qqzzalt" and dtab.current().source == "ai"
    assert app.t("dict.ai_alt") in dtab.ai_out.get("1.0", "end") and dtab.save_btn.winfo_manager()   # autosave off -> not stored yet
    before = app.repos.dictionary.count("ai"); dtab.save_ai_entry(); app.update()
    assert app.repos.dictionary.count("ai") == before + 1 and not dtab.save_btn.winfo_manager()
    assert any(r["headword"] == "Qqzzalt" and r["source"] == "ai" and r["example"] == "Qqzzalt!" for r in app.repos.dictionary.all())
    app.select("tab.settings"); tab = app.current_page(); tab.delete_key(); app.update()
    assert secrets.get_secret("alt_api_key") == "" and app.ai_alt.api_key == "" and tab.key_state.cget("text") == app.t("settings.alt_key_none")
    app.settings.update({"alt_enabled": False, "dict_ai": "auto", "dict_ai_autosave": True}); C.save_settings(app.settings)


def _word():
    return {"de": "Haus", "fr": "maison", "en": "house"}[C.TARGET_LANG]


def _cols(tab):
    value = tab.tree.cget("displaycolumns")
    return tuple(value) if isinstance(value, (tuple, list)) else tuple(str(value).split())


def test_dictionary_direction_selector_reruns_search_persists_and_fills_turkish(app, mock_ai):
    from fca import dictionary as D
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "off", "dict_ai_autosave": True, "alt_enabled": False, "dict_direction": "auto"})
    C.save_settings(app.settings); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    word, target, other = _word(), C.TARGET_LANG, D.OTHER_LANG
    t2o, o2t = f"{target}2{other}", f"{other}2{target}"
    assert tab.direction.get() == app.t("dict.dir_auto") and set(tab.direction_box.cget("values")) == set(tab._direction_labels.values())
    assert _cols(tab)[:2] == ("head", "trans") and ("tr" in _cols(tab)) is D.HAS_TR
    tab.query.set(word); tab.search(); app.update()
    assert tab.dir_label.cget("text") == f"{target.upper()} → {other.upper()}" and tab.current().headword == word
    assert tab.w_trans.cget("text").startswith(app.t("dict.translation") + ":") and (tab.w_tr.winfo_manager() != "") is D.HAS_TR
    # switching the combobox re-runs the query in the fixed direction, updates the label and persists the setting
    tab.direction.set(tab._direction_labels[o2t]); tab._direction_changed(); app.update()
    assert app.settings["dict_direction"] == o2t and C.load_settings()["dict_direction"] == o2t
    assert tab.dir_label.cget("text") == D.direction_text(o2t) == f"{other.upper()} → {target.upper()}"
    assert tab.tree.get_children() == () and app.t("dict.no_result") in tab.ai_out.get("1.0", "end") and mock_ai.count() == 0   # only the source side is searched; AI off
    tab.direction.set(tab._direction_labels[t2o]); tab._direction_changed(); app.update()
    assert C.load_settings()["dict_direction"] == t2o and tab.dir_label.cget("text") == D.direction_text(t2o) and tab.current().headword == word
    app.settings["dict_direction"] = "auto"; C.save_settings(app.settings); app.select("tab.settings"); app.select("tab.dictionary"); app.update()
    assert tab.direction.get() == app.t("dict.dir_auto")                                   # picked up on show, like the AI policy
    if not D.HAS_TR:
        return
    # a *2tr search that finds an entry without a Turkish gloss asks the AI and writes the gloss into that entry (no duplicate).
    # The query is always set before the direction is switched: switching re-runs whatever query is in the box.
    t2tr, tr2t = f"{target}2tr", f"tr2{target}"
    app.repos.dictionary.add("Qqzzhaus", "qqzz-house", "n", "", "", "user", ""); tab.dict.extend([D.Entry("Qqzzhaus", "n", "", "qqzz-house", "", D.SOURCE_USER)])
    app.settings["dict_ai"] = "local"; C.save_settings(app.settings); tab.on_show()
    mock_ai.content = json.dumps([{"headword": "Qqzzhaus", "pos": "n", "extra": "", "translation_en": "qqzz-house", "translation_tr": "qqzz-ev; qqzz-hane", "example": "", "note": ""}])
    tab.query.set("Qqzzhaus"); tab.direction.set(tab._direction_labels[t2tr]); tab._direction_changed()
    first = tab.tree.get_children()[0]                                                       # synchronous part: listed with "—", AI pending
    assert _cols(tab)[:3] == ("head", "tr", "trans") and tab.tree.set(first, "tr") == "—" and app.status.get() == app.t("dict.tr_missing")
    assert tab.w_tr.cget("text") == f"{app.t('dict.turkish')}: —" and tab.dir_label.cget("text") == D.direction_text(t2tr)
    assert _pump(app, lambda: tab.current() is not None and tab.current().tr == "qqzz-ev; qqzz-hane"), "Turkish gloss was not filled"
    assert mock_ai.count("/chat/completions") == 1 and tab.current().source == "user" and not _ai_rows(tab) and not tab.save_btn.winfo_manager()
    rows = [r for r in app.repos.dictionary.all() if r["headword"] == "Qqzzhaus"]
    assert [(r["source"], r["tr"]) for r in rows] == [("user", "qqzz-ev; qqzz-hane")]           # updated in place, not duplicated
    assert tab.tree.set(tab.tree.get_children()[0], "tr") == "qqzz-ev; qqzz-hane" and "qqzz-ev" in tab.w_tr.cget("text")
    assert app.t("dict.tr_filled") in app.status.get() and app.t("dict.turkish") in tab.ai_out.get("1.0", "end") and "qqzz-hane" in tab.ai_out.get("1.0", "end")
    tab.query.set("qqzz-hane"); tab.direction.set(tab._direction_labels[tr2t]); tab._direction_changed(); app.update()
    assert tab.dir_label.cget("text") == D.direction_text(tr2t) and tab.current().headword == "Qqzzhaus" and mock_ai.count("/chat/completions") == 1
    tab.add_to_bank(); bank = app.repos.words.search("Qqzzhaus")[0]
    assert bank["tr"] == "qqzz-ev" and bank["en"] == "qqzz-house"                                # first Turkish sense feeds the word bank
    # a *2tr search on an entry that already has its gloss never asks the AI
    tab.query.set("Qqzzhaus"); tab.direction.set(tab._direction_labels[t2tr]); tab._direction_changed(); _pump(app, lambda: False, 0.5)
    assert mock_ai.count("/chat/completions") == 1 and tab.current().tr == "qqzz-ev; qqzz-hane"
    # autosave off: nothing is written until "Save", which then merges the gloss into the existing entry
    app.settings.update({"dict_ai_autosave": False, "dict_direction": "auto"}); C.save_settings(app.settings); tab.on_show()
    app.repos.dictionary.add("Qqzzbaum", "qqzz-tree", "n", "", "", "user", ""); tab.dict.extend([D.Entry("Qqzzbaum", "n", "", "qqzz-tree", "", D.SOURCE_USER)])
    mock_ai.content = json.dumps([{"headword": "Qqzzbaum", "pos": "n", "extra": "", "translation_en": "qqzz-tree", "translation_tr": "qqzz-ağaç", "example": "", "note": ""}])
    tab.query.set("Qqzzbaum"); tab.search(); app.update()
    assert tab.current().source == "user" and mock_ai.count("/chat/completions") == 1                 # auto never targets Turkish: no request
    tab.ask_ai()
    assert _pump(app, lambda: mock_ai.count("/chat/completions") == 2), (tab.ai_out.get("1.0", "end"), app.status.get())
    assert _pump(app, lambda: _ai_rows(tab)), (tab.ai_out.get("1.0", "end"), app.status.get())
    assert tab.current().source == "ai" and tab.save_btn.winfo_manager()
    assert [r["tr"] for r in app.repos.dictionary.all() if r["headword"] == "Qqzzbaum"] == [""] and tab.dict.twin(tab.current()).tr == ""
    before = app.repos.dictionary.count(); tab.save_ai_entry(); app.update()
    assert app.repos.dictionary.count() == before and [r["tr"] for r in app.repos.dictionary.all() if r["headword"] == "Qqzzbaum"] == ["qqzz-ağaç"]
    assert tab.current().source == "user" and tab.current().tr == "qqzz-ağaç" and not tab.save_btn.winfo_manager() and not _ai_rows(tab)
    # a built-in entry without a gloss (if any is left) is completed through an "ai" twin row that merges on the next start
    bare = next((e for e in tab.dict.entries if e.source == D.SOURCE_BUILTIN and not e.tr and len(tab.dict.find(e.headword)) == 1), None)
    if bare is not None:
        app.settings.update({"dict_ai_autosave": True, "dict_direction": t2tr}); C.save_settings(app.settings); tab.on_show()
        mock_ai.content = json.dumps([{"headword": bare.headword, "pos": bare.pos, "extra": bare.extra, "translation_en": bare.translation, "translation_tr": "qqzz-gloss"}])
        tab.query.set(bare.headword); tab.search()
        assert tab.current().headword == bare.headword and not tab.current().tr and app.status.get() == app.t("dict.tr_missing")
        assert _pump(app, lambda: tab.dict.twin(bare) is not None and tab.dict.twin(bare).tr == "qqzz-gloss")
        assert tab.dict.twin(bare).source == D.SOURCE_BUILTIN and tab.current().tr == "qqzz-gloss" and tab.current().source == D.SOURCE_BUILTIN
        assert any(r["headword"] == bare.headword and r["translation"] == bare.translation and r["source"] == "ai" and r["tr"] == "qqzz-gloss" for r in app.repos.dictionary.all())
        rebuilt = D.build_dictionary([(r["headword"], r["translation"], r["pos"], r["extra"], r["note"], r["source"], r["example"], r["tr"]) for r in app.repos.dictionary.all()])
        assert rebuilt.twin(bare).tr == "qqzz-gloss" and rebuilt.twin(bare).source == D.SOURCE_BUILTIN
    app.settings.update({"dict_ai": "auto", "dict_ai_autosave": True, "dict_direction": "auto"}); C.save_settings(app.settings)


def _db_rows(app, head):
    return sorted((r["source"], r["translation"], r["pos"], r["tr"]) for r in app.repos.dictionary.all() if r["headword"] == head)


def _tree_rows(tab):
    return [(tab.tree.set(i, "head"), tab.tree.set(i, "trans"), tab.tree.set(i, "tr"), tab.tree.set(i, "src")) for i in tab.tree.get_children()]


def test_dictionary_turkish_fill_completes_the_stored_entry_instead_of_duplicating_it(app, mock_ai):
    """The guide promises that a *2tr search completes the existing entry and creates no duplicate. That must hold when the AI's
    English wording differs from the stored one, when a word has several senses, and when the stored part of speech is empty
    (Add-entry dialog) or spelled out (CSV "noun") while the AI says "n" - and the completed entry must never be asked again."""
    from fca import dictionary as D
    if not D.HAS_TR:
        return
    t2tr = f"{C.TARGET_LANG}2tr"
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "local", "dict_ai_autosave": True, "alt_enabled": False, "dict_direction": t2tr})
    C.save_settings(app.settings); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    assert _pump(app, lambda: tab.ai_state.cget("text") == app.t("dict.state_local"), 5)
    ai_src = app.t("dict.ai_source")

    def fill(head, answer):
        """Search ``head`` in the *2tr direction with ``answer`` as the AI reply; wait for the fill and one extra tick."""
        mock_ai.content = json.dumps(answer, ensure_ascii=False); before = mock_ai.count("/chat/completions")
        tab.query.set(head); tab.search()
        assert app.status.get() == app.t("dict.tr_missing") and tab.current().tr == ""          # synchronous part: listed without a gloss, AI pending
        assert _pump(app, lambda: mock_ai.count("/chat/completions") > before and all(r[3] for r in _db_rows(app, head))), (tab.ai_out.get("1.0", "end"), _db_rows(app, head))
        _pump(app, lambda: False, 0.3)
        assert app.t("dict.tr_filled") in app.status.get() and not tab.save_btn.winfo_manager()
        landed = _tree_rows(tab)                                    # what the user sees when the answer lands
        again = mock_ai.count("/chat/completions"); tab.search(); _pump(app, lambda: False, 0.4)
        assert mock_ai.count("/chat/completions") == again, "a completed entry was asked again"
        return landed

    # 1. divergent English: stored "attic", AI "attic; loft" -> the gloss lands in the stored row, no "ai" row, one tree row
    app.repos.dictionary.add("Qqzzgrenier", "attic", "n", "m", "", "user", ""); tab.dict.extend([D.Entry("Qqzzgrenier", "n", "m", "attic", "", D.SOURCE_USER)])
    landed = fill("Qqzzgrenier", [{"headword": "Qqzzgrenier", "pos": "n", "extra": "m", "translation_en": "attic; loft", "translation_tr": "tavan arası", "example": "", "note": ""}])
    assert _db_rows(app, "Qqzzgrenier") == [("user", "attic", "n", "tavan arası")]
    assert landed == _tree_rows(tab) == [("Qqzzgrenier", "attic", "tavan arası", app.t("dict.user"))] and tab.current().tr == "tavan arası"
    # 2. polysemous headword: each sense gets its own gloss, nothing extra is stored
    for trans in ("to fly", "to steal"):
        app.repos.dictionary.add("Qqzzvoler", trans, "v", "", "", "user", ""); tab.dict.extend([D.Entry("Qqzzvoler", "v", "", trans, "", D.SOURCE_USER)])
    landed = fill("Qqzzvoler", [{"headword": "Qqzzvoler", "pos": "v", "extra": "", "translation_en": "to fly; to soar", "translation_tr": "uçmak"},
                                {"headword": "Qqzzvoler", "pos": "v", "extra": "", "translation_en": "to steal; to rob", "translation_tr": "çalmak"}])
    assert _db_rows(app, "Qqzzvoler") == [("user", "to fly", "v", "uçmak"), ("user", "to steal", "v", "çalmak")]
    assert [(r[1], r[2], r[3]) for r in landed] == [("to fly", "uçmak", app.t("dict.user")), ("to steal", "çalmak", app.t("dict.user"))]   # answer order, no AI rows
    assert sorted((r[1], r[2]) for r in _tree_rows(tab)) == [("to fly", "uçmak"), ("to steal", "çalmak")]
    # 3. stored pos "" (Add-entry dialog) and "noun" (CSV) vs the AI's "n": completed in place, pos kept, one row in SQLite / memory / tree
    for head, trans, pos, gloss in (("Qqzzpluie", "rain", "", "yağmur"), ("Qqzzneige", "snow", "noun", "kar")):
        app.repos.dictionary.add(head, trans, pos, "", "", "user", ""); tab.dict.extend([D.Entry(head, pos, "", trans, "", D.SOURCE_USER)])
        landed = fill(head, [{"headword": head, "pos": "n", "extra": "f", "translation_en": trans, "translation_tr": gloss, "example": "", "note": ""}])
        assert _db_rows(app, head) == [("user", trans, pos, gloss)] and [(e.pos, e.tr) for e in tab.dict.find(head)] == [(pos, gloss)]
        assert landed == _tree_rows(tab) == [(head, trans, gloss, app.t("dict.user"))] and tab.current().source == "user"
    assert not any(r["source"] == "ai" and r["headword"] in ("Qqzzgrenier", "Qqzzvoler", "Qqzzpluie", "Qqzzneige") for r in app.repos.dictionary.all())
    # 4. a genuinely new headword in the same answer is still stored and listed (answer order: the completed entry, then the new one)
    app.repos.dictionary.add("Qqzzpain", "qqzz-bread", "n", "m", "", "user", ""); tab.dict.extend([D.Entry("Qqzzpain", "n", "m", "qqzz-bread", "", D.SOURCE_USER)])
    landed = fill("Qqzzpain", [{"headword": "Qqzzpain", "pos": "n", "extra": "m", "translation_en": "qqzz-bread", "translation_tr": "qqzz-ekmek"},
                               {"headword": "Qqzzbaguette", "pos": "n", "extra": "f", "translation_en": "qqzz-baguette", "translation_tr": "qqzz-baget"}])
    assert _db_rows(app, "Qqzzpain") == [("user", "qqzz-bread", "n", "qqzz-ekmek")] and _db_rows(app, "Qqzzbaguette") == [("ai", "qqzz-baguette", "n", "qqzz-baget")]
    assert landed == [("Qqzzpain", "qqzz-bread", "qqzz-ekmek", app.t("dict.user")), ("Qqzzbaguette", "qqzz-baguette", "qqzz-baget", ai_src)]
    assert tab.dict.lookup("Qqzzbaguette", t2tr)[1][0].tr == "qqzz-baget"                 # the new entry is searchable at once
    # 5. autosave off + divergent English: "Save" merges the gloss into the stored entry instead of adding a row
    app.settings["dict_ai_autosave"] = False; C.save_settings(app.settings)
    app.repos.dictionary.add("Qqzzcave", "cellar", "n", "f", "", "user", ""); tab.dict.extend([D.Entry("Qqzzcave", "n", "f", "cellar", "", D.SOURCE_USER)])
    mock_ai.content = json.dumps([{"headword": "Qqzzcave", "pos": "n", "extra": "f", "translation_en": "cellar; basement", "translation_tr": "mahzen"}], ensure_ascii=False)
    tab.query.set("Qqzzcave"); tab.search(); app.update()
    assert _pump(app, lambda: _ai_rows(tab)), (tab.ai_out.get("1.0", "end"), app.status.get())
    assert tab.current().source == "ai" and tab.save_btn.winfo_manager() and _db_rows(app, "Qqzzcave") == [("user", "cellar", "n", "")]
    before = app.repos.dictionary.count(); tab.save_ai_entry(); app.update()
    assert app.repos.dictionary.count() == before and _db_rows(app, "Qqzzcave") == [("user", "cellar", "n", "mahzen")]
    assert _tree_rows(tab) == [("Qqzzcave", "cellar", "mahzen", app.t("dict.user"))] and not tab.save_btn.winfo_manager() and not _ai_rows(tab)
    app.settings.update({"dict_ai": "auto", "dict_ai_autosave": True, "dict_direction": "auto"}); C.save_settings(app.settings)


def test_dictionary_random_word_is_found_under_every_fixed_direction(app, mock_ai):
    """"Random word" picks a built-in headword; under EN → FR / TR → FR the headword side is not the search side, so the search
    must flip the pair for that one pick instead of reporting the word missing and asking the AI."""
    from fca import dictionary as D
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "local", "dict_ai_autosave": True, "alt_enabled": False})
    C.save_settings(app.settings); app.refresh_ai_clients(); mock_ai.content = "[]"
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    for code in D.DIRECTIONS:
        app.settings["dict_direction"] = code; C.save_settings(app.settings); tab.on_show(); tab.query.set(""); app.update()
        for _ in range(3):
            before = mock_ai.count("/chat/completions"); tab.random_word(); _pump(app, lambda: False, 0.3)
            listed = [r[0] for r in _tree_rows(tab)]                     # the pick is listed (an accent-equal headword such as "la"/"là" may sort first)
            assert tab.query.get() in listed and tab.current() is not None and tab.current().source == "builtin", (code, tab.query.get(), listed[:5])
            assert mock_ai.count("/chat/completions") == before and app.t("dict.no_result") not in app.status.get(), (code, tab.query.get(), app.status.get())
            expected = D.DEFAULT_DIRECTION if code == "auto" else (code if D.source_field(code) == "headword" else D.direction_code(*reversed(D.split_direction(code))))
            assert tab.dir_label.cget("text") == D.direction_text(expected) and tab.direction.get() == tab._direction_labels[code]   # selector untouched
        assert app.settings["dict_direction"] == code and C.load_settings()["dict_direction"] == code
    app.settings.update({"dict_ai": "auto", "dict_direction": "auto"}); C.save_settings(app.settings)
