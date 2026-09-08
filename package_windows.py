"""Windows dagitim arsivini uretir: dist/FrenchCourseAI-Windows.zip.

Arsivin kokunde uc dosya bulunur - FrenchCourseAI.exe, LICENSE ve
THIRD_PARTY_NOTICES.md - boylece MIT metni ve ucuncu taraf bildirimleri
indirilen paketle birlikte gelir. build.bat bu betigi derlemeden sonra cagirir.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
ARCHIVE = DIST / "FrenchCourseAI-Windows.zip"
MEMBERS = [DIST / "FrenchCourseAI.exe", ROOT / "LICENSE", ROOT / "THIRD_PARTY_NOTICES.md"]


def main() -> int:
    missing = [p for p in MEMBERS if not p.is_file()]
    if missing:
        for path in missing:
            print(f"HATA: {path} bulunamadi.", file=sys.stderr)
        print("Lisanssiz ya da eksik paket uretilmez.", file=sys.stderr)
        return 1

    ARCHIVE.unlink(missing_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in MEMBERS:
            archive.write(path, path.name)

    names = zipfile.ZipFile(ARCHIVE).namelist()
    print(f"Packaged: {ARCHIVE} ({ARCHIVE.stat().st_size} bytes)")
    print("  " + ", ".join(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
