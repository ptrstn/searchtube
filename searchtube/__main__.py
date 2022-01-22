import argparse

import pandas

from searchtube import __version__
from searchtube.core import YoutubeSearchSession


def parse_arguments():
    parser = argparse.ArgumentParser(description="YouTube search client")

    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    parser.add_argument("query", help="Search query")

    parser.add_argument("--language", help=" BCP-47 code to set the response language")

    parser.add_argument(
        "--limit",
        type=int,
        help="Limit of the amount of videos in result",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    query = args.query

    kwargs = {}
    if args.limit:
        kwargs["limit"] = args.limit
    if args.language:
        kwargs["hl"] = args.language

    search_session = YoutubeSearchSession()
    result = search_session.search(query=query, **kwargs)
    result_df = pandas.DataFrame(result)
    print(result_df)


if __name__ == "__main__":
    main()
