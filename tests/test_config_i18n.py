from pathlib import Path

from fca import config as C
from fca.i18n import LANG_NAMES, LOCALES, SYSTEM_PROMPTS


def test_identity_and_isolated_paths():
    assert (C.APP_NAME, C.APP_SLUG, C.TARGET_LANG, C.TARGET_LANG_NAME) == ("French Course AI", "FrenchCourseAI", "fr", "Français")
    assert C.DB_PATH.name == "FrenchCourseAI.db"
    assert C.APP_SLUG.lower() not in "germancourseai"


def test_settings_roundtrip_is_filtered_and_atomic():
    data = C.load_settings(); data["ui_lang"] = "fr"; data["daily_goal"] = 37; data["api_key"] = "must-not-persist"
    C.save_settings(data); back = C.load_settings()
    assert back["ui_lang"] == "fr" and back["daily_goal"] == 37
    assert "api_key" not in C.SETTINGS_PATH.read_text(encoding="utf-8")
    assert not C.SETTINGS_PATH.with_suffix(".tmp").exists()


def test_all_i18n_keys_exist_in_three_languages():
    assert tuple(LANG_NAMES) == C.UI_LANGS
    keys = set(LOCALES["tr"])
    assert len(keys) >= 140
    assert all(set(LOCALES[lang]) == keys for lang in C.UI_LANGS)
    assert all(value.strip() for lang in C.UI_LANGS for value in LOCALES[lang].values())


def test_system_prompts_follow_interface_language():
    assert set(SYSTEM_PROMPTS) == set(C.UI_LANGS)
    assert "Türkçe" in SYSTEM_PROMPTS["tr"] and "article" in SYSTEM_PROMPTS["en"]
    assert "français simple" in SYSTEM_PROMPTS["fr"] and "genre" in SYSTEM_PROMPTS["fr"]


def test_french_search_and_spelling_forms_are_separate():
    assert C.normalize_search("école") == "ecole"
    assert C.normalize_search("français") == C.normalize_search("francais")
    assert C.normalize_search("cœur") == C.normalize_search("coeur")
    assert C.answer_equal("l'école", "l'école")
    assert not C.answer_equal("l'ecole", "l'école")
    assert C.normalize_search("l’école") == C.normalize_search("ecole") or "ecole" in C.normalize_search("l’école")
