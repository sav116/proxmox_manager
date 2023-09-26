from pydantic import BaseModel
from environs import Env
from loguru import logger
import sys
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

env = Env()
env.read_env()

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

def logger_decorator(func):
    """Logger decorator"""
    def wrapper(*func_args, **kwargs):
        logger.info(f"Calling function: {func.__name__}")
        start_time = datetime.now()
        result = func(*func_args, **kwargs)
        logger.info(f"Duration: {datetime.now() - start_time}")
        return result
    return wrapper

config_data = {
    "hostname": env.str("PVE_URL"),
    "username": env.str("PVE_USERNAME"),
    "password": env.str("PVE_PASSWORD"),
    "node_name": env.str("PVE_NODENAME")
}

class ProxmoxVMConfig(BaseModel):
    hostname: str
    username: str
    password: str
    node_name: str

config = ProxmoxVMConfig(**config_data)
