# Rate Limiting Systems — Python Assignment

In this assignment you will implement two classic rate limiting algorithms from scratch using Python.

## What is rate limiting?

Rate limiting controls how many requests a client can make in a given time window.
It protects servers from being overwhelmed and ensures fair access for all users.

---

## Tasks

| Task | Algorithm | Folder |
|------|-----------|--------|
| 1 | Fixed Window Counter | `task1_fixed_window/` |
| 2 | Token Bucket | `task2_token_bucket/` |

Each folder contains:
- `solution.py` — **this is the file you edit**
- `test_solution.py` — tests (do not modify)
- `README.md` — detailed instructions for that task

---

## Setup

```bash
# Make sure you have Python 3.8+
python --version

# Install pytest
pip install pytest

# Run all tests
pytest

# Run tests for one task only
pytest task1_fixed_window/
pytest task2_token_bucket/
```

---

## How to submit

1. Fill in your solution in each `solution.py` file
2. Make sure **all tests pass** with `pytest`
3. Push your code to GitHub

---

## Grading

- Each passing test = points
- All tests green = full marks
- Partial credit is given for partially passing tests

---

## Rules

- You may **not** modify any `test_solution.py` file
- You may **not** use any external libraries — only the Python standard library
- Each task must be solved independently
