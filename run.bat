@echo off
echo Installing midiutil...
python -m pip install midiutil

echo Running main.py...
python metalerator/main.py

pause
