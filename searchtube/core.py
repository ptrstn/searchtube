import json

import requests

from searchtube.exceptions import NoMoreResultsException
from searchtube.extractors import (
    extract_contents,
    extract_items,
    extract_continuation_token,
    extract_continuation_contents,
    extract_videos,
    extract_search_suggestions,
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
    def _create_base_search_data(hl=None) -> dict:
        """
        :param hl: BCP-47 code that uniquely identifies a human language
        :return: Search data dictionary
        """

        data = {
            "context": {
                "client": {
                    "clientName": SEARCH_CLIENT_NAME,
                    "clientVersion": SEARCH_CLIENT_VERSION,
                },
            },
        }

        if hl:
            data["context"]["client"]["hl"] = hl

        return data

    @staticmethod
    def _create_initial_search_data(query: str, **kwargs) -> dict:
        data = YoutubeSearchSession._create_base_search_data(**kwargs)
        data["query"] = query
        return data

    @staticmethod
    def _create_continuation_search_data(continuation_token: str, **kwargs) -> dict:
        data = YoutubeSearchSession._create_base_search_data(**kwargs)
        data["continuation"] = continuation_token
        return data

    def _perform_search(self, data: dict) -> dict:
        response = self.session.post(url=SEARCH_URL, data=json.dumps(data))
        return response.json()

    def _initialize_search(self, query, **kwargs) -> str:
        print(f"Initializing search for query '{query}'...")
        data = self._create_initial_search_data(query, **kwargs)
        search_json_response = self._perform_search(data)

        contents = extract_contents(search_json_response)
        items = extract_items(contents)
        continuation_token = extract_continuation_token(contents)
        videos = extract_videos(items)

        self.items.extend(items)
        self.videos.extend(videos)

        return continuation_token

    def _continue_search(self, continuation_token, **kwargs) -> str:
        print(f"Continuing search with token {continuation_token[:50]}...")
        data = self._create_continuation_search_data(continuation_token, **kwargs)
        search_json_response = self._perform_search(data)

        contents = extract_continuation_contents(search_json_response)
        items = extract_items(contents)

        if len(items) == 1 and "messageRenderer" in items[0]:
            message = items[0]["messageRenderer"]["text"]["runs"][0]["text"]
            raise NoMoreResultsException(message)

        next_continuation_token = extract_continuation_token(contents)
        videos = extract_videos(items)

        self.items.extend(items)
        self.videos.extend(videos)

        return next_continuation_token

    def search(self, query, limit: int = None, **kwargs):
        assert not limit or limit >= 0, "Limit has to be >= 0"
        continuation_token = self._initialize_search(query, **kwargs)

        while limit and len(self.videos) < limit:
            try:
                continuation_token = self._continue_search(continuation_token, **kwargs)
            except NoMoreResultsException as e:
                print(e)
                break

        self.videos = self.videos[:limit]
        return self.videos


def suggest_search(query: str) -> list:
    url = f"{SUGGEST_BASE_URL}{SUGGEST_PATH}{SUGGEST_PARAMETERS}&q={query}"
    response = requests.get(url)
    suggestions = extract_search_suggestions(response.text)
    return suggestions


def search(query: str, **kwargs):
    search_session = YoutubeSearchSession()
    return search_session.search(query=query, **kwargs)
