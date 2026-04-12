from __future__ import annotations
import logging
import os

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf.csrf import CSRFProtect

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

# ── Security configuration ─────────────────────────────────────────────────────
# Set SECRET_KEY env var in production; the fallback is for local dev only.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-secret-key-CHANGE-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True   # JS cannot read the session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # mitigates CSRF via cross-site navigation
app.config['WTF_CSRF_ENABLED'] = True           # global CSRF protection on all POST requests

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# ── Flask-Login setup ──────────────────────────────────────────────────────────
login_manager = LoginManager(app)
login_manager.login_view = 'login'          # redirect here when @login_required fails
login_manager.session_protection = 'strong' # regenerates session on every request


# ── Models ─────────────────────────────────────────────────────────────────────
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    # pbkdf2:sha256 hashes can be up to 256 chars
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(1000), nullable=False)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return User.query.get(int(user_id))


# Create tables if they don't exist yet (idempotent)
with app.app_context():
    db.create_all()


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('secrets'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Server-side validation
        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html'), 400

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
            return render_template('register.html'), 400

        # Prevent email enumeration: use a generic redirect instead of revealing
        # whether the email exists, but here we guide the user to log in.
        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'warning')
            return redirect(url_for('login'))

        hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new_user = User(name=name, email=email, password=hashed)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        logger.info("user_registered user_id=%s", new_user.id)
        return redirect(url_for('secrets'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('secrets'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        # Use the same error message for "not found" and "wrong password"
        # to prevent user enumeration (OWASP A07).
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'danger')
            logger.warning("login_failed email_hash=%s", hash(email))
            return render_template('login.html'), 401

        login_user(user)
        logger.info("login_success user_id=%s", user.id)
        return redirect(url_for('secrets'))

    return render_template('login.html')


@app.route('/secrets')
@login_required
def secrets():
    return render_template('secrets.html', name=current_user.name)


@app.route('/logout')
@login_required
def logout():
    logger.info("logout user_id=%s", current_user.id)
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    # send_from_directory protects against path-traversal attacks
    return send_from_directory(
        directory=os.path.join(app.root_path, 'static', 'files'),
        filename='cheat_sheet.pdf',
        as_attachment=True,
    )


if __name__ == "__main__":
    # Never run debug=True in production
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
