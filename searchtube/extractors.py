def extract_contents(data: dict):
    return data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
        "sectionListRenderer"
    ]["contents"]


def extract_continuation_contents(data: dict):
    return data["onResponseReceivedCommands"][0]["appendContinuationItemsAction"][
        "continuationItems"
    ]


def extract_items(contents: dict):
    return contents[0]["itemSectionRenderer"]["contents"]


def extract_continuation_token(contents: dict):
    return contents[1]["continuationItemRenderer"]["continuationEndpoint"][
        "continuationCommand"
    ]["token"]
