import json

import requests

from searchtube.extractors import (
    extract_contents,
    extract_items,
    extract_continuation_token,
    extract_continuation_contents,
)
from searchtube.settings import (
    SUGGEST_BASE_URL,
    SUGGEST_PATH,
    SUGGEST_PARAMETERS,
    SEARCH_CLIENT_NAME,
    SEARCH_CLIENT_VERSION,
    SEARCH_URL,
)


class YoutubeSearchSession:
    def __init__(self):
        self.session = requests.session()
        self.items = []

    @staticmethod
    def _create_initial_search_data(query: str) -> str:
        data = {
            "context": {
                "client": {
                    "clientName": SEARCH_CLIENT_NAME,
                    "clientVersion": SEARCH_CLIENT_VERSION,
                },
            },
            "query": query,
        }
        return json.dumps(data)

    @staticmethod
    def _create_continuation_search_data(continuation_token: str) -> str:
        data = {
            "context": {
                "client": {
                    "clientName": SEARCH_CLIENT_NAME,
                    "clientVersion": SEARCH_CLIENT_VERSION,
                },
            },
            "continuation": continuation_token,
        }

        return json.dumps(data)

    def _perform_search(self, data: str):
        response = self.session.post(url=SEARCH_URL, data=data)
        return response.json()

    def _initialize_search(self, query) -> str:
        data = self._create_initial_search_data(query)
        search_result = self._perform_search(data)

        contents = extract_contents(search_result)
        items = extract_items(contents)
        continuation_token = extract_continuation_token(contents)

        self.items.extend(items)
        return continuation_token

    def _continue_search(self, continuation_token) -> str:
        data = self._create_continuation_search_data(continuation_token)
        search_result = self._perform_search(data)

        contents = extract_continuation_contents(search_result)
        items = extract_items(contents)
        next_continuation_token = extract_continuation_token(contents)

        self.items.extend(items)
        return next_continuation_token

    def search(self, query, limit=20):
        assert limit >= 0, "Limit can't be negative"
        continuation_token = self._initialize_search(query)

        while len(self.videos) < limit:
            continuation_token = self._continue_search(continuation_token)

        self.videos = self.videos[:limit]
        return self.videos

    def print_items(self):
        for idx, item in enumerate(self.items):
            if "videoRenderer" in item:
                video_id = item["videoRenderer"]["videoId"]
                title = item["videoRenderer"]["title"]["runs"][0]["text"]
                print(f"{idx} {video_id} {title}")


def suggest_search(search_text):
    url = f"{SUGGEST_BASE_URL}{SUGGEST_PATH}{SUGGEST_PARAMETERS}&q={search_text}"
    response = requests.get(url)
    return response.text
