import configparser
import logging as log
import os
from transformers import logging as tlog
from pathlib import Path
from queue import Queue
import sys


default_context = '''A chat between a user and a helpful {character}. The {character} is helpful, polite and specialises in problem solving. The {character} thinks step by step and lists each step rationally.
'''

config = configparser.ConfigParser()
config.read("./main_settings.ini")

tlog.set_verbosity(tlog.CRITICAL)
filepath = os.path.abspath("./logs/logs.log")

file_handler = log.FileHandler(filename=filepath)
stdout_handler = log.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

log.basicConfig(handlers=handlers, level=log.DEBUG)
urllib3_logger = log.getLogger('urllib3')
urllib3_logger.setLevel(log.WARNING)


context_path = config["prompt"]["context_path"]
if not os.path.exists(f"{context_path}assistant.txt"):
    
    if not os.path.exists(context_path):
        os.mkdir(context_path)
        log.debug("Created path for context.")
    with open(f"{context_path}assistant.txt", "w") as f:
        f.write(default_context)
        f.close()
        log.debug('Created the "assistant" default character.')


def load_context_character_ls():
    return [Path(filename).stem for filename in os.listdir(context_path) if Path(filename).suffix == ".txt"]

context_ls = load_context_character_ls()


queue = Queue()

def load_template():
    try:
        character = config["prompt"]["character"]
        with open(f"./prompt_contexts/{character}.txt", "r") as f:  
            context = f.read()
            f.close()
            prompt_type = config["prompt"]["prompt_type"]
            log.debug(f"Prompt template loaded: {character}")

    except Exception as e:
        log.critical(f"Failure to read file. Check if './prompt_contexts/{character}.txt' exists and is not corrupted. Error: {e}\nResetting to defaults...")
        character = "assistant"
        prompt_type = "vicunav1.1"
        context = default_context
    return context, character, prompt_type

context, character, prompt_type = load_template()

#print(config['prompt']['context'])