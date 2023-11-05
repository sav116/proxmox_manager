from loguru import logger
import sys
from datetime import datetime

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

def logger_decorator(func):
    """Logger decorator"""
    def wrapper(*func_args, **kwargs):
        logger.info(f"Calling function: {func.__name__}, with args: {func_args[1:]}")
        start_time = datetime.now()
        result = func(*func_args, **kwargs)
        logger.info(f"Сompleted function: {func.__name__}, duration: {datetime.now() - start_time}, returned type: {type(result)}")
        return result
    return wrapper