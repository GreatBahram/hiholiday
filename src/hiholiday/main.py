import sys
import argparse

from hiholiday.api import HiHoliday
from hiholiday.__version__ import version

def main():
    parser = argparse.ArgumentParser(
        description='Simple CLI for HiHoliday (airplane booking) website.',
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version}"
    )

    if len(sys.argv) < 2:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()


if __name__ == '__main__':
    main()
