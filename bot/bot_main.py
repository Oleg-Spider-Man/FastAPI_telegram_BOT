import asyncio

import httpx

from config import BOT_TOKEN
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from keyboard import kb


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.reply("Приветствую! Нажми кнопку", reply_markup=kb.as_markup())


@dp.callback_query(lambda call: call.data == "callback_data")
async def handle_callback(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("напишите артикул")


@dp.message(lambda msg: msg.text.isdigit())
async def receive_artikul(msg: types.Message):
    artikul = msg.text
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8000/api/v1/products", json={"artikul": artikul})
        if response.status_code == 200:
            data = response.json()
            await msg.reply(f"Данные по товару: {data}")
        else:
            await msg.reply("Не удалось получить данные о товаре.")

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
