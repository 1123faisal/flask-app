from flask import Flask, abort, render_template

app = Flask(__name__)


PROJECTS = [
    {
        "slug": "habit-tracker-python-mongodb",
        "title": "Habit tracking app with Python and MongoDB",
        "summary": "A habit tracker focused on streaks, reminders, and consistency analytics.",
        "category": "Python | Web",
        "image": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=1280&q=80",
        "description": [
            "This project helps users build long-term routines by tracking daily habits and visualizing progress over time.",
            "I designed a lightweight Flask backend with MongoDB data storage so users can quickly add habits and log completions from any device.",
            "The app includes streak logic, weekly summaries, and simple accountability features to keep users engaged.",
        ],
        "technologies": ["Python", "Flask", "MongoDB", "Jinja", "HTML", "CSS"],
        "production_url": "#",
    },
    {
        "slug": "personal-finance-react",
        "title": "Personal finance tracking app with React",
        "summary": "A clean dashboard for budgets, monthly trends, and spending insights.",
        "category": "React | JavaScript",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1280&q=80",
        "description": [
            "This app gives users a simple way to see where their money goes and set realistic monthly goals.",
            "I used component-driven React architecture with chart widgets, transaction filters, and category breakouts.",
            "Performance and readability were a priority, so state is organized to keep interactions fast and predictable.",
        ],
        "technologies": ["React", "JavaScript", "Chart.js", "Vite", "CSS Modules"],
        "production_url": "#",
    },
    {
        "slug": "rest-api-docs-postman-swagger",
        "title": "REST API Documentation with Postman and Swagger",
        "summary": "Developer-first API docs with examples, auth guides, and endpoint contracts.",
        "category": "Writing",
        "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1280&q=80",
        "description": [
            "I documented an API ecosystem using both Swagger and Postman collections for better onboarding.",
            "The project focused on clear request/response examples, status code behavior, and authentication flows.",
            "I also created testing collections so teams could validate endpoints quickly before integration.",
        ],
        "technologies": ["OpenAPI", "Swagger", "Postman", "REST", "Markdown"],
        "production_url": "#",
    },
]


def find_project_by_slug(slug: str):
    for project in PROJECTS:
        if project["slug"] == slug:
            return project
    return None


@app.get("/")
def index():
    return render_template("index.html", page_title="Projects", projects=PROJECTS)


@app.get("/about")
def about():
    return render_template("about.html", page_title="About")


@app.get("/contact")
def contact():
    return render_template("contact.html", page_title="Contact")


@app.get("/projects/<slug>")
def detail(slug: str):
    project = find_project_by_slug(slug)
    if not project:
        abort(404)
    return render_template("detail.html", page_title=project["title"], project=project)


if __name__ == "__main__":
    app.run(debug=True)
