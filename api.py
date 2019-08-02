#!/usr/bin/env python3
import datetime
import collections

import requests

from bs4 import BeautifulSoup

__all__ = ["HiHoliday"]


FLIGHT_CITIES_CODES = {
    "abadan": "ABD",
    "ahwaz": "AWZ",
    "amesterdam": "AMS",
    "ankara": "ANK",
    "antalia": "AYT",
    "arbil": "EBL",
    "ardebil": "ADU",
    "asalooyeh": "PGU",
    "azmir": "IZM",
    "bojnoord": "BJB",
    "baghdad": "BGW",
    "bakoo": "GYD",
    "bam": "BXR",
    "bandar-Abbas": "BND",
    "bandar-Mahshahr": "MRX",
    "bankook": "BKK",
    "beyroot": "BEY",
    "birjand": "XBJ",
    "booshehr": "BUZ",
    "chabahar": "ZBR",
    "dameshgh": "DAM",
    "dehli": "DEL",
    "denizlii": "DNZ",
    "dezfoul": "DEF",
    "doshanbeh": "DYU",
    "dubai": "DXB",
    "gachsaran": "GCH",
    "gorgan": "GBT",
    "hamedan": "HDM",
    "ilam": "IIL",
    "iranshahr": "IHR",
    "irvan": "EVN",
    "isfehan": "IFN",
    "istanbul": "IST",
    "jiroft": "JYR",
    "kerman": "KER",
    "kermanshah": "KSH",
    "khoram-Abad": "KHD",
    "kish": "KIH",
    "koalalampour": "KUL",
    "lamard": "LFM",
    "lar": "LRR",
    "mashhad": "MHD",
    "masqat": "MCT",
    "najaf": "NJF",
    "noshahr": "NSH",
    "orumieh": "OMH",
    "qeshm": "GSM",
    "rafsanjan": "RJN",
    "ramsar": "RZR",
    "rasht": "RAS",
    "sabzevar": "AFZ",
    "sannandej": "SDG",
    "sari": "SRY",
    "shahre-Kuwait": "KWI",
    "shahrekord": "CQD",
    "sharjeh": "SHJ",
    "shiraz": "SYZ",
    "sirjan": "SYJ",
    "soleymanieh": "ISU",
    "sparta": "ISE",
    "tabriz": "TBZ",
    "tehran": "THR",
    "yasooj": "YES",
    "yazd": "YZD",
    "zabol": "ACZ",
    "zahedan": "ZAH",
    "zanjan": "JWN",
}
DATE_FMT = "%Y-%m-%d"


Flight = collections.namedtuple(
    "Flight", ["airline", "aircraft", "flightno", "time", "capacity", "price"]
)


class HiHoliday:
    MAIN_URL = "http://hiholiday.ir/Flight/"

    @property
    def cities(self):
        return (city.title() for city in FLIGHT_CITIES_CODES.keys())

    def code(self, city):
        return FLIGHT_CITIES_CODES.get(city.lower())

    def search_onway(
        self, departure_code, arrival_code, departure_date=None, capacity=1
    ):
        if departure_date is None:
            departure_date = datetime.datetime.today().strftime(DATE_FMT)
        route = departure_code + "-" + arrival_code
        url = "/".join([self.MAIN_URL, "oneway", route, departure_date, "1"])
        data = self._download(url)
        flights = self._parse(data)
        return flights

    def _download(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            data = ""
        else:
            data = response.text
        return data

    def _parse(self, data):
        soup = BeautifulSoup(data, "lxml")
        rows = soup.select(".flight-row")
        flights = []
        for row in rows:
            info = row.select_one("span")

            airline = info.get("data-sort-airline", "")
            aircraft = info.get("data-aircraft")
            flightno = info.get("data-sort-flightno", "")
            time = info.get("data-sort-time", "")
            capacity = info.get("data-sort-capacity", 0)
            price = info.get("data-sort-price", 0)

            hour, minute = time.split(":")
            time = datetime.time(int(hour), int(minute))
            capacity = int(capacity)

            flights.append(Flight(airline, aircraft, flightno, time, capacity, price))

        return flights
