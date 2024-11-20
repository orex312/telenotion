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


# чтение даты из json файла
def read_json_data (sFile_json_data):
    with open (sFile_json_data, 'r') as json_file:
         data = json.load (json_file)
    return data
bot_data = read_json_data ('bot_info.json')

API_TOKEN = bot_data["bot_token"]



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

@dp.message (Command("json"))
async def send_text_echo(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True)) # строка исключительно для тестов
    await message.reply (message.model_dump_json(indent=4, exclude_none=True))

#dp.message.register(send_weather, F.content_type == ContentType.TEXT)

# Она запускает поллинг, то есть постоянный опрос сервера Telegram на наличие апдейтов для бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)

