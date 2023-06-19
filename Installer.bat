
@echo off
set root=C:\Users\%USERNAME%\anaconda3\condabin
if not exist %root% (
    echo Anaconda not installed! Please install anaconda.
    pause
    exit /b 1
) else (
    echo Anaconda found.
)

set pathdir=%cd%

call %root%\activate.bat
call mkdir %pathdir%\environment
call conda env create --prefix %pathdir%\environment\telebot-env -f telebot-env.yml
call conda activate %pathdir%\environment\telebot-env

echo Now installing model. Default model chosen: TheBloke_Wizard-Vicuna-13B-Uncensored-GPTQ
echo Please be patient, the file is big.
call cd %pathdir%\gptqmodels
call git clone https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GPTQ
pause