# Security Reference — OWASP Top 10 for Flask

## A01 — Broken Access Control

```python
# Every protected route
@bp.route('/secrets')
@login_required
def secrets() -> Response: ...

# Verify ownership before returning/modifying a resource
file = File.query.get_or_404(file_id)
if file.user_id != current_user.id:
    abort(403)
```

## A02 — Cryptographic Failures

```python
# Password hashing — always use pbkdf2:sha256 with salt
from werkzeug.security import generate_password_hash, check_password_hash

hashed = generate_password_hash(raw_password, method='pbkdf2:sha256', salt_length=16)
is_valid = check_password_hash(hashed, raw_password)

# Secret key — NEVER hardcode; load from environment
import os
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
```

## A03 — Injection (SQL / Template)

```python
# ✅ Parameterised via ORM
user = User.query.filter_by(email=email).first()

# ❌ Never do this
db.session.execute(f"SELECT * FROM user WHERE email = '{email}'")

# Jinja2 auto-escapes HTML in templates — do not use |safe on user data
```

## A04 — Insecure Design

- Validate business rules **server-side** even if you validate client-side
- Never expose internal IDs in sequential integers where enumeration is a risk — use UUIDs for public-facing resource identifiers
- Enforce rate limits on sensitive actions (login, password reset)

## A05 — Security Misconfiguration

```python
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True          # HTTPS only
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## A07 — Authentication Failures

- Lock or throttle accounts after N failed logins (use `flask-limiter`)
- Invalidate sessions on logout: `logout_user()` + `session.clear()`
- Use `login_manager.session_protection = 'strong'`
- Don't leak whether an email is registered in error messages

## A08 — Software and Data Integrity (File Uploads)

```python
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
@login_required
def upload() -> Response:
    f = request.files.get('file')
    if not f or not allowed_file(f.filename):
        abort(400)
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    ...
```

Store uploads **outside** the `static/` folder to prevent direct URL access.

## A10 — SSRF

- Never fetch URLs from user input without an explicit allowlist of domains
- Use `urllib.parse.urlparse` to validate scheme (`https` only) and hostname against allowlist
