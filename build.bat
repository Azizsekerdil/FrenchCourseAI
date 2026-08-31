@echo off
setlocal
cd /d "%~dp0"
python -m PyInstaller --noconfirm --clean FrenchCourseAI.spec
if errorlevel 1 exit /b %errorlevel%
echo Built: %CD%\dist\FrenchCourseAI.exe
