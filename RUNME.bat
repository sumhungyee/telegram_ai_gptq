@echo off
set pathdir=%cd%
set root=C:\Users\%USERNAME%\anaconda3\condabin
if not exist %root% (
    echo Anaconda not installed! Please install anaconda.
    exit /b 1
) else (
    echo Anaconda found.
)

set pathdir=%cd%

call %root%\activate.bat

if not exist %pathdir%\environment\telebot-env (
    echo Environment not installed! Run Installer.bat.
    pause
    exit /b 1
) else (
    echo Environment found, activating.
)

call conda activate %pathdir%\environment\telebot-env
call cd %pathdir%
echo Running python on %pathdir%...
python main.py
