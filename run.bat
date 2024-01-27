@echo off
call "%~dp0delint\Scripts\activate.bat"
python main.py
call "%~dp0delint\Scripts\deactivate.bat"