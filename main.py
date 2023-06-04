from loader import *

import threading

botapi = config["telebot"]["API"]


bot = start_telebot(botapi)


event = threading.Event()

"""
prompt_template='''A chat between a user and an extremely rude and stupid {character}. The {character} is not helpful, and extremely rude.  Whenever the user asks a programming question, the {character} gives a nonsensical reply. The {character} curses and uses vulgarities very often, and aims to be as offensive as possible.
The {character} always denies being an artificial intelligence or a robot, and claims that his name is "Chummy" whenever asked. The conversation ends quickly after one reply by the {character}.
### USER: {prompt}
### {CHARACTER}:'''
character = "man"
"""

"""
prompt_template='''A chat between a user and an avid fan of minecraft, who is a {character}. The {character} is helpful and likes to play minecraft. Even though the {character} is knowledgeable, he will not pretend to know things that he does not know.
The {character} always denies being an artificial intelligence or a robot, and claims that his name is "Chummy" whenever asked. The conversation ends quickly after one reply by the {character}.
### USER: {prompt}
### {CHARACTER}:'''
character = "friend"
"""

"""
prompt_template='''A chat between a user and a helpful {character}. The {character} is helpful, polite and specialises in coding and programming. When writing code, the {character} formats code in code chunks, using three backticks ``` at the start and end of every code chunk. The conversation ends quickly after one reply by the {character}.
### USER: {prompt}
### {CHARACTER}:'''
character = "assistant"
"""

prompt_template='''A chat between a user and a helpful {character}. The {character} is helpful, polite and specialises in problem solving. The {character} thinks step by step and lists each step rationally.
### USER: {prompt}
### {CHARACTER}:'''
character = "assistant"



def answer_from_queue():

    quantized_model_dir = config["models"]["MODELPATH"]
    model_basename = config["models"]["MODELBASENAME"]
    
    tokenizer = load_tokenizer(quantized_model_dir)
    model = load_model(quantized_model_dir, model_basename)
    pipeline = load_pipeline(model, tokenizer)
    while not event.is_set():  
        if queue.qsize() >= 1:
            msg = queue.get()
            try:       
                reply = get_reply(msg.text, character, prompt_template, pipeline)
                if reply:
                    do_reply(msg, reply, bot)    
                else:
                    log.warning(f'Reply Empty!')
            

            except Exception as e:
                log.error(f'FAILED TO GENERATE REPLY! Error message: {e}. Restarting...')
                do_reply(msg, ":( oh no i crashed and died. Restarting bot...", bot)

                del model, tokenizer, pipeline
                clear_cuda_memory()

                model = load_model(quantized_model_dir,  model_basename)
                tokenizer = AutoTokenizer.from_pretrained(quantized_model_dir, use_fast=False)
                pipeline = load_pipeline(model, tokenizer)
                
answerer=threading.Thread(target=answer_from_queue)
answerer.start() 


def do_reply(msg, text, bot, try_again=True):
    if try_again:
        try:
            bot.reply_to(msg, text)
            log.debug(f'Reply Successful! Reply: {text}')
        except Exception as e:
            log.error("REPLY FAILED. Exception occured: {e}")
            time.sleep(2)
            log.warning("Trying to reply again...")
            do_reply(msg, text, bot, try_again=False)
        

@bot.message_handler(commands = ["chat"])
def add_to_queue(msg):
    if f"/chat{config['telebot']['BOTNAME']}" not in msg.text:
        msg.text = msg.text[len("/chat "):]
        add_task(queue, msg)
        log.debug(f"Message added to queue. {queue.qsize()} {'messages' if queue.qsize() != 1 else 'message'} in queue.")
              

bot.infinity_polling(timeout = 20, long_polling_timeout=7)
event.set()