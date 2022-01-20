import argparse

from searchtube import __version__
from searchtube.core import YoutubeSearchSession


def parse_arguments():
    parser = argparse.ArgumentParser(description="YouTube search client")

    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    return parser.parse_args()


def main():
    search_session = YoutubeSearchSession()
    search_session.search("Adam and Eve")
    search_session.print_items()


if __name__ == "__main__":
    main()
