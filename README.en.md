# French Course AI

French Course AI is an independent Windows desktop learning app built around local-first student data. Its Turkish, English and French interfaces expose the same feature set and French-specific content.

> Core learning features and student data are local. Opening resource links and using optional remote services requires the internet, so the app does not make a misleading “100% offline” claim.

## Features

- SM-2/Leitner spaced review, daily goal and streak
- More than 160 built-in A1 words with noun article, gender and plural
- French-Turkish-English dictionary, favorites and mistake drills
- Trilingual **French ↔ English ↔ Turkish dictionary** tab: 1,210+ built-in entries with gender and irregular plurals, direction selector (`Auto`, `FR → EN`, `EN → FR`, `FR → TR`, `TR → FR`; a fixed direction searches only the source language and the choice is saved), Turkish column and detail line, accent/œ/elision-tolerant search, TTS, add-to-word-bank (the Turkish gloss becomes the word's `tr` field when present), CSV/TSV import/export (`tr` column; header row recognised, old layout accepted)
- **AI-assisted dictionary**: words missing from the dictionary are looked up as structured JSON through LM Studio or an alternative OpenAI-compatible endpoint (NVIDIA NIM or any URL + API key); results (gender/plural, English and Turkish translation, example sentence, note) are cached in the local dictionary and work offline afterwards; when a `FR → TR` search finds an entry without a Turkish gloss the AI is asked in the background and the gloss is added to that same entry (no duplicate)
- Cards, multiple choice, typing, listening and matching study modes
- CEFR A1-C1 profiles and a scored exam engine
- French spelling, accent and sound lab covering all requested diacritics, apostrophe/elision, liaison, silent finals, nasal vowels, key vowel contrasts, rhythm and dictation
- Grammar labs for articles, gender/number, adjective agreement/position, pronouns, `y/en`, verb groups, negation, questions, present and past/future tenses, imperative, reflexives, prepositions and partitives
- Pronunciation, speaking, free writing and handwriting tools
- Local PDF text reading and page notes
- Open-license Resource Center with visible license and attribution
- Local AI tutor through LM Studio for explanation, translation, correction, conversation and vision/OCR tasks
- Per-task model profiles and a text-free token ledger
- Weekly progress report, light/dark themes and learner profiles
- Unicode CSV and `.fcapack` import/export

## Install and run from source

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\French_Course_AI.pyw
```

User data is stored under `%APPDATA%\FrenchCourseAI`. Set `FCA_HOME` to an isolated folder for testing or portable evaluation.

## Build the Windows EXE

```powershell
python -m pip install -r requirements-dev.txt
.\build.bat
```

Output: `dist\FrenchCourseAI.exe`. Build output and user data are excluded from Git.

## Local AI

Install LM Studio, download a chat model, and start its OpenAI-compatible Local Server. The default endpoint is `http://127.0.0.1:1234`. If the server is unavailable, only AI functions are disabled; the app keeps running.

Prompt and response text is not persisted. The token ledger stores only model, task, token counts, duration and success status.

### Dictionary AI provider

The dictionary tab can use two providers:

- **LM Studio** (local, no key) — `app.ai`, the address above.
- **Alternative endpoint** — any OpenAI-compatible API: the default is `https://integrate.api.nvidia.com/v1` (NVIDIA NIM, model `meta/llama-3.1-8b-instruct`), but another base URL such as OpenRouter, Groq or Ollama, a model name and an API key can be entered. Leave the key empty for a server that needs none (e.g. Ollama/LM Studio on another machine on your network): whether a key is required is decided by the server, not guessed from the address. The model name is sent exactly as typed. Enable it on the Settings page and check it with "Test connection"; the dictionary uses the same `GET /v1/models` probe.

The **Dictionary AI provider** policy (Settings page and the dictionary toolbar) is `Auto` (LM Studio if reachable, otherwise the alternative endpoint if enabled and reachable), `LM Studio`, `Alternative` or `Off`. When a search finds nothing locally the AI is asked in the background; the entries it returns are listed with source `AI` and, by default, stored in the `dict_entries` table. "Ask AI" merges AI entries on top of the list even when local results exist. The AI is asked for both `translation_en` and `translation_tr`; when a `FR → TR` search finds an entry without a Turkish gloss the AI is asked automatically and the returned gloss is written into the existing entry (for built-in entries an `ai`-sourced twin row lands in `dict_entries`; no new entry is created). The answer is matched to the existing entry by headword and meaning - a shared English sense - so it still lands when the AI words the English differently (`attic` / `attic; loft`), when a word has several senses (each gets its own gloss) or when the entry was added by hand without a part of speech.

The API key is stored in the Windows Credential Manager (`FrenchCourseAI/alt_api_key`); off Windows, or if the API fails, it falls back to `settings/secrets.json`. The key is never written to `settings.json`. The `FRENCHCOURSEAI_API_KEY` environment variable overrides the stored key.

## Privacy and optional internet use

- Profiles, progress, exams, PDF notes and counters live in a separate local SQLite database.
- SRS, exams, dictionary, grammar and packs work without internet access.
- Resource links open only on user action and use the internet.
- Remote AI services are optional and off by default; the API key lives in the Credential Manager, never in the settings file.

## Tests

```powershell
python -m pytest -q
```

The suite covers the window and all 18 pages, immediate/persistent language switching, complete i18n catalogs, migrations, 150+ seed words, the 1,210+-entry dictionary engine (fixed and automatic directions, Turkish field, import/export, SQLite user entries), AI dictionary lookup against a local mock OpenAI server (JSON parsing, Bearer header, provider resolution, the dictionary-tab flow), the secret store (file backend), the `dict_entries` schema migration, SRS, study/exam flows, accent-insensitive search, strict accented spelling, Unicode CSV, offline AI behavior, token privacy and pack round-trips. Tests never touch the real network or the Credential Manager.

## Structure

```text
French_Course_AI.pyw    entry point
fca/                    independent Python package
  tabs/                 modular learning, lab, reading and system pages
  db.py                 SQLite schema, migrations and repositories
  srs.py                SM-2 / Leitner scheduling
  content.py            French-specific learning content
  seed_words.py         original A1 starter vocabulary
  dictionary.py         dictionary engine and structured AI lookup
  dict_data.py          built-in FR-EN-TR dictionary data
  ai_client.py          OpenAI-compatible client (LM Studio, NIM, ...) and provider resolution
  secrets.py            API-key store (Credential Manager / file fallback)
tests/                  automated tests
grammar/                offline grammar notes
Resources/              learner-owned course files
docs/presentation/      editable PPTX, PDF and screenshots
```
