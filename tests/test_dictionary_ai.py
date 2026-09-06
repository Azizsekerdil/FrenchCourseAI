"""AI-driven dictionary lookup and provider resolution against a local mock OpenAI server (no real network)."""
from __future__ import annotations

import json
import time

import pytest

from fca import config as C
from fca import dictionary as D
from fca.ai_client import AIClient, AIError, resolve_provider


def test_ai_lookup_parses_fenced_json_and_sends_bearer(mock_ai):
    client = AIClient(mock_ai.base, api_key="sk-test-123")
    entries = D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    assert len(entries) == len(mock_ai.sample) and all(e.source == D.SOURCE_AI for e in entries)
    first, sample = entries[0], mock_ai.sample[0]
    assert (first.headword, first.pos, first.extra, first.translation) == (sample["headword"], "n", sample["extra"], sample["translation"])
    assert first.example == sample["example"] and first.note == sample["note"]
    assert all(e.pos in D.POS_LABELS for e in entries)
    second = entries[1]
    assert second.pos == "n"                                             # "noun" normalised to the dictionary's code
    assert (second.headword, second.extra, second.gender, second.display) == ("pause", "f", "f", "pause")   # "la pause": article stripped, gender kept
    chat = mock_ai.chats[-1]
    assert chat["auth"] == "Bearer sk-test-123"
    assert chat["body"]["model"] == mock_ai.MODEL and client.last_model == mock_ai.MODEL
    user = chat["body"]["messages"][-1]["content"]
    assert sample["headword"] in user and "JSON" in user and C.TARGET_LANG_NAME in user
    assert all(r["auth"] == "Bearer sk-test-123" for r in mock_ai.requests)       # /models probe carries it too


def test_no_key_means_no_authorization_header(mock_ai):
    client = AIClient(mock_ai.base)
    assert D.ai_lookup(client, "x", "tr")
    assert all(r["auth"] == "" for r in mock_ai.requests)
    assert D.ai_lookup(client, "   ", "tr") == [] and mock_ai.count("/chat/completions") == 1   # blank query never hits the network


def test_garbage_output_yields_empty_list_without_raising(mock_ai):
    mock_ai.content = "Sorry, I cannot help with that."
    assert D.ai_lookup(AIClient(mock_ai.base), "x", "en") == []
    for garbage in ("", "null", "[]", "[1, 2]", '[{"headword": 5}]', "```\n[{broken\n```", '[{"headword": "a", "translation": null}]',
                    '{"headword": "a"}', "[[[", "]]]", '[{"headword": {"x": 1}, "translation": "y"}]', "[" * 5000):
        assert D.parse_ai_entries(garbage) == [], garbage


def test_parser_is_tolerant_and_bounded():
    rows = D.parse_ai_entries('Here you go:\n```json\n[{"headword": "x", "translation": ["y", "z"], "pos": "Verb"}]\n```\nHope it helps!')
    assert rows[0].translation == "y; z" and rows[0].pos == "v" and rows[0].source == D.SOURCE_AI
    assert D.parse_ai_entries('[{"headword": "x", "translation": "y"}]')[0].pos == "phr"          # missing pos
    long = "a" * 500
    e = D.parse_ai_entries(json.dumps([{"headword": long, "translation": long, "example": long, "note": long, "extra": long}]))[0]
    assert len(e.headword) <= 80 and len(e.translation) <= 200 and len(e.example) <= 240 and len(e.note) <= 240 and len(e.extra) <= 80
    many = D.parse_ai_entries(json.dumps([{"headword": f"w{i}", "translation": "t"} for i in range(12)]))
    assert len(many) == D.AI_MAX_ENTRIES
    mixed = D.parse_ai_entries(json.dumps([7, {"headword": "ok", "translation": "fine"}, {"headword": "", "translation": "x"}, "str"]))
    assert [e.headword for e in mixed] == ["ok"]
    e = D.parse_ai_entries('[{"headword": "la maison", "pos": "n", "extra": "", "translation": "house"}]')[0]
    assert (e.headword, e.extra, e.gender, e.display) == ("maison", "f", "f", "maison")
    e = D.parse_ai_entries('[{"headword": "l\'œil", "pos": "nom", "extra": "m, yeux", "translation": "eye"}]')[0]
    assert (e.pos, e.headword, e.extra, e.plural, e.gender) == ("n", "œil", "m yeux", "yeux", "m")
    e = D.parse_ai_entries('[{"headword": "les gens", "pos": "n", "extra": "pl", "translation": "people"}]')[0]
    assert (e.headword, e.extra, e.gender) == ("gens", "pl", "pl")


def test_normalize_pos_covers_codes_names_and_localised_labels():
    assert D.normalize_pos("noun") == "n" and D.normalize_pos("Substantiv") == "n" and D.normalize_pos("isim") == "n"
    assert D.normalize_pos("verb.") == "v" and D.normalize_pos("ADJ") == "adj" and D.normalize_pos("n.") == "n"
    assert D.normalize_pos("noun (m)") == "n" and D.normalize_pos("Wendung") == "phr" and D.normalize_pos("interjection") == "int"
    assert D.normalize_pos("whatever") == "phr" and D.normalize_pos(None) == "phr" and D.normalize_pos(3) == "phr"


def test_ai_prompt_explains_convention_and_direction():
    prompt = D.ai_prompt("maison", "tr")
    assert "maison" in prompt and "headword" in prompt and "translation" in prompt and "example" in prompt
    assert all(code in prompt for code in D.POS_LABELS) and str(D.AI_MAX_ENTRIES) in prompt
    assert "Detect the direction" in prompt and C.TARGET_LANG_NAME in prompt
    assert '"m"' in prompt and "yeux" in prompt and "English" in prompt


def test_closed_port_raises_aierror_quickly():
    client = AIClient("http://127.0.0.1:9")
    started = time.monotonic()
    with pytest.raises(AIError):
        D.ai_lookup(client, "maison", "en")
    assert time.monotonic() - started < 5
    assert client.available(timeout=0.2) is False and client.reachable(timeout=0.2) is False


def test_client_url_headers_and_host_classification():
    remote = AIClient(C.NIM_BASE + "/", api_key="k", model="meta/llama-3.1-8b-instruct", trust_model=True)
    assert remote._url("models") == "https://integrate.api.nvidia.com/v1/models"
    assert remote._headers()["Authorization"] == "Bearer k" and not remote.is_local
    assert remote.choose_model("dictionary") == "meta/llama-3.1-8b-instruct"        # trusted model name: no catalogue probe, no network
    local = AIClient("http://localhost:11434")
    assert local._url("chat/completions") == "http://localhost:11434/v1/chat/completions"
    assert local.is_local and "Authorization" not in local._headers()
    local.configure(api_key="abc", model="m")
    assert local.api_key == "abc" and local.model == "m" and local.base == "http://localhost:11434"
    # the host is parsed, not substring-matched; it only tells loopback apart (shorter probe timeout), never key requirements
    for base in ("http://127.0.0.1:1234", "http://127.0.0.1:1234/v1", "http://127.0.0.2:1234", "http://[::1]:11434",
                 "http://0.0.0.0:8080", "http://host.docker.internal:1234", "http://LOCALHOST:1234"):
        assert AIClient(base).is_local, base
    for base in ("http://192.168.1.20:11434", "http://10.0.0.5:1234/v1", "https://api.localhost-proxy.example/v1",
                 "http://mylocalhost.example.com", "https://api.example.com/v1?x=127.0.0.1", "http://[::1"):
        assert not AIClient(base).is_local, base


def test_provider_resolution_follows_policy(mock_ai):
    local_ok, local_down = AIClient(mock_ai.base), AIClient("http://127.0.0.1:9")
    alt, alt_down = AIClient(mock_ai.base, api_key="k", trust_model=True), AIClient("http://127.0.0.1:9", api_key="k", trust_model=True)
    base = {"ai_enabled": True, "alt_enabled": True}
    assert resolve_provider({**base, "dict_ai": "off"}, local_ok, alt) is None
    assert resolve_provider({**base, "dict_ai": "local"}, local_ok, alt) is local_ok
    assert resolve_provider({**base, "dict_ai": "local"}, local_down, alt) is None
    assert resolve_provider({**base, "dict_ai": "alt"}, local_ok, alt) is alt
    assert resolve_provider({**base, "dict_ai": "alt"}, local_ok, alt_down) is None
    assert resolve_provider({**base, "alt_enabled": False, "dict_ai": "alt"}, local_ok, alt) is None
    assert resolve_provider({**base, "dict_ai": "auto"}, local_ok, alt) is local_ok
    assert resolve_provider({**base, "dict_ai": "auto"}, local_down, alt) is alt
    assert resolve_provider({**base, "dict_ai": "auto"}, local_down, alt_down) is None
    assert resolve_provider({**base, "alt_enabled": False, "dict_ai": "auto"}, local_down, alt) is None
    assert resolve_provider({**base, "ai_enabled": False, "dict_ai": "auto"}, local_ok, alt) is alt
    assert resolve_provider({**base, "ai_enabled": False, "dict_ai": "local"}, local_ok, alt) is None
    assert resolve_provider({**base, "dict_ai": "bogus"}, local_ok, alt) is local_ok                # unknown -> auto
    assert resolve_provider({}, local_ok, alt) is local_ok                                          # defaults: auto, local enabled
    assert mock_ai.count("/models") == 2                                                            # one cached probe per client
    assert {r["auth"] for r in mock_ai.requests} == {"", "Bearer k"}                                # the alt probe carries its key


def test_alt_verdict_comes_from_the_server_not_from_the_host(mock_ai, monkeypatch):
    """A key-less Ollama/LM Studio on another LAN machine is used; a keyed API without its key is not - the verdict of 'Test connection'."""
    monkeypatch.setattr(AIClient, "is_local", property(lambda self: False))         # the mock now "lives" on 192.168.x.x
    lan = AIClient(mock_ai.base, trust_model=True)                                    # no key
    assert not lan.is_local and lan.reachable() and lan.models() == [mock_ai.MODEL]
    settings = {"ai_enabled": False, "alt_enabled": True, "dict_ai": "alt"}
    assert resolve_provider(settings, None, lan) is lan
    assert resolve_provider({**settings, "dict_ai": "auto"}, None, lan) is lan
    assert D.ai_lookup(lan, "x", "en") and mock_ai.chats[-1]["auth"] == ""
    mock_ai.require_key = "nvapi-secret"                                               # now a cloud API that insists on a key
    nokey, keyed = AIClient(mock_ai.base, trust_model=True), AIClient(mock_ai.base, api_key="nvapi-secret", trust_model=True)
    assert not nokey.reachable() and nokey.models() == []                              # exactly what the Test button reports
    assert resolve_provider(settings, None, nokey) is None and resolve_provider(settings, None, keyed) is keyed
    with pytest.raises(AIError):
        D.ai_lookup(nokey, "x", "en")
    assert D.ai_lookup(keyed, "x", "en") and mock_ai.chats[-1]["auth"] == "Bearer nvapi-secret"


def test_choose_model_falls_back_to_an_installed_model_unless_trusted(mock_ai, monkeypatch):
    lmstudio = AIClient(mock_ai.base, model="qwen2.5-7b-instruct")
    assert lmstudio.choose_model("chat") == mock_ai.MODEL                              # configured model not loaded -> an installed one
    monkeypatch.setattr(AIClient, "is_local", property(lambda self: False))            # LM Studio on another LAN machine: same behaviour
    assert lmstudio.choose_model("chat") == mock_ai.MODEL and lmstudio.choose_model("chat", mock_ai.MODEL) == mock_ai.MODEL
    assert lmstudio.chat("hi", "chat", "en") and mock_ai.chats[-1]["body"]["model"] == mock_ai.MODEL
    probes = mock_ai.count("/models")
    alt = AIClient(mock_ai.base, api_key="k", model="meta/llama-3.1-8b-instruct", trust_model=True)
    assert alt.choose_model("dictionary") == "meta/llama-3.1-8b-instruct" and mock_ai.count("/models") == probes   # typed name wins, no probe
    assert alt.chat("hi", "dictionary", "en") and mock_ai.chats[-1]["body"]["model"] == "meta/llama-3.1-8b-instruct"
    assert AIClient(mock_ai.base, trust_model=True).choose_model("chat") == mock_ai.MODEL                        # nothing configured -> probe


def test_reachability_cache_expires_and_can_be_invalidated(mock_ai):
    client = AIClient(mock_ai.base)
    assert client.reachable() and client.reachable() and mock_ai.count("/models") == 1
    assert client.reachable(ttl=0) and mock_ai.count("/models") == 2
    client.invalidate(); assert client.reachable() and mock_ai.count("/models") == 3
    client.configure(base=mock_ai.base); assert client.reachable() and mock_ai.count("/models") == 4


def test_token_logger_and_alt_model_are_used(mock_ai):
    log = []
    AIClient(mock_ai.base, lambda *a: log.append(a)).chat("hi", "chat", "en")
    alt = AIClient(mock_ai.base, lambda *a: log.append(a), api_key="k", model=mock_ai.MODEL)
    assert D.ai_lookup(alt, "x", "de") and mock_ai.chats[-1]["body"]["model"] == mock_ai.MODEL
    assert mock_ai.chats[-1]["body"]["temperature"] <= 0.2 and mock_ai.chats[-1]["body"]["messages"][0]["role"] == "system"
    assert [(row[0], row[1], row[2], row[3], row[5]) for row in log] == [(mock_ai.MODEL, "chat", 42, 17, True), (mock_ai.MODEL, "dictionary", 42, 17, True)]


def test_entry_defaults_and_table_roundtrip_keep_example(tmp_path):
    e = D.Entry("maison", "n", "f", "house")
    assert e.example == "" and e.source == D.SOURCE_BUILTIN
    ai = D.Entry("Zzqqxx", "n", "m", "zzq-thing", "n", D.SOURCE_AI, "Le zzqqxx est vieux.")
    out = tmp_path / "ai.csv"
    assert D.write_table(out, [ai]) == 1
    back = D.read_table(out)[0]
    assert back.example == "Le zzqqxx est vieux." and back.source == D.SOURCE_USER
    d = D.build_dictionary([("Zzqqxx", "zzq-thing", "n", "m", "", "ai", "Le zzqqxx est vieux."), ("Qqzz", "qqz-fence", "n", "m", "", "bogus", "")])
    by = d.count_by_source()
    assert by.get(D.SOURCE_AI, 0) == 1 and d.lookup("Qqzz")[1][0].source == D.SOURCE_USER
    assert d.lookup("Zzqqxx")[1][0].example == "Le zzqqxx est vieux."
    assert d.contains(ai) and not d.contains(D.Entry("nope", "n", "", "nothing"))
    assert d.contains(D.Entry("maison", "n", "f", "house", "", D.SOURCE_AI))      # duplicates of built-in entries are recognised


# ---------------------------------------------------------------------------
# Thinking models (gemma-4 / qwen3): reasoning_effort field, truncated-answer retry, model ranking
# ---------------------------------------------------------------------------
def test_local_client_sends_reasoning_off_and_records_finish_reason(mock_ai):
    mock_ai.reasoning_tokens = 3
    client = AIClient(mock_ai.base)
    assert client.is_local
    entries = D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    assert entries and entries[0].source == D.SOURCE_AI
    body = mock_ai.chats[-1]["body"]
    assert body.get("reasoning_effort") == "none" and body["max_tokens"] == D.AI_MAX_TOKENS
    assert client.last_finish_reason == "stop" and client.last_reasoning_tokens == 3


def test_remote_client_does_not_send_reasoning_field(mock_ai):
    class RemoteClient(AIClient):                     # hosted endpoint stand-in
        is_local = property(lambda self: False)

    client = RemoteClient(mock_ai.base, api_key="k")
    assert D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    assert "reasoning_effort" not in mock_ai.chats[-1]["body"]
    assert AIClient(mock_ai.base).is_local                       # class property untouched


def test_server_rejecting_extra_fields_gets_a_retry_without_them(mock_ai):
    mock_ai.reject_fields = {"reasoning_effort"}
    client = AIClient(mock_ai.base)
    assert D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    chats = mock_ai.chats
    assert len(chats) == 2
    assert "reasoning_effort" in chats[0]["body"] and "reasoning_effort" not in chats[1]["body"]


def test_truncated_empty_answer_is_retried_with_a_bigger_budget(mock_ai):
    mock_ai.queue = [("", "length"), (mock_ai.content, "stop")]
    client = AIClient(mock_ai.base)
    assert D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    chats = mock_ai.chats
    assert len(chats) == 2 and chats[1]["body"]["max_tokens"] == D.AI_MAX_TOKENS * 3
    mock_ai.queue = [("Sorry, I cannot help with that.", "stop")]          # not truncated: no retry
    assert D.ai_lookup(client, "zzqqxx", "en") == [] and len(mock_ai.chats) == 3


def test_rank_models_skips_specialist_models_and_prefers_fitting_general_models():
    from fca import ai_client as A
    installed = ["qwen/qwen3.6-35b-a3b", "google/gemma-4-12b-qat", "qwen/qwen3-vl-8b", "biomistral-7b",
                 "qwen2.5-math-7b-instruct", "moondream-2b-2025-04-14", "text-embedding-nomic-embed-text-v1.5"]
    ranked = A.rank_models(installed, "dictionary")
    assert ranked[0] == "google/gemma-4-12b-qat"
    assert "qwen2.5-math-7b-instruct" not in ranked and "text-embedding-nomic-embed-text-v1.5" not in ranked
    assert A.rank_models(["text-embedding-x"], "chat") == ["text-embedding-x"]
    assert A.rank_models(["gemma-4-12b-qat", "qwen2.5-7b-instruct"], "chat")[0] == "qwen2.5-7b-instruct"
    assert A.model_size_b("qwen/qwen3.6-35b-a3b") == 35.0 and A.is_specialist("qwen/qwen3-vl-8b")


def test_choose_model_avoids_specialist_models(monkeypatch, mock_ai):
    client = AIClient(mock_ai.base)
    monkeypatch.setattr(client, "models", lambda timeout=1.5: ["qwen2.5-math-7b-instruct", "google/gemma-4-12b-qat"])
    assert client.choose_model("dictionary") == "google/gemma-4-12b-qat"
