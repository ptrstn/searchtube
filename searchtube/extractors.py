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
    published_time = item["videoRenderer"]["publishedTimeText"]["simpleText"]
    duration = item["videoRenderer"]["lengthText"]["simpleText"]
    view_count = item["videoRenderer"]["viewCountText"]["simpleText"]
    author = item["videoRenderer"]["ownerText"]["runs"][0]["text"]
    channel_url = item["videoRenderer"]["ownerText"]["runs"][0]["navigationEndpoint"][
        "commandMetadata"
    ]["webCommandMetadata"]["url"]

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
