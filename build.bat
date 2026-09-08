@echo off
setlocal
cd /d "%~dp0"

rem v1.3.0'dan itibaren paket TEMIZ bir sanal ortamda derlenir. Daha once
rem PyInstaller kuresel yorumlayiciyla calisiyordu ve pypdf'in istege bagli
rem importlari uzerinden orada kurulu olan Pillow, numpy, lxml, cryptography,
rem fontTools gibi kutuphaneler de .exe'ye giriyordu. Depo disinda kurulan bu
rem ortamda yalnizca requirements.txt + PyInstaller bulunur.
rem Kendi yorumlayicinizi kullanmak icin BUILD_PYTHON degiskenini tanimlayin.

if defined BUILD_PYTHON goto build

set "BUILD_VENV=%TEMP%\FrenchCourseAI-build-venv"
echo Temiz sanal ortam hazirlaniyor: %BUILD_VENV%
python -m venv --clear "%BUILD_VENV%"
if errorlevel 1 exit /b %errorlevel%
set "BUILD_PYTHON=%BUILD_VENV%\Scripts\python.exe"
"%BUILD_PYTHON%" -m pip install --upgrade pip
if errorlevel 1 exit /b %errorlevel%
"%BUILD_PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 exit /b %errorlevel%
"%BUILD_PYTHON%" -m pip install pyinstaller
if errorlevel 1 exit /b %errorlevel%

:build
"%BUILD_PYTHON%" -m PyInstaller --noconfirm --clean FrenchCourseAI.spec
if errorlevel 1 exit /b %errorlevel%
echo Built: %CD%\dist\FrenchCourseAI.exe

rem Dagitim ZIP'i: .exe yaninda MIT lisansi ve ucuncu taraf bildirimleri de gider.
"%BUILD_PYTHON%" package_windows.py
if errorlevel 1 exit /b %errorlevel%
