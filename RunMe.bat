@echo off

REM Install required packages
echo Installing required packages...
pip install pygetwindow==0.0.9 pywinauto==0.6.0 keyboard==0.13.5

REM Run the SCPTimer.py script
echo Running SCPTimer.py...
python SCPTimer.py
