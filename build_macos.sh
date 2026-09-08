#!/usr/bin/env bash
set -eo pipefail

cd "$(dirname "$0")"
PROJECT_ROOT="$(pwd)"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "HATA: macOS .app paketi bir Mac üzerinde oluşturulmalıdır."
  exit 1
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt
"$PYTHON_BIN" -m pip install pyinstaller

rm -rf build/macos "dist/FrenchCourseAI.app" "dist/FrenchCourseAI-macOS" "dist/FrenchCourseAI-macOS.zip"
mkdir -p build/macos

ICON_ARGS=()
if command -v sips >/dev/null && command -v iconutil >/dev/null && [[ -f assets/app-final.png ]]; then
  ICONSET="build/macos/FrenchCourseAI.iconset"
  mkdir -p "$ICONSET"
  for size in 16 32 128 256 512; do
    sips -z "$size" "$size" assets/app-final.png --out "$ICONSET/icon_${size}x${size}.png" >/dev/null
    double=$((size * 2))
    sips -z "$double" "$double" assets/app-final.png --out "$ICONSET/icon_${size}x${size}@2x.png" >/dev/null
  done
  iconutil -c icns "$ICONSET" -o build/macos/FrenchCourseAI.icns
  ICON_ARGS=(--icon "$PROJECT_ROOT/build/macos/FrenchCourseAI.icns")
fi

DATA_ARGS=()
[[ -d assets ]] && DATA_ARGS+=(--add-data "$PROJECT_ROOT/assets:assets")
[[ -d Resources ]] && DATA_ARGS+=(--add-data "$PROJECT_ROOT/Resources:Resources")
[[ -d grammar ]] && DATA_ARGS+=(--add-data "$PROJECT_ROOT/grammar:grammar")
# Lisans metinleri ikili paketin icinde de yer almalidir (MIT + Apache-2.0 yukumlulukleri);
# eksiklerse paketleme bilerek durur, lisanssiz bir paket yayinlanmaz.
for licence_file in LICENSE THIRD_PARTY_NOTICES.md; do
  [[ -f "$licence_file" ]] || { echo "HATA: $licence_file bulunamadi; lisanssiz paket uretilmez."; exit 1; }
  DATA_ARGS+=(--add-data "$PROJECT_ROOT/$licence_file:.")
done

SIGN_ARGS=()
if [[ -n "${APPLE_CODESIGN_IDENTITY:-}" ]]; then
  SIGN_ARGS=(--codesign-identity "$APPLE_CODESIGN_IDENTITY")
fi

"$PYTHON_BIN" -m PyInstaller --noconfirm --clean --onedir --windowed \
  --workpath build/macos/pyinstaller --specpath build/macos \
  --name "FrenchCourseAI" \
  --osx-bundle-identifier "com.frenchcourseai.desktop" \
  "${ICON_ARGS[@]}" "${SIGN_ARGS[@]}" "${DATA_ARGS[@]}" \
  --hidden-import pypdf \
  --hidden-import fca.secrets --hidden-import fca.dictionary --hidden-import fca.dict_data --hidden-import fca.tabs.dictionary \
  French_Course_AI.pyw

APP_PATH="dist/FrenchCourseAI.app"
[[ -d "$APP_PATH" ]] || { echo "HATA: $APP_PATH oluşturulamadı."; exit 1; }

# Dagitim klasoru: .app yaninda MIT lisansi ve ucuncu taraf bildirimleri de gider.
STAGE_DIR="dist/FrenchCourseAI-macOS"
rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR"
ditto "$APP_PATH" "$STAGE_DIR/FrenchCourseAI.app"
cp LICENSE "$STAGE_DIR/LICENSE"
cp THIRD_PARTY_NOTICES.md "$STAGE_DIR/THIRD_PARTY_NOTICES.md"

# --keepParent yok: STAGE_DIR'in icerigi arsivin kokune gider,
# yani .app eskisi gibi zip'in kokunde durur, yaninda iki lisans dosyasiyla.
ditto -c -k "$STAGE_DIR" "dist/FrenchCourseAI-macOS.zip"
echo "Tamamlandı: $APP_PATH"
echo "Dağıtım ZIP'i: dist/FrenchCourseAI-macOS.zip (FrenchCourseAI.app + LICENSE + THIRD_PARTY_NOTICES.md)"
