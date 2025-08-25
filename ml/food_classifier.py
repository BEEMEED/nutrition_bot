import base64
from openai import OpenAI
from handlers.stats import text
from aiogram import Router,F
from aiogram.types import callback_query,CallbackQuery
import json
from datetime import datetime
from handlers.stats import vivod_stat
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def image_photo(name,user_id,weight,month):
    image_path = name
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="qwen/qwen2.5-vl-7b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f'''Проанализируй фото и опиши блюдо.  
                                                Оцени калории и БЖУ на {weight} граммах,если если граммовка указана как 0 то 250г.  
                                                Ответь строго по шаблону:

                                                🍽 Результат анализа
                                                [Название блюда] ({weight} г)
                                                🔥[XXX] ккал | Б: [X.X] г | Ж: [X.X] г | У: [X.X] г

                                                🎯 итого:
                                                🔥[XXX] ккал
                                                💪Белки: [X.X] г
                                                🧈Жиры: [X.X] г
                                                🍞Углеводы: [X.X] г

                                                Не добавляй пояснений, комментариев, предупреждений. Только шаблон.'''},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=512
    )
    text(message=response.choices[0].message.content,user_id=user_id)
    return response.choices[0].message.content

def image_etik(name,user_id,month):
    image_path = name
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
    model="Qwen2-VL-7B-Instruct",
    messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f'''Проанализируй фото и опиши блюдо.  
                                                Оцени калории и БЖУ на столько то граммах,если граммовка не указана на упаковке то 250г.  
                                                Ответь строго по шаблону:

                                                🍽 Результат анализа
                                                [Название блюда] (вес г)
                                                🔥[XXX] ккал | Б: [X.X] г | Ж: [X.X] г | У: [X.X] г

                                                🎯 итого:
                                                🔥[XXX] ккал
                                                💪Белки: [X.X] г
                                                🧈Жиры: [X.X] г
                                                🍞Углеводы: [X.X] г

                                                Не добавляй пояснений, комментариев, предупреждений. Только шаблон.'''},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=512
    )
    text(message=response.choices[0].message.content,user_id=user_id)
    return response.choices[0].message.content
router = Router()

    