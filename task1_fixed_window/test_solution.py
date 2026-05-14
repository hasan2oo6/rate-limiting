"""
Tests for Task 1 — Fixed Window Rate Limiter.
DO NOT MODIFY THIS FILE.
"""

import time
from unittest.mock import patch
from solution import FixedWindowRateLimiter


def make_limiter(max_requests=5, window_seconds=60):
    return FixedWindowRateLimiter(max_requests=max_requests, window_seconds=window_seconds)


class TestBasicBehavior:

    def test_first_request_is_allowed(self):
        limiter = make_limiter(max_requests=3)
        assert limiter.is_allowed("alice") is True

    def test_requests_within_limit_are_all_allowed(self):
        limiter = make_limiter(max_requests=3)
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is True

    def test_request_over_limit_is_denied(self):
        limiter = make_limiter(max_requests=3)
        limiter.is_allowed("alice")
        limiter.is_allowed("alice")
        limiter.is_allowed("alice")
        assert limiter.is_allowed("alice") is False

    def test_limit_of_one(self):
        limiter = make_limiter(max_requests=1)
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is False


class TestMultipleClients:

    def test_clients_are_tracked_independently(self):
        limiter = make_limiter(max_requests=2)
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is False
        assert limiter.is_allowed("bob")   is True
        assert limiter.is_allowed("bob")   is True
        assert limiter.is_allowed("bob")   is False

    def test_new_client_always_starts_fresh(self):
        limiter = make_limiter(max_requests=3)
        for _ in range(3):
            limiter.is_allowed("alice")
        assert limiter.is_allowed("newuser") is True


class TestWindowReset:

    def test_counter_resets_after_window_expires(self):
        limiter = make_limiter(max_requests=2, window_seconds=60)

        with patch("solution.time") as mock_time:
            mock_time.time.return_value = 1000.0
            limiter.is_allowed("alice")
            limiter.is_allowed("alice")
            assert limiter.is_allowed("alice") is False

            mock_time.time.return_value = 1060.0
            assert limiter.is_allowed("alice") is True
            assert limiter.is_allowed("alice") is True
            assert limiter.is_allowed("alice") is False

    def test_partial_window_does_not_reset(self):
        limiter = make_limiter(max_requests=2, window_seconds=60)

        with patch("solution.time") as mock_time:
            mock_time.time.return_value = 960.0
            limiter.is_allowed("alice")
            limiter.is_allowed("alice")

            mock_time.time.return_value = 990.0
            assert limiter.is_allowed("alice") is False

    def test_multiple_window_cycles(self):
        limiter = make_limiter(max_requests=1, window_seconds=10)

        with patch("solution.time") as mock_time:
            for window in range(4):
                mock_time.time.return_value = float(window * 10)
                assert limiter.is_allowed("alice") is True
                assert limiter.is_allowed("alice") is False
