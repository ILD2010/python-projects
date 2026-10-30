# Sentinel Lab

Sentinel Lab is a visual, terminal-based security operations simulator written in Python.
It generates safe, fictional web traffic, analyzes each request, assigns threat scores,
and lets you investigate alerts from an interactive dashboard.

## What you will learn

- How a multi-file Python program is organized
- Dataclasses, enums, type hints, and object-oriented design
- Separating data, business logic, presentation, and persistence
- Rule-based security detection and risk scoring
- JSON file storage, testing, and error handling
- How reusable core logic can later power a desktop application

## Safety

This is a defensive local simulator. It does not scan websites, send network requests,
or attack systems. Every IP address and request is generated locally for training.

## Setup

Python 3.11 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Run the automated tests with:

```bash
python -m unittest discover -s tests -v
```

## Program map

```text
main.py                  Starts the application
sentinel/models.py       Defines requests, alerts, and severity levels
sentinel/generator.py    Produces fictional normal and suspicious traffic
sentinel/rules.py        Contains individual detection rules
sentinel/analyzer.py     Runs rules and calculates alert scores
sentinel/store.py        Saves and loads investigation state
sentinel/dashboard.py    Builds the visual terminal interface
tests/                   Verifies the detection engine
```

## Suggested review order

1. `main.py`
2. `sentinel/models.py`
3. `sentinel/generator.py`
4. `sentinel/rules.py`
5. `sentinel/analyzer.py`
6. `sentinel/store.py`
7. `sentinel/dashboard.py`

