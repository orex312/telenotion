from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User, ContentType
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row, Column, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Case, List
import bot_config
import logging
import text
import random




BOT_TOKEN = bot_config.test_bot_token

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


class MainDialog(StatesGroup):
	start = State()
	all_welcome = State()
	donate = State()
	donate_rubs = State()
	donate_stars = State()
	






# обработка доната рублями
async def donate_rubs(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	await callback.message.edit_text(text='Донат рублями 💵 по карточке')
	await dialog_manager.done()  


# обработка доната звездами
async def donate_stars (callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	await callback.message.edit_text (text='Донат звездами ⭐️ телеграм')
	await dialog_manager.done()


async def show_all_welcome (callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	await dialog_manager.start(MainDialog.all_welcome)


async def donate_window (callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	await dialog_manager.start (MainDialog.donate)









# Это классический хэндлер, который будет срабатывать на команду /start
@router.message(Command("start"))
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=MainDialog.start, mode=StartMode.RESET_STACK)


PRICE = types.LabeledPrice (label = "Подписка на месяц", amount = 10 * 100) #копейки
async def donate_rubs_done (callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	message = callback.message
	#if bot_config.test_pay_token.split(':')[1] == 'TEST':
	#	await bot.send_message(message.chat.id, "Попробуем оплатить")
    
	await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=bot_config.test_pay_token,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

# обработка и утверждение платежа перед тем, как пользователь его совершит
@dp.pre_checkout_query (lambda query: True)
async def pre_checkout (pre_checkout_q: types.PreCheckoutQuery):
	await bot.answer_pre_checkout_query (pre_checkout_q.id, ok=True)


# обработка успешного платежа
@router.message (F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def succesful_payment (message: types.Message, dialog_manager: DialogManager):
	print ("Succesful payment:")
	payment_info = message.successful_payment
	#await message.reply (payment_info.model_dump_json(indent=4, exclude_none=True))
	await bot.send_message (message.chat.id, 
						f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
	await dialog_manager.start(state=MainDialog.start, mode=StartMode.RESET_STACK)

	










async def get_username (event_from_user: User, **kwargs):
	return {'username': event_from_user.username}

async def welcome_getter (event_from_user: User, **kwargs):
	return {'username': event_from_user.username, 'number': random.randint(1, 5)}

async def get_welcome_words (event_from_user: User, **kwargs):
	username = event_from_user.username
	return {'items': (
		(1, text.random_welcome_1.format(username = username)),
		(2, text.random_welcome_2.format(username = username)),
		(3, text.random_welcome_3.format(username = username)),
		(4, text.random_welcome_4.format(username = username)),
		(5, text.random_welcome_5.format(username = username)),
	)}









start_dialog = Dialog(
	# Стартовое окно
	Window (
		Case (
			texts={
				1: Format (text=text.random_welcome_1),
				2: Format (text=text.random_welcome_2),
				3: Format (text=text.random_welcome_3),
				4: Format (text=text.random_welcome_4),
				5: Format (text=text.random_welcome_5),
			},
			selector='number',
		),
		Column (
			Button (text=Const(text.main_window_my_info), id = text.main_window_my_info_id),
			Button (text=Const(text.main_window_my_tasks), id = text.main_window_my_tasks_id),
			Button (text=Const(text.main_window_new_tasks), id = text.main_window_new_tasks_id),
			Button (text=Const(text.main_window_donate), id = text.main_window_donate_id, on_click = donate_window),
			Button (text=Const('Показать список приветствий'), id = 'welcome_list', on_click=show_all_welcome),
		),
		getter=welcome_getter,
		state=MainDialog.start,
	),
	# Окно списка приветствий
	Window (
		Format (text='Список приветствий'),
		List (
			field=Format('{item[0]}.  {item[1]}'),
			items = 'items'),
		SwitchTo (Const('back'), id='back', state=MainDialog.start),
		getter = get_welcome_words,
		state = MainDialog.all_welcome,
	),
	# Окно выбора варианта доната
	Window (
		Format (text=text.donate_word),
		Column (
			SwitchTo (Const(text.donate_stars), id = text.donate_stars_id, state = MainDialog.donate_stars),
			SwitchTo (Const(text.donate_rubs), id = text.donate_rubs_id, state = MainDialog.donate_rubs),
		),
		SwitchTo (Const('back'), id='back', state=MainDialog.start),
		getter=get_username,
		state = MainDialog.donate,
	),
	# Окно диалога доната рублями
	Window (
		Format (text.welcome_donate_rubs),
		SwitchTo (Const('back'), id='back', state=MainDialog.donate),
		getter=get_username,
		state = MainDialog.donate_rubs
	),
	# Окно диалога доната звездами
	Window (
		Format (text.welcome_donate_stars),
		SwitchTo (Const('back'), id='back', state=MainDialog.donate),
		getter=get_username,
		state = MainDialog.donate_stars
	),
)


#@dp.message.register (succesful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)


def test():
	return 0

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	dp.include_router(router)
	dp.include_router(start_dialog)
	setup_dialogs(dp)
	dp.run_polling(bot)




