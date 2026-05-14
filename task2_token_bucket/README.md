# Task 2 — Token Bucket

## The idea

Each client has a "bucket" that holds tokens.

- The bucket starts **full**
- Each request **consumes 1 token**
- Tokens **refill over time** at a steady rate
- If the bucket is **empty**, the request is denied

```
Bucket capacity: 5 tokens
Refill rate: 1 token per second

t=0s  [T][T][T][T][T]   full — 5 requests allowed
t=0s  [T][T][T][ ][ ]   3 requests made
t=2s  [T][T][T][T][T]   2 seconds passed → 2 tokens refilled (capped at 5)
```

## Why it's better than fixed window

Users who make requests slowly accumulate tokens and can handle a short burst.
This feels natural — like a savings account you can spend down and slowly refill.

---

## Your job

Open `solution.py` and implement the `TokenBucketRateLimiter` class.

### Class interface

```python
limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1.0)

limiter.is_allowed("user_123")  # True or False
```

### Parameters

| Parameter | Meaning |
|-----------|---------|
| `capacity` | Maximum number of tokens the bucket can hold |
| `refill_rate` | Tokens added **per second** (can be a float, e.g. 0.5 = 1 token every 2s) |

### Rules

- Each client has their own independent bucket
- A new client starts with a **full bucket** (`capacity` tokens)
- Each allowed request removes exactly 1 token
- Tokens are added continuously over time at `refill_rate` tokens/second
- Tokens can **never exceed** `capacity`
- A request is denied if the bucket has **fewer than 1 token**

---

## Example

```python
limiter = TokenBucketRateLimiter(capacity=3, refill_rate=1.0)

limiter.is_allowed("alice")  # True  — 2 tokens left
limiter.is_allowed("alice")  # True  — 1 token left
limiter.is_allowed("alice")  # True  — 0 tokens left
limiter.is_allowed("alice")  # False — empty!

# ... 2 seconds pass ...

limiter.is_allowed("alice")  # True  — 2 tokens refilled, 1 used = 1 left
```

---

## Hints

- Store per-client: `tokens` (float) and `last_refill_time` (float from `time.time()`)
- On every request, first calculate how many tokens to add:
  `tokens_to_add = elapsed_seconds * refill_rate`
- Cap tokens at `capacity`: `tokens = min(capacity, tokens + tokens_to_add)`
- Then check if `tokens >= 1` — if yes, subtract 1 and allow
- You do NOT need a background thread — calculate refill lazily on each request
