from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from utils.keyboards.main_menu import ScanCB
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType
from ml.food_classifier import image_photo, image_etik
from states.diary_states import wait
from datetime import datetime
import asyncio
from utils.keyboards.main_menu import back

import os
from concurrent.futures import ProcessPoolExecutor

router = Router()


@router.callback_query(ScanCB.filter(F.value == "photo"))
async def photo(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(wait.wait_photo)
    assert call.message is not None
    await call.message.answer("Пришлите фото еды и вес в граммах, для распознования")

@router.callback_query(ScanCB.filter(F.value == "etik"))
async def etiketka(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(wait.wait_et)
    assert call.message is not None
    await call.message.answer("Пришлите этикетку еды и вес в граммах, для распознования")


@router.message(wait.wait_photo, F.content_type == ContentType.PHOTO)
async def photo_Ed(mes: Message, bot: Bot):
    assert mes.photo is not None
    photo = mes.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
   
    destination = f"photo_{file_id}.jpg"
    weight = mes.text
    assert file_path is not None
    photo_data = await bot.download_file(file_path, destination=destination)

    await mes.answer("фото получено")
    assert mes.from_user is not None
    user_id,day_month = mes.from_user.id, datetime.now().strftime("%d.%m")
    
    result = (
        image_photo(name=destination, user_id=user_id, weight=weight,month=day_month)
        or "Не удалось определить блюдо."
    )
    await mes.answer(result, reply_markup=back)
    os.remove(destination)


@router.message(wait.wait_et, F.content_type == ContentType.PHOTO)
async def photo_et(mes: Message, bot: Bot):
    if mes.photo is not None:
        photo = mes.photo[-1]
    else:
        return
    
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = f"J:/h/nutrition_bot/photo_{file_id}.jpg"
    weight = mes.text
    assert file_path is not None
    photo_data = await bot.download_file(file_path, destination=destination)

    assert mes.from_user is not None
    user_id,day_month = mes.from_user.id, datetime.now().strftime("%d.%m")
    
    await mes.answer("фото получено")
    result = (
        image_etik(name=destination, user_id=user_id,month=day_month)
        or "Не удалось определить блюдо."
    )
    await mes.answer(result, reply_markup=back)
    os.remove(destination)
