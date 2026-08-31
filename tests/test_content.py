from fca import content
from fca.seed_words import WORDS


def test_has_at_least_150_original_a1_words():
    assert len(WORDS) >= 150
    assert len({w["fr"] for w in WORDS}) >= 150
    required = {"fr", "tr", "en", "article", "gender", "plural", "part_of_speech", "example_fr", "example_tr", "example_en", "frequency_rank", "deck", "audio"}
    assert all(required <= set(word) for word in WORDS)


def test_nouns_have_article_plural_and_natural_example():
    nouns = [w for w in WORDS if w["part_of_speech"] == "noun"]
    assert len(nouns) >= 90
    assert all(w["article"] in {"le", "la", "l'"} and w["gender"] and w["plural"] for w in nouns)
    assert all(w["fr"] in w["example_fr"] for w in nouns)


def test_orthography_covers_required_french_features():
    text = " ".join(" ".join(row) for row in content.ORTHOGRAPHY)
    for token in ("é", "è", "ê", "ë", "à", "â", "î", "ï", "ô", "ù", "û", "ü", "ç", "Apostrophe", "Liaison", "nasales", "u / ou"):
        assert token in text


def test_grammar_topics_cover_requirements():
    codes = {t["code"] for t in content.GRAMMAR_TOPICS}
    required = {"article.def", "article.indef", "noun.gender", "noun.number", "adj.agreement", "adj.position",
                "pron.subject", "pron.object", "pron.y_en", "verb.etre", "verb.er", "verb.ir", "verb.re",
                "verb.irregular", "negation", "questions", "tense.present", "tense.passe_compose", "tense.imparfait",
                "tense.futur_proche", "tense.futur_simple", "imperative", "reflexive", "prepositions", "partitive",
                "numbers", "time", "date", "elision_liaison"}
    assert required <= codes


def test_all_labs_generate_valid_exercises():
    for lab in ("grammar", "articles", "verbs", "tenses", "pronouns", "orthography"):
        items = content.build(lab, 8)
        assert len(items) == 8
        assert all(item["answer"] in item["options"] and item["prompt"] for item in items)
    assert content.build("unknown", 3) == []


def test_resource_catalog_is_open_and_attributed():
    assert len(content.RESOURCES) >= 4
    assert all(r["license"] and r["attribution"] and r["url"].startswith("https://") for r in content.RESOURCES)
    assert all("CC" in r["license"] or "Public" in r["license"] or "public" in r["license"] for r in content.RESOURCES)
