# French Course AI — User Guide

Version 1.2.1 · Windows and macOS desktop app · Interface languages: Türkçe, English, Français

## Table of contents

- [1. About this guide](#1-about-this-guide)
- [2. Installation](#2-installation)
- [3. Opening the app for the first time](#3-opening-the-app-for-the-first-time)
- [4. Screens](#4-screens)
- [5. The dictionary in detail](#5-the-dictionary-in-detail)
- [6. Artificial intelligence](#6-artificial-intelligence)
- [7. Data management](#7-data-management)
- [8. Shortcuts and tips](#8-shortcuts-and-tips)
- [9. Troubleshooting](#9-troubleshooting)
- [10. Release notes summary](#10-release-notes-summary)
- [11. Frequently asked questions](#11-frequently-asked-questions)

---

## 1. About this guide

French Course AI is a standalone desktop application for learners of French. This guide describes **version 1.2.1** and can be read on its own: no step needs another document.

It is written for a learner working somewhere between A1 and B1 in French, with Turkish as the third language of the dictionary. If you have just installed the app, read the guide end to end; in daily use, jump to the section you need. [4. Screens](#4-screens) covers all 18 pages in sidebar order; [5. The dictionary](#5-the-dictionary-in-detail) and [6. Artificial intelligence](#6-artificial-intelligence) describe what changed most in version 1.2.1.

Button and field names are quoted as the English interface shows them; switch the language and the same controls appear in Turkish or French. The core features work without the internet — only the Resource Center links and the optional alternative AI endpoint use it.

## 2. Installation

There is no installer, no Python requirement and no need for administrator rights; the packages are portable.

### 2.1 Windows (zip)

1. Download `FrenchCourseAI-Windows.zip`.
2. Right-click the zip and use **Extract All** to unpack it into a folder.
3. Double-click `FrenchCourseAI.exe`; nothing is installed, the app simply opens.
4. If SmartScreen warns you, choose **More info → Run anyway**.

The zip holds only `FrenchCourseAI.exe`; the `assets`, `Resources` and `grammar` folders are bundled inside the executable. Still extract the zip into a folder and run the .exe from there.

### 2.2 macOS (zip, Apple Silicon)

The `FrenchCourseAI-macOS.zip` package is built for Apple Silicon (arm64) and is **not notarized**:

1. Double-click the zip and move `FrenchCourseAI.app` into your **Applications** folder.
2. **Right-click** the app (or Control-click it) and choose **Open**.
3. Press **Open** again in the warning dialog.

This is needed only the first time; if you double-click instead, macOS says the app cannot be opened (see [9. Troubleshooting](#9-troubleshooting)).

### 2.3 Running from source

Python 3.11 or newer is required; the only runtime dependency is `pypdf`, used for PDF reading.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\French_Course_AI.pyw
```

To build your own `.exe`, run `python -m pip install -r requirements-dev.txt` and then `.\build.bat` (output `dist\FrenchCourseAI.exe`); the macOS package is produced on a Mac with `./build_macos.sh` (output `dist/FrenchCourseAI-macOS.zip`).

### 2.4 Where your data lives

| Platform | Data folder |
| --- | --- |
| Windows | `%APPDATA%\FrenchCourseAI` |
| macOS / Linux | `~/.frenchcourseai` |

Four subfolders are created inside it: `data` (the SQLite database `FrenchCourseAI.db`), `settings` (`settings.json`, plus `secrets.json` when needed), `exports` and `downloads`.

For portable use, point the **`FCA_HOME`** environment variable at another folder; the app then creates everything there and never touches the default location:

```powershell
$env:FCA_HOME = "D:\FrenchData"
.\FrenchCourseAI.exe
```

## 3. Opening the app for the first time

The window opens at 1360 × 860 (minimum 1080 × 700): a grouped sidebar of 18 pages on the left, the page title plus the profile, language and AI indicators along the top, and a status bar at the bottom. The app starts on **Spaced Review**. On first launch the following is prepared in the background:

- **Profile.** A default profile named `Alex` is created. The **+** button at the top adds a profile and the list beside it switches between them. Progress, exams and notes are per profile; words and the dictionary are shared.
- **Interface language.** The list next to the 🌐 icon offers **Türkçe · English · Français** (Turkish by default); the choice applies immediately and is saved.
- **Theme.** Dark by default; pick `dark` / `light` in **Settings → Theme** and press **Save** to redraw the window.
- **Daily goal.** 20 by default; Settings accepts 5-200 and the Progress page shows it.
- **Data.** 162 A1 words are written to the database and the 1,219-entry built-in dictionary is loaded into memory. Both ship inside the app; nothing is downloaded.

The **AI:** badge in the top right probes the LM Studio address shortly after start-up and reads **Available** or **Unavailable**; without LM Studio only the AI features wait.

## 4. Screens

The sidebar has five groups; the 18 pages below are described in sidebar order.

| Group | Pages |
| --- | --- |
| **LEARN** | Spaced Review · Word Bank · Dictionary FR-EN-TR · Exam |
| **LABS** | Spelling & Sound · Pronunciation · Grammar |
| **READ & EXPLORE** | Resource Center · PDF Reader · Course Library |
| **PRACTICE** | AI Tutor · Speaking · Writing & Handwriting |
| **PROGRESS & SYSTEM** | Progress · Packs · Token Ledger · Offline Guide · Settings |

### 4.1 LEARN group

**Spaced Review** — drills words along the forgetting curve; four tiles show **Due today**, **New**, **Mistakes** and **Favorites**.
*How:* pick `new`, `due`, `wrong` or `favorites` from the queue list (these four codes stay English in every interface language), choose **Cards**, **Multiple choice**, **Typing**, **Listening** or **Matching** as the mode and a card count between 5 and 50 (10 by default), then press **Start**; **Show answer** reveals the glosses, after which you grade yourself with **Again**, **Hard**, **Good** or **Easy**.
*Tip:* in this version the mode only changes **Listening** — the word is spoken as the card opens; **Multiple choice**, **Typing** and **Matching** run the same card flow. Anything you mark **Easy** returns at ever longer intervals.

**Word Bank** — the personal list that feeds review and exams; the columns are **French**, **Turkish**, **English**, **Article**, **Plural** and **Deck**.
*How:* type in the box and press **Search** or Enter; the search covers all three languages and selecting a row shows the example sentences underneath. **★ Favorite** toggles a favorite, **↑ Export** writes a UTF-8 CSV and **↓ Import** reads one back.
*Tip:* words added from the dictionary land in the `Dictionary FR-EN-TR` deck.

**Dictionary FR-EN-TR** — this page is covered in full in [section 5](#5-the-dictionary-in-detail).

**Exam** — builds a multiple-choice exam from random word-bank entries and scores it as a percentage.
*How:* set **Question count** between 5 and 50 (10 by default) and press **Start**; each question offers four Turkish options and you confirm with **Check**. At the end you see **Exam complete** and **Score: …%** (the score carries one decimal, for example `Score: 80.0%`).
*Tip:* the result feeds the weekly report and shows up on the Progress chart.

### 4.2 LABS group

**Spelling & Sound** — introduces the French spelling marks and runs dictation; the table lists `A–Z`, `é`, `è / ê / ë`, `à / â`, `î / ï`, `ô`, `ù / û / ü`, `ç`, `'`, `liaison`, `finale`, `nasales`, `r`, `u / ou` and `rythme`.
*How:* select a row on the left and its rule appears on the right. Under **Dictation exercise**, **▶ Speak** reads the word in the box; type what you hear and press **Check** — a ✓ for a hit, or `→` with the correct spelling.
*Tip:* replace the pre-filled word with your own. The comparison is **accent-sensitive**: `eleve` and `élève` count as different.

**Pronunciation** — speaks any word you type and lists nine sound groups (`r`, `u / ou`, `on`, `an / en`, `in / ain`, `eu / œu`, `é / è`, `oi`, `ch / j`) with IPA and examples.
*How:* type the word and press **▶ Speak**.
*Tip:* **◉ Compare with microphone** is not active in this version; pressing it prints **Unavailable**.

**Grammar** — a lab of 29 topics: definite articles, noun gender, adjective agreement, `y` and `en`, the perfect past (`Passé composé`), elision and liaison, and more.
*How:* pick a topic on the left and its rule and example appear on the right; select an option under **Exercise**, press **Check**, and **Next** brings a new one.
*Tip:* the 18-question pool is independent of the topic, and your right/wrong counts are recorded against the exercise's own topic, not the one selected in the list. The pool covers 18 of the 29 topics, so the remaining ones never receive a count.

### 4.3 READ & EXPLORE group

**Resource Center** — lists four openly licensed external sources (Wikibooks, Tatoeba, LibriVox, Project Gutenberg) with level, **License:** and **Attribution:**.
*How:* the **Open ↗** button on a card opens the link in your default browser.
*Tip:* the notice **ⓘ Opening links uses the internet.** sits at the top; the app links to these sources, it does not bundle them.

**PDF Reader** — shows the text of a local PDF page by page and keeps a separate note per page.
*How:* open a file with **Choose PDF**, move through it with the **Page** spinner, then write in the **Page note** box and press **Save**; the note is tied to profile + file + page and reloads when you return.
*Tip:* the last PDF you opened is remembered. Scanned PDFs leave the text pane empty; use the **Image / OCR** task for those.

**Course Library** — lists the `Resources` folder next to the app with the columns **Name**, **Part of speech** (the label the app reuses for the file type) and **MB**.
*How:* **Open course folder** opens the folder in Explorer, **Refresh** rebuilds the list, and double-clicking a row opens the file in its default application.
*Tip:* subfolders are scanned too, so you can organise your lessons by topic. When you run from source, the `Resources` folder next to the app is listed; in the packaged .exe that folder is unpacked into a temporary directory on each launch and removed when the app closes, so do not keep your lesson files there.

### 4.4 PRACTICE group

**AI Tutor** — four tasks against the local model: **Explain**, **Translate**, **Correct** and **Image / OCR**.
*How:* choose the **Task**, type your text and press **Send**. For the image task, first pick a `.png`, `.jpg`, `.jpeg` or `.webp` file with the **Image / OCR** button; if the text box is empty a built-in prompt is used.
*Tip:* the footer reads **🔒 Prompt and response text is never saved; only token counts are logged.** When the AI is unreachable you get **AI is disabled or LM Studio cannot be reached.**

**Speaking** — written role-play in five scenarios: `Au café`, `À la gare`, `À l'hôtel`, `Dans un magasin`, `Chez le médecin`.
*How:* pick a **Scenario** and press **Start conversation**; the model asks one short question, and you type your French reply into the box below and press **Send**.
*Tip:* this page always uses local LM Studio; the alternative endpoint serves the dictionary only.

**Writing & Handwriting** — free writing with AI correction on the left, a mouse-driven writing canvas on the right.
*How:* the prompt reads **Write in French about what you did today.**; type your text and press **Correct with AI** to get the corrected version and the rule explanation in the lower box. Draw in the **Handwriting area** with the mouse and empty it with **Clear**.
*Tip:* the canvas is never saved; leaving the page discards it.

### 4.5 PROGRESS & SYSTEM group

**Progress** — the tiles **Daily goal**, **Day streak**, **Studied** and **Learned**, a bar chart of the **Last 7 days**, and the **Weekly report** line (Correct · Wrong · Score).
*How:* just open the page; "Studied" counts words you have answered at least once, "Learned" those in Leitner box 4 or higher, and each bar is that day's correct + wrong total.
*Tip:* "Day streak" counts consecutive days of study and resets if you skip one.

**Packs** — writes your word bank (optionally with progress) into a single `.fcapack` file and reads it back.
*How:* with **Include progress** ticked, the profile's review data goes into the pack too; **↑ Export** saves the file, **↓ Import** opens one, and you get **Pack created** or **Pack imported**.
*Tip:* packs are tagged with the target language, so a pack from another language's app is rejected.

**Token Ledger** — the tiles **Calls** and **Total tokens** plus a table of the last 500 calls: `Ts`, `Model`, `Task`, `Prompt Tokens`, `Completion Tokens`, `Total Tokens`, `Ms`, `Ok`.
*How:* open the page and read the list; it shows which model spent how many tokens on which task.
*Tip:* the table holds no prompt or response text at all; it is your source for cost tracking.

**Offline Guide** — summarises which features are local and which need the internet, and prints the full path of your data folder at the bottom.
*How:* open the page and read it; dictionary directions, the AI policy, where the key is kept and the CSV layout are summarised there as well.
*Tip:* read the data-folder path from here when you make a backup.

**Settings** — every persistent preference in the app.

| Setting | Value | Default |
| --- | --- | --- |
| **Theme** | `dark` / `light` | `dark` |
| **Daily goal** | 5-200 | 20 |
| **Text to speech** | on / off | on |
| **Local AI** | on / off | on |
| **LM Studio address** | URL | `http://127.0.0.1:1234` |
| **Default model** | model name | `qwen2.5-7b-instruct` |
| **Dictionary AI provider** | Auto / LM Studio / Alternative / Off | Auto |
| **Save AI dictionary results into the dictionary** | on / off | on |
| **Use the alternative endpoint** | on / off | off |
| **Base URL** | URL | `https://integrate.api.nvidia.com/v1` |
| **Model** | model name | `meta/llama-3.1-8b-instruct` |
| **API key** | secret text | empty |

*How:* change the values and press **Save**; **Settings saved** appears and the window is redrawn if the theme changed. **Test connection** probes the alternative endpoint and reports **Connection OK · N models** or **Connection failed**; **Delete key** removes the stored key.
*Tip:* the label beside the key field reads **••••• stored** or **no key stored**; the key is never printed back to the screen.

## 5. The dictionary in detail

The dictionary is a trilingual search engine: **French ↔ English ↔ Turkish**. Its 1,219 built-in entries ship inside the app and work offline; your own entries and cached AI entries are layered on top. The counter at the bottom shows the split: `… entries · built-in … · user … · AI …`.

### 5.1 Direction selector

The **Direction:** list on the second toolbar row offers five choices:

| Choice | Code | What it does | When to pick it |
| --- | --- | --- | --- |
| **Auto** | `auto` | Searches all three sides; the best-scoring side decides the direction | Everyday use |
| **FR → EN** | `fr2en` | Searches French headwords only | The English gloss of a French word |
| **EN → FR** | `en2fr` | Searches English glosses only | Producing French from English |
| **FR → TR** | `fr2tr` | Searches French headwords and moves the Turkish column forward | The Turkish gloss of a French word; **this is the direction that has the AI fill a missing gloss** |
| **TR → FR** | `tr2fr` | Searches Turkish glosses only | The French word for a Turkish one |

The choice is saved at once and survives a restart. The small label right of the search box prints the current direction (`FR → EN` and so on); in **Auto** mode it shows what the engine decided. A fixed direction scans only the source side, so lookalike strings in the other languages cannot interfere.

### 5.2 The Turkish column and the detail panel

The table columns are **French**, **English**, **Turkish**, **Part of speech**, **Gender / Plural** and **Source**. In the `FR → TR` direction the **Turkish** column moves right next to the headword; entries with no known Turkish gloss are marked `—`.

The detail panel shows the headword in large type; below it the part of speech, the gender (`m`, `f`, `mf`, `pl`), the article where one applies (`le`, `la`, `les`, or `le/la` for common-gender nouns) and any irregular plural; the **English:** and **Turkish:** lines (Turkish moves to the top in `FR → TR`); an « example sentence » if there is one; the note; and, when the word is already in your bank, a **★ Word Bank: …** line. The buttons are **🔊 Speak**, **✦ Ask AI**, **Copy**, **★ Add to word bank** and — only for unsaved AI entries — **💾 Save to dictionary**. Below them sit the **Recent lookups** list, which keeps 12 queries, and the **AI answer** box.

### 5.3 Search rules

The list refreshes quietly as soon as you have typed two letters; Enter or **Search** runs a full search (it records the query in the history and asks the AI when needed). Ranking runs from best to weakest:

1. **Exact match** — the headword or one of the senses equals the query.
2. Exact match after a leading `to` / `the` / `a` / `an` / `sich` / `se` / `s'` is dropped (both `to speak` and `speak` find `parler`).
3. **Prefix** — the query `mai` returns `maison`.
4. **Word start** — the query starts one of the words of a multi-word gloss.
5. **Substring** — for queries of at least three letters.
6. **Note field** — a last resort when nothing else matches.

The search tolerates the following without altering the stored spelling:

- **Accents do not matter:** `eleve` → `élève`, `ecole` → `école`.
- **Ligatures are expanded:** `œ` → `oe`, `æ` → `ae`; `oeil` and `œil` are the same.
- **Elision is stripped:** the prefixes `l'`, `d'`, `j'`, `s'`, `qu'`, `n'`, `m'`, `t'`, `c'` are ignored (`l'école` → `école`).
- **Turkish letters are folded:** `ç/c`, `ğ/g`, `ş/s`, `ö/o`, `ü/u`, `İ/I/ı → i`; `ışık` and `isik` give the same result.

This tolerance applies **to search only**; dictation and exam answers are compared accent-sensitively.

### 5.4 Source labels

| Label | Meaning |
| --- | --- |
| **built-in** | The core dictionary shipped with the app (1,219 entries) |
| **user** | Entries you added by hand or imported from CSV/TSV |
| **AI** | Entries returned by the AI and cached in the local dictionary |

Once an AI entry is stored it is found offline as well; a second lookup never touches the network.

### 5.5 Filling a missing Turkish gloss with the AI

This is the most visible change in version 1.2.0. When a search in the **FR → TR** direction finds an entry whose Turkish column is `—` and the AI policy is not **Off**, the app asks the AI in the background: the status bar first reads **Turkish gloss missing, asking the AI…** and then **Turkish gloss added by the AI**.

The gloss that comes back is **written into the existing entry**; no duplicate is created beside it. Matching goes through the headword and a shared English sense, so the gloss reaches the right entry even when the AI words the English differently (`attic` / `attic; loft`), when the word is polysemous (each sense gets its own gloss), or when you added the entry by hand and left the part-of-speech field empty.

**✦ Ask AI** is independent of this: it asks even when local results exist and puts the AI entries on top of the list. When nothing is found at all, the AI is queried automatically and the message **Not found in the dictionary. Ask the AI or add it yourself.** appears. The answer ends with **Answered by: LM Studio · model-name** or **Answered by: Alternative · model-name**. With **Save AI dictionary results into the dictionary** switched off, entries are only displayed; select the one you want and press **💾 Save to dictionary** to keep it.

### 5.6 Adding to the word bank

**★ Add to word bank** copies the selected entry into your study deck: when a Turkish gloss exists, its first sense goes into the word's `tr` field and the English gloss into `en`; without a Turkish gloss the first English sense fills the Turkish field. For nouns the gender (`masculin`, `féminin`, `masculin/féminin`, `pluriel`), the article and any irregular plural are carried over too. The word joins the `Dictionary FR-EN-TR` deck and turns up in the **New** queue of Spaced Review.

### 5.7 CSV import / export

**↑ Export CSV** writes the results currently listed, or the whole dictionary when the list is empty; the file name defaults to `dictionary_fr.csv` and the dialog starts in the `exports` folder.

| # | Column | Contents |
| --- | --- | --- |
| 1 | `headword` | French headword (no article, correct accents) |
| 2 | `translation` | English gloss; senses separated by `; ` |
| 3 | `pos` | Part-of-speech code: `n`, `v`, `adj`, `adv`, `pron`, `prep`, `conj`, `num`, `art`, `int`, `part`, `phr` |
| 4 | `extra` | For nouns the gender (`m`, `f`, `mf`, `pl`) plus an irregular plural; empty otherwise |
| 5 | `note` | Short note; for verbs usually the participe passé |
| 6 | `source` | `builtin`, `user` or `ai` |
| 7 | `example` | Short French example sentence (may be empty) |
| 8 | `tr` | Turkish gloss; senses separated by `; ` |

```csv
headword,translation,pos,extra,note,source,example,tr
maison,house,n,f,,builtin,,ev
œil,eye,n,m yeux,,builtin,,göz
aller,to go,v,,allé (être),builtin,,gitmek
journal,newspaper; diary,n,m journaux,,builtin,,gazete; günlük
```

**↓ Import CSV/TSV** reads `.csv`, `.tsv` and `.txt` files and detects the delimiter itself. With a header row the columns may come in **any order**, and names such as `word`, `target`, `français`, `meaning`, `english`, `türkçe`, `turkish` and `definition` are recognised. Without a header the order above is assumed; the older layout without a `tr` column is accepted as well. Empty rows are skipped and the same entry is never added twice.

### 5.8 Adding an entry by hand

**+ Add entry** opens a small window with **French**, **English**, **Turkish**, **Part of speech (n/v/adj/…)**, **Gender / Plural**, **Note / definition** and **Example sentence**. If the search box holds text, the matching field is pre-filled. Leaving the French or the English field empty raises **French and English fields are required.** **Save** (or Enter) stores the entry with the `user` source; **Esc** closes the window.

## 6. Artificial intelligence

The AI is **optional**: with it switched off, vocabulary, review, exams, grammar, the dictionary, PDFs and progress all keep working.

### 6.1 Installing LM Studio and its local server

1. Install LM Studio and download a chat model.
2. Open its **Local Server** (OpenAI-compatible) section, load the model and start the server.
3. The default address is `http://127.0.0.1:1234`; if you use a different port, write it into **Settings → LM Studio address**.
4. Wait for the badge in the top right to read **AI: Available**.

The local server needs no key and your requests never leave the machine.

### 6.2 Model selection

| Task | Preferred models |
| --- | --- |
| `chat` | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `grammar` (Explain) | `qwen2.5-7b-instruct`, `qwen2.5-14b-instruct` |
| `translate` (Translate) | `qwen2.5-7b-instruct`, `gemma-2-9b-it` |
| `correct` (Correct / Writing) | `qwen2.5-7b-instruct`, `qwen2.5-14b-instruct` |
| `dialogue` (Speaking) | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `dictionary` (Dictionary) | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `vision` (Image / OCR) | `qwen2-vl-7b-instruct`, `llava-v1.6-mistral-7b` |

The **Default model** from Settings is used directly if LM Studio has it loaded; otherwise the first loaded model from that task's profile is chosen, and failing that the top of the ranking. **Specialist models are skipped** in that ranking: names containing `embed`, `rerank`, `math`, `coder`, `code-`, `vision`, `-vl`, `llava`, `moondream`, `bio`, `medic`, `whisper`, `tts`, `audio`, `clip`, `sd-` or `stable-diffusion` are used only when nothing else exists. Ties favour 4-16 billion parameter models whose names contain `instruct` / `-it` / `chat` / `assistant`.

### 6.3 Alternative endpoint

The group heading in Settings reads **Alternative endpoint (OpenAI-compatible: NVIDIA NIM, OpenRouter, Groq, Ollama…)**.

1. Tick **Use the alternative endpoint**.
2. Enter the **Base URL**; the default is `https://integrate.api.nvidia.com/v1` (NVIDIA NIM).
3. Enter the **Model** name (default `meta/llama-3.1-8b-instruct`); it is sent to the server **exactly as typed**.
4. Paste your key into **API key**; leave it empty for a server that needs none (an Ollama or LM Studio elsewhere on your network, say) — whether a key is required is decided by the server, not guessed from the address.
5. Press **Save**, then **Test connection**: you get **Connection OK · N models**, plus **selected model not listed** if the name is not in the catalogue.

The alternative endpoint is used **by the dictionary only**; the AI Tutor, Speaking and Writing pages always talk to local LM Studio.

### 6.4 How the API key is stored

The key is **never written into `settings.json`**. On Windows it lives in the Credential Manager under the name `FrenchCourseAI/alt_api_key`; off Windows, or if that API is unavailable, the file `settings/secrets.json` takes over. **Delete key** removes it from both places, and the `FRENCHCOURSEAI_API_KEY` environment variable overrides the stored key when it is set.

### 6.5 Dictionary AI policy

You can change the policy either from **Settings → Dictionary AI provider** or from the **AI:** list on the dictionary toolbar; both write the same setting.

| Policy | Behaviour |
| --- | --- |
| **Auto** | LM Studio when reachable; otherwise the alternative endpoint when it is enabled and reachable; otherwise no AI |
| **LM Studio** | The local server only; no AI when it is unreachable |
| **Alternative** | The alternative endpoint only; no AI when it is off or unreachable |
| **Off** | No AI call is ever made |

The status label on the toolbar tells you the current truth: **LM Studio: connected**, **Alternative: ready**, **AI unreachable** or **AI off**. The reachability probe is a `GET /v1/models` request and the verdict is cached for 30 seconds. **Test connection** sends the same request, but it probes the values currently in the form (an unsaved key included) while the dictionary uses the saved ones, so the two can disagree until you press Save.

### 6.6 Token ledger and privacy

Every AI call adds one row to the Token Ledger: timestamp, model, task, prompt tokens, completion tokens, total, duration in ms and success flag. **Prompt and response text is never stored anywhere**, and an image you send is not kept either.

Dictionary calls ask for structured JSON: at most 5 entries, a 1,200-token budget and a 90-second timeout. Because "thinking" models can spend the whole budget on reasoning and return nothing, local servers are sent a `reasoning_effort` field (a server that rejects it is retried without it); if the answer was cut off by the length limit, the call is repeated once with three times the budget.

## 7. Data management

**Profiles.** The list in the top bar shows the profiles and **+** adds one. Each profile keeps its own review schedule, exam history, favorites, PDF notes and grammar statistics; the word bank, the dictionary and the settings are shared. This version has no delete-profile button in the interface.

**Backups.** There are three routes: Word Bank → **↑ Export** (a UTF-8 word CSV), Dictionary → **↑ Export CSV** (columns as in [5.7](#57-csv-import--export)), Packs → **↑ Export** (`.fcapack`). The most complete backup is a copy of the whole data folder; close the app before copying it.

**Resetting.** There is no "delete everything" button inside the app. For a clean start, close the app, back up and delete the data folder (or just `data\FrenchCourseAI.db`); the next launch recreates the database, the default profile and the built-in word deck. To reset only the preferences, delete `settings\settings.json`. To experiment without deleting anything, use a temporary folder via `FCA_HOME`.

## 8. Shortcuts and tips

| Shortcut | Where | What it does |
| --- | --- | --- |
| **Enter** | Dictionary search box | Runs a full search (records history, asks the AI when needed) |
| **Typing 2+ letters** | Dictionary search box | Refreshes the list quietly, without asking the AI |
| **Double-click** | Dictionary result list | Speaks the selected headword |
| **Enter** | Add-entry window | Saves the entry |
| **Esc** | Add-entry window | Closes the window |
| **Enter** | Word Bank search box | Runs the search |
| **Double-click** | Course Library list | Opens the file in its default application |
| **Drag with the mouse** | Handwriting area | Draws a line |

Other tips:

- **🎲 Random word** opens a random built-in entry; it finds the word even under a fixed `EN → FR` or `TR → FR` direction, because the direction is flipped for that one search and your choice is left untouched.
- **Copy** puts the entry on the clipboard as `headword — English — Turkish`.
- Speech uses the Windows speech engine and picks an `fr-*` voice when one is installed.

## 9. Troubleshooting

**LM Studio will not connect / the badge says "Unavailable".** The local server is not running, no model is loaded, or the address differs. Load a model in LM Studio and start **Local Server**, compare **LM Studio address** in Settings with the server's port (default `http://127.0.0.1:1234`), and make sure **Local AI** is ticked. The verdict is cached for 30 seconds, so switch pages once and come back.

**The AI answers with nothing / "The AI returned no entry for this query."** Usually a "thinking" model has spent its token budget on reasoning, or the model is too small to produce JSON. Pick an instruct model such as `qwen2.5-7b-instruct` in Settings and avoid models named `coder`, `math` or `embed`. The app retries a truncated answer once with a larger budget, but a proper chat model removes the problem entirely.

**No Turkish gloss — the column shows `—`.** The entry was added without one (by hand or from CSV), or the AI policy is **Off**. Switch the direction to **FR → TR** and search again; unless the policy is Off, the missing gloss is fetched in the background and written into that same entry. If you would rather not use the AI, fill it in with **+ Add entry** or import a CSV that has the `tr` column.

**macOS says the app cannot be opened.** The package is not notarized. Instead of double-clicking, **right-click and choose Open**, then press **Open** in the warning; the permission is remembered afterwards.

**There is no sound.** **Text to speech** may be off, no French voice may be installed, or you may be on a non-Windows system. Tick **Text to speech** in Settings and install the French voice from *Settings → Time & language → Speech* on Windows; speech relies on the Windows `System.Speech` engine.

**The .exe does not start.** It may have been run from inside the zip, blocked by SmartScreen, or quarantined by antivirus software. Extract the zip into a folder, choose **More info → Run anyway** at the SmartScreen prompt, and add a folder exception in your antivirus if needed. If it still fails, run `python .\French_Course_AI.pyw` from source to see the error message.

**Where is my data?** `%APPDATA%\FrenchCourseAI` on Windows, `~/.frenchcourseai` on macOS/Linux; the full path is always printed at the bottom of the **Offline Guide** page. With `FCA_HOME` set, the data lives there instead — and deleting the app does not delete that folder.

## 10. Release notes summary

| Version | Highlights |
| --- | --- |
| **v1.0.0** | The 18-page shell: SM-2/Leitner review, word bank (162 A1 words), exam, spelling/pronunciation/grammar labs, Resource Center, PDF reader, course library, AI Tutor through LM Studio, speaking and writing, progress, packs, token ledger; tr/en/fr interface; Windows and macOS packages |
| **v1.1.0** | The **dictionary tab** (bidirectional French-English) and its **AI connection**: LM Studio or an alternative OpenAI-compatible endpoint, the AI policy, and the key stored in the Credential Manager |
| **v1.1.1** | Dictionary AI fixes: empty answers from thinking models, better model selection |
| **v1.1.2** | Dictionary AI polish: cleanup of the noun `extra` field, a direction label on the AI answer, toolbar layout, deduplicated senses |
| **v1.2.0** | The **direction selector** (`Auto`, `FR → EN`, `EN → FR`, `FR → TR`, `TR → FR`; the choice is saved) and **Turkish as a third language**: a Turkish column in the table and the detail panel, a missing Turkish gloss filled by the AI into the same entry in the `FR → TR` direction, a `tr` column in CSV, 1,219 built-in entries |
| **v1.2.1** | **ASCII and upper-case support for Turkish search**: `sinav` = `SINAV` = `sınav`, `cok` = `çok`, `ogrenci` = `öğrenci`; Turkish folding runs before the French accent simplification, a match found only through folding ranks below a direct match, and the spelling shown is unchanged. Also the **user guide** was added to the repository (`docs/KULLANIM_KILAVUZU.md` and `docs/USER_GUIDE.md`; the PDF is published as a release asset) |

## 11. Frequently asked questions

**Does the app work without the internet?** Yes. Vocabulary, review, exams, grammar, the 1,219 built-in dictionary entries, PDF notes and progress are entirely local; only the Resource Center links and the alternative AI endpoint need a connection.

**Is the dictionary useful without the AI?** It is. The built-in dictionary carries 1,219 entries with gender, irregular plurals and both English and Turkish glosses; the AI only steps in for missing words and missing Turkish glosses.

**Is my data sent to a server?** No. Your profiles, progress, exams, notes and dictionary stay in a SQLite file on your computer; only when you enable the alternative endpoint yourself do dictionary queries go to that service — and prompt/response text is stored nowhere.

**Where is my API key kept?** In the Windows Credential Manager under `FrenchCourseAI/alt_api_key`, and in `settings/secrets.json` on other systems. It is never written into `settings.json` and never shown back on screen.

**What if Auto guesses the direction wrongly?** Pick a fixed direction: `chat` is both the French word for "cat" and an English word, and `FR → EN` removes the ambiguity.

**Do I have to type the accents?** Not for searching: `eleve` finds `élève` and `oeil` finds `œil`. In dictation and exam answers the comparison is accent-sensitive, because the point there is to teach correct spelling.

**How do I load my own word list?** Use **↓ Import** in the Word Bank (a word CSV) or **↓ Import CSV/TSV** in the Dictionary (a dictionary table; it recognises the header row and does not care about column order).

**How do I get a word into both the dictionary and my study deck?** Select the entry in the dictionary and press **★ Add to word bank**; the word joins the `Dictionary FR-EN-TR` deck and shows up in the **New** queue in your next session.

**Which model should I install?** `qwen2.5-7b-instruct` is a good starting point; instruct models of 4-16 billion parameters are both fast enough and good enough.

**Will uninstalling the app delete my data?** No. Removing the program folder leaves the data folder untouched; to delete the data as well, remove `%APPDATA%\FrenchCourseAI` by hand.
