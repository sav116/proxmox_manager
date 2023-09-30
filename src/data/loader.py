from aiogram import Bot, Dispatcher

from data.config import config
from utils.proxmox import ProxmoxNode

bot = Bot(config.bot_token)
dp = Dispatcher(bot)

node = ProxmoxNode(config)