"""Command Line Interface (CLI) for HiHoliday project."""

import sys
import argparse

from hiholiday.api import HiHoliday
from hiholiday.__version__ import version


def search(frm, to, date, capacity, verbose=False):
    """ List oneway flights.
    # TODO:
    [] - add url link at the bottom of the cli.
    [] - justify columns.
    """
    hh = HiHoliday()
    flights = hh.search_onway(frm, to, date, capacity)
    if verbose:
        formatstr = "{} {} {} {} {} {}"
    else:
        formatstr = "{} {}"
    print(formatstr.format("Airline", "AirCraft", "FlightNo", "Time", "Capacity", "Price"))
    print(formatstr.format("-------", "--------", "--------", "----", "--------", "-----"))
    for f in flights:
        print(formatstr.format(
            f.airline, f.aircraft, f.flightno, f.time, f.capacity, f.price))


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

    if len(sys.argv) < 2:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    if args.op == "search":
        search(args.frm, args.to, args.date, args.capacity, args.verbose)


if __name__ == "__main__":
    main()
