# telegram_ai
A telegram bot run on a large language model.
![image](https://github.com/sumhungyee/telegram_ai/assets/113227987/fb7f9124-27db-48ba-8a09-f25ac794236e)

## Requirements
1. A Windows computer.
2. A Nvidia GPU.
3. A telegram account.
4. Python 3.10.16
5. [CUDA toolkit (A version not later than 11.8)](https://developer.nvidia.com/cuda-toolkit-archive). Currently tested on 11.2.

## Installation guide
0. Obtain and follow the instructions of the installer for the [CUDA toolkit (A version not later than 11.8)](https://developer.nvidia.com/cuda-toolkit-archive).
1. Open the command prompt on your computer. Simply search "terminal" on the bottom left and open up the terminal.
2. Choose a location on your computer (where you would like to store these files), and note/copy its directory, perhaps using windows explorer. For example, `C:\Users\AI_bot`. or `C:\Users\xyz\OneDrive\Desktop\AI_bot`. Then navigate to this location on the command prompt by typing and entering `cd <directory>`. For example, `cd C:\Users\AI_bot`
3. Go to the terminal, and clone this repository by entering `git clone https://github.com/sumhungyee/telegram_ai.git`
4. Navigate to the folder you have just created at `<directory>` and click on `Install.bat`. This will take a long time.
5. In the meantime, go to telegram and search for the user/bot "BotFather". Create a bot and receive your API token, as well as bot handle.
6. Adjust and fill in the parameters in `main_settings.ini`! Fill in your API token for telegram and your bot's handle. Decrease or increase the value under your GPU's VRAM (and make sure to give around 3-4GB of buffer). 
7. Click on  `RUNME.bat` to run the bot!

## Making Changes
### Adding characters/contexts
Navigate to the `prompt_contexts` folder. `Assistant` is already provided. The name of the text file `assistant.txt` serves as the character name, while the text within the text file serves as the context for prompts. To be more specific, naming the text file as `cat.txt` is sufficient in changing the character's identity to a cat.

### Changing models (LLMs)
Note that this bot relies on AutoGPTQ, and has mainly been tested on LLaMA-based models. To source for available models online, one can try **GPTQ models** [finding TheBloke's quantized models on Huggingface](https://huggingface.co/TheBloke).

Download these models and add them to the `gptqmodels` folder, and change the settings in `main_settings.ini` to ensure that the link points to the model you want.

### **IMPORTANT, FOR DEVELOPERS**
Different models are trained with different prompt templates. It is important to ensure that your model's prompt template matches the prompt template you are feeding it. For a list of prompt templates, see [this link](https://www.reddit.com/r/LocalLLaMA/wiki/models#wiki_prompt_templates).

Currently, only Vicunav1.1 is supported, however, one can choose to extend this by visiting `loader.py` under the `gptq` folder, extending from the `PromptTypes` and `DelayedReply` classes. 
 



