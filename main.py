from gptq.loader import *

import threading

botapi = config["telebot"]["API"]
bot = start_telebot(botapi)
print("Bot Online!\n")
event = threading.Event()
def answer_from_queue():

    quantized_model_dir = config["models"]["MODELPATH"]
    model_basename = config["models"]["MODELBASENAME"]
    
    tokenizer = load_tokenizer(quantized_model_dir)
    model = load_model(quantized_model_dir, model_basename)
    pipeline = load_pipeline(model, tokenizer)
    while not event.is_set():  
        if queue.qsize() >= 1:
            task = queue.get()
            try:       
                reply = task.execute(pipeline)
                if reply:
                    do_reply(task.msg, f"{task.character.capitalize()}: {reply}", bot)    
                else:
                    do_reply(task.msg, "(No reply to that)", bot)
                    log.warning(f'Reply Empty!')
            

            except Exception as e:
                log.error(f'FAILED TO GENERATE REPLY! Error message: {e}. Restarting...')
                do_reply(task.msg, ":( oh no i crashed and died. Restarting bot...", bot)

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
            if try_again:
                log.warning("Trying to reply again...")
            do_reply(msg, text, bot, try_again=False)
        

@bot.message_handler(commands = ["chat"])
def add_to_queue(msg):
    curr_queue_size = queue.qsize()
    if f"/chat{config['telebot']['BOTNAME']}" not in msg.text:
        msg.text = msg.text[len("/chat "):]
        task = DelayedReply(msg, *load_template())
        
        queue_status = f"Message added to queue. {curr_queue_size} other {'messages' if curr_queue_size != 1 else 'message'} in queue."
        log.debug(queue_status)
        do_reply(msg, queue_status, bot)
        add_task(queue, task)
        
        

@bot.message_handler(commands = ["set_character"])
def set_character(msg):
    context_ls = load_context_character_ls()
    chara_name = msg.text[len("/set_character "):]
    if chara_name in context_ls:
        config["prompt"]["character"] = chara_name

        found = f"Character set to {chara_name}!"
        log.debug(found)
        do_reply(msg, found, bot)

    else:
        not_found = f"""
        Character not found! Here are a list of characters available:\n{", ".join(context_ls)}
        """
        log.warning(f"Character {chara_name} not found")
        do_reply(msg, not_found, bot)
    


bot.infinity_polling(timeout = 10, long_polling_timeout=5)
event.set()