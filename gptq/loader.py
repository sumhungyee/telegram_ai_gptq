
from transformers import TextGenerationPipeline, AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM
from logs.startup import *

import gc
import telebot
import torch
import time
import torch
torch.cuda.is_available()


def start_telebot(botapi):
    bot = telebot.TeleBot(botapi)
    return bot

def load_model(quantized_model_dir, model_basename):
    
    return AutoGPTQForCausalLM.from_quantized(quantized_model_dir,
        use_safetensors=True,
        model_basename=model_basename,
        device=config["devices"]['device'],
        max_memory = {0: config["max memory"]['firstgpu'], 'cpu': config["max memory"]['cpu']},
        use_triton=True)

def load_pipeline(model, tokenizer):
    return TextGenerationPipeline(
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=300,
    temperature=0.7,
    top_p=0.95
)

def load_tokenizer(quantized_model_dir, use_fast=False):
    return AutoTokenizer.from_pretrained(quantized_model_dir, use_fast=use_fast)


def get_reply(prompt, character, prompt_template, pipeline) -> str:

    template = prompt_template.format(character=character, prompt=prompt, CHARACTER=character.upper())

    log.debug(f"Message received. Template message:\n{template} \nComputing...")
    
    begin = time.time()
    generated = pipeline(template)[0]['generated_text']
    opener = f"{character.upper()}: "
    end = "\n### USER:"
    chopped = generated[generated.find(end) + len(end) : ]

    reply = chopped[chopped.find(opener) + len(opener) : chopped.find(end) ]
    print(f"Reply:\n{reply}")
    elapsed = time.time() - begin
    
    log.debug(f"Text generation successful! Full generation:\n{generated}")
    log.debug(f"Text generated in {elapsed} seconds")
    return reply

def poll_task(queue):
    if queue.qsize() < 1:
        print("Queue is empty!")
    else:
        msg = queue.get()
        log.debug(f"Message successfully polled. Message: \n{msg.text}")
        return msg
    
def add_task(queue, msg) -> None:
    queue.put(msg)
    
def clear_cuda_memory():
    torch.cuda.empty_cache()
    gc.collect()
        

class PromptTypes:
    VICUNA11 = "vicunav1.1"


class DelayedReply:
    def __init__(self, msg, context, character, prompt_type):
        self.msg = msg
        self.context = context
        self.character = character
        self.prompt_type = prompt_type

    def gen_template(self):
        string = '''\n### USER: {prompt}\n### {CHARACTER}:'''
        if self.prompt_type == PromptTypes.VICUNA11:      
            log.debug(f"Loaded prompt type: {self.prompt_type}")
        else:
            log.warning("Prompt type not found. Reverting to default")   
        return self.context + string
    
    def execute(self, pipeline):
        template = self.gen_template()
        return get_reply(self.msg.text, self.character, template, pipeline)
