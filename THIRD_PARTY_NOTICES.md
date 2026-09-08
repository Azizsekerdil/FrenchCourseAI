# Third-Party Notices

French Course AI itself is distributed under the MIT License (see [LICENSE](LICENSE)).
This file lists the third-party components that the source tree uses and that the
published binaries embed, together with the licence each component is actually
released under.

Every licence below was read from the installed package metadata
(`License` / `License-Expression`) or from the licence file the component itself
ships, not from memory. The versions are the ones present in the build
environment that produced the v1.2.1 packages; `numpy 2.4.6` and
`cryptography 50.0.0` are additionally confirmed by the `.dist-info` directories
embedded in `FrenchCourseAI.exe`.

Scope of "distributed binaries":

* `FrenchCourseAI.exe` / `FrenchCourseAI-Windows.zip` — one-file PyInstaller build,
  Windows x64, produced by `build.bat` from `FrenchCourseAI.spec`. The zip holds
  `FrenchCourseAI.exe`, `LICENSE` and this file.
* `FrenchCourseAI-macOS.zip` — `FrenchCourseAI.app`, built by
  `build_macos.sh` / `.github/workflows/build-macos.yml`. The zip holds
  `FrenchCourseAI.app`, `LICENSE` and this file.

`LICENSE` and `THIRD_PARTY_NOTICES.md` are also packaged *inside* both binaries, so
the notices travel with the application even when the archive is discarded; see
"How that obligation is actually discharged" at the end of section 4.

> **Applies from this revision onward.** The two licence files were added to
> `FrenchCourseAI.spec`, `build_macos.sh` and `build.bat` *after* the v1.2.1
> archives were cut, so the v1.2.1 artefacts already on disk and any copy already
> published do **not** contain them. Re-cut both archives from this revision before
> the next release; until then the paragraph above describes what the build scripts
> produce, not what a v1.2.1 download contains.

---

## 1. Direct dependency of the source code

`pypdf` is the only non-standard-library package imported anywhere in `fca/`.

| Component | Version | Licence | Used for |
| --- | --- | --- | --- |
| [pypdf](https://github.com/py-pdf/pypdf) | 6.13.2 (pinned `>=5.0,<7`) | BSD-3-Clause | `PdfReader` in `fca/tabs/reading.py` — extracting page text for the PDF reader page. |

## 2. Build and test tooling (not part of the shipped application code)

| Component | Version | Licence | Used for |
| --- | --- | --- | --- |
| [pytest](https://github.com/pytest-dev/pytest) | 9.1.1 (pinned `>=8.0,<10`) | MIT | Running the automated test suite. |
| [PyInstaller](https://github.com/pyinstaller/pyinstaller) | 6.21.0 (pinned `>=6.0,<7`) | GPL-2.0-or-later **with the bootloader exception** | Freezing the app into `FrenchCourseAI.exe` and `FrenchCourseAI.app`. |
| [pyinstaller-hooks-contrib](https://github.com/pyinstaller/pyinstaller-hooks-contrib) | 2026.6 | Dual: **Apache-2.0** for `_pyinstaller_hooks_contrib/rthooks`, **GPL-2.0-or-later** for every other hook/file | Required PyInstaller dependency (community hooks). Only one Apache-2.0 run-time hook is distributed — see below. |
| [altgraph](https://github.com/ronaldoussoren/altgraph) | 0.17.5 | MIT | PyInstaller dependency (import graph). |
| [packaging](https://github.com/pypa/packaging) | 26.2 | Apache-2.0 OR BSD-2-Clause | Required by both PyInstaller and pytest (version/requirement parsing). |
| [pefile](https://github.com/erocarrera/pefile) | 2024.8.26 | MIT | PyInstaller dependency (Windows PE analysis; `sys_platform == "win32"` only). |
| [pywin32-ctypes](https://github.com/enthought/pywin32-ctypes) | 0.2.3 | BSD-3-Clause | PyInstaller dependency (Windows API access at build time; Windows only). |
| [macholib](https://github.com/ronaldoussoren/macholib) | 1.16.4 | MIT | PyInstaller dependency for `sys_platform == "darwin"` — installed by `build_macos.sh` and by the macOS CI job, never on Windows. |
| [setuptools](https://github.com/pypa/setuptools) | 65.5.0 | MIT | PyInstaller dependency (packaging helpers). |

Transitive dependencies of these tools are listed one level deep, as above. pytest
additionally requires `pluggy` (MIT), `iniconfig` (MIT), `pygments` (BSD-2-Clause),
`colorama` (BSD-3-Clause, Windows only) and `packaging`; none of them, and none of
PyInstaller's own dependencies, reaches either published binary.

**PyInstaller obligation.** PyInstaller is GPL-2.0-or-later, but its authors grant
"unlimited permission to link or embed compiled bootloader and related files into
combinations with other programs, and to distribute those combinations without any
restriction coming from the use of those files" (COPYING.txt, *Bootloader
Exception*). Only the bootloader, PyInstaller's own Apache-2.0 run-time hooks, and
— in the Windows build — one Apache-2.0 run-time hook from PyInstaller Community
Hooks (`pyi_rth_cryptography_openssl.py`, which carries
`SPDX-License-Identifier: Apache-2.0`) end up inside the frozen application, so the
GPL does **not** reach French Course AI, which stays MIT-licensed. Neither
PyInstaller nor the GPL-2.0-or-later build-time hooks of pyinstaller-hooks-contrib
are ever redistributed by this project.

The run-time hooks that are actually embedded were read out of the built packages.
`FrenchCourseAI.exe` carries five: `pyi_rth__tkinter`, `pyi_rth_inspect`,
`pyi_rth_multiprocessing` and `pyi_rth_pkgutil` from `PyInstaller/hooks/rthooks/`,
plus `pyi_rth_cryptography_openssl` from `_pyinstaller_hooks_contrib/rthooks/`.
`FrenchCourseAI.app` carries only `pyi_rth__tkinter` and `pyi_rth_inspect`, both
PyInstaller's own — no pyinstaller-hooks-contrib code reaches the macOS package.

## 3. Embedded in the published binaries, per platform (Python runtime and its libraries)

PyInstaller copies the interpreter and its C extension libraries into the package.
Which native libraries are *redistributed* differs between the two platforms: the
Windows CPython build ships its own copies, whereas the macOS build links several
of them against the libraries already present in `/usr/lib`, so those are not
redistributed at all. The **Where** column records what was read out of the built
packages — the exe's PyInstaller manifest, and the Mach-O load commands and
version strings of the files inside `FrenchCourseAI.app`. Unless the column says
otherwise, versions are those of the Windows CPython 3.11.9 build.

### PSF-2.0

| Component | Version | Where | Note |
| --- | --- | --- | --- |
| [CPython](https://www.python.org/) | 3.11.9 | Both | The interpreter, standard library and `python311.dll` / `Python.framework`. Licensed under the Python Software Foundation License Version 2. |

### BSD-style / permissive

| Component | Version | Licence | Where | Note |
| --- | --- | --- | --- | --- |
| [Tcl/Tk](https://www.tcl-lang.org/) | 8.6 (Windows 8.6.12, macOS 8.6.13) | Tcl/Tk licence (BSD-style) | Both | The whole user interface is `tkinter`; `tcl86t.dll` / `tk86t.dll` (`libtcl8.6.dylib` / `libtk8.6.dylib`) plus `_tcl_data`, `_tk_data` and `tcl8` are embedded. `_tk_data/license.terms` is the one licence file PyInstaller already copied on its own. |
| [SQLite](https://sqlite.org/) | 3.45.1 | Public domain | Both | `sqlite3.dll` behind `sqlite3` — the local learner database. On macOS it is statically linked into `_sqlite3.cpython-311-darwin.so`, which reports the same 3.45.1. |
| [zlib](https://zlib.net/) | 1.3.1 | Zlib licence | **Windows only** | Compression for `zipfile` (`.fcapack` packs) and the PyInstaller archive. On macOS `zlib.cpython-311-darwin.so` links `/usr/lib/libz.1.dylib` (the system copy, 1.2.11) and nothing is redistributed. |
| [bzip2 / libbzip2](https://sourceware.org/bzip2/) | 1.0.8 | BSD-style (Julian Seward) | **Windows only** | `_bz2` in the standard library. On macOS `_bz2.cpython-311-darwin.so` links `/usr/lib/libbz2.1.0.dylib`. |
| [XZ Utils / liblzma](https://tukaani.org/xz/) | 5.2.3 on macOS, read from the version string in `_lzma.cpython-311-darwin.so`; the Windows `_lzma.pyd` exposes no version string, so its exact version is unconfirmed | **Public domain** for the 5.2 series measured here — liblzma was relicensed to 0BSD only from XZ Utils 5.6 onward, so "0BSD" would be the wrong label for this copy | Both, statically linked (neither `_lzma.pyd` nor `_lzma...darwin.so` imports an external liblzma) | `_lzma` in the standard library. Should a future CPython build embed 5.6 or later, this row becomes 0BSD. A *different*, newer liblzma — 5.8.3, genuinely 0BSD — is linked into Pillow's `_imaging` on Windows; see section 4. |

### MIT

| Component | Version | Licence | Where | Note |
| --- | --- | --- | --- | --- |
| [libffi](https://sourceware.org/libffi/) | as shipped in `libffi-8.dll` | MIT | **Windows only** | Backs `ctypes`, which `fca/secrets.py` uses to reach the Windows Credential Manager. `libffi-8.dll` is a separate DLL inside the exe. On macOS `_ctypes.cpython-311-darwin.so` links `/usr/lib/libffi.dylib`. |
| [Expat](https://libexpat.github.io/) | 2.6.0 | MIT | Both, statically linked | `pyexpat` / `xml.parsers.expat` in the standard library; both platforms' `pyexpat` report `expat_2.6.0`. |

### Apache-2.0

| Component | Version | Where | Note |
| --- | --- | --- | --- |
| [OpenSSL](https://www.openssl.org/) | 3.0.13 | Both | `libssl-3.dll` / `libcrypto-3.dll` (`libssl.3.dylib` / `libcrypto.3.dylib`) behind `ssl`, `hashlib` and the HTTPS calls in `fca/ai_client.py`. OpenSSL 3.x is Apache-2.0. |

### Microsoft Distributable Code (Windows binary only)

`VCRUNTIME140.dll`, `VCRUNTIME140_1.dll`, `ucrtbase.dll` and the
`api-ms-win-*.dll` forwarders are Microsoft Distributable Code embedded by the
CPython Windows build and by PyInstaller. They are redistributable under
Microsoft's own terms; see the "Additional Conditions for this Windows binary
build" section of the CPython `LICENSE.txt`.

## 4. Additionally embedded in the Windows x64 build of v1.2.1

`fca/` never imports these packages. They entered `FrenchCourseAI.exe` because
PyInstaller follows the optional imports inside `pypdf`
(`pypdf/_page.py` → `PIL`, `pypdf/_font.py` → `fontTools`,
`pypdf/_crypt_providers/_cryptography.py` → `cryptography`) and then their own
optional imports, and because those packages happened to be installed on the
machine that produced the Windows build. The macOS CI job installs only
`requirements.txt`, so `FrenchCourseAI.app` contains **none** of them — its
archive holds `pypdf` and the standard library only.

They are listed here because they are genuinely present in the published Windows
binary.

### BSD-3-Clause

| Component | Version | Why it is there |
| --- | --- | --- |
| [numpy](https://numpy.org/) | 2.4.6 | Optional import of Pillow and fontTools. Its own SPDX expression is `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0` (vendored pocketfft, libdivide, Highway, x86-simd-sort and the random-number sources). It also ships `numpy.libs/libscipy_openblas64_*.dll` — see the note below. |
| [lxml](https://lxml.de/) | 6.1.1 | Optional import of `fontTools.misc.etree`. The Windows wheel statically links libxml2 and libxslt (both MIT); no GNU libiconv is linked in. |
| [lxml-html-clean](https://github.com/fedora-python/lxml_html_clean) | 0.4.5 | Optional import of `lxml.html.clean`. |

### MIT / MIT-CMU

| Component | Version | Why it is there |
| --- | --- | --- |
| [Pillow](https://python-pillow.github.io/) | 12.2.0 | Optional import of `pypdf` (embedded-image handling). MIT-CMU (HPND-style) licence. Its Windows wheel statically links further upstream projects into the `.pyd` files that PyInstaller embedded — see the sub-list below. |
| [fontTools](https://github.com/fonttools/fonttools) | 4.63.0 | Optional import of `pypdf` (embedded-font handling). |
| [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) | 4.15.0 | Optional import of `lxml.html.soupparser`. |
| [soupsieve](https://github.com/facelessuser/soupsieve) | 2.8.4 | `beautifulsoup4` dependency. |
| [charset-normalizer](https://github.com/jawah/charset_normalizer) | 3.4.7 | `beautifulsoup4` dependency. |
| [PyYAML](https://pyyaml.org/) | 6.0.3 | Imported by `numpy/__config__.py`. |
| [cffi](https://github.com/python-cffi/cffi) | 2.0.0 | Only the `_cffi_backend` extension module is embedded, added by PyInstaller alongside `cryptography`. |

### PSF-style

| Component | Version | Why it is there |
| --- | --- | --- |
| [defusedxml](https://github.com/tiran/defusedxml) | 0.7.1 | Optional import of `PIL.Image`. PSF licence. |
| [typing-extensions](https://github.com/python/typing_extensions) | 4.15.0 | Typing helper pulled in by the above. PSF-2.0. |
| [pywin32](https://github.com/mhammond/pywin32) | 312 | `win32/win32pdh.pyd` and `pywin32_system32/pywintypes311.dll`, added by PyInstaller's pywin32 support. PyPI classifies it as the PSF licence; the shipped `win32/License.txt` is a permissive BSD-style notice by Mark Hammond. |

### Dual-licensed

| Component | Version | Licence | Why it is there |
| --- | --- | --- | --- |
| [cryptography](https://github.com/pyca/cryptography) | 50.0.0 | Apache-2.0 **OR** BSD-3-Clause (recipient's choice) | Optional import of `pypdf` for AES-encrypted PDFs. Its `.dist-info` (including `licenses/LICENSE.APACHE`, `licenses/LICENSE.BSD` and the Rust SBOMs) is embedded alongside it. |

### Pillow's statically linked native libraries

Pillow's Windows wheel ships no separate DLLs; the upstream C libraries are linked
straight into its extension modules. `pillow-12.2.0.dist-info/licenses/LICENSE`
reproduces twelve upstream licence texts, but only the extensions listed below are
actually inside `FrenchCourseAI.exe`, so only their libraries are redistributed.
The mapping was read from the extensions themselves (embedded version strings) and
the versions cross-checked against `PIL.features.version()` and the `===== name-version =====`
headers of that licence file.

| Embedded extension | Statically linked library | Version | Licence |
| --- | --- | --- | --- |
| `PIL\_imaging.cp311-win_amd64.pyd` | [libjpeg-turbo](https://libjpeg-turbo.org/) | 3.1.4.1 | IJG / BSD-3-Clause / zlib (libjpeg-turbo's three-part licence) |
| | [libtiff](http://www.simplesystems.org/libtiff/) | 4.7.1 | libtiff licence (MIT-style, Sam Leffler / Silicon Graphics) |
| | [OpenJPEG](https://www.openjpeg.org/) | 2.5.4 | BSD-2-Clause |
| | [zlib-ng](https://github.com/zlib-ng/zlib-ng) | 2.3.3 | Zlib licence |
| | [XZ Utils / liblzma](https://tukaani.org/xz/) | 5.8.3, per the `===== xz-5.8.3 =====` header of Pillow's licence file (libtiff's LZMA codec) | 0BSD — this copy *is* post-5.6, unlike CPython's; see section 3 |
| `PIL\_webp.cp311-win_amd64.pyd`, and libtiff's WebP codec inside `_imaging` | [libwebp](https://developers.google.com/speed/webp) | 1.6.0 | BSD-3-Clause (Google) |
| `PIL\_avif.cp311-win_amd64.pyd` | [libavif](https://github.com/AOMediaCodec/libavif) | 1.4.1 | BSD-2-Clause (Joe Drago) |
| | [dav1d](https://code.videolan.org/videolan/dav1d) (AV1 decoder) | bundled with libavif 1.4.1 | BSD-2-Clause (VideoLAN and dav1d authors) |
| | [libaom](https://aomedia.googlesource.com/aom/) (AV1 encoder; the binary identifies itself as "AOMedia Project AV1 Encoder 3.13.2") | 3.13.2 | BSD-2-Clause **plus the Alliance for Open Media Patent License 1.0** |
| `PIL\_imagingcms.cp311-win_amd64.pyd` | [Little CMS 2](https://littlecms.com/) | 2.18 | MIT (Marti Maria Saguer) |

libavif's own notice, reproduced inside Pillow's licence file, additionally covers
the third-party code libavif carries: dav1d's `src/obu.c`, the IJG-derived
`third_party/iccjpeg`, and `third_party/libyuv` (BSD-3-Clause, Google).

**libaom is the one gap in the upstream text.** Pillow's licence file has no
`===== aom-… =====` section, so the BSD-2-Clause notice and the Alliance for Open
Media Patent License 1.0 that libaom carries are not reproduced anywhere in the
package by anyone but this document. Neither is a copyleft licence and neither
affects French Course AI's own MIT terms, but the attribution and the patent grant
are named here so that nothing embedded in `_avif` goes unrecorded.

**Not embedded.** Pillow's licence file also carries FreeType 2.14.3 (FTL or
GPL-2.0 dual licence — the FTL option is taken), HarfBuzz 13.2.1 (Old MIT),
libpng 1.6.56 (PNG Reference Library License v2) and brotli 1.2.0 (MIT). Those
four are linked into `PIL\_imagingft.cp311-win_amd64.pyd`, which PyInstaller did
**not** pull into this build — the exe's manifest contains `_imaging`, `_avif`,
`_webp`, `_imagingcms`, `_imagingmath` and `_imagingtk` and no `_imagingft` — so
they are not redistributed and no obligation attaches to them here. Excluding
`PIL` from the PyInstaller build would remove every library in this section;
nothing in `fca/` needs it.

None of these libraries is under a copyleft licence. Every one of them carries the
ordinary "reproduce the copyright notice and licence text with binary
redistributions" obligation, and unlike numpy's and cryptography's, Pillow's
aggregated licence file is **not** among the `.dist-info` folders PyInstaller
happened to copy into the exe. The attribution for the libraries above therefore
rests entirely on this document, which is why each is named individually and why
`THIRD_PARTY_NOTICES.md` is now packaged inside and alongside both binaries. Their
full texts (libaom's excepted, see above) are in
`pillow-12.2.0.dist-info/licenses/LICENSE` in the build environment.

### Obligations attached to section 4

* **numpy → OpenBLAS → GCC runtime.** `numpy.libs/libscipy_openblas64_*.dll` is
  OpenBLAS (BSD-3-Clause) with LAPACK (BSD-3-Clause-Open-MPI), and it is
  statically linked against the **GCC runtime library (libgfortran/libgcc),
  which is GPL-3.0-or-later WITH GCC-exception-3.1**. The GCC Runtime Library
  Exception is an additional permission under section 7 of the GPLv3 that lets
  the compiled result be distributed under any licence, so this does not make
  the application copyleft — but it is the one GPL-family text inside the
  Windows binary and it is named here deliberately. The same DLL folder carries
  a Microsoft `msvcp140-*.dll`. Excluding `numpy` (and the rest of section 4)
  from the PyInstaller build removes this component entirely; nothing in `fca/`
  needs it.
* **cryptography's Rust crates.** `cryptography/hazmat/bindings/_rust.pyd` statically
  links the crates listed in the embedded
  `cryptography-50.0.0.dist-info/sboms/cryptography-rust.cyclonedx.json`. All are
  permissive or permissively dual-licensed (`MIT OR Apache-2.0`,
  `Apache-2.0 OR BSD-3-Clause`, `Apache-2.0 WITH LLVM-exception`,
  `(MIT OR Apache-2.0) AND Unicode-3.0`). One crate, `self_cell`, is
  `Apache-2.0 OR GPL-2.0-only`; the Apache-2.0 option is taken, so no copyleft
  obligation follows.
* **lxml isoschematron resources.** `lxml/isoschematron/resources/**` (embedded in
  the exe) contains the ISO Schematron RELAX NG schema (© ISO) and the
  iso-schematron-xslt1 stylesheets (© Rick Jelliffe / Academia Sinica Computing
  Centre). Those files carry their own notices inside them and must stay
  unmodified with their notices intact.
* **Apache-2.0 components** (OpenSSL, the run-time hooks from PyInstaller and from
  PyInstaller Community Hooks, and the Apache-2.0 option of `cryptography` and of
  numpy's vendored Highway, which is dual Apache-2.0 / BSD-3-Clause) require the
  licence text and attribution notices to travel with the binary, and any modified
  file to be marked as changed. No file of any third-party component is modified
  by this project.
* **BSD / MIT / MIT-CMU / PSF / Zlib components** require their copyright notice
  and licence text to be reproduced with binary redistributions — which is what
  this file, together with the licence files embedded in the package, is for.
* **How that obligation is actually discharged** (from this revision onward — see
  the note under "Scope of distributed binaries" about the already-cut v1.2.1
  archives). `LICENSE` (the project's own
  MIT text) and `THIRD_PARTY_NOTICES.md` (this file) are packaged **inside** both
  binaries and placed **next to** them in both release archives:
  `FrenchCourseAI.spec` adds them to `datas`, `build_macos.sh` adds them via
  `--add-data` and stages them beside `FrenchCourseAI.app` before `ditto` builds
  the zip, and `build.bat` adds them beside `FrenchCourseAI.exe` in
  `FrenchCourseAI-Windows.zip`. At run time they sit next to the frozen
  application's other data files — `sys._MEIPASS` for the one-file exe, and
  `FrenchCourseAI.app/Contents/Resources/` for the .app (which is where PyInstaller
  puts `--add-data` targets, symlinked from `Contents/Frameworks/`). Beyond those two files,
  the packages also carry the licence texts PyInstaller collects on its own:
  `_tk_data/license.terms`, `cryptography-50.0.0.dist-info/licenses/*` and
  `numpy-2.4.6.dist-info/licenses/**` in the Windows exe. Pillow's, lxml's and
  fontTools' licence files are *not* among them, so for those components the
  attribution rests on this document.
* **No MPL-2.0 component is present.** (Had one been, its source files would have
  to remain available in their original form under MPL-2.0 §3.) `certifi` is
  installed in the build environment but is *not* pulled into either binary.

## 5. Learning material

All learning content in this repository is written for the project and is covered
by the project's MIT licence: `fca/seed_words.py` (A1 starter vocabulary),
`fca/dict_data.py` (the built-in FR–EN–TR dictionary), `fca/content.py`
(orthography, pronunciation, grammar topics and exercises) and `grammar/*.md`.
No third-party course material, corpus or dictionary is bundled.

### Resource Center links

`fca/content.py` (`RESOURCES`) lists four openly licensed external collections.
The application only opens the URL in the learner's browser
(`webbrowser.open` in `fca/tabs/reading.py`) — it never downloads or bundles the
material. Anything a learner fetches keeps the licence of its own source and
must be attributed accordingly:

| Source | Licence as listed in the app |
| --- | --- |
| [French — Wikibooks](https://en.wikibooks.org/wiki/French) | CC BY-SA 4.0 — Wikibooks contributors |
| [Tatoeba French sentences](https://tatoeba.org/en/downloads) | CC BY 2.0 FR / selected CC0 — Tatoeba contributors; sentence-level attribution must be preserved |
| [LibriVox French audiobooks](https://librivox.org/search?primary_key=2&search_category=language&search_page=1&search_form=get_results) (the French-language search the app opens) | Public domain in the USA; local status must be checked — LibriVox volunteers |
| [Project Gutenberg French shelf](https://www.gutenberg.org/browse/languages/fr) | Project Gutenberg public-domain terms; local status must be checked — Project Gutenberg and the named authors/editors |

Files the learner drops into `Resources/` stay on the learner's machine; they are
neither tracked in this repository nor included in any release.

## 6. Documentation tooling

`docs/presentation/generate_presentations.mjs` is a one-off helper that regenerates
the slide deck through an internal Node renderer (`@oai/artifact-tool`, resolved
from the `ARTIFACT_TOOL` environment variable). That renderer is not part of this
repository, is not redistributed with it, and is not needed to build, test or run
French Course AI.

---

*Last verified: 2026-09-08, against French Course AI 1.2.1.*
