# попробуем иначе
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram import F



class BOT (object) :
	API_TOKEN = 123
	

def read_data (sFile_data):
	pFile_data = open (sFile_data, "r")
	read_token = pFile_data.readline ()
	return read_token
API_TOKEN = read_data ("bot_info.txt")



# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def send_any_echo(message: Message):
    print ("================================================================================================================ANY")
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.send_copy (chat_id = message.chat.id)
    
dp.message.register(send_any_echo)

# Она запускает поллинг, то есть постоянный опрос сервера Telegram на наличие апдейтов для бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)