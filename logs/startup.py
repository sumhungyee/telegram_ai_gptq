import configparser
import logging as log
import os
from transformers import logging as tlog
from queue import Queue

config = configparser.ConfigParser()
config.read("./main_settings.ini")

no_api_message = "Your api here"

tlog.set_verbosity(tlog.CRITICAL)
filepath = os.path.abspath("./logs/logs.log")

try:
    logger_config_level = eval(config["logger"]["LEVEL"])
    log.basicConfig(filename=filepath, level=logger_config_level)
except AttributeError as a:
    print(f"Attribute Error found: {a}\n\nSetting level to debug...")
    logger_config_level = log.DEBUG
except NameError as n:
    print(f"Attribute Error found: {n}\n\nSetting level to debug...")
    logger_config_level = log.DEBUG
except Exception as e:
    print(f"Error found: {e}\n\nSetting level to debug...")
    logger_config_level = log.DEBUG
finally:
    log.basicConfig(filename=filepath, level=logger_config_level)

queue = Queue()


