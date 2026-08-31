"""French-specific accents, pronunciation, grammar and open resources."""
from __future__ import annotations

import random

ORTHOGRAPHY = [
    ("A–Z", "Alphabet français", "Les lettres de base sont latines; les signes diacritiques changent la lecture ou distinguent les mots.", "Paris se lit P-A-R-I-S."),
    ("é", "Accent aigu", "é représente souvent un son fermé [e].", "été · café · école"),
    ("è / ê / ë", "Accents sur e", "è et ê indiquent souvent [ɛ]; ë sépare deux voyelles.", "père · fête · Noël"),
    ("à / â", "Accents sur a", "à distingue la préposition de a; â conserve une histoire graphique.", "à Paris · âge"),
    ("î / ï", "Accents sur i", "ï marque souvent que les voyelles se prononcent séparément.", "île · naïf"),
    ("ô", "Accent circonflexe", "ô note souvent un o fermé ou une ancienne graphie.", "hôtel · drôle"),
    ("ù / û / ü", "Accents sur u", "ù distingue où de ou; ü sépare deux voyelles.", "où · sûr · capharnaüm"),
    ("ç", "C cédille", "ç donne le son [s] devant a, o ou u.", "garçon · français · reçu"),
    ("'", "Apostrophe et élision", "Le, la, je, me, te, se, de s'élident devant une voyelle ou un h muet.", "l'école · j'aime · d'accord"),
    ("liaison", "Liaison", "Une consonne finale normalement muette peut se lier à la voyelle suivante.", "les‿amis · vous‿avez"),
    ("finale", "Consonnes finales", "Beaucoup de consonnes finales sont muettes, avec des exceptions.", "petit · grand · nez"),
    ("nasales", "Voyelles nasales", "an/en, on, in/ain et un se prononcent avec l'air passant par le nez.", "enfant · bon · pain · un"),
    ("r", "R français", "Le r standard est produit au fond de la gorge.", "rue · Paris"),
    ("u / ou", "Deux voyelles distinctes", "u [y] demande des lèvres rondes avec la langue de i; ou vaut [u].", "tu / tout · rue / roue"),
    ("rythme", "Rythme du groupe", "Le français accentue surtout la dernière syllabe prononcée d'un groupe.", "un petit café · à demain"),
]

PRONUNCIATION = [
    ("r", "[ʁ]", "rue, Paris"), ("u / ou", "[y] / [u]", "tu / tout"),
    ("on", "[ɔ̃]", "bon, maison"), ("an / en", "[ɑ̃]", "sans, enfant"),
    ("in / ain", "[ɛ̃]", "vin, pain"), ("eu / œu", "[ø] / [œ]", "deux, sœur"),
    ("é / è", "[e] / [ɛ]", "été, père"), ("oi", "[wa]", "moi, voiture"),
    ("ch / j", "[ʃ] / [ʒ]", "chat, jour"),
]

_TOPIC_ROWS = [
    ("article.def", "Belirli artikeller", "Definite articles", "Articles définis", "le, la, l' ve çoğul les.", "le, la, l' and plural les.", "le, la, l' et le pluriel les.", "le livre · la table · l'école · les amis"),
    ("article.indef", "Belirsiz artikeller", "Indefinite articles", "Articles indéfinis", "un, une ve çoğul des.", "un, une and plural des.", "un, une et le pluriel des.", "un café · une pomme · des livres"),
    ("noun.gender", "İsim cinsiyetleri", "Noun gender", "Genre des noms", "İsimleri artikelleriyle öğren.", "Learn nouns with their article.", "Apprendre les noms avec leur article.", "le train · la gare"),
    ("noun.number", "Tekil ve çoğul", "Singular and plural", "Singulier et pluriel", "Çoğul genellikle -s alır; yazıda görünür, çoğu kez duyulmaz.", "Plural usually adds -s; it is often silent.", "Le pluriel prend souvent -s, généralement muet.", "un livre · des livres"),
    ("adj.agreement", "Sıfat uyumu", "Adjective agreement", "Accord des adjectifs", "Sıfat isimle cinsiyet ve sayıda uyum sağlar.", "The adjective agrees in gender and number.", "L'adjectif s'accorde en genre et en nombre.", "un petit café · une petite maison"),
    ("adj.position", "Sıfatların konumu", "Adjective position", "Place des adjectifs", "Çoğu sıfat isimden sonra; bazı yaygın sıfatlar önce gelir.", "Most adjectives follow; common short adjectives may precede.", "La plupart suivent le nom; certains adjectifs fréquents le précèdent.", "une voiture rouge · un petit hôtel"),
    ("pron.subject", "Kişi zamirleri", "Subject pronouns", "Pronoms sujets", "je, tu, il/elle/on, nous, vous, ils/elles.", "je, tu, il/elle/on, nous, vous, ils/elles.", "je, tu, il/elle/on, nous, vous, ils/elles.", "Nous habitons ici."),
    ("pron.object", "Nesne zamirleri", "Object pronouns", "Pronoms compléments", "le, la, les, lui, leur genellikle çekimli fiilden önce gelir.", "le, la, les, lui, leur usually precede the finite verb.", "le, la, les, lui, leur se placent généralement avant le verbe.", "Je le vois. · Je lui parle."),
    ("pron.y_en", "y ve en", "y and en", "Pronoms y et en", "y yer veya à + şeyin; en de + şeyin yerini tutar.", "y replaces a place/à phrase; en replaces a de phrase.", "y remplace un lieu ou à + chose; en remplace de + chose.", "J'y vais. · J'en veux."),
    ("verb.etre", "être ve avoir", "être and avoir", "Être et avoir", "İki temel düzensiz fiil, ayrıca birleşik zaman yardımcılarıdır.", "Two core irregular verbs and compound-tense auxiliaries.", "Deux verbes irréguliers essentiels et auxiliaires.", "je suis · j'ai"),
    ("verb.er", "Düzenli -er fiilleri", "Regular -er verbs", "Verbes réguliers en -er", "parler: je parle, nous parlons, ils parlent.", "parler: je parle, nous parlons, ils parlent.", "parler : je parle, nous parlons, ils parlent.", "Nous parlons français."),
    ("verb.ir", "Düzenli -ir fiilleri", "Regular -ir verbs", "Verbes réguliers en -ir", "finir: je finis, nous finissons.", "finir: je finis, nous finissons.", "finir : je finis, nous finissons.", "Elle finit le travail."),
    ("verb.re", "Düzenli -re fiilleri", "Regular -re verbs", "Verbes réguliers en -re", "vendre: je vends, nous vendons.", "vendre: je vends, nous vendons.", "vendre : je vends, nous vendons.", "Ils vendent du pain."),
    ("verb.irregular", "Düzensiz fiiller", "Irregular verbs", "Verbes irréguliers", "aller, faire, venir, prendre gibi fiiller ezberlenir.", "Forms of aller, faire, venir and prendre must be learned.", "Il faut apprendre les formes de aller, faire, venir et prendre.", "je vais · nous faisons · ils viennent"),
    ("negation", "Olumsuzluk", "Negation", "Négation", "ne ... pas çekimli fiili çevreler; konuşmada ne düşebilir.", "ne ... pas surrounds the finite verb; spoken French may omit ne.", "ne ... pas encadre le verbe; à l'oral ne peut disparaître.", "Je ne parle pas anglais."),
    ("questions", "Soru yapıları", "Questions", "Interrogation", "Tonlama, est-ce que veya devrik yapı kullanılabilir.", "Use intonation, est-ce que, or inversion.", "On utilise l'intonation, est-ce que ou l'inversion.", "Tu viens ? · Est-ce que tu viens ?"),
    ("tense.present", "Présent", "Present tense", "Présent", "Şimdiki eylem, alışkanlık ve yakın gelecek için kullanılır.", "Used for current action, habit and near future.", "Il exprime l'action actuelle, l'habitude et parfois le futur proche.", "Je travaille aujourd'hui."),
    ("tense.passe_compose", "Passé composé", "Perfect past", "Passé composé", "avoir/être + participe passé; bitmiş olay.", "avoir/être + past participle for completed events.", "avoir/être + participe passé pour une action terminée.", "Elle est arrivée. · J'ai mangé."),
    ("tense.imparfait", "Imparfait", "Imperfect", "Imparfait", "Geçmişte durum, alışkanlık veya sürmekte olan arka plan.", "Past state, habit or ongoing background.", "État, habitude ou arrière-plan dans le passé.", "Quand j'étais petit, j'habitais à Lyon."),
    ("tense.futur_proche", "Futur proche", "Near future", "Futur proche", "aller + mastar; yakın veya planlı gelecek.", "aller + infinitive for a near or planned future.", "aller + infinitif pour un futur proche ou prévu.", "Nous allons partir."),
    ("tense.futur_simple", "Futur simple", "Simple future", "Futur simple", "Mastar/kök + ai, as, a, ons, ez, ont.", "Infinitive/stem + ai, as, a, ons, ez, ont.", "Infinitif/radical + ai, as, a, ons, ez, ont.", "Demain, je travaillerai."),
    ("imperative", "Emir kipi", "Imperative", "Impératif", "Özne zamiri kullanılmaz: parle, parlons, parlez.", "No subject pronoun: parle, parlons, parlez.", "Sans pronom sujet : parle, parlons, parlez.", "Écoutez et répétez."),
    ("reflexive", "Dönüşlü fiiller", "Reflexive verbs", "Verbes pronominaux", "me, te, se, nous, vous, se fiilden önce gelir.", "me, te, se, nous, vous, se precede the verb.", "me, te, se, nous, vous, se précèdent le verbe.", "Je me lève à sept heures."),
    ("prepositions", "Edatlar", "Prepositions", "Prépositions", "à, de, en, au, aux yer ve yön ifadelerinde birleşebilir.", "à, de, en, au, aux combine in place/direction phrases.", "à, de, en, au, aux servent à exprimer lieu et direction.", "à Paris · en France · au Canada"),
    ("partitive", "Partitif artikeller", "Partitive articles", "Articles partitifs", "Belirsiz miktar: du, de la, de l', des; olumsuzda çoğu kez de.", "Unspecified amount: du, de la, de l', des; often de after negation.", "Quantité indéfinie : du, de la, de l', des; souvent de après négation.", "Je bois du café. · Je ne bois pas de café."),
    ("numbers", "Sayılar", "Numbers", "Nombres", "21 vingt et un; 80 quatre-vingts; 81 quatre-vingt-un.", "21 vingt et un; 80 quatre-vingts; 81 quatre-vingt-un.", "21 vingt et un ; 80 quatre-vingts ; 81 quatre-vingt-un.", "Il a vingt et un ans."),
    ("time", "Saat", "Telling time", "Heure", "Il est deux heures; et quart, et demie, moins le quart.", "Il est deux heures; et quart, et demie, moins le quart.", "Il est deux heures ; et quart, et demie, moins le quart.", "Le cours commence à neuf heures."),
    ("date", "Tarih", "Dates", "Date", "Tarih: le + sayı + ay; yalnız ayın biri premier.", "Use le + number + month; only the first is premier.", "On dit le + nombre + mois ; seul le premier jour est premier.", "Nous sommes le trois mai."),
    ("elision_liaison", "Elision ve liaison", "Elision and liaison", "Élision et liaison", "Elision yazıda apostrofla; liaison konuşmada ses bağlantısıyla görünür.", "Elision is written with an apostrophe; liaison links sounds in speech.", "L'élision s'écrit avec une apostrophe; la liaison relie les sons à l'oral.", "l'ami · les‿amis"),
]

GRAMMAR_TOPICS = [{"code": code, "title": {"tr": tr, "en": en, "fr": fr},
                   "rule": {"tr": rtr, "en": ren, "fr": rfr}, "example": example}
                  for code, tr, en, fr, rtr, ren, rfr, example in _TOPIC_ROWS]

EXERCISES = [
    {"topic": "article.def", "prompt": "___ école est fermée.", "answer": "L'", "options": ["Le", "La", "L'", "Les"], "explain": "École commence par une voyelle : l'école."},
    {"topic": "article.indef", "prompt": "Elle a ___ voiture.", "answer": "une", "options": ["un", "une", "des", "de"], "explain": "Voiture est féminin singulier."},
    {"topic": "noun.number", "prompt": "un journal → des ___", "answer": "journaux", "options": ["journals", "journaux", "journales", "journal"], "explain": "La plupart des noms en -al font -aux."},
    {"topic": "adj.agreement", "prompt": "une maison ___ (petit)", "answer": "petite", "options": ["petit", "petite", "petits", "petites"], "explain": "Féminin singulier : petite."},
    {"topic": "pron.object", "prompt": "Je vois Marie. → Je ___ vois.", "answer": "la", "options": ["le", "la", "lui", "leur"], "explain": "Marie est un complément direct féminin."},
    {"topic": "pron.y_en", "prompt": "Tu vas à Paris ? Oui, j'___ vais.", "answer": "y", "options": ["en", "y", "le", "lui"], "explain": "y remplace un lieu introduit par à."},
    {"topic": "verb.etre", "prompt": "Nous ___ étudiants.", "answer": "sommes", "options": ["avons", "êtes", "sommes", "sont"], "explain": "être, nous : sommes."},
    {"topic": "verb.er", "prompt": "Vous ___ français. (parler)", "answer": "parlez", "options": ["parle", "parles", "parlez", "parlent"], "explain": "Verbe en -er, vous : -ez."},
    {"topic": "verb.ir", "prompt": "Nous ___ le travail. (finir)", "answer": "finissons", "options": ["finons", "finissons", "finisez", "finit"], "explain": "finir, nous : finissons."},
    {"topic": "verb.re", "prompt": "Ils ___ des livres. (vendre)", "answer": "vendent", "options": ["vendes", "vendent", "vendez", "vendre"], "explain": "vendre, ils : vendent."},
    {"topic": "negation", "prompt": "Je ___ parle ___ anglais.", "answer": "ne … pas", "options": ["ne … pas", "pas … ne", "non", "ne … plus de"], "explain": "ne et pas encadrent le verbe conjugué."},
    {"topic": "questions", "prompt": "___ vous parlez français ?", "answer": "Est-ce que", "options": ["Est-ce que", "Est que", "Qu'est", "C'est que"], "explain": "Est-ce que introduit une question neutre."},
    {"topic": "tense.passe_compose", "prompt": "Elle ___ arrivée hier.", "answer": "est", "options": ["a", "est", "va", "était"], "explain": "arriver se conjugue avec être au passé composé."},
    {"topic": "tense.futur_proche", "prompt": "Nous ___ partir.", "answer": "allons", "options": ["avons", "sommes", "allons", "faisons"], "explain": "Futur proche : aller + infinitif."},
    {"topic": "reflexive", "prompt": "Je ___ lève à sept heures.", "answer": "me", "options": ["se", "me", "te", "nous"], "explain": "Pronom réfléchi de je : me."},
    {"topic": "prepositions", "prompt": "J'habite ___ France.", "answer": "en", "options": ["à", "au", "en", "aux"], "explain": "Pays féminin : en France."},
    {"topic": "partitive", "prompt": "Je bois ___ café.", "answer": "du", "options": ["de", "du", "de la", "des"], "explain": "Café est masculin : du café."},
    {"topic": "elision_liaison", "prompt": "le ami → ___", "answer": "l'ami", "options": ["le ami", "l'ami", "la ami", "les ami"], "explain": "le s'élide devant une voyelle."},
]


def build(lab="grammar", n=10, rng=None):
    if lab not in {"grammar", "articles", "verbs", "tenses", "pronouns", "orthography"}: return []
    rng = rng or random.Random(); source = list(EXERCISES)
    if lab == "articles": source = [e for e in source if e["topic"].startswith(("article.", "partitive"))]
    elif lab == "verbs": source = [e for e in source if e["topic"].startswith("verb.")]
    elif lab == "tenses": source = [e for e in source if e["topic"].startswith("tense.")]
    elif lab == "pronouns": source = [e for e in source if e["topic"].startswith("pron.")]
    elif lab == "orthography":
        source = [{"topic": "orthography", "prompt": f"Quelle forme est correcte ? {ex}", "answer": ex.split(" · ")[0],
                   "options": [ex.split(" · ")[0], ex.split(" · ")[0].replace("é", "e"), ex.split(" · ")[0].replace("ç", "c")], "explain": rule}
                  for _symbol, _name, rule, ex in ORTHOGRAPHY if " · " in ex]
    return [dict(rng.choice(source)) for _ in range(n)] if source else []


RESOURCES = [
    {"id": "wikibooks-fr", "title": "French - Wikibooks", "kind": "book", "level": "A1-C1",
     "url": "https://en.wikibooks.org/wiki/French", "license": "CC BY-SA 4.0", "attribution": "Wikibooks contributors", "online": True},
    {"id": "tatoeba-fr", "title": "Tatoeba French sentences", "kind": "data", "level": "A1-C1",
     "url": "https://tatoeba.org/en/downloads", "license": "CC BY 2.0 FR / selected CC0", "attribution": "Tatoeba contributors; preserve sentence-level attribution", "online": True},
    {"id": "librivox-fr", "title": "LibriVox French audiobooks", "kind": "audio", "level": "B1-C1",
     "url": "https://librivox.org/search?primary_key=2&search_category=language&search_page=1&search_form=get_results",
     "license": "Public domain in the USA; check local status", "attribution": "LibriVox volunteers", "online": True},
    {"id": "gutenberg-fr", "title": "Project Gutenberg French shelf", "kind": "book", "level": "B1-C1",
     "url": "https://www.gutenberg.org/browse/languages/fr", "license": "Project Gutenberg public-domain terms; check local status",
     "attribution": "Project Gutenberg and named authors/editors", "online": True},
]
