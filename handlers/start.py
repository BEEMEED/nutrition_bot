from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram import types
from aiogram.types import Message,CallbackQuery
from utils.keyboards.main_menu import kb
router = Router()


@router.message(Command("start"))
async def start(mes: Message):
    messag = await mes.answer(
                    "Привет 👋\n"
                    "Я бот, который поможет тебе следить за питанием и калориями.\n"
                    "📸 Отправь мне фото еды — я посчитаю калории.\n"
                    "🏷 Скинь фото этикетки — я распознаю состав и посчитаю всё автоматически.\n"
                    "📊 Веди дневник калорий прямо здесь, и я помогу отслеживать прогресс."
,reply_markup=kb)
    assert mes.from_user is not None
    user_id = mes.from_user.id
    
@router.callback_query(F.data=="back")
async def backk(cal:CallbackQuery):
    await cal.answer('')
    assert cal.message is not None
    await cal.message.answer(
        "Привет 👋\n"
        "Я бот, который поможет тебе следить за питанием и калориями.\n"
        "📸 Отправь мне фото еды — я посчитаю калории.\n"
        "🏷 Скинь фото этикетки — я распознаю состав и посчитаю всё автоматически.\n"
        "📊 Веди дневник калорий прямо здесь, и я помогу отслеживать прогресс.",
        reply_markup=kb
    )