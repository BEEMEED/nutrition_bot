import re
import json
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile
from ml.graphics import photo_cal
from utils.db import get_db, save_db  
from utils.path_utils import get_project_root
import os

router = Router()
def text(message, user_id: str):
    date = datetime.now().strftime("%d.%m")
    pattern = r"(🔥\s*\d+\s*ккал\s*\|\s*Б:\s*[\d.,]+ г\s*\|\s*Ж:\s*[\d.,]+ г\s*\|\s*У:\s*[\d.,]+ г)"
    match = re.search(pattern, message)
    user_id = str(user_id)
    if not match:
        return

    result_line = match.group(1).split('|')
    kkal = int(''.join([x for x in result_line[0] if x.isdigit()]))
    belk = float(''.join([x for x in result_line[1] if x.isdigit() or x == '.']))
    shir = float(''.join([x for x in result_line[2] if x.isdigit() or x == '.']))
    uglev = float(''.join([x for x in result_line[3] if x.isdigit() or x == '.']))
    

    data = get_db()
 


    if user_id not in data:
        data[user_id] = {} 
    if date not in data[user_id]:
        data[user_id][date] = {"kkal": 0, "belk": 0.0, "shir": 0.0, "uglev": 0.0, "water": 0.0}


    data[user_id][date]["kkal"] += kkal
    data[user_id][date]["belk"] += belk
    data[user_id][date]["shir"] += shir
    data[user_id][date]["uglev"] += uglev

    save_db(data)
        

@router.callback_query(F.data == "stats")
async def vivod_stat(query:CallbackQuery,bot:Bot):
    await query.answer('')
    user_id = str(query.from_user.id)
    
    data = get_db()
    date = datetime.now().strftime("%d.%m")
    user_data = data.get(user_id, {}).get(date, {
    "kkal": 0,
    "belk": 0,
    "shir": 0,
    "uglev": 0,
    "water": 0
    })
    
    user_data_dict = data.get(user_id, {})
    all_dates = list(user_data_dict.keys())
    all_kkal = [values.get("kkal", 0) for values in user_data_dict.values()]
        
    photo_cal(days=all_dates,calls=all_kkal,user_id=user_id)
    
    text = (
        f"📊 Статистика за сегодня.\n\n"
        f"💪 {user_data['kkal']}ккал | 🧈 {user_data['belk']}г | "
        f"🥩 {user_data['shir']}г | 🍞 {user_data['uglev']}г\n"
        f"💧 {user_data.get('water', 0)}мл"
    )
    
    photo_patch = get_project_root() / f"pidor_{user_id}.png"
    assert query.message is not None
    try:
        if photo_patch.exists():
            await bot.send_photo(
                chat_id=query.message.chat.id,
                photo=FSInputFile(photo_patch),
                caption=text
            )
    finally:
        if photo_patch.exists():
            photo_patch.unlink()

@router.callback_query(F.data == "water")
async def water(call: CallbackQuery):
    await call.answer()
    user_id = str(call.from_user.id)
    
    data = get_db()
    date = datetime.now().strftime("%d.%m")
    
    if user_id not in data:
        data[user_id] = {}
    if date not in data[user_id]:
        data[user_id][date] = {
            "kkal": 0, "belk": 0, "shir": 0, "uglev": 0, "water": 0
        }
    
    data[user_id][date]["water"] += 250
    save_db(data)
    
    await vivod_stat(call, call.bot)