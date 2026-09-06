from __future__ import annotations

import tkinter as tk
from dataclasses import replace
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .. import config as C
from .. import dictionary as D
from ..ai_client import AIError
from ..ui import BaseTab


class DictionaryTab(BaseTab):
    """Three-language dictionary (target ↔ English ↔ Turkish): built-in core entries + the user's own entries + cached AI entries.

    The direction selector (setting ``dict_direction``) is ``auto`` or one of :data:`fca.dictionary.DIRECTIONS`; a fixed
    direction searches only its source side. In a ``*2tr`` direction an entry without a Turkish gloss is completed by the AI
    (per the AI policy) and the gloss is written into that entry instead of adding a duplicate."""
    key, subtitle_key = "tab.dictionary", "dict.subtitle"
    MAX_HISTORY = 12
    POLICY_KEYS = {"auto": "dict.ai_auto", "local": "dict.ai_local", "alt": "dict.ai_alt", "off": "dict.ai_off"}
    COLUMNS = ("head", "trans", "tr", "pos", "extra", "src") if D.HAS_TR else ("head", "trans", "pos", "extra", "src")

    def build(self):
        self.heading()
        self.dict = D.build_dictionary([(r["headword"], r["translation"], r["pos"], r["extra"], r["note"], r.get("source", D.SOURCE_USER),
                                         r.get("example", ""), r.get("tr", "")) for r in self.repos.dictionary.all()])
        self.results = []; self.history = []; self._typed = ""; self._ai_seq = 0; self._ai_busy = False
        bar = ttk.Frame(self); bar.pack(fill="x", pady=(0, 6))
        airow = ttk.Frame(self)          # direction + AI policy + provider state live on their own row so the toolbar never overflows
        self.query = tk.StringVar()
        self.entry = ttk.Entry(bar, textvariable=self.query, font=("Segoe UI", 12)); self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _e: self.search()); self.entry.bind("<KeyRelease>", self._on_key)
        ttk.Button(bar, text=self.t("g.search"), style="Accent.TButton", command=self.search).pack(side="left", padx=5)
        self.dir_label = ttk.Label(bar, text="", style="Muted.TLabel", width=9); self.dir_label.pack(side="left", padx=(2, 8))
        ttk.Button(bar, text="🎲 " + self.t("dict.random"), command=self.random_word).pack(side="left")
        ttk.Label(airow, text=self.t("dict.direction"), style="Muted.TLabel").pack(side="left", padx=(0, 4))
        self._direction_labels = {code: (self.t("dict.dir_auto") if code == "auto" else D.direction_text(code)) for code in D.DIRECTIONS}
        self.direction = tk.StringVar(value=self._direction_labels[self._direction()])
        self.direction_box = ttk.Combobox(airow, textvariable=self.direction, state="readonly", width=10, values=[self._direction_labels[c] for c in D.DIRECTIONS])
        self.direction_box.pack(side="left"); self.direction_box.bind("<<ComboboxSelected>>", self._direction_changed)
        ttk.Label(airow, text=self.t("dict.ai_policy"), style="Muted.TLabel").pack(side="left", padx=(14, 4))
        self._policy_labels = {code: self.t(k) for code, k in self.POLICY_KEYS.items()}
        self.policy = tk.StringVar(value=self._policy_labels.get(self.app.settings.get("dict_ai", "auto"), self._policy_labels["auto"]))
        self.policy_box = ttk.Combobox(airow, textvariable=self.policy, state="readonly", width=11, values=[self._policy_labels[c] for c in C.DICT_AI_POLICIES])
        self.policy_box.pack(side="left"); self.policy_box.bind("<<ComboboxSelected>>", self._policy_changed)
        self.ai_state = ttk.Label(airow, text="", style="Muted.TLabel"); self.ai_state.pack(side="left", padx=(8, 0))
        airow.pack(fill="x", pady=(0, 8))
        ttk.Button(bar, text="+ " + self.t("dict.add_entry"), command=self.add_entry).pack(side="right", padx=3)
        ttk.Button(bar, text=f"↓ {self.t('dict.import')}", command=self.import_file).pack(side="right", padx=3)
        ttk.Button(bar, text=f"↑ {self.t('dict.export')}", command=self.export_file).pack(side="right", padx=3)

        pane = ttk.PanedWindow(self, orient="horizontal"); pane.pack(fill="both", expand=True)
        left = ttk.Frame(pane)
        self.tree = ttk.Treeview(left, columns=self.COLUMNS, show="headings", selectmode="browse")
        specs = {"head": (self.t("dict.headword"), 190, False), "trans": (self.t("dict.translation"), 220, True),
                 "tr": (self.t("dict.turkish"), 200, True), "pos": (self.t("words.pos"), 70, False),
                 "extra": (self.t("dict.extra"), 110, False), "src": (self.t("dict.source"), 70, False)}
        for col in self.COLUMNS:
            title, width, stretch = specs[col]
            self.tree.heading(col, text=title); self.tree.column(col, width=width, minwidth=40, anchor="w", stretch=stretch)
        self.tree.configure(displaycolumns=self._columns_for(self._direction()))
        vs = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview); self.tree.configure(yscrollcommand=vs.set)
        self.tree.pack(side="left", fill="both", expand=True); vs.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.selected); self.tree.bind("<Double-1>", lambda _e: self.speak())
        pane.add(left, weight=3)

        right = self.card(pane); pane.add(right, weight=2)
        self.w_head = ttk.Label(right, text="—", style="Card.TLabel", font=("Segoe UI", 24, "bold"), wraplength=360, justify="left"); self.w_head.pack(anchor="w")
        self.w_meta = ttk.Label(right, text="", style="CardMuted.TLabel", wraplength=360, justify="left"); self.w_meta.pack(anchor="w", pady=(4, 0))
        self.w_trans = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 12, "bold"), wraplength=360, justify="left"); self.w_trans.pack(anchor="w", pady=(10, 0))
        self.w_tr = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 12, "bold"), wraplength=360, justify="left")
        if D.HAS_TR: self.w_tr.pack(anchor="w", pady=(2, 0))
        self.w_example = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 10, "italic"), wraplength=360, justify="left"); self.w_example.pack(anchor="w", pady=(6, 0))
        self.w_note = ttk.Label(right, text="", style="CardMuted.TLabel", wraplength=360, justify="left"); self.w_note.pack(anchor="w", pady=(6, 0))
        self.w_bank = ttk.Label(right, text="", style="CardMuted.TLabel", wraplength=360, justify="left"); self.w_bank.pack(anchor="w", pady=(6, 0))
        row1 = ttk.Frame(right, style="Card.TFrame"); row1.pack(anchor="w", pady=(12, 3))
        ttk.Button(row1, text="🔊 " + self.t("pron.speak"), command=self.speak).pack(side="left")
        ttk.Button(row1, text="✦ " + self.t("dict.ask_ai"), command=self.ask_ai).pack(side="left", padx=4)
        ttk.Button(row1, text=self.t("dict.copy"), command=self.copy_entry).pack(side="left")
        row2 = ttk.Frame(right, style="Card.TFrame"); row2.pack(anchor="w", pady=(0, 10))
        ttk.Button(row2, text="★ " + self.t("dict.to_bank"), style="Accent.TButton", command=self.add_to_bank).pack(side="left")
        self.save_btn = ttk.Button(row2, text="💾 " + self.t("dict.save_entry"), command=self.save_ai_entry)   # packed only for unsaved AI entries
        ttk.Label(right, text=self.t("dict.history") + ":", style="CardMuted.TLabel").pack(anchor="w")
        self.hist = tk.Listbox(right, height=5, activestyle="none", relief="flat", highlightthickness=0,
                               bg=self.palette["panel"], fg=self.palette["fg"], font=("Segoe UI", 9))
        self.hist.pack(fill="x"); self.hist.bind("<<ListboxSelect>>", self._pick_history)
        ttk.Label(right, text=self.t("dict.ai_answer") + ":", style="CardMuted.TLabel").pack(anchor="w", pady=(10, 0))
        self.ai_out = self.text(right, height=8); self.ai_out.pack(fill="both", expand=True); self.ai_out.configure(state="disabled")

        self.count_label = ttk.Label(self, text="", style="Muted.TLabel"); self.count_label.pack(anchor="w", pady=(6, 0))
        self._update_count(); self.entry.focus_set(); self.refresh_ai_state()

    # ------------------------------------------------------------------
    def on_show(self):
        """Called by the shell whenever the page is selected: pick up settings changed elsewhere."""
        label = self._policy_labels.get(self.app.settings.get("dict_ai", "auto"))
        if label and label != self.policy.get(): self.policy.set(label)
        label = self._direction_labels[self._direction()]
        if label != self.direction.get(): self.direction.set(label)
        self.refresh_ai_state()

    def _policy_changed(self, _event=None):
        code = next((c for c, label in self._policy_labels.items() if label == self.policy.get()), "auto")
        self.app.settings["dict_ai"] = code; C.save_settings(self.app.settings); self.refresh_ai_state()

    def _direction(self) -> str:
        """The chosen direction code (validated; ``auto`` when the setting is missing or stale)."""
        code = self.app.settings.get("dict_direction", "auto")
        return code if code in D.DIRECTIONS else "auto"

    def _direction_changed(self, _event=None):
        """Combobox handler: persist the choice and re-run the current query in the new direction."""
        code = next((c for c, label in self._direction_labels.items() if label == self.direction.get()), "auto")
        self.app.settings["dict_direction"] = code; C.save_settings(self.app.settings)
        if self.query.get().strip(): self.search()
        else: self.dir_label.configure(text=""); self._fill(code, [])

    def _columns_for(self, direction: str) -> tuple:
        """Column order: headword | English | Türkçe | … - the Turkish column moves right after the headword for ``*2tr``."""
        if D.HAS_TR and D.target_field(direction) == "tr":
            return ("head", "tr", "trans", "pos", "extra", "src")
        return self.COLUMNS

    def refresh_ai_state(self):
        """Provider status label ("LM Studio: connected" / "Alternative: ready" / "AI off"), probed in the background."""
        if self.app.settings.get("dict_ai", "auto") == "off":
            self.ai_state.configure(text=self.t("dict.state_off")); return
        self.ai_state.configure(text="…")
        def work(): return self.app.dict_provider()
        def done(client):
            if not self.winfo_exists(): return
            key = "dict.state_none" if client is None else ("dict.state_alt" if client is self.app.ai_alt else "dict.state_local")
            self.ai_state.configure(text=self.t(key))
        self.app.run_async(work, done, lambda _exc: self.winfo_exists() and self.ai_state.configure(text=self.t("dict.state_none")))

    def _update_count(self):
        by = self.dict.count_by_source()
        self.count_label.configure(text=f"{len(self.dict)} {self.t('dict.entries')}  ·  {self.t('dict.builtin')} {by.get(D.SOURCE_BUILTIN, 0)}"
                                        f"  ·  {self.t('dict.user')} {by.get(D.SOURCE_USER, 0)}  ·  {self.t('dict.ai_source')} {by.get(D.SOURCE_AI, 0)}")

    def _on_key(self, event):
        q = self.query.get().strip()
        if not q: self._typed = ""; self.dir_label.configure(text=""); self._fill(self._direction(), []); return
        if q == self._typed or event.keysym in ("Return", "Up", "Down"): return     # Shift/Ctrl/arrows/Escape…: the text did not change
        if len(q) >= 2: self.search(quiet=True)

    def search(self, quiet: bool = False, direction: str | None = None):
        """Look the query up locally (in ``direction``, default the selector's) and, unless quiet, ask the AI when nothing was found
        or when a ``*2tr`` hit still lacks its Turkish gloss."""
        q = self.query.get().strip()
        if not q: return
        if not quiet or q != self._typed: self._cancel_ai()  # a new query (or an explicit search) supersedes a pending AI answer
        self._typed = q
        direction = direction or self._direction()
        rows = self._list(q, direction)
        if quiet: return
        self._remember(q)
        if rows:
            self._select_first()
            self.app.status.set(f"'{q}': {len(rows)} {self.t('dict.results')}")
            if self._turkish_missing(rows, direction) and self.app.settings.get("dict_ai", "auto") != "off":
                self._run_ai(q, merge=True); self.app.status.set(self.t("dict.tr_missing"))
        else:
            self.app.status.set(self.t("dict.no_result")); self._write_ai(self.t("dict.no_result"))
            if self.app.settings.get("dict_ai", "auto") != "off": self._run_ai(q, merge=False)

    def _turkish_missing(self, rows: list, direction: str | None = None) -> bool:
        """True when a fixed ``*2tr`` search found an entry whose Turkish gloss is still unknown (the AI can fill it)."""
        direction = direction or self._direction()
        return D.HAS_TR and direction != "auto" and D.target_field(direction) == "tr" and bool(rows) and not rows[0].tr

    def _list(self, q: str, direction: str | None = None) -> list:
        """Local lookup shown in the tree together with the effective direction label; returns the rows."""
        direction, rows = self.dict.lookup(q, direction or self._direction())
        self._fill(direction, rows)
        self.dir_label.configure(text=D.direction_text(direction))
        return rows

    def _fill(self, direction, rows):
        for item in self.tree.get_children(): self.tree.delete(item)
        self.tree.configure(displaycolumns=self._columns_for(direction))
        if D.HAS_TR: self.w_tr.pack_configure(**({"before": self.w_trans} if D.target_field(direction) == "tr" else {"after": self.w_trans}))
        self.results = rows; lang = self.app.ui_lang
        names = {D.SOURCE_BUILTIN: self.t("dict.builtin"), D.SOURCE_USER: self.t("dict.user"), D.SOURCE_AI: self.t("dict.ai_source")}
        for i, e in enumerate(rows):
            extra = e.plural if e.pos == "n" and C.TARGET_LANG == "de" else e.extra
            values = {"head": e.display, "trans": e.translation, "tr": e.tr or "—", "pos": e.pos_label(lang), "extra": extra, "src": names.get(e.source, e.source)}
            self.tree.insert("", "end", iid=str(i), values=tuple(values[c] for c in self.COLUMNS))

    def _select_first(self):
        children = self.tree.get_children()
        if children: self.tree.selection_set(children[0]); self.tree.focus(children[0]); self.selected()

    def _remember(self, q):
        if q in self.history: self.history.remove(q)
        self.history.insert(0, q); del self.history[self.MAX_HISTORY:]
        self.hist.delete(0, "end")
        for h in self.history: self.hist.insert("end", h)

    def _pick_history(self, _event=None):
        sel = self.hist.curselection()
        if sel: self.query.set(self.hist.get(sel[0])); self.search()

    def current(self):
        sel = self.tree.selection()
        if not sel: return None
        try: return self.results[int(sel[0])]
        except (ValueError, IndexError): return None

    def selected(self, _event=None):
        e = self.current()
        if not e: return
        lang = self.app.ui_lang
        self.w_head.configure(text=e.display)
        meta = e.pos_label(lang)
        if e.pos == "n" and e.gender:
            art = {"de": e.extra.split()[0] if e.extra.split() else "", "fr": {"m": "le", "f": "la", "pl": "les", "mf": "le/la"}.get(e.gender, "")}.get(C.TARGET_LANG, "")
            meta += f" · {self.t('words.gender')}: {e.gender}" + (f" ({art})" if art else "")
        if e.plural: meta += f" · {self.t('words.plural')}: {e.plural}"
        elif e.extra and e.pos != "n": meta += f" · {e.extra}"
        if e.source == D.SOURCE_AI: meta += f" · {self.t('dict.ai_source')}"
        self.w_meta.configure(text=meta)
        self.w_trans.configure(text=f"{self.t('dict.translation')}: {e.translation}")
        if D.HAS_TR: self.w_tr.configure(text=f"{self.t('dict.turkish')}: {e.tr or '—'}")
        self.w_example.configure(text=f"« {e.example} »" if e.example else "")
        self.w_note.configure(text=e.note)
        hits = [w for w in self.repos.words.search(e.headword, limit=5) if C.normalize_search(w["target"]) == C.normalize_search(e.headword)]
        self.w_bank.configure(text=f"★ {self.t('tab.words')}: {hits[0]['tr']} ({hits[0]['deck']})" if hits else "")
        if e.source == D.SOURCE_AI and self.dict.would_change(e): self.save_btn.pack(side="left", padx=4)
        else: self.save_btn.pack_forget()

    # ------------------------------------------------------------------
    def speak(self):
        e = self.current()
        if e: self.app.speak(e.headword)

    def random_word(self):
        """A random built-in headword. It is always searched on the headword side: under a fixed EN → FR / TR → FR direction the
        pair is flipped for this one search (the selector keeps the user's choice), so the pick is found locally instead of
        reported missing and sent to the AI."""
        e = self.dict.random_entry()
        if not e: return
        chosen = self._direction()
        direction = chosen if D.source_field(chosen) == "headword" else D.direction_code(*reversed(D.split_direction(chosen)))
        self.query.set(e.headword); self.search(direction=direction)

    def copy_entry(self):
        e = self.current()
        if not e: return
        self.clipboard_clear(); self.clipboard_append(f"{e.display} — {e.translation}" + (f" — {e.tr}" if e.tr else "")); self.app.status.set(self.t("dict.copied"))

    def add_to_bank(self):
        """The word bank's ``tr`` field gets the first Turkish sense when the entry has one, else the first translation sense (old behaviour)."""
        e = self.current()
        if not e: return
        first = e.translation.split(";")[0].strip()
        turkish = e.tr.split(";")[0].strip() if e.tr else ""
        fields = {"pos": e.pos, "deck": self.t("tab.dictionary"), "example_target": e.example, "example_en": e.note if C.TARGET_LANG == "en" else ""}
        if C.TARGET_LANG == "de" and e.pos == "n":
            art = e.extra.split()[0] if e.extra.split() else ""
            fields.update(article=art, gender={"der": "masculine", "die": "feminine", "das": "neuter"}.get(art, ""), plural=e.plural)
        elif C.TARGET_LANG == "fr" and e.pos == "n":
            fields.update(gender={"m": "masculin", "f": "féminin", "mf": "masculin/féminin", "pl": "pluriel"}.get(e.gender, ""), plural=e.plural,
                          article={"m": "le", "f": "la", "pl": "les"}.get(e.gender, ""))
        if C.TARGET_LANG == "en": self.repos.words.add(e.headword, first, e.headword, **fields)
        else: self.repos.words.add(e.headword, turkish or first, e.translation, **fields)
        self.app.status.set(f"{self.t('dict.added_bank')}: {e.headword}"); self.selected()

    # ------------------------------------------------------------------ AI
    def ask_ai(self):
        """Explicit lookup: AI entries are merged on top of whatever the local dictionary found."""
        e = self.current(); text = self.query.get().strip() or (e.headword if e else "")
        if not text: return
        if self.app.settings.get("dict_ai", "auto") == "off":
            self._write_ai(self.t("ai.status_off")); return
        self._run_ai(text, merge=True)

    def _model_for(self, client) -> str:
        return self.app.settings.get("alt_model" if client is self.app.ai_alt else "ai_model", "") or ""

    def _cancel_ai(self):
        """Forget a pending AI request: its answer would be stale, and so is the progress text it left on screen."""
        self._ai_seq += 1
        if self._ai_busy: self._ai_busy = False; self._write_ai(""); self.app.status.set(self.t("g.ready"))

    def _run_ai(self, q: str, merge: bool):
        self._cancel_ai(); seq = self._ai_seq; self._ai_busy = True
        self._write_ai(self.t("dict.ai_asking")); self.app.status.set(self.t("dict.ai_asking"))
        def work():
            client = self.app.dict_provider()
            if client is None: return client, None
            return client, D.ai_lookup(client, q, self.app.ui_lang, self._model_for(client))
        def done(result):
            if seq != self._ai_seq or not self.winfo_exists(): return
            self._ai_busy = False; client, entries = result
            if client is None: self._write_ai(self.t("ai.status_off")); self.app.status.set(self.t("ai.status_off")); return
            self._show_ai_entries(q, entries, client, merge)
        def error(exc):
            if seq != self._ai_seq or not self.winfo_exists(): return
            self._ai_busy = False
            self._write_ai(f"{self.t('ai.status_off')}\n\n({exc})" if isinstance(exc, AIError) else self.t("ai.status_off"))
            self.app.status.set(self.t("ai.status_off")); self.refresh_ai_state()
        self.app.run_async(work, done, error)

    def _ai_direction(self, q: str, entries: list) -> str:
        """Direction label for an AI answer: the chosen fixed direction, else which side of the answer the query matched."""
        chosen = self._direction()
        if chosen != "auto": return chosen
        qn = C.normalize_search(q)
        if qn in {C.normalize_search(e.headword) for e in entries}: return D.DEFAULT_DIRECTION
        if any(qn in D._senses(e.translation) for e in entries): return D.direction_code(D.OTHER_LANG, C.TARGET_LANG)   # "to procrastinate" -> remettre: the query was the other language
        if D.HAS_TR and any(qn in D._senses(e.tr) for e in entries): return D.direction_code("tr", C.TARGET_LANG)
        return self.dict.lookup(q)[0]

    def _show_ai_entries(self, q: str, entries: list, client, merge: bool):
        provider = f"{self.app.provider_name(client)} · {getattr(client, 'last_model', '') or self._model_for(client)}"
        if not entries:
            self._write_ai(f"{self.t('dict.ai_none')}\n\n— {self.t('dict.answered_by')}: {provider}"); self.app.status.set(self.t("dict.ai_none")); return
        filled, shown = [], {}
        if self.app.settings.get("dict_ai_autosave", True):
            filled, shown = self._fill_turkish(entries)           # glosses complete existing entries first…
            fresh = [e for e in entries if e not in shown]         # …only the rest are genuinely new entries
            if fresh: self._persist(fresh)
        direction = self._ai_direction(q, entries)
        if shown:       # existing entries carry (part of) the answer: list those in the answer's order - never an AI copy - then the local hits
            top: list = []
            for e in entries:
                for x in shown.get(e, [e]):
                    if x not in top: top.append(x)
            rows = top + [x for x in self.dict.lookup(q, self._direction())[1] if x not in top]
        else:
            rows = entries + ([e for e in self.results if e.source != D.SOURCE_AI] if merge else [])
        self._fill(direction, rows)
        self.dir_label.configure(text=D.direction_text(direction))
        self._select_first()
        lang = self.app.ui_lang; lines = []
        for e in entries:
            head = e.display + (f"  ({e.extra})" if e.extra and not (e.pos == "n" and C.TARGET_LANG == "de") else (f"  ({e.plural})" if e.plural else ""))
            lines.append(f"• {head}  [{e.pos_label(lang)}]\n    {self.t('dict.translation')}: {e.translation}")
            if D.HAS_TR: lines.append(f"    {self.t('dict.turkish')}: {e.tr or '—'}")
            if e.example: lines.append(f"    « {e.example} »")
            if e.note: lines.append(f"    ({e.note})")
        lines.append(f"\n— {self.t('dict.answered_by')}: {provider}")
        self._write_ai("\n".join(lines))
        self.app.status.set(f"{self.t('dict.tr_filled')}: {', '.join(e.headword for e in filled)}" if filled else f"'{q}': {len(entries)} {self.t('dict.ai_results')}")

    def _gloss_targets(self, a, entries: list) -> list:
        """Stored entries (without a Turkish gloss, same headword) that AI entry ``a`` completes when it has no twin: those
        sharing an English sense with it (``attic`` / ``attic; loft``; a polysemous word gets each sense's own gloss), else -
        when the answer holds a single entry for this headword and a single such stored entry of a compatible part of
        speech exists - that entry."""
        bare = [e for e in self.dict.find(a.headword) if not e.tr]
        senses = D.sense_keys(a.translation)
        hits = [e for e in bare if senses & D.sense_keys(e.translation)]
        if hits: return hits
        siblings = [x for x in entries if D._norm(x.headword) == D._norm(a.headword)]
        if len(siblings) == 1 and len(bare) == 1 and D.pos_compatible(bare[0].pos, a.pos): return bare
        return []

    def _fill_turkish(self, entries: list) -> tuple[list, dict]:
        """Existing entries that lack a Turkish gloss get it from a matching AI answer - in memory and in SQLite - so the
        dictionary never grows a duplicate just to carry the Turkish side.

        Returns ``(filled, shown)``: the stored entries that gained their gloss, and for every AI entry that an existing entry
        already represents (its twin, or the entries its gloss went into) those stored entries - such an AI entry must not
        be stored as a new row, and the list shows the stored entries in its place."""
        filled, shown = [], {}
        for a in entries:
            twin = self.dict.twin(a)
            if twin is not None: targets = [twin] if a.tr and not twin.tr else []
            elif a.tr: targets = self._gloss_targets(a, entries)
            else: targets = []
            for e in targets:
                self._persist([replace(e, source=D.SOURCE_AI, tr=a.tr)])
                filled.append(self.dict.twin(e))
            if twin is not None or targets: shown[a] = [self.dict.twin(e) for e in targets] or [twin]
        return filled, shown

    def _persist(self, entries: list) -> int:
        """Store AI entries in SQLite and in the in-memory dictionary; returns how many rows were new to SQLite.

        An entry whose twin is already stored is never inserted again: it either adds nothing, or - when only the Turkish
        gloss is new - updates that row in place (for a built-in twin it leaves an ``ai`` row with the twin's identity and the
        gloss, which is merged into the built-in entry on the next start)."""
        rows = []
        for e in entries:
            twin = self.dict.twin(e)
            if twin is not None:
                if not (e.tr and not twin.tr): continue
                if self.repos.dictionary.set_tr(twin.headword, twin.translation, e.tr): continue
                rows.append((twin.headword, twin.translation, twin.pos, twin.extra, twin.note, twin.example, e.tr))
            else:
                rows.append((e.headword, e.translation, e.pos, e.extra, e.note, e.example, e.tr))
        n = self.repos.dictionary.add_many(rows, D.SOURCE_AI) if rows else 0
        self.dict.extend(entries); self._update_count(); return n

    def save_ai_entry(self):
        """Autosave off: store the selected AI entry - its gloss completes an existing entry when one matches (no duplicate),
        otherwise it becomes a new row."""
        e = self.current()
        if not e or e.source != D.SOURCE_AI: return
        _filled, shown = self._fill_turkish([e])
        if e not in shown: self._persist([e])
        self.app.status.set(f"{self.t('dict.ai_saved')}: {e.headword}")
        if shown and self.query.get().strip(): self._list(self.query.get().strip()); self._select_first()   # show the completed entry, not the AI copy
        else: self.selected()

    def _write_ai(self, text):
        self.ai_out.configure(state="normal"); self.ai_out.delete("1.0", "end"); self.ai_out.insert("1.0", text); self.ai_out.configure(state="disabled")

    # ------------------------------------------------------------------
    def add_entry(self):
        dlg = tk.Toplevel(self); dlg.title(self.t("dict.add_entry")); dlg.configure(background=self.palette["bg"]); dlg.transient(self.app); dlg.grab_set()
        fields = {}
        q = self.query.get().strip(); src = D.source_field(self.dict.lookup(q, self._direction())[0]) if q else ""
        specs = [("headword", self.t("dict.headword"), q if src == "headword" else ""),
                 ("translation", self.t("dict.translation"), q if src == "translation" else "")]
        if D.HAS_TR: specs.append(("tr", self.t("dict.turkish"), q if src == "tr" else ""))
        specs += [("pos", self.t("words.pos") + " (n/v/adj/…)", ""), ("extra", self.t("dict.extra"), ""), ("note", self.t("dict.note"), ""),
                  ("example", self.t("dict.example"), "")]
        for i, (key, label, value) in enumerate(specs):
            ttk.Label(dlg, text=label).grid(row=i, column=0, sticky="w", padx=12, pady=5)
            var = tk.StringVar(value=value); ttk.Entry(dlg, textvariable=var, width=40).grid(row=i, column=1, padx=12, pady=5); fields[key] = var
        def save():
            head, trans = fields["headword"].get().strip(), fields["translation"].get().strip()
            if not head or not trans: messagebox.showwarning(C.APP_NAME, self.t("dict.required"), parent=dlg); return
            pos, extra, note, example = (fields[k].get().strip() for k in ("pos", "extra", "note", "example"))
            tr = fields["tr"].get().strip() if "tr" in fields else ""
            self.repos.dictionary.add(head, trans, pos, extra, note, D.SOURCE_USER, example, tr)
            self.dict.extend([D.Entry(head, pos, extra, trans, note, D.SOURCE_USER, example, tr)])
            dlg.destroy(); self._update_count(); self.query.set(head); self.search()
        ttk.Button(dlg, text=self.t("g.save"), style="Accent.TButton", command=save).grid(row=len(specs), column=1, sticky="e", padx=12, pady=12)
        dlg.bind("<Return>", lambda _e: save()); dlg.bind("<Escape>", lambda _e: dlg.destroy())

    def import_file(self):
        path = filedialog.askopenfilename(title=self.t("dict.import"), filetypes=[("CSV / TSV", "*.csv *.tsv *.txt"), ("*", "*.*")])
        if not path: return
        try: entries = D.read_table(Path(path))
        except Exception as exc: messagebox.showerror(C.APP_NAME, str(exc), parent=self); return
        n = self.repos.dictionary.add_many([(e.headword, e.translation, e.pos, e.extra, e.note, e.example, e.tr) for e in entries], D.SOURCE_USER)
        self.dict.extend(entries); self._update_count(); self.app.status.set(f"{n} {self.t('dict.imported')}")

    def export_file(self):
        path = filedialog.asksaveasfilename(title=self.t("dict.export"), defaultextension=".csv", initialdir=str(C.EXPORT_DIR),
                                            initialfile=f"dictionary_{C.TARGET_LANG}.csv", filetypes=[(self.t("words.csv"), "*.csv")])
        if not path: return
        n = D.write_table(Path(path), self.results or self.dict.entries); self.app.status.set(f"{n} {self.t('dict.exported')}")
