from aiogram import types


assets = ["BTC", "ETH", "GOLD", "OIL"]

choiced_assets = { a: False for a in assets }  # В будущем значение будет браться из БД


def get_main_keyboard(choiced_assets):
    printed_assets = [f'✅  {a}' if choiced_assets[a] else a for a in assets]
    kb = [
        [types.KeyboardButton(text=asset) for asset in printed_assets],
        [types.KeyboardButton(text='Подтвердить выбор!')],
    ]
    main_kb = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Выберите интересующие инструмент из меню и подтвердите выбор"
    )
    return main_kb

