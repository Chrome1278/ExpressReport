from aiogram import types

assets = ["BTC", "ETH", "GOLD", "BR1!", "SPX", "DJI", "AAPL", "MSFT"]
choiced_assets = {a: False for a in assets}


def get_main_keyboard(user_assets):
    printed_assets = [f'✅  {a}' if user_assets[a] else a for a in assets]
    kb = [
        [types.KeyboardButton(text=asset) for asset in printed_assets[i:i + 2]]
        for i in range(0, len(printed_assets), 2)
    ]
    kb.append([types.KeyboardButton(text='Пояснение аббревиатур активов')])
    kb.append([types.KeyboardButton(text='Подтвердить выбор!')])

    main_kb = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Выберите интересующие инструмент из меню и подтвердите выбор"
    )
    return main_kb
