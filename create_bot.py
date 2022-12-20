from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

API_TOKEN = '5680049690:AAFfjGkvZyCgHffHvwIwuJaxjBCsJdCgHyM'

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)