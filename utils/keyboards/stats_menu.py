from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

kb_stat = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🏠назад",callback_data="back")],
    [InlineKeyboardButton(text="+250ml💧",callback_data="water")]
])