# Python Demo — Flask Multi-Page Web App

A multi-page Flask web application built as a portfolio demo. Includes a personal CV page, a blog, a TinDog landing page, and a login system — all with responsive Bootstrap 5 layouts and separate CSS per page.

---

## Pages

| Route | Description |
|---|---|
| `/` | Personal CV — skills, experience, education, projects |
| `/blogs` | Blog post list fetched from a remote JSON API |
| `/blogs/<id>` | Individual blog post detail view |
| `/tindog` | TinDog — a Tinder-style landing page for dogs |
| `/login` | Login form with session management |
| `/logout` | Clears session and redirects to login |
| `/guess/<name>` | Gender guesser using the [Genderize.io](https://genderize.io) API |

---

## Tech Stack

- **Python 3.12+** with **Flask 3.x**
- **Jinja2** template inheritance (`base.html` → page templates)
- **Bootstrap 5.3** (CDN) — responsive grid and components
- **Bootstrap Icons 1.11** (CDN)
- **AOS 2.3** — scroll animations on the TinDog page
- **Google Fonts** — Inter + Playfair Display (CV/Blog), Montserrat + Ubuntu (TinDog/Login)
- **uv** — fast Python package manager

---

## Project Structure

```
python-demo/
├── server.py              # Flask app and all route handlers
├── pyproject.toml         # Project metadata and dependencies
│
├── templates/
│   ├── base.html          # Shared HTML shell (Bootstrap, Icons, blocks)
│   ├── index.html         # CV page
│   ├── blog.html          # Blog list
│   ├── blog_detail.html   # Blog post detail
│   ├── tindog.html        # TinDog landing page
│   ├── login.html         # Login form
│   └── guess.html         # Gender guesser result
│
└── static/
    ├── style.css          # Shared styles (reset, CSS vars, keyframes, footer)
    ├── cv.css             # CV page styles
    ├── blog.css           # Blog list + detail styles
    ├── tindog.css         # TinDog landing page styles
    └── login.css          # Login page styles
```

---

## Getting Started

**Prerequisites:** Python 3.12+ and [uv](https://github.com/astral-sh/uv) installed.

```bash
# Clone the repo
git clone <repo-url>
cd python-demo

# Install dependencies
uv sync

# Run the development server
uv run python server.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Demo Credentials

The login page uses hardcoded demo credentials (replace with a real user store for production):

| Field | Value |
|---|---|
| Email | `demo@tindog.com` |
| Password | `password123` |

---

## External APIs

- **[Genderize.io](https://genderize.io)** — predicts gender from a first name (`/guess/<name>`)
- **[npoint.io](https://www.npoint.io)** — serves the blog post JSON data (`/blogs`)
