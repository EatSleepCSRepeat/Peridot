@echo off

python -c "import requests" >nul 2>nul
if %errorlevel% neq 0 (
    pip install requests
)
python -c "import colorama" >nul 2>nul
if %errorlevel% neq 0 (
    pip install colorama
)
python ./src/peridot.py
