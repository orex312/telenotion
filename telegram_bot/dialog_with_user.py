# попробуем иначе
import logging
import requests
import json
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram import F



class BOT:
	def __init__(self, BOT_TOKEN, URL, MAX_COUNTER):
          self.BOT_TOKEN = BOT_TOKEN
          self.URL = URL
          self.MAX_COUNTER = MAX_COUNTER
	

def read_data (sFile_data):
	pFile_data = open (sFile_data, "r")
	read_token = pFile_data.readline ()
	return read_token
API_TOKEN = read_data ("bot_info.txt")



# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

tg_api = 'https://api.telegram.org/bot'
@dp.message (Command(commands=["weather"]))
async def send_weather (message: Message):
      api_url = 'https://api.telegram.org/bot7767052229:AAGcy1tK09SyCAXXz17Uso41WSYQqD-RxRM/sendMessage?chat_id=235503146&text=Привет, Mikhail!'
      req_url = f'{api_url}{BOT}/'
      resp = requests.get (api_url)
      await message.reply (resp.text)
      return 0
    
#dp.message.register(send_weather, F.content_type == ContentType.TEXT)

# Она запускает поллинг, то есть постоянный опрос сервера Telegram на наличие апдейтов для бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)