
@echo off
setlocal enabledelayedexpansion
set root=C:\Users\%USERNAME%\anaconda3\condabin
if not exist %root% (
    echo Anaconda not installed! Please install anaconda.
    pause
    exit /b 1
) else (
    echo Anaconda found.
)

set pathdir=%cd%
mkdir %pathdir%\environment
call %root%\activate.bat
if not exist %pathdir%\environment\telebot-env (
   
    call conda env create --prefix %pathdir%\environment\telebot-env -f telebot-env.yaml
    call conda activate %pathdir%\environment\telebot-env
) else (  
    echo Environment already found.
    choice /c yn /m "Reinstall environment:  "
    
    if !errorlevel! equ 1 (    
        rmdir /s /q %pathdir%\environment
        echo Reinstalling...
       
        call conda env create --prefix %pathdir%\environment\telebot-env -f telebot-env.yaml
        call conda activate %pathdir%\environment\telebot-env

    ) else if !errorlevel! equ 2 (
        echo Not reinstalling.
        
    ) else (
        echo Unrecognised input, not reinstalling.
    )
    
)
if not exist %pathdir%\gptqmodels\Wizard-Vicuna-13B-Uncensored-GPTQ (
    echo Now installing model. Default model chosen: TheBloke_Wizard-Vicuna-13B-Uncensored-GPTQ
    echo Please be patient, the file is big.
    call cd %pathdir%\gptqmodels
    call git clone https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GPTQ

) else (
    echo Model already found.
    choice /c yn /m "Reinstall model? Useful if your download is not complete/corrupted:  "
    if !errorlevel! equ 1 ( 
        rmdir /s /q %pathdir%\gptqmodels\Wizard-Vicuna-13B-Uncensored-GPTQ
        echo Reinstalling...
        echo Please be patient, the file is big.
        call cd %pathdir%\gptqmodels
        call git clone https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GPTQ

    ) else if !errorlevel! equ 2 (
        echo Not reinstalling.
    ) else (
        echo Unrecognised command. Not reinstalling.
    )

)

pause