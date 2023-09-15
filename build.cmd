pyinstaller --noconfirm --onefile  "tts-radio-generator.py"
copy dist\*.exe . /y
if not exist ".\dist\conf"   mkdir .\dist\conf
if not exist ".\dist\output" mkdir .\dist\output
if not exist ".\dist\sounds" mkdir .\dist\sounds
if not exist ".\dist\temp"   mkdir .\dist\temp

copy .\conf\default.yml .\dist\conf\ /Y
copy .\conf\default-google.yml .\dist\conf\ /Y
copy .\conf\example.csv .\dist\conf\ /Y

copy .\sounds\*.wav .\dist\sounds\ /Y
copy .\README.md .\dist\ /Y

pause
