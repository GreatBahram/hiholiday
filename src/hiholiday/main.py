"""Command Line Interface (CLI) for HiHoliday project."""

import argparse
import datetime
import sys
from difflib import get_close_matches

from hiholiday.__version__ import version
from hiholiday.api import DATE_FMT, HiHoliday


def search(frm, to, date, capacity, days=0, verbose=False):
    """ List oneway flights."""
    hh = HiHoliday()
    flights, url = hh.search_onway(frm, to, capacity, date, days)
    if verbose:
        formatstr = "{:<22s} {:^8s} {:<8s} {:^5s} {:^3} {:<9}"
        headers = formatstr.format(
            "Airline", "AirCraft", "FlightNo", "Time", "Cap", "Price",
        )
    else:
        formatstr = "{:<22s} {:^5} {:^3} {:<9}"
        headers = formatstr.format("Airline", "Time", "Cap", "Price")
    print("-" * len(headers))
    print(headers)
    print("-" * len(headers))
    for f in flights:
        if verbose:
            print(
                formatstr.format(
                    f.airline,
                    f.aircraft,
                    f.flightno,
                    f.time.strftime("%H:%M"),
                    f.capacity,
                    "{:,}".format(int(f.price)),
                )
            )
        else:
            print(
                formatstr.format(
                    f.airline,
                    f.time.strftime("%H:%M"),
                    f.capacity,
                    "{:,}".format(int(f.price)),
                )
            )

    print("-" * len(headers))
    print(f"URL: {url}")


def translate(city=None, similar=True):
    """ Return an IATA code for given city. """
    hh = HiHoliday()
    if similar:
        possible_cities = get_close_matches(city, hh.cities)
        if possible_cities:
            city  = possible_cities[0]
    iata_code = hh.code(city)
    if iata_code:
        print(f"* {city.title()}: {iata_code}")
    else:
        print("Not found", file=sys.stderr)
        raise SystemExit(1)


# The main entry point.
def main():
    parser = argparse.ArgumentParser(
        description="Simple CLI for HiHoliday (airline booking) website."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")

    subparsers = parser.add_subparsers()

    # `search` command
    s = subparsers.add_parser("search", help="Performs a one way search.")
    s.add_argument(
        "frm",
        type=str,
        help="Departure from."
    )
    s.add_argument(
        "to",
        type=str,
        help="Departure from."
    )
    s.add_argument(
        "--date",
        help="Departure date, like: 2019-08-11."
    )
    s.add_argument(
        "--capacity",
        type=int,
        default=1,
        help="Number of travellers."
    )
    s.add_argument(
        "--price",
        type=int,
        help="Maximum flight's price."
    )
    s.add_argument(
        "--days",
        type=int,
        default=0,
        help="Days from now."
    )
    s.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose mode."
    )
    s.set_defaults(op="search")

    # `translate` command
    t = subparsers.add_parser("translate", help="Translate cityname to IATA code.")
    t.add_argument(
        "city",
        type=str,
        help="City name."
    )
    t.add_argument(
        "--no-similar",
        default=True,
        action='store_false',
        help="Prevent it from finding the best “good enough” match."
    )
    t.set_defaults(op="translate")

    if len(sys.argv) < 2:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    if args.op == "search":
        search(args.frm, args.to, args.date, args.capacity, args.days, args.verbose)
    elif args.op == 'translate':
        translate(args.city, args.no_similar)


if __name__ == "__main__":
    main()
