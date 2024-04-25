import asyncio

import pandas as pd

from uk_fuel_prices_api import UKFuelPricesApi

api = UKFuelPricesApi()

import json
import subprocess
import datetime


async def main():
    await setup()
    geoJson = formatAsGeoJSON()
    writeJsonToFile(geojson=geoJson)
    gitCommitAndPush()


async def setup():
    await api.get_prices()


def formatAsGeoJSON() -> str:
    geojson = {"type": "FeatureCollection", "name": "UK Fuel Stations", "features": []}

    for _, row in api.stations.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["longitude"], row["latitude"]],
            },
            "properties": {
                "site_id": row["site_id"],
                "brand": row["brand"],
                "address": row["address"],
                "postcode": row["postcode"],
                "last_updated": row["last_updated"],
                "prices": {},
            },
        }

        if row["B7"] > 0:
            feature["properties"]["prices"]["B7"] = row["B7"]

        if row["E5"] > 0:
            feature["properties"]["prices"]["E5"] = row["E5"]

        if row["E10"] > 0:
            feature["properties"]["prices"]["E10"] = row["E10"]

        if row["SDV"] > 0:
            feature["properties"]["prices"]["SDV"] = row["SDV"]

        geojson["features"].append(feature)

    return geojson


def writeJsonToFile(geojson: str):
    f = open("stations.json", "w")

    json.dump(geojson, fp=f)

    f.close()


def gitCommitAndPush():
    commitmsg = (
        "-m Auto commit at "
        + datetime.datetime.now().replace(microsecond=0).isoformat()
    )

    subprocess.run(["git", "stage", "stations.json"])
    subprocess.run(["git", "commit", commitmsg])
    subprocess.run(["git", "push"])


asyncio.run(main())
