"""Command Line Interface (CLI) for HiHoliday project."""

import sys
import argparse

from hiholiday.api import HiHoliday
from hiholiday.__version__ import version


def search(frm, to, date, capacity, verbose=False):
    """ List oneway flights.
    # TODO:
    [] - add url link at the bottom of the cli.
    [X] - justify columns.
    """
    hh = HiHoliday()
    flights, url = hh.search_onway(frm, to, date, capacity)
    if verbose:
        formatstr = "{:<40s} {:^8s} {:^8s} {:^8s} {:^8} {:^7}"
    else:
        formatstr = "{:<40s} {:^8}"
    headers = formatstr.format(
        "Airline", "AirCraft", "FlightNo", "Time", "Capacity", "Price"
    )
    print("-" * len(headers))
    print(headers)
    print("-" * len(headers))
    for f in flights:
        print(
            formatstr.format(
                f.airline,
                f.aircraft,
                f.flightno,
                f.time.strftime("%H:%M"),
                f.capacity,
                f.price,
            )
        )
    print("-" * len(headers))
    print(f"URL: {url}")


def translate(city=None):
    """
    Return an IATA code for given city.
    [] - add --similar to find out easily.
    """
    hh = HiHoliday()
    formatstr = "{:^9s}"
    iata_code = hh.code(city)
    if iata_code:
        print(formatstr.format("IATA code"))
        print("---------")
        print(formatstr.format(iata_code))
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
    t.set_defaults(op="translate")

    if len(sys.argv) < 2:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    if args.op == "search":
        search(args.frm, args.to, args.date, args.capacity, args.verbose)
    elif args.op == 'translate':
        translate(args.city)


if __name__ == "__main__":
    main()
