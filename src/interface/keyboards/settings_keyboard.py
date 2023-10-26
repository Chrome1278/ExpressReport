from aiogram import types


def get_settings_keyboard():
    kb = [
        [types.KeyboardButton(text='Настройки подписки')],
    ]
    set_kb = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        is_persistent=False,
    )
    return set_kb
