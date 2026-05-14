"""
Tests for Task 2 — Token Bucket Rate Limiter.
DO NOT MODIFY THIS FILE.
"""

import time
from unittest.mock import patch
from solution import TokenBucketRateLimiter


def make_limiter(capacity=5, refill_rate=1.0):
    return TokenBucketRateLimiter(capacity=capacity, refill_rate=refill_rate)


class TestBasicBehavior:

    def test_first_request_is_allowed(self):
        limiter = make_limiter(capacity=3)
        assert limiter.is_allowed("alice") is True

    def test_requests_within_capacity_all_allowed(self):
        limiter = make_limiter(capacity=3)
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is True

    def test_request_when_empty_is_denied(self):
        limiter = make_limiter(capacity=3)
        limiter.is_allowed("alice")
        limiter.is_allowed("alice")
        limiter.is_allowed("alice")
        assert limiter.is_allowed("alice") is False

    def test_capacity_of_one(self):
        limiter = make_limiter(capacity=1)
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is False


class TestMultipleClients:

    def test_clients_are_tracked_independently(self):
        limiter = make_limiter(capacity=2)
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is True
        assert limiter.is_allowed("alice") is False
        assert limiter.is_allowed("bob")   is True

    def test_new_client_starts_with_full_bucket(self):
        limiter = make_limiter(capacity=3)
        limiter.is_allowed("alice")
        limiter.is_allowed("alice")
        limiter.is_allowed("alice")
        assert limiter.is_allowed("newuser") is True


class TestTokenRefill:

    def test_tokens_refill_over_time(self):
        limiter = make_limiter(capacity=3, refill_rate=1.0)

        with patch("solution.time") as mock_time:
            mock_time.time.return_value = 1000.0
            limiter.is_allowed("alice")
            limiter.is_allowed("alice")
            limiter.is_allowed("alice")
            assert limiter.is_allowed("alice") is False

            mock_time.time.return_value = 1002.0
            assert limiter.is_allowed("alice") is True
            assert limiter.is_allowed("alice") is True
            assert limiter.is_allowed("alice") is False

    def test_tokens_capped_at_capacity(self):
        limiter = make_limiter(capacity=3, refill_rate=1.0)

        with patch("solution.time") as mock_time:
            mock_time.time.return_value = 1000.0
            limiter.is_allowed("alice")

            mock_time.time.return_value = 9999.0
            assert limiter.is_allowed("alice") is True
            assert limiter.is_allowed("alice") is True
            assert limiter.is_allowed("alice") is True
            assert limiter.is_allowed("alice") is False  # capped at 3

    def test_fractional_refill_rate(self):
        limiter = make_limiter(capacity=2, refill_rate=0.5)

        with patch("solution.time") as mock_time:
            mock_time.time.return_value = 1000.0
            limiter.is_allowed("alice")
            limiter.is_allowed("alice")
            assert limiter.is_allowed("alice") is False

            mock_time.time.return_value = 1001.0
            assert limiter.is_allowed("alice") is False  # only 0.5 tokens added

            mock_time.time.return_value = 1002.0
            assert limiter.is_allowed("alice") is True   # 1 full token refilled

    def test_burst_then_slow_requests(self):
        limiter = make_limiter(capacity=3, refill_rate=1.0)

        with patch("solution.time") as mock_time:
            mock_time.time.return_value = 1000.0
            limiter.is_allowed("alice")
            limiter.is_allowed("alice")
            limiter.is_allowed("alice")
            assert limiter.is_allowed("alice") is False

            for i in range(1, 6):
                mock_time.time.return_value = 1000.0 + i
                assert limiter.is_allowed("alice") is True
