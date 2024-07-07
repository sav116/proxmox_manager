from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import config
from utils.proxmox import ProxmoxNode

storage = MemoryStorage()

bot = Bot(config.bot_token)
dp = Dispatcher(bot, storage=storage)

node = ProxmoxNode(config)