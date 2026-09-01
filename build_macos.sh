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

rm -rf build/macos "dist/FrenchCourseAI.app"
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
  French_Course_AI.pyw

APP_PATH="dist/FrenchCourseAI.app"
[[ -d "$APP_PATH" ]] || { echo "HATA: $APP_PATH oluşturulamadı."; exit 1; }

ditto -c -k --keepParent "$APP_PATH" "dist/FrenchCourseAI-macOS.zip"
echo "Tamamlandı: $APP_PATH"
echo "Dağıtım ZIP'i: dist/FrenchCourseAI-macOS.zip"
