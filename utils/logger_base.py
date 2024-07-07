from loguru import logger
import sys
from datetime import datetime
import re
from data.config import config


must_be_hidden = ['hostname', 'username', 'bot_token', 'password']
hidden_pattern = '|'.join([str(config.model_dump()[k]) for k in config.model_dump() if k in must_be_hidden])

def masked_out(message: str):
    pattern = re.compile(hidden_pattern)
    return pattern.sub("*****", message)

def logger_decorator(func):
    """Logger decorator"""
    def wrapper(*func_args, **kwargs):
        logger.info(masked_out(f"Call: {func.__module__} {func.__name__} | args: {func_args[1:]}"))
        start_time = datetime.now()
        result = func(*func_args, **kwargs)
        logger.info(masked_out(f"Сompleted: {func.__module__} {func.__name__} | returned type {type(result)}, size {sys.getsizeof(result)} | duration: {datetime.now() - start_time}"))
        return result
    return wrapper

logger.add(sys.stderr, filter="my_module", level="INFO")