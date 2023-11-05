from pydantic import BaseModel
from environs import Env
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

env = Env()
env.read_env()

config_data = {
    "hostname": env.str("PVE_URL"),
    "username": env.str("PVE_USERNAME"),
    "password": env.str("PVE_PASSWORD"),
    "node_name": env.str("PVE_NODENAME"),
    "bot_token": env.str("BOT_TOKEN"),
    "admins": env.list("ADMINS")
}

class ProxmoxVMConfig(BaseModel):
    hostname: str
    username: str
    password: str
    node_name: str
    bot_token: str
    admins: list
    
config = ProxmoxVMConfig(**config_data)
