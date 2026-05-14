# Task 1 — Fixed Window Counter

## The idea

Divide time into fixed blocks (windows) of N seconds.
Each client is allowed at most `max_requests` requests per window.
When the window ends, the counter resets to zero.

```
Window 1 (0s–59s)    Window 2 (60s–119s)
┌────────────────┐   ┌────────────────┐
│  requests: 8   │   │  requests: 0   │  ← resets!
│  limit: 10     │   │  limit: 10     │
└────────────────┘   └────────────────┘
```

## The boundary problem (bonus understanding)

A user can send 10 requests at 0:59 and 10 more at 1:00 — that is 20 in 2 seconds
even though the limit is 10/minute. This is the known weakness of fixed window.
You do NOT need to fix this — just implement the basic version.

---

## Your job

Open `solution.py` and implement the `FixedWindowRateLimiter` class.

### Class interface

```python
limiter = FixedWindowRateLimiter(max_requests=5, window_seconds=60)

limiter.is_allowed("user_123")  # True or False
```

### Rules

- Each `client_id` is tracked **independently**
- A request is **allowed** if the client has made fewer than `max_requests` in the current window
- The window is based on **wall clock time** — use `time.time()`
- When a new window starts, the counter resets automatically

---

## Example

```python
limiter = FixedWindowRateLimiter(max_requests=3, window_seconds=60)

limiter.is_allowed("alice")  # True  (1st request)
limiter.is_allowed("alice")  # True  (2nd request)
limiter.is_allowed("alice")  # True  (3rd request)
limiter.is_allowed("alice")  # False (over limit)

limiter.is_allowed("bob")    # True  (bob has his own counter)
```

---

## Hints

- Store a dictionary mapping `client_id` → `(count, window_start_time)`
- To check which window you're in: `int(time.time() / window_seconds)`
- If the window has changed since last request, reset the counter to 0
