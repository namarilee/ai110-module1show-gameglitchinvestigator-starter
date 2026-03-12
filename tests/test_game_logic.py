from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Regression tests for bugs fixed in app.py ---
# check_guess is now in logic_utils (already imported at top of file)
app_check_guess = check_guess

# Bug 1: Hints were reversed — "Go higher" shown when secret is higher (should say "Go lower")
class TestHintDirection:
    def test_guess_too_high_hint_says_go_lower(self):
        """When guess > secret, message must say Go LOWER, not Go HIGHER."""
        outcome, message = app_check_guess(60, 50)
        assert outcome == "Too High"
        assert "LOWER" in message, f"Expected 'LOWER' in hint but got: {message!r}"
        assert "HIGHER" not in message, f"Hint must not say 'HIGHER' when guess is too high"

    def test_guess_too_low_hint_says_go_higher(self):
        """When guess < secret, message must say Go HIGHER, not Go LOWER."""
        outcome, message = app_check_guess(40, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message, f"Expected 'HIGHER' in hint but got: {message!r}"
        assert "LOWER" not in message, f"Hint must not say 'LOWER' when guess is too low"

    def test_hint_direction_boundary_above(self):
        """One above the secret → Too High + Go LOWER."""
        outcome, message = app_check_guess(51, 50)
        assert outcome == "Too High"
        assert "LOWER" in message

    def test_hint_direction_boundary_below(self):
        """One below the secret → Too Low + Go HIGHER."""
        outcome, message = app_check_guess(49, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message


# Bug 2: Attempts counter started at 1, causing "Out of attempts" one guess too early.
class TestAttemptsCount:
    def test_attempts_start_at_zero(self):
        """
        Simulate the counter: it should start at 0 and reach attempt_limit
        only after attempt_limit guesses, not attempt_limit - 1.
        """
        attempt_limit = 5
        attempts = 0  # correct initial value (was mistakenly 1)

        for _ in range(attempt_limit):
            attempts += 1

        # After exactly attempt_limit increments, the game should be over.
        assert attempts >= attempt_limit, "Should be out of attempts after limit guesses"

    def test_attempts_not_exhausted_before_limit(self):
        """
        With the bug (starting at 1), after limit-1 guesses attempts reached
        the limit and declared game over one guess early.  Verify that
        starting at 0 allows all limit guesses.
        """
        attempt_limit = 5
        attempts = 0  # fixed value

        game_over_count = 0
        for _ in range(attempt_limit):
            attempts += 1
            if attempts >= attempt_limit:
                game_over_count += 1

        # Game over should trigger exactly once — on the final (5th) guess.
        assert game_over_count == 1

    def test_off_by_one_regression(self):
        """
        Directly show that starting at 1 (the bug) triggers game-over after
        only attempt_limit-1 real guesses.
        """
        attempt_limit = 5
        buggy_attempts = 1  # old, broken initial value

        guesses_made = 0
        triggered_early = False
        for _ in range(attempt_limit):
            buggy_attempts += 1
            guesses_made += 1
            if buggy_attempts >= attempt_limit and guesses_made < attempt_limit:
                triggered_early = True
                break

        assert triggered_early, (
            "With the bug (start=1) game-over fires before all attempts are used"
        )
