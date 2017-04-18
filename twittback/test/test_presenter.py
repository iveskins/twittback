import arrow

import twittback.presenter

import pytest


@pytest.fixture
def presenter():
    renderer = twittback.presenter.FakeRenderer()
    return twittback.presenter.HTMLPresenter(renderer=renderer)


def test_index(presenter):
    start_timestamp = arrow.get("2017-10-01").timestamp
    end_timestamp = arrow.get("2018-02-02").timestamp

    presenter.gen_index(start_timestamp, end_timestamp)

    year_groups = [
        ("2017", [("10", "October"), ("11", "November"), ("12", "December")]),
        ("2018", [("01", "January"), ("02", "February")]),
    ]
    expected_context = {"year_groups": year_groups}
    assert presenter.renderer.calls == [
        ("index.html", expected_context),
    ]
