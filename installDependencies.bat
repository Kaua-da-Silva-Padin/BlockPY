@echo OFF
pip install pyinstaller ttkbootstrap
pyinstaller --onefile main.py
pause