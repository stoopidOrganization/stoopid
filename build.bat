@echo off
pyinstaller --noconfirm --onefile --console --icon "images/stoopidlogo.ico"  "stoopid.py"
move dist\stoopid.exe stoopid.exe
echo Starting cleanup...
del dist /F /Q /S
del build /F /Q /S
rmdir build /S /Q
rmdir dist /S /Q