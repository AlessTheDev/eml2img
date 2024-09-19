@echo off
:: Get the directory of the .bat file
set script_dir=%~dp0

:: Call the Python script using the full path to the script directory
python "%script_dir%EmailToImg\main.py" %*
