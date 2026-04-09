# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (inside venv)
pip install -r requirements.txt

# Run the dev server (port 5001, debug mode)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_foo.py
```

Activate the virtual environment first on Windows: `venv\Scripts\activate`

## Architecture

This is **Spendly**, a Flask expense-tracker web app built as a step-by-step student project. Many routes in `app.py` are stubs with placeholder strings — they are meant to be filled in during later steps of the tutorial.

**Key files:**
- `app.py` — all Flask routes; single-file entry point, runs on port 5001
- `database/db.py` — SQLite helpers (`get_db`, `init_db`, `seed_db`) to be implemented by students in Step 1; uses `row_factory` and foreign-key enforcement
- `templates/base.html` — shared layout (navbar + footer); all pages extend this
- `static/css/style.css` — global styles; `static/css/landing.css` — landing-page-only styles
- `static/js/main.js` — placeholder, students add JS as features are built

**Template system:** Jinja2 with `{% block title %}`, `{% block head %}`, `{% block content %}`, `{% block scripts %}` extension points defined in `base.html`.

**Planned step progression (per inline comments in app.py):**
1. Database setup (`db.py`)
2–3. Auth (register, login, logout)
4. Profile page
5–6. Expense listing/dashboard
7–9. Add, edit, delete expenses

**Currency:** INR (₹) — the app targets Indian users.
