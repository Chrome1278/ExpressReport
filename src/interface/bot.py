import asyncio
import logging

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from src.configs.config_reader import config
from src.interface.keyboards.start_keyboard import choiced_assets, get_main_keyboard
from src.interface.keyboards.settings_keyboard import get_settings_keyboard

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Приветствуем! Выберите финансовые активы из списка ниже, за которыми хотите следить",
        reply_markup=get_main_keyboard(choiced_assets)
    )


@dp.message(F.text.lower() != "настройки подписки")
async def handle_message(message: types.Message):
    text = message.text.lower()
    if text == 'подтвердить выбор!':
        subs = [key for key, value in choiced_assets.items() if value]
        if subs:
            await message.reply(
                f"Ваши подписки сохранены!\nВы подписались на:\n{', '.join(subs)}",
                reply_markup=get_settings_keyboard()
            )
        else:
            await message.reply(
                f"Вы не выбрали ни один из активов.\nВыберите минимум один.",
                reply_markup=get_main_keyboard(choiced_assets)
            )
    else:
        if '  ' in text:
            text = text.split()[1]
        asset = text.upper()
        if choiced_assets[asset]:
            choiced_assets[asset] = False
            await message.reply(
                f"Вы отписались от {asset}", reply_markup=get_main_keyboard(choiced_assets)
            )
        else:
            choiced_assets[asset] = True
            await message.reply(
                f"Вы подписались на {asset}", reply_markup=get_main_keyboard(choiced_assets)
            )


@dp.message(F.text.lower() == "настройки подписки")
async def with_puree(message: types.Message):
    subs = [key for key, value in choiced_assets.items() if value]
    await message.reply(
        f"Сейчас вы подписаны на:\n{', '.join(subs)}",
        reply_markup=get_main_keyboard(choiced_assets)
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
