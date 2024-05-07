import asyncio
import logging
import sys
from os import getenv
from json import  loads,dumps,JSONDecodeError
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from pydantic import ValidationError

from DataModel import Text
from DbClient import AsyncClient

client = AsyncClient('admin')
load_dotenv()
TOKEN = getenv("TOKEN")
assert TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def command_start_handler(message: Message):
    try:
        list_data = loads(message.text)
        res = await client.get_data(Text.validate(list_data))
        await bot.send_message(message.chat.id,dumps(res))
    except (ValidationError,JSONDecodeError):
        await bot.send_message(message.chat.id,'no data')


async def main() -> None:

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
