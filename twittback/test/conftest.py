import pytest

import twittback.server


@pytest.fixture()
def app():
    return twittback.server.app
