from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
class ScanCB(CallbackData, prefix="scan"):
    value: str


kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="по фото", callback_data=ScanCB(value="photo").pack())],
    [InlineKeyboardButton(text="по этикетке", callback_data=ScanCB(value="label").pack())],
    [InlineKeyboardButton(text="статистика за день",callback_data="stats")]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🏠домой",callback_data="back")]
])

