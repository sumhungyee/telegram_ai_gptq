# telegram_ai
A telegram bot run on a large language model. This is a very new project and I'm happy to get some feedback.

### Sample Image 1
![image](https://github.com/sumhungyee/telegram_ai/assets/113227987/fb7f9124-27db-48ba-8a09-f25ac794236e)

### Sample Image 2
<img width="508" alt="image2" src="https://github.com/sumhungyee/telegram_ai/assets/113227987/93a27871-92a8-4709-950d-d285057a532d">

## Requirements
1. A Windows computer.
2. A Nvidia GPU.
3. A telegram account.
4. [Anaconda](https://www.anaconda.com/download)
5. [CUDA toolkit (A version not after 11.8)](https://developer.nvidia.com/cuda-toolkit-archive). Currently tested on 11.2.

## Installation guide
0. Ensure that the requirements have been installed. Download and execute the installers from the links above and follow the instructions of the installers.
1. Open the command prompt on your computer. Simply search "terminal" on the bottom left and open up the terminal. If you run into any installation problems of the `safetensors` file, it may be that your git version is older than 2.34. Run `git update-git-for-windows` in the command prompt.
2. Choose a location on your computer (where you would like to store these files), and note/copy its directory, perhaps using windows explorer. For example, `C:\Users\AI_bot` or `C:\Users\xyz\OneDrive\Desktop\AI_bot`. Then navigate to this location on the command prompt by typing and entering `cd <directory>`. For example, `cd C:\Users\AI_bot`.
3. Go to the terminal, and clone this repository by entering `git clone https://github.com/sumhungyee/telegram_ai.git`
4. Navigate to the folder you have just created at `<directory>` and click on `Installer.bat`. This will take a long time.
5. In the meantime, go to telegram and search for the user/bot "BotFather". Create a bot and receive your API token, as well as bot handle.
6. Adjust and fill in the parameters in `main_settings.ini`! Fill in your API token for telegram and your bot's handle. Decrease or increase the value under your GPU's VRAM (and make sure to give around 3-4GB of buffer). 
7. Click on  `RUNME.bat` to run the bot!

## Making Changes
### Adding characters/contexts
Navigate to the `prompt_contexts` folder. `Assistant` is already provided, and users may use the text file as an example to create a context. The name of the text file `assistant.txt` serves as the character name, while the text within the text file serves as the context for prompts. To be more specific, naming the text file as `cat.txt` is sufficient in changing the character's identity to a cat.

### Switching characters
After adding a text file to the `prompt_contexts` folder, simply go to telegram and use the `/set_character` command. Users may switch back and forth between characters. Messages that are generating or still in-queue will not be affected.

## For Developers
### Changing models (LLMs)
Note that this bot relies on AutoGPTQ, and has mainly been tested on LLaMA-based models. To source for available models online, users can try smaller-parameter **GPTQ models** [finding TheBloke's quantized models on Huggingface](https://huggingface.co/TheBloke).

Download these models and add them to the `gptqmodels` folder, and change the settings in `main_settings.ini` to ensure that the link points to the model you want.
For example, run `git clone https://huggingface.co/TheBloke/wizardLM-13B-1.0-GPTQ` to install wizardLM 13B v1.0 GPTQ.

### Limitations
1. Stateless. This is beneficial for group-chats, and saves a lot of effort and memory.
2. Can be very slow, depending on the speed of your computer. 

Different models are trained with different prompt templates. It is important to ensure that your model's prompt template matches the prompt template you are feeding it. For a list of prompt templates, see [this link](https://www.reddit.com/r/LocalLLaMA/wiki/models#wiki_prompt_templates).
Currently, only Vicunav1.1 is supported, however, one can choose to extend this by visiting `loader.py` under the `gptq` folder, extending from the `PromptTypes` and `DelayedReply` classes. 
 
## Acknowledgements
Special thanks to TheBloke for helping to debug and providing template code.


