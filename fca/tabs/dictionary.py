from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .. import config as C
from .. import dictionary as D
from ..ai_client import AIError
from ..ui import BaseTab


class DictionaryTab(BaseTab):
    """Bidirectional dictionary: built-in core entries + the user's own entries + cached AI entries."""
    key, subtitle_key = "tab.dictionary", "dict.subtitle"
    MAX_HISTORY = 12
    POLICY_KEYS = {"auto": "dict.ai_auto", "local": "dict.ai_local", "alt": "dict.ai_alt", "off": "dict.ai_off"}

    def build(self):
        self.heading()
        self.dict = D.build_dictionary([(r["headword"], r["translation"], r["pos"], r["extra"], r["note"], r.get("source", D.SOURCE_USER), r.get("example", ""))
                                        for r in self.repos.dictionary.all()])
        self.results = []; self.history = []; self._typed = ""; self._ai_seq = 0; self._ai_busy = False
        bar = ttk.Frame(self); bar.pack(fill="x", pady=(0, 9))
        self.query = tk.StringVar()
        self.entry = ttk.Entry(bar, textvariable=self.query, font=("Segoe UI", 12)); self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _e: self.search()); self.entry.bind("<KeyRelease>", self._on_key)
        ttk.Button(bar, text=self.t("g.search"), style="Accent.TButton", command=self.search).pack(side="left", padx=5)
        self.dir_label = ttk.Label(bar, text="", style="Muted.TLabel", width=9); self.dir_label.pack(side="left", padx=(2, 8))
        ttk.Button(bar, text="🎲 " + self.t("dict.random"), command=self.random_word).pack(side="left")
        ttk.Label(bar, text=self.t("dict.ai_policy"), style="Muted.TLabel").pack(side="left", padx=(12, 3))
        self._policy_labels = {code: self.t(k) for code, k in self.POLICY_KEYS.items()}
        self.policy = tk.StringVar(value=self._policy_labels.get(self.app.settings.get("dict_ai", "auto"), self._policy_labels["auto"]))
        self.policy_box = ttk.Combobox(bar, textvariable=self.policy, state="readonly", width=11, values=[self._policy_labels[c] for c in C.DICT_AI_POLICIES])
        self.policy_box.pack(side="left"); self.policy_box.bind("<<ComboboxSelected>>", self._policy_changed)
        self.ai_state = ttk.Label(bar, text="", style="Muted.TLabel"); self.ai_state.pack(side="left", padx=(6, 0))
        ttk.Button(bar, text="+ " + self.t("dict.add_entry"), command=self.add_entry).pack(side="right", padx=3)
        ttk.Button(bar, text=f"↓ {self.t('dict.import')}", command=self.import_file).pack(side="right", padx=3)
        ttk.Button(bar, text=f"↑ {self.t('dict.export')}", command=self.export_file).pack(side="right", padx=3)

        pane = ttk.PanedWindow(self, orient="horizontal"); pane.pack(fill="both", expand=True)
        left = ttk.Frame(pane)
        cols = ("head", "trans", "pos", "extra", "src")
        self.tree = ttk.Treeview(left, columns=cols, show="headings", selectmode="browse")
        for col, title, width, stretch in ((("head", self.t("dict.headword"), 190, False), ("trans", self.t("dict.translation"), 260, True),
                                            ("pos", self.t("words.pos"), 70, False), ("extra", self.t("dict.extra"), 110, False),
                                            ("src", self.t("dict.source"), 70, False))):
            self.tree.heading(col, text=title); self.tree.column(col, width=width, minwidth=40, anchor="w", stretch=stretch)
        vs = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview); self.tree.configure(yscrollcommand=vs.set)
        self.tree.pack(side="left", fill="both", expand=True); vs.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.selected); self.tree.bind("<Double-1>", lambda _e: self.speak())
        pane.add(left, weight=3)

        right = self.card(pane); pane.add(right, weight=2)
        self.w_head = ttk.Label(right, text="—", style="Card.TLabel", font=("Segoe UI", 24, "bold"), wraplength=360, justify="left"); self.w_head.pack(anchor="w")
        self.w_meta = ttk.Label(right, text="", style="CardMuted.TLabel", wraplength=360, justify="left"); self.w_meta.pack(anchor="w", pady=(4, 0))
        self.w_trans = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 12, "bold"), wraplength=360, justify="left"); self.w_trans.pack(anchor="w", pady=(10, 0))
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
        self.refresh_ai_state()

    def _policy_changed(self, _event=None):
        code = next((c for c, label in self._policy_labels.items() if label == self.policy.get()), "auto")
        self.app.settings["dict_ai"] = code; C.save_settings(self.app.settings); self.refresh_ai_state()

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
        if not q: self._typed = ""; self.dir_label.configure(text=""); self._fill("target", []); return
        if q == self._typed or event.keysym in ("Return", "Up", "Down"): return     # Shift/Ctrl/arrows/Escape…: the text did not change
        if len(q) >= 2: self.search(quiet=True)

    def search(self, quiet: bool = False):
        q = self.query.get().strip()
        if not q: return
        if not quiet or q != self._typed: self._cancel_ai()  # a new query (or an explicit search) supersedes a pending AI answer
        self._typed = q
        direction, rows = self.dict.lookup(q)
        self._fill(direction, rows)
        self.dir_label.configure(text=f"{C.TARGET_LANG.upper()} → {self._other()}" if direction == "target" else f"{self._other()} → {C.TARGET_LANG.upper()}")
        if quiet: return
        self._remember(q)
        if rows:
            first = self.tree.get_children()[0]; self.tree.selection_set(first); self.tree.focus(first); self.selected()
            self.app.status.set(f"'{q}': {len(rows)} {self.t('dict.results')}")
        else:
            self.app.status.set(self.t("dict.no_result")); self._write_ai(self.t("dict.no_result"))
            if self.app.settings.get("dict_ai", "auto") != "off": self._run_ai(q, merge=False)

    def _other(self) -> str: return "TR" if C.TARGET_LANG == "en" else "EN"

    def _fill(self, direction, rows):
        for item in self.tree.get_children(): self.tree.delete(item)
        self.results = rows; lang = self.app.ui_lang
        names = {D.SOURCE_BUILTIN: self.t("dict.builtin"), D.SOURCE_USER: self.t("dict.user"), D.SOURCE_AI: self.t("dict.ai_source")}
        for i, e in enumerate(rows):
            extra = e.plural if e.pos == "n" and C.TARGET_LANG == "de" else e.extra
            self.tree.insert("", "end", iid=str(i), values=(e.display, e.translation, e.pos_label(lang), extra, names.get(e.source, e.source)))

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
        self.w_trans.configure(text=e.translation.replace("; ", "\n"))
        self.w_example.configure(text=f"« {e.example} »" if e.example else "")
        self.w_note.configure(text=e.note)
        hits = [w for w in self.repos.words.search(e.headword, limit=5) if C.normalize_search(w["target"]) == C.normalize_search(e.headword)]
        self.w_bank.configure(text=f"★ {self.t('tab.words')}: {hits[0]['tr']} ({hits[0]['deck']})" if hits else "")
        if e.source == D.SOURCE_AI and not self.dict.contains(e): self.save_btn.pack(side="left", padx=4)
        else: self.save_btn.pack_forget()

    # ------------------------------------------------------------------
    def speak(self):
        e = self.current()
        if e: self.app.speak(e.headword)

    def random_word(self):
        e = self.dict.random_entry()
        if e: self.query.set(e.headword); self.search()

    def copy_entry(self):
        e = self.current()
        if not e: return
        self.clipboard_clear(); self.clipboard_append(f"{e.display} — {e.translation}"); self.app.status.set(self.t("dict.copied"))

    def add_to_bank(self):
        e = self.current()
        if not e: return
        first = e.translation.split(";")[0].strip()
        fields = {"pos": e.pos, "deck": self.t("tab.dictionary"), "example_target": e.example, "example_en": e.note if C.TARGET_LANG == "en" else ""}
        if C.TARGET_LANG == "de" and e.pos == "n":
            art = e.extra.split()[0] if e.extra.split() else ""
            fields.update(article=art, gender={"der": "masculine", "die": "feminine", "das": "neuter"}.get(art, ""), plural=e.plural)
        elif C.TARGET_LANG == "fr" and e.pos == "n":
            fields.update(gender={"m": "masculin", "f": "féminin", "mf": "masculin/féminin", "pl": "pluriel"}.get(e.gender, ""), plural=e.plural,
                          article={"m": "le", "f": "la", "pl": "les"}.get(e.gender, ""))
        if C.TARGET_LANG == "en": self.repos.words.add(e.headword, first, e.headword, **fields)
        else: self.repos.words.add(e.headword, first, e.translation, **fields)
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

    def _show_ai_entries(self, q: str, entries: list, client, merge: bool):
        provider = f"{self.app.provider_name(client)} · {getattr(client, 'last_model', '') or self._model_for(client)}"
        if not entries:
            self._write_ai(f"{self.t('dict.ai_none')}\n\n— {self.t('dict.answered_by')}: {provider}"); self.app.status.set(self.t("dict.ai_none")); return
        if self.app.settings.get("dict_ai_autosave", True): self._persist(entries)
        rows = entries + ([e for e in self.results if e.source != D.SOURCE_AI] if merge else [])
        direction = "target" if C.normalize_search(q) in {C.normalize_search(e.headword) for e in entries} else self.dict.lookup(q)[0]
        self._fill(direction, rows)
        first = self.tree.get_children()[0]; self.tree.selection_set(first); self.tree.focus(first); self.selected()
        lang = self.app.ui_lang; lines = []
        for e in entries:
            head = e.display + (f"  ({e.extra})" if e.extra and not (e.pos == "n" and C.TARGET_LANG == "de") else (f"  ({e.plural})" if e.plural else ""))
            lines.append(f"• {head}  [{e.pos_label(lang)}]\n    → {e.translation}")
            if e.example: lines.append(f"    « {e.example} »")
            if e.note: lines.append(f"    ({e.note})")
        lines.append(f"\n— {self.t('dict.answered_by')}: {provider}")
        self._write_ai("\n".join(lines))
        self.app.status.set(f"'{q}': {len(entries)} {self.t('dict.ai_results')}")

    def _persist(self, entries: list) -> int:
        n = self.repos.dictionary.add_many([(e.headword, e.translation, e.pos, e.extra, e.note, e.example) for e in entries], D.SOURCE_AI)
        self.dict.extend(entries); self._update_count(); return n

    def save_ai_entry(self):
        e = self.current()
        if not e or e.source != D.SOURCE_AI: return
        self._persist([e]); self.app.status.set(f"{self.t('dict.ai_saved')}: {e.headword}"); self.selected()

    def _write_ai(self, text):
        self.ai_out.configure(state="normal"); self.ai_out.delete("1.0", "end"); self.ai_out.insert("1.0", text); self.ai_out.configure(state="disabled")

    # ------------------------------------------------------------------
    def add_entry(self):
        dlg = tk.Toplevel(self); dlg.title(self.t("dict.add_entry")); dlg.configure(background=self.palette["bg"]); dlg.transient(self.app); dlg.grab_set()
        fields = {}
        q = self.query.get().strip(); direction, _ = self.dict.lookup(q) if q else ("target", [])
        specs = [("headword", self.t("dict.headword"), q if direction == "target" else ""),
                 ("translation", self.t("dict.translation"), q if direction != "target" else ""),
                 ("pos", self.t("words.pos") + " (n/v/adj/…)", ""), ("extra", self.t("dict.extra"), ""), ("note", self.t("dict.note"), ""),
                 ("example", self.t("dict.example"), "")]
        for i, (key, label, value) in enumerate(specs):
            ttk.Label(dlg, text=label).grid(row=i, column=0, sticky="w", padx=12, pady=5)
            var = tk.StringVar(value=value); ttk.Entry(dlg, textvariable=var, width=40).grid(row=i, column=1, padx=12, pady=5); fields[key] = var
        def save():
            head, trans = fields["headword"].get().strip(), fields["translation"].get().strip()
            if not head or not trans: messagebox.showwarning(C.APP_NAME, self.t("dict.required"), parent=dlg); return
            pos, extra, note, example = (fields[k].get().strip() for k in ("pos", "extra", "note", "example"))
            self.repos.dictionary.add(head, trans, pos, extra, note, D.SOURCE_USER, example)
            self.dict.extend([D.Entry(head, pos, extra, trans, note, D.SOURCE_USER, example)])
            dlg.destroy(); self._update_count(); self.query.set(head); self.search()
        ttk.Button(dlg, text=self.t("g.save"), style="Accent.TButton", command=save).grid(row=len(specs), column=1, sticky="e", padx=12, pady=12)
        dlg.bind("<Return>", lambda _e: save()); dlg.bind("<Escape>", lambda _e: dlg.destroy())

    def import_file(self):
        path = filedialog.askopenfilename(title=self.t("dict.import"), filetypes=[("CSV / TSV", "*.csv *.tsv *.txt"), ("*", "*.*")])
        if not path: return
        try: entries = D.read_table(Path(path))
        except Exception as exc: messagebox.showerror(C.APP_NAME, str(exc), parent=self); return
        n = self.repos.dictionary.add_many([(e.headword, e.translation, e.pos, e.extra, e.note, e.example) for e in entries], D.SOURCE_USER)
        self.dict.extend(entries); self._update_count(); self.app.status.set(f"{n} {self.t('dict.imported')}")

    def export_file(self):
        path = filedialog.asksaveasfilename(title=self.t("dict.export"), defaultextension=".csv", initialdir=str(C.EXPORT_DIR),
                                            initialfile=f"dictionary_{C.TARGET_LANG}.csv", filetypes=[(self.t("words.csv"), "*.csv")])
        if not path: return
        n = D.write_table(Path(path), self.results or self.dict.entries); self.app.status.set(f"{n} {self.t('dict.exported')}")
