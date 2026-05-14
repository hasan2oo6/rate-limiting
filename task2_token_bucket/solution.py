import time


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        # TODO: add your data structures here

    def is_allowed(self, client_id: str) -> bool:
        # TODO: implement this method
        raise NotImplementedError("Implement is_allowed()")
