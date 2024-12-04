from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User, ContentType
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row, Column, SwitchTo, Next, Back
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from dialogs import MainDialog, router
import bot_config
import logging
import text




BOT_TOKEN = bot_config.test_bot_token

#bt = Bot(token=BOT_TOKEN)
#dp = Dispatcher()
#router = Router()


class DonateDialog(StatesGroup):
	donate = State()
	donate_rubs = State()
	donate_rubs_accept = State()
	donate_stars = State()
	donate_stars_accept = State()
	congrats_4_donate = State()
	


async def go_main(
        callback: CallbackQuery, 
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.start(state=MainDialog.start, mode=StartMode.RESET_STACK)





# обработка доната рублями
async def donate_rubs(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	await callback.message.edit_text(text='Донат рублями 💵 по карточке')
	await dialog_manager.done()  


# обработка доната звездами
async def donate_stars (callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	await callback.message.edit_text (text='Донат звездами ⭐️ телеграм')
	await dialog_manager.done()


async def show_all_welcome (callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	await dialog_manager.start(DonateDialog.all_welcome)


async def donate_window (callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	await dialog_manager.start (DonateDialog.donate)







async def donate_rubs_done (callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	PRICE = types.LabeledPrice (label = "Добровольно пожертвование", amount = int(dialog_manager.dialog_data['value']) * 100) #копейки
	from main import bot as bt
	#message = callback.message
	#if bot_config.test_pay_token.split(':')[1] == 'TEST':
	#	await bt.send_message(message.chat.id, "Попробуем оплатить")
	await bt.send_invoice(dialog_manager.event.message.chat.id,
                           title="Добровольно пожертвование",
                           description="Разовое добровольное пожертвование \nна поддержку развития проекта",
                           provider_token=bot_config.test_pay_token,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

async def donate_stars_done (callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
	PRICE = types.LabeledPrice (label = "Добровольно пожертвование", amount = int(dialog_manager.dialog_data['value'])) 
	from main import bot as bt

	message = callback.message 
	await bt.send_invoice(message.chat.id,
                           title="Добровольно пожертвование",
                           description="Разовое добровольное пожертвование \nна поддержку развития проекта",
                           provider_token=bot_config.test_pay_token,
                           currency="XTR",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

# обработка и утверждение платежа перед тем, как пользователь его совершит
@router.pre_checkout_query (lambda query: True)
async def pre_checkout (pre_checkout_q: types.PreCheckoutQuery):
	from main import bot as bt
	await bt.answer_pre_checkout_query (pre_checkout_q.id, ok=True)

# обработка успешного платежа
@router.message (F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def succesful_payment (message: types.Message, dialog_manager: DialogManager):

	await dialog_manager.start(state=DonateDialog.congrats_4_donate)

	



async def get_username (event_from_user: User, **kwargs):
	return {'username': event_from_user.username}

async def get_value (dialog_manager: DialogManager, **kwargs):
	#print (dialog_manager.event.model_dump_json(indent=3, exclude_none=True))
	resp = dialog_manager.dialog_data['value']
	return {'value': resp}

def sum_check (text: str) -> str:
	if all(ch.isdigit() for ch in text) and 1 <= int(text) <= 1000000:
		return text
	raise ValueError

async def incorrect_sum (message: Message, widget: ManagedTextInput, dialo_manager: DialogManager, text: str):
	await message.answer ('Некорректное значение, поробуйте еще раз')

async def correct_sum (message: Message, widget: ManagedTextInput, dialo_manager: DialogManager, text: str):
	dialo_manager.dialog_data['value'] = text
	await dialo_manager.next()





# Это классический хэндлер, который будет срабатывать на команду /start
@router.message(Command("start"))
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=DonateDialog.donate, mode=StartMode.RESET_STACK)

donate_dialog = Dialog(

	# Окно выбора варианта доната
	Window (
		Format (text=text.donate_word),
		Column (
			SwitchTo (Const(text.donate_stars), id = text.donate_stars_id, state = DonateDialog.donate_stars),
			SwitchTo (Const(text.donate_rubs + " тестовая"), id = text.donate_rubs_id, state = DonateDialog.donate_rubs),
		),
		Button(Const("Меню📖"), id="task", on_click=go_main),
		getter=get_username,
		state = DonateDialog.donate,
		parse_mode="HTML",
	),

	Window (
		Format (text.welcome_donate_rubs),
		Const (text.enter_donate_value),
		TextInput (
			id = 'donate_rubs',
			type_factory = sum_check,
			on_success = correct_sum,
			on_error = incorrect_sum,
		),
		SwitchTo (Const('back'), id='back', state=DonateDialog.donate),
		Button(Const("Меню📖"), id="task", on_click=go_main),
		getter=get_username,
		state = DonateDialog.donate_rubs,
		parse_mode="HTML",
	),

	
	# Подтверждение доната рублями
	Window (
		Const ('Подтверждение оплаты рубликами'),
		Format ('Сумма в рублях - {value}'),
		Row (
			Button (Const(text.accept), id = text.accept_id, on_click = donate_rubs_done),
			Button (Const(text.cancel), id = text.cancel_id, on_click = Back())
		),
		Button(Const("Меню📖"), id="task", on_click=go_main),
		getter = get_value,
		state = DonateDialog.donate_rubs_accept,
		parse_mode="HTML",
	),


	# Окно доната звездами
	Window (
		Format (text.welcome_donate_stars),
		Const (text.enter_donate_value),
		TextInput (
			id = 'donate_stars',
			type_factory = sum_check,
			on_success = correct_sum,
			on_error = incorrect_sum,
		),
		SwitchTo (Const('back'), id='back', state=DonateDialog.donate),
		Button(Const("Меню📖"), id="task", on_click=go_main),
		getter=get_username,
		state = DonateDialog.donate_stars,
		parse_mode="HTML",
	),

	# Подтверждение оплаты звездами
	Window (
		Const ('Подтверждение оплаты звёздочками'),
		Format ('Сумма в звездах - {value}'),
		Row (
			Button (Const(text.accept), id = text.accept_id, on_click = donate_stars_done),
			Button (Const(text.cancel), id = text.cancel_id, on_click = Back())
		),
		Button(Const("Меню📖"), id="task", on_click=go_main),
		getter = get_value,
		state = DonateDialog.donate_stars_accept,
		parse_mode="HTML",
	),

	# Окно благодарности
	Window (
		Format (text.congrats_4_donate),
		Button (Const('Главное меню'), id='back', on_click = go_main),
		getter = get_username,
		state = DonateDialog.congrats_4_donate,
		parse_mode = "HTML",
	)
)





