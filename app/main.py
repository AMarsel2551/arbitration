import asyncio
from aiogram.fsm.context import FSMContext
from app.settings import tb_settings, DATA_RUB, DATA_KZT
from aiogram import Bot, Dispatcher, Router
from app.logger import log
from aiogram.client.default import DefaultBotProperties
from app.functional import filter_callback, check_need
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import BotCommand
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


bot = Bot(tb_settings.TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
router = Router()


# Команды
commands = [
    BotCommand(command="/start", description="Команда старта"),
    # BotCommand(command="/help", description="Команда помощи"),
]


# Начальное меню
KeyboardMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="START", callback_data="start"),
            InlineKeyboardButton(text="EXIT", callback_data="exit"),
        ],
        # [
        #     InlineKeyboardButton(text="RUB", callback_data="rub"),
        #     InlineKeyboardButton(text="KZT", callback_data="kzt"),
        # ]
    ]
)


@router.callback_query(lambda c: filter_callback(c, ['start']))
async def start(callback_query: CallbackQuery, state: FSMContext):
    await check_need()


@router.callback_query(lambda c: filter_callback(c, ['exit']))
async def exit(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text='...', reply_markup=KeyboardMenu)
    await state.clear()


@router.callback_query(lambda c: filter_callback(c, ['rub']))
async def rub(callback_query: CallbackQuery, state: FSMContext):
    await check_need(data=DATA_RUB)


@router.callback_query(lambda c: filter_callback(c, ['kzt']))
async def kzt(callback_query: CallbackQuery, state: FSMContext):
    await check_need(data=DATA_KZT)


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    await message.answer('...', reply_markup=KeyboardMenu)


async def main() -> None:
    dp.include_router(router)
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


async def schedule_telegram_bot():
    while ...:
        try:
            await main()
        except Exception as error:
            break # todo убрать!
            log.error(f"main error: {error}")

asyncio.run(schedule_telegram_bot())