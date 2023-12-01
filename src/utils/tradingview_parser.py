import asyncio

from tradingview_ta import TA_Handler, Interval

from src.configs.assets_description import assets_description as ad, assets
from src.database.db_handlers import add_new_asset_info


async def get_assets_info_from_tv():
    for asset_name in assets:
        asset_info = ad[asset_name]
        asset_handler = TA_Handler(
            symbol=asset_info['symbol'],
            screener=asset_info['screener'],
            exchange=asset_info['exchange'],
            interval=Interval.INTERVAL_1_DAY,
        )
        asset_trade_info = asset_handler.get_analysis()
        asset_day_summary = asset_trade_info.summary
        asset_date = asset_trade_info.time.date()

        asset_fullday_info = asset_handler.get_indicators()
        asset_open = asset_fullday_info['open']
        asset_close = asset_fullday_info['close']
        asset_low = asset_fullday_info['low']
        asset_high = asset_fullday_info['high']

        asset_update_info = {
            'asset_name': asset_name,
            'n_buy': asset_day_summary['BUY'],
            'n_sell': asset_day_summary['SELL'],
            'n_neutral': asset_day_summary['NEUTRAL'],
            'recommendation': asset_day_summary['RECOMMENDATION'],
            'open_price': asset_open,
            'close_price': asset_close,
            'low_price': asset_low,
            'high_price': asset_high,
            'update_date': asset_date
        }
        await add_new_asset_info(asset_update_info)

#
if __name__ == "__main__":
    asyncio.run(get_assets_info_from_tv())
