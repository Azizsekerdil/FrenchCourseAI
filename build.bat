@echo off
setlocal
cd /d "%~dp0"
python -m PyInstaller --noconfirm --clean FrenchCourseAI.spec
if errorlevel 1 exit /b %errorlevel%
echo Built: %CD%\dist\FrenchCourseAI.exe

rem Dagitim ZIP'i: .exe yaninda MIT lisansi ve ucuncu taraf bildirimleri de gider.
if exist "dist\FrenchCourseAI-Windows.zip" del /q "dist\FrenchCourseAI-Windows.zip"
copy /y "LICENSE" "dist\LICENSE" >nul
if errorlevel 1 exit /b %errorlevel%
copy /y "THIRD_PARTY_NOTICES.md" "dist\THIRD_PARTY_NOTICES.md" >nul
if errorlevel 1 exit /b %errorlevel%
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Compress-Archive -Path 'dist\FrenchCourseAI.exe','dist\LICENSE','dist\THIRD_PARTY_NOTICES.md' -DestinationPath 'dist\FrenchCourseAI-Windows.zip' -Force"
if errorlevel 1 exit /b %errorlevel%
echo Packaged: %CD%\dist\FrenchCourseAI-Windows.zip (FrenchCourseAI.exe + LICENSE + THIRD_PARTY_NOTICES.md)
