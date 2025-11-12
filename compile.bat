@echo off
echo === Building ASTROTRACKER app ===

REM Set venv python path
set VENV_PY=%CD%\.venv\Scripts\python.exe

REM Set source and destination for CITATION file
set CITATION_SRC=%CD%\.venv\Lib\site-packages\astroquery\CITATION
set CITATION_DEST=astroquery

REM Set the JSON used by astroquery.simbad
set SIMBAD_JSON_SRC=%CD%\.venv\Lib\site-packages\astroquery\simbad\data\query_criteria_fields.json
set SIMBAD_JSON_DEST=astroquery\simbad\data

REM Build EXE with PyInstaller
%VENV_PY% -m PyInstaller --onefile --noconsole --name astrotracker main.py ^
	--add-data "%CITATION_SRC%;%CITATION_DEST%" ^
	--add-data "%SIMBAD_JSON_SRC%;%SIMBAD_JSON_DEST%"

echo === Build complete ===
pause
