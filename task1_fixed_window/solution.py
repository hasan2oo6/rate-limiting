import time


class FixedWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # TODO: add your data structures here

    def is_allowed(self, client_id: str) -> bool:
        # TODO: implement this method
        raise NotImplementedError("Implement is_allowed()")
