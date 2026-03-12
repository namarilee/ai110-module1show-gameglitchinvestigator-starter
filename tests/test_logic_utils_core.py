import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


@pytest.mark.parametrize(
    "difficulty,expected",
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 100)),
        ("Hard", (1, 50)),
        ("Unknown", (1, 100)),
    ],
)
def test_get_range_for_difficulty(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        (None, (False, None, "Enter a guess.")),
        ("", (False, None, "Enter a guess.")),
        ("abc", (False, None, "That is not a number.")),
        ("42", (True, 42, None)),
        ("42.8", (True, 42, None)),
        (" 7 ", (True, 7, None)),
    ],
)
def test_parse_guess_cases(raw, expected):
    assert parse_guess(raw) == expected


def test_check_guess_win_message():
    outcome, message = check_guess(25, 25)
    assert outcome == "Win"
    assert "Correct" in message


def test_check_guess_with_string_secret_path():
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert "LOWER" in message


@pytest.mark.parametrize(
    "current,outcome,attempt,expected",
    [
        (0, "Win", 1, 80),
        (0, "Win", 20, 10),
        (10, "Too High", 2, 15),
        (10, "Too High", 3, 5),
        (10, "Too Low", 4, 5),
        (10, "Unknown", 4, 10),
    ],
)
def test_update_score_paths(current, outcome, attempt, expected):
    assert update_score(current, outcome, attempt) == expected
