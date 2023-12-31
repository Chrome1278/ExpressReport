import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.configs.config_reader import config
from src.interface.keyboards.start_keyboard import get_main_keyboard, assets, choiced_assets
from src.interface.keyboards.settings_keyboard import get_settings_keyboard
from src.database import db_handlers
from envs.db_secrets import db_url
from src.utils.report_preparing import get_report_msg
from src.utils.tradingview_parser import get_assets_info_from_tv


engine = create_async_engine(db_url)
async_session = sessionmaker(engine, class_=AsyncSession)
async_session = async_session()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

scheduler_msg = AsyncIOScheduler(timezone="Europe/Moscow")
scheduler_db = AsyncIOScheduler(timezone="Europe/Moscow")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    is_new_user = await db_handlers.is_new_user(user_id)
    if is_new_user:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        if last_name:
            user_name = f"{first_name} {last_name}"
        else:
            user_name = first_name
        for k in assets:
            choiced_assets[k] = False
        subscribes = [value for key, value in choiced_assets.items()]
        await db_handlers.create_new_user(user_id, user_name, subscribes)
        await message.answer(
            f"Приветствуем! Выберите финансовые активы из списка ниже, за которыми хотите следить",
            reply_markup=get_main_keyboard(choiced_assets)
        )
    else:
        current_user_subs = await db_handlers.get_user_subscribes(user_id)
        for k, v in zip(assets, current_user_subs):
            choiced_assets[k] = v
        await message.answer(
            f"Приветствуем! Выберите финансовые активы из списка ниже, за которыми хотите следить",
            reply_markup=get_main_keyboard(choiced_assets)
        )


@dp.message(F.text.lower() == "настройки подписки")
async def cmd_settings(message: types.Message):
    current_user_subs = await db_handlers.get_user_subscribes(message.from_user.id)
    for k, v in zip(assets, current_user_subs):
        choiced_assets[k] = v
    subs = [key for key, value in choiced_assets.items() if value]
    await message.reply(
        f"Сейчас вы подписаны на:\n{', '.join(subs)}",
        reply_markup=get_main_keyboard(choiced_assets)
    )


@dp.message(F.text.lower() == "пояснение аббревиатур активов")
async def cmd_assets_info(message: types.Message):
    text = """
    BTC - Bitcoin (Криптовалюта)
    ETH - Etherium (Криптовалюта)
    SPX - S&P500 (Индекс)
    DJI - Dow Jones (Индекс)
    AAPL - Apple (Технологии)
    MSFT - Microsoft (Технологии)
    """
    await message.reply(
        f"Ниже представлены пояснения к имеющимся аббревиатурам:\n{text}",
        reply_markup=get_main_keyboard(choiced_assets)
    )


async def load_assets_info_at_time():
    scheduler_db.add_job(
        get_assets_info_from_tv,
        trigger='cron',
        hour='9',
        minute='55',
    )
    scheduler_db.start()


async def send_message_to_user_at_time(user_id: int):
    scheduler_msg.add_job(
        bot.send_message,
        trigger='cron',
        hour='10',
        minute='00',
        args=(user_id, await get_report_msg(user_id))
    )
    scheduler_msg.start()


@dp.message()
async def handle_message(message: types.Message):
    text = message.text.lower()
    if text == 'подтвердить выбор!':
        subs = [key for key, value in choiced_assets.items() if value]
        subscribes = [value for key, value in choiced_assets.items()]
        if subs:
            user_id = message.from_user.id
            current_user_subs = await db_handlers.get_user_subscribes(user_id)
            if subscribes != current_user_subs:
                await db_handlers.update_user_subs(user_id, subscribes)
            await message.reply(
                f"Ваши подписки сохранены!\nВы подписались на:\n{', '.join(subs)}",
                reply_markup=get_settings_keyboard()
            )
            if scheduler_msg.state == 0:
                await bot.send_message(
                    message.from_user.id,
                    'Теперь по вашим подпискам будет приходить ежедневный отчёт '
                    'о настроениях по каждому активу. '
                    'Он будет появляться каждый день в 10:00. Не забудьте включить уведомления!'
                )
                await send_message_to_user_at_time(message.from_user.id)
        else:
            await message.reply(
                f"Вы не выбрали ни один из активов.\nВыберите минимум один.",
                reply_markup=get_main_keyboard(choiced_assets)
            )
    else:
        if '  ' in text:
            text = text.split()[1]
        asset = text.upper()
        if asset in choiced_assets:
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


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await load_assets_info_at_time()
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()

