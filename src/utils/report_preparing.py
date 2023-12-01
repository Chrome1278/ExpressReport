from src.configs.assets_description import assets
from src.database import db_handlers


async def get_report_msg(user_id):
    full_report_text = "### ОТЧЁТ ПО ВАШИМ АКТИВАМ ###\n"
    date_in_report = True
    current_user_subs = await db_handlers.get_user_subscribes(user_id)
    choiced_assets = [a for a, a_b in zip(assets, current_user_subs) if a_b]
    for asset in choiced_assets:
        asset_info = await db_handlers.get_last_asset_info(asset)
        n_buy = asset_info.n_buy,
        n_buy = n_buy[0]
        n_sell = asset_info.n_sell,
        n_sell = n_sell[0]
        n_neutral = asset_info.n_neutral,
        n_neutral = n_neutral[0]
        recommendation = asset_info.recommendation,
        recommendation = recommendation[0]
        open_price = asset_info.open_price,
        open_price = open_price[0]
        close_price = asset_info.close_price,
        close_price = close_price[0]
        low_price = asset_info.low_price,
        low_price = low_price[0]
        high_price = asset_info.high_price,
        high_price = high_price[0]

        if date_in_report:
            date_in_report = False
            update_date = asset_info.update_date
            update_date = update_date.strftime("%Y-%m-%d")
            full_report_text += f"! Дата сбора информации: {update_date} !\n\n"

        asset_report = f"--- Инструмент: {asset} ---\n" \
                       f"Цена открытия: {open_price}$\n" \
                       f"Цена закрытия: {close_price}$\n" \
                       f"Минимальная цена за сутки: {low_price}$\n" \
                       f"Максимальная цена за сутки: {high_price}$\n" \
                       f"Количесво рекомендаций к покупке: {n_buy}\n" \
                       f"Количесво рекомендаций к продаже: {n_sell}\n" \
                       f"Количесво нейтральных рекомендаций: {n_neutral}\n" \
                       f"*Итоговая рекомендация: {recommendation}*\n\n"

        full_report_text += asset_report
    return full_report_text
