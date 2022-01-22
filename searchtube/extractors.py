import re


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


def extract_video(item: dict):
    video_id = item["videoRenderer"]["videoId"]
    title = item["videoRenderer"]["title"]["runs"][0]["text"]
    author = item["videoRenderer"]["ownerText"]["runs"][0]["text"]
    channel_url = item["videoRenderer"]["ownerText"]["runs"][0]["navigationEndpoint"][
        "commandMetadata"
    ]["webCommandMetadata"]["url"]

    try:
        published_time = item["videoRenderer"]["publishedTimeText"]["simpleText"]
    except KeyError:
        # Some videos do not contain a published time
        # Example query: "Jesus Christ" + "Junior NRB"
        published_time = None

    try:
        view_count = item["videoRenderer"]["viewCountText"]["simpleText"]
    except KeyError:
        # Scheduled videos do not have a view count yet
        view_count = None

    try:
        duration = item["videoRenderer"]["lengthText"]["simpleText"]
    except KeyError:
        # Live or scheduled videos do not have a duration
        duration = None

    return {
        "video_id": video_id,
        "title": title,
        "published_time": published_time,
        "duration": duration,
        "view_count": view_count,
        "author": author,
        "channel_url": channel_url,
    }


def extract_videos(items: list):
    return [extract_video(item) for item in items if "videoRenderer" in item]


def extract_search_suggestions(response_text: str) -> list:
    result = re.findall(r"\(.*?\)", response_text)
    _, suggestions, _ = eval(result[0])
    return [item[0] for item in suggestions]
