import asyncio

import pandas as pd

from uk_fuel_prices_api import UKFuelPricesApi
api = UKFuelPricesApi()

async def main():
    await api.get_prices()

    geojDataframe = api.stations.to_dict(orient='records', lines=True)


    print(geojDataframe)

asyncio.run(main())