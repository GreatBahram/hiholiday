#!/usr/bin/env python3
import collections
import datetime
import re

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
    MAIN_URL = "http://hiholiday.ir/Flight"

    @property
    def cities(self):
        return (city.title() for city in FLIGHT_CITIES_CODES.keys())

    def code(self, city):
        return FLIGHT_CITIES_CODES.get(city.lower())

    def search_onway(
        self, departure_code, arrival_code, capacity=1, departure_date=None, days=0
    ):
        if departure_date:
            if isinstance(departure_date, str):
                try:
                    departure_date = datetime.datetime.strptime(
                        departure_date, DATE_FMT
                    )
                except Exception:
                    raise ValueError("Invalid Date")
        else:
            departure_date = datetime.datetime.today()
        if days and days < 1:
            raise ValueError("Days cannot be negative")

        departure_date = departure_date + datetime.timedelta(days=days)
        departure_date_str = departure_date.strftime(DATE_FMT)

        route = departure_code + "-" + arrival_code
        url = "/".join([self.MAIN_URL, "oneway", route, departure_date_str, "1"])
        data = self._download(url)
        flights = self._parse(data)
        return (flights, url)

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
            airline, aircraft = self._parse_airline(airline)
            if not airline:
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

    def _parse_airline(self, airline):
        """ Translate airline Persian names to English and return aircraft type."""
        aircraft = None
        airline_translate = {
            "کاسپین ایر": "Caspian Airlines",
            "کارون ایر": "Karun Airlines",
            "ایران آسمان": "Air Aseman Airlines",
            "ایران آسمان": "Aseman Airlines",
            "تابان ایر": "Taban Airlines",
            "ایران ایرتور": "Iran Airtour Airline",
            "ساها ایر": "Saha Airlines",
            "معراج": "Meraj Airlines",
            "زاگرس ایر": "Zagros Airlines",
            "آتا": "ATA Airlines",
            "ماهان ایر": "Mahan Air",
            "وارش": "Varesh Airline",
            "قشم ایر": "Qeshm Airlines",
            "ایران ایر": "Iran Air",
        }
        if airline:
            airline, sep, remainder = airline.partition("(")
            airline = airline.rstrip()
            airline = airline_translate.get(airline, airline)
            airline = " ".join([airline, sep + remainder])

            match = re.search(r"(.*) \((.*)\)", airline)
            if match:
                airline, aircraft = match.groups()
        return (airline, aircraft)
