import datetime
import secrets
import requests

from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Demo credentials — replace with a real user store / hashed passwords in production
DEMO_USERS = {
    "demo@tindog.com": "password123",
}

@app.route("/", methods=["GET"])
def index():
    year = datetime.datetime.now().year
    return render_template("index.html", year=year)


@app.route("/guess/<name>", methods=["GET"])
def guess(name):
    response = requests.get(f"https://api.genderize.io/?name={name}")
    data = response.json()
    return render_template(
        "guess.html",
        name=name,
        gender=data.get("gender", "unknown"),
        probability=data.get("probability", 0),
    )

@app.route("/blogs", methods=["GET"])
def blogs():
    response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
    data = response.json()
    return render_template("blog.html", blogs=data)


@app.route("/blogs/<int:blog_id>", methods=["GET"])
def blog_detail(blog_id):
    response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
    data = response.json()
    blog = next((b for b in data if b["id"] == blog_id), None)
    if blog is None:
        return "Post not found", 404
    return render_template("blog_detail.html", blog=blog)


@app.route("/tindog")
def tindog():
    return render_template("tindog.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if email in DEMO_USERS and DEMO_USERS[email] == password:
            session["user"] = email
            return redirect(url_for("tindog"))

        return render_template("login.html", error="Invalid email or password.", email=email)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
