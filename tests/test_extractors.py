from searchtube.extractors import extract_search_suggestions, extract_video


def test_extract_search_suggestions():
    response_text = (
        "window.google.ac.h("
        '["peter",['
        '["peter althof",0,[433,131]],'
        '["peter maffay",0,[512,433,131]],'
        '["peter hahn",0,[512,433,131]],'
        '["peter thiel",0,[512,433]],'
        '["peter kraus",0,[512,433]],'
        '["peter mitterrutzner",0,[433,131]],'
        '["peter pan",0,[512]],'
        '["peter weck",0,[512,433]],'
        '["peter falk",0,[512]],'
        '["peter wright",0,[512]],'
        '["peter cornelius",0,[512,433]],'
        '["peter westenthaler",0,[512,433]],'
        '["peter kaiser",0,[512]],'
        '["peter rosegger",0,[512,433]]'
        "],"
        '{"k":1,"q":"uRLqS8vLP31N_ncGuxUXfhBNBYo"}])'
    )

    suggestions = extract_search_suggestions(response_text)

    assert len(suggestions) == 14
    assert suggestions[0] == "peter althof"
    assert suggestions[1] == "peter maffay"
    assert suggestions[13] == "peter rosegger"


def test_extract_video():
    item = {
        "videoRenderer": {
            "videoId": "6abc2FEa2P0",  # video_id
            "title": {
                "runs": [{"text": "A Video title"}],  # title
            },
            "publishedTimeText": {"simpleText": "vor 1 Tag"},  # published_time
            "lengthText": {
                "simpleText": "22:00",  # duration
            },
            "viewCountText": {"simpleText": "7.407 Aufrufe"},  # view_count
            "ownerText": {
                "runs": [
                    {
                        "text": "An author name",  # author
                        "navigationEndpoint": {
                            "commandMetadata": {
                                "webCommandMetadata": {
                                    "url": "/c/TheChannel",  # channel_url
                                }
                            },
                        },
                    }
                ]
            },
        },
    }

    video = extract_video(item)

    assert video["video_id"] == "6abc2FEa2P0"
    assert video["title"] == "A Video title"
    assert video["published_time"] == "vor 1 Tag"
    assert video["duration"] == "22:00"
    assert video["view_count"] == "7.407 Aufrufe"
    assert video["author"] == "An author name"
    assert video["channel_url"] == "/c/TheChannel"


def test_incomplete_extract_video():
    item = {
        "videoRenderer": {
            "videoId": "6abc2FEa2P0",  # video_id
            "title": {
                "runs": [{"text": "A Video title"}],  # title
            },
            "ownerText": {
                "runs": [
                    {
                        "text": "An author name",  # author
                        "navigationEndpoint": {
                            "commandMetadata": {
                                "webCommandMetadata": {
                                    "url": "/c/TheChannel",  # channel_url
                                }
                            },
                        },
                    }
                ]
            },
        },
    }

    video = extract_video(item)

    assert video["video_id"] == "6abc2FEa2P0"
    assert video["title"] == "A Video title"
    assert video["published_time"] is None
    assert video["duration"] is None
    assert video["view_count"] is None
    assert video["author"] == "An author name"
    assert video["channel_url"] == "/c/TheChannel"
