# попробуем иначе
import telegram_bot.bot_config as bot_config
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram import F


class BOT:
	def __init__(self, BOT_TOKEN, URL, MAX_COUNTER):
		self.BOT_TOKEN = BOT_TOKEN
		self.URL = URL
		self.MAX_COUNTER = MAX_COUNTER

# Создаем объекты бота и диспетчера
bot = Bot(bot_config.bot_token)
dp = Dispatcher()

# ========================================================================================================= описание прайса
PRICE = types.LabeledPrice (label = "Подписка на месяц", amount = 500*100) # amount сумма в копейках

# ============================================================================================================= обработчики
@dp.message (Command("pay"))
async def buy_month (message: types.Message):
	if bot_config.pay_token.split(':')[1] == 'TEST':
		await bot.send_message(message.chat.id, "Попробуем оплатить")
    
	await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=bot_config.pay_token,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

@dp.message (Command("json"))
async def send_reply_json(message: types.Message):
    print(message.model_dump_json(indent=4, exclude_none=True)) # строка исключительно для тестов
    await message.reply (message.model_dump_json(indent=4, exclude_none=True))
    return 0
# или такая регистрация обработчика
#dp.message.register (send_reply_json, F.content_type == ContentType.TEXT)

# =========================================================================================================================

# Она запускает поллинг, то есть постоянный опрос сервера Telegram на наличие апдейтов для бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
