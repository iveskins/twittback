import types

import twittback.edit

import pytest


def setup_edit_test(tweet_factory, repository, mock, *, nvim_returncode):
    tweet_1 = tweet_factory.make_tweet(42, "First tweet!", date="2017-07-07")
    tweet_2 = tweet_factory.make_tweet(57, "Second tweet", date="2017-08-02")
    repository.add_tweets([tweet_1, tweet_2])

    spy = types.SimpleNamespace()
    spy.cmd = None

    def fake_run(cmd):
        stub_process = mock.Mock()
        spy.cmd = cmd
        stub_process.returncode = nvim_returncode
        path = cmd[1]
        with open(path, "w") as stream:
            stream.write("changed")
        return stub_process

    mock.patch("subprocess.run", fake_run)
    return spy


def test_edit_happy(tweet_factory, repository, mock):
    spy = setup_edit_test(tweet_factory, repository, mock, nvim_returncode=0)

    twittback.edit.edit(repository, 42)
    assert spy.cmd[0] == "nvim"

    assert repository.tweet_by_id(42).text == "changed"


def test_edit_editor_nonzero_exit(tweet_factory, repository, mock):
    spy = setup_edit_test(tweet_factory, repository, mock, nvim_returncode=1)
    with pytest.raises(SystemExit) as e:
        twittback.edit.edit(repository, 42)

    error_message = e.value.args[0]
    assert "Edit failed" in error_message

    assert repository.tweet_by_id(42).text == "First tweet!"


def test_edit_no_such_id(tweet_factory, repository, mock):
    spy = setup_edit_test(tweet_factory, repository, mock, nvim_returncode=1)

    with pytest.raises(SystemExit) as e:
        twittback.edit.edit(repository, 1001)
    error_message = e.value.args[0]
    assert "No such id" in error_message
    assert "1001" in error_message
