from searchtube.extractors import extract_search_suggestions


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
