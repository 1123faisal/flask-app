---
name: generate-expert-code
description: 'Generate expert-level Python/Flask web API code. Use when: writing new routes, models, services, blueprints, forms, or any production-grade Python/Flask code. Enforces security (OWASP Top 10), SOLID architecture, performance optimization, observability (structured logging), pytest testing strategy, and strict type safety (type hints + input validation).'
argument-hint: 'Describe the feature, route, model, or service to generate'
---

# Generate Expert-Level Python/Flask Code

## When to Use
- Writing new Flask routes, blueprints, or REST endpoints
- Creating or extending SQLAlchemy models
- Implementing authentication, authorization, or session logic
- Adding form validation (WTForms) or API input handling
- Designing service layer, repository pattern, or utility modules
- Any production Python/Flask code requiring a high quality bar

---

## Procedure

### 1. Analyze the Request
Before writing a single line:
- Map the data flow: **input source → validation → business logic → persistence → response**
- Identify every trust boundary (user input, database results, env vars, file system, external APIs)
- List failure modes: what can go wrong at each step?
- Determine who is allowed to perform the action (auth/authz requirements)

### 2. Choose the Right Architecture Layer

| Concern | Where it lives |
|---------|---------------|
| HTTP routing, request parsing, response shaping | `routes/` (Blueprint) |
| Business rules, orchestration | `services/` |
| Data access, queries | `repositories/` or model class methods |
| DB schema, relationships | `models/` (SQLAlchemy) |
| Input validation / forms | `forms/` (WTForms) or Pydantic schemas |
| Config, secrets | `config.py` + environment variables |

Apply SOLID:
- **S**: Each class/function has one reason to change
- **O**: Extend via new classes, not by modifying existing ones
- **L**: Subtypes behave like their base types
- **I**: Prefer narrow interfaces over fat ones
- **D**: Depend on abstractions; inject dependencies

### 3. Apply Security Controls (see [security.md](./references/security.md))

Run through the OWASP checklist before finalising code:

- **A01 Broken Access Control** — every sensitive route must have `@login_required`; verify resource *ownership* (`resource.user_id == current_user.id`)
- **A02 Cryptographic Failures** — use `generate_password_hash(pw, method='pbkdf2:sha256', salt_length=16)`; load `SECRET_KEY` exclusively from an env var
- **A03 Injection** — use SQLAlchemy ORM or parameterised queries only; never format raw SQL strings
- **A04 Insecure Design** — enforce business rules server-side; never trust client-supplied IDs or flags
- **A05 Security Misconfiguration** — `DEBUG=False` in production; set `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'`
- **A06 Vulnerable Components** — note any library version concerns if relevant
- **A07 Auth Failures** — apply rate limiting on login; use `check_password_hash` in constant time; expire sessions
- **A08 Data Integrity** — validate file type (MIME + extension), size limits, and store outside webroot
- **A10 SSRF** — never fetch user-supplied URLs without an allowlist

### 4. Write the Code

Apply these rules consistently:

```python
# ✅ Route: thin controller, delegates to service
@auth_bp.route('/register', methods=['POST'])
def register() -> Response:
    form = RegisterForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form), 400
    user = user_service.create_user(
        email=form.email.data,
        password=form.password.data,
        name=form.name.data,
    )
    login_user(user)
    return redirect(url_for('main.secrets'))

# ✅ Service: business logic, no HTTP concerns
class UserService:
    def create_user(self, email: str, password: str, name: str) -> User:
        if user_repo.find_by_email(email):
            raise DuplicateEmailError(email)
        hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        return user_repo.create(email=email, password=hashed, name=name)

# ✅ Repository: data access only
class UserRepository:
    def find_by_email(self, email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    def create(self, **kwargs: Any) -> User:
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user
```

### 5. Add Type Annotations

- Annotate all function signatures: parameters **and** return types
- Use `from __future__ import annotations` at the top of each module (deferred evaluation)
- Use `X | None` instead of `Optional[X]` (Python 3.10+ union syntax)
- Use `TypeAlias` for complex repeated types
- Avoid `Any` unless unavoidable; prefer `object` or a typed `Protocol`

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Response
```

### 6. Add Observability

- Use structured logging (key=value pairs) so logs are machine-parseable
- Log at the correct level: `DEBUG` for internals, `INFO` for significant events, `WARNING` for recoverable issues, `ERROR` for failures
- Never log passwords, tokens, or PII
- Include a correlation/request ID on every log line when feasible

```python
import logging
logger = logging.getLogger(__name__)

# ✅ Structured, no PII
logger.info("user_registered email_hash=%s", hash(email))
logger.warning("login_failed email_hash=%s attempts=%d", hash(email), attempts)
logger.error("db_commit_failed error=%s", exc, exc_info=True)
```

### 7. Suggest Tests (see [testing.md](./references/testing.md))

For every feature generated, immediately outline the test cases:

| Scenario | Type | pytest marker |
|----------|------|---------------|
| Happy path | Unit | `@pytest.mark.unit` |
| Invalid inputs | Unit | `@pytest.mark.unit` |
| Auth/access requirements | Integration | `@pytest.mark.integration` |
| Edge cases / boundaries | Unit | `@pytest.mark.unit` |
| Full HTTP round-trip | Integration | `@pytest.mark.integration` |

---

## Code Quality Checklist

Before outputting code, verify:

- [ ] No hardcoded secrets or credentials
- [ ] All user inputs validated before use
- [ ] Ownership checks on every resource access
- [ ] No raw SQL strings
- [ ] All functions have type annotations
- [ ] Logging added at boundaries (entry, error, significant state change)
- [ ] Single responsibility per function / class
- [ ] Database session errors handled; session not left dirty
- [ ] File paths sanitised with `werkzeug.utils.secure_filename`
- [ ] `SECRET_KEY` and DB URI read from `os.environ` / config class, not hardcoded

---

## Configuration Pattern

Always recommend loading config from environment variables:

```python
import os

class ProductionConfig:
    SECRET_KEY: str = os.environ['SECRET_KEY']          # crash-fast if missing
    SQLALCHEMY_DATABASE_URI: str = os.environ['DATABASE_URL']
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Lax'
    DEBUG: bool = False
    TESTING: bool = False
```

---

## References

- [Security checklist](./references/security.md)
- [Architecture patterns](./references/architecture.md)
- [Testing patterns](./references/testing.md)
