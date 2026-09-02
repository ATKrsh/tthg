@echo off
title TTHG - Unblock & Sign Executable
cd /d "%~dp0"
echo Unblocking TTHG executables and applying Authenticode digital code signature...
powershell -ExecutionPolicy Bypass -File "%~dp0sign_and_unblock.ps1"
echo Done. Press any key to exit.
pause > nul
