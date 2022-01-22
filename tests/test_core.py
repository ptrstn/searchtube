from searchtube.core import YoutubeSearchSession

from searchtube import search, suggest_search


def test_create_base_search_data():
    data = YoutubeSearchSession._create_base_search_data()
    assert "context" in data
    assert "client" in data["context"]
    assert "clientName" in data["context"]["client"]
    assert "clientName" in data["context"]["client"]
    assert "hl" not in data["context"]["client"]

    data = YoutubeSearchSession._create_base_search_data(hl="de")
    assert "context" in data
    assert "client" in data["context"]
    assert "clientName" in data["context"]["client"]
    assert "clientName" in data["context"]["client"]
    assert "hl" in data["context"]["client"]
    assert data["context"]["client"]["hl"] == "de"


def test_create_initial_search_data():
    data = YoutubeSearchSession._create_initial_search_data(query="A search query")
    assert data["query"] == "A search query"

    data = YoutubeSearchSession._create_initial_search_data(query="B", hl="fr")
    assert data["query"] == "B"
    assert data["context"]["client"]["hl"] == "fr"


def test_create_continuation_search_data():
    data = YoutubeSearchSession._create_continuation_search_data(
        continuation_token="abcd"
    )
    assert data["continuation"] == "abcd"


def test_youtube_search():
    search_session = YoutubeSearchSession()
    query = "Socrates"
    result = search_session.search(query)
    assert len(result) < 30


def test_youtube_search_5():
    search_session = YoutubeSearchSession()
    query = "Adam and Eve"
    result = search_session.search(query, limit=5)
    assert len(result) == 5


def test_youtube_search_42():
    search_session = YoutubeSearchSession()
    query = "john the baptist"
    result = search_session.search(query, limit=42)
    assert len(result) == 42


def test_youtube_search_no_published_time():
    # Some videos seem to not display the date published:
    # Example:
    # https://www.youtube.com/results?search_query=%22Jesus+Christ!%22+%22Junior+NRB%22

    search_session = YoutubeSearchSession()
    query = '"Jesus Christ!" "Junior NRB"'
    result = search_session.search(query=query, limit=1)

    assert len(result) == 1
    video = result[0]

    assert video["video_id"] == "lS0OkUIllJw"
    assert video["title"] == "Jesus Christ!"
    assert not video["published_time"]
    assert video["duration"] == "3:14"
    assert "/channel/" in video["channel_url"]


def test_suggest_search():
    result = suggest_search("peter")
    assert len(result) > 0
    assert "peter pan" in result


def test_search_unique():
    videos = search("baeda26", limit=30)
    assert len(videos) < 20
