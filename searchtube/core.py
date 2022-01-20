import json

import requests

from searchtube.extractors import (
    extract_contents,
    extract_items,
    extract_continuation_token,
    extract_continuation_contents,
    extract_videos,
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
        self.videos = []

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
        print(f"Initializing search for query '{query}'...")
        data = self._create_initial_search_data(query)
        search_result = self._perform_search(data)

        contents = extract_contents(search_result)
        items = extract_items(contents)
        continuation_token = extract_continuation_token(contents)
        videos = extract_videos(items)

        self.items.extend(items)
        self.videos.extend(videos)

        return continuation_token

    def _continue_search(self, continuation_token) -> str:
        print(f"Continuing search with token {continuation_token[:50]}...")
        data = self._create_continuation_search_data(continuation_token)
        search_result = self._perform_search(data)

        contents = extract_continuation_contents(search_result)
        items = extract_items(contents)
        next_continuation_token = extract_continuation_token(contents)
        videos = extract_videos(items)

        self.items.extend(items)
        self.videos.extend(videos)

        return next_continuation_token

    def search(self, query, limit=20):
        assert limit >= 0, "Limit can't be negative"
        continuation_token = self._initialize_search(query)

        while len(self.videos) < limit:
            continuation_token = self._continue_search(continuation_token)

        self.videos = self.videos[:limit]
        return self.videos


def suggest_search(search_text):
    url = f"{SUGGEST_BASE_URL}{SUGGEST_PATH}{SUGGEST_PARAMETERS}&q={search_text}"
    response = requests.get(url)
    return response.text
