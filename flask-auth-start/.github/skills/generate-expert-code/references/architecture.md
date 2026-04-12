# Architecture Reference — Flask / Python Patterns

## Project Layout

```
app/
├── __init__.py          # Application factory (create_app)
├── config.py            # Config classes (Dev, Test, Production)
├── extensions.py        # db, login_manager, csrf — initialised here, imported everywhere
├── models/
│   ├── user.py
│   └── file.py
├── repositories/
│   ├── user_repository.py
│   └── file_repository.py
├── services/
│   ├── user_service.py
│   └── file_service.py
├── routes/
│   ├── auth.py          # Blueprint: /register, /login, /logout
│   ├── main.py          # Blueprint: /, /secrets
│   └── files.py         # Blueprint: /upload, /download/<id>
├── forms/
│   ├── register_form.py
│   └── login_form.py
├── static/
└── templates/
```

## Application Factory

```python
# app/__init__.py
from flask import Flask
from .extensions import db, login_manager, csrf
from .config import config_by_name

def create_app(config_name: str = 'development') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .routes.auth import auth_bp
    from .routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
```

## Repository Pattern

Keep all SQL in repository classes. Services never import `db` directly.

```python
# app/repositories/user_repository.py
from __future__ import annotations
from typing import Any
from ..extensions import db
from ..models.user import User

class UserRepository:
    def find_by_email(self, email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    def find_by_id(self, user_id: int) -> User | None:
        return User.query.get(user_id)

    def create(self, email: str, password: str, name: str) -> User:
        user = User(email=email, password=password, name=name)
        db.session.add(user)
        db.session.commit()
        return user
```

## Service Layer

```python
# app/services/user_service.py
from __future__ import annotations
from werkzeug.security import generate_password_hash, check_password_hash
from ..repositories.user_repository import UserRepository
from ..models.user import User
from ..exceptions import DuplicateEmailError, InvalidCredentialsError

class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def register(self, email: str, raw_password: str, name: str) -> User:
        if self._repo.find_by_email(email):
            raise DuplicateEmailError(f"Email already registered: {email}")
        hashed = generate_password_hash(raw_password, method='pbkdf2:sha256', salt_length=16)
        return self._repo.create(email=email, password=hashed, name=name)

    def authenticate(self, email: str, raw_password: str) -> User:
        user = self._repo.find_by_email(email)
        if not user or not check_password_hash(user.password, raw_password):
            raise InvalidCredentialsError()
        return user
```

## Blueprint Route (Thin Controller)

```python
# app/routes/auth.py
from __future__ import annotations
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..forms.register_form import RegisterForm
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from ..exceptions import DuplicateEmailError, InvalidCredentialsError

auth_bp = Blueprint('auth', __name__)
_service = UserService(UserRepository())

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = _service.register(form.email.data, form.password.data, form.name.data)
            login_user(user)
            return redirect(url_for('main.secrets'))
        except DuplicateEmailError:
            flash('That email is already registered.', 'danger')
    return render_template('register.html', form=form)
```

## Custom Exceptions

```python
# app/exceptions.py
class AppError(Exception):
    """Base class for all application errors."""

class DuplicateEmailError(AppError):
    pass

class InvalidCredentialsError(AppError):
    pass

class ForbiddenError(AppError):
    pass
```

## SOLID Quick Reference

| Principle | Flask Application |
|-----------|------------------|
| SRP | Routes only handle HTTP; services only handle business logic |
| OCP | Add new features as new Blueprints/services; don't modify existing ones |
| LSP | Subclass models must honour parent constraints |
| ISP | Use narrow service interfaces; don't pass `app` objects into services |
| DIP | Services receive repositories via constructor injection |

## Performance Guidelines

- **Eager-load relationships** to avoid N+1 queries: `User.query.options(joinedload(User.files)).all()`
- **Paginate** large result sets: `User.query.paginate(page=page, per_page=20)`
- **Index** frequently filtered columns: `db.Column(db.String(100), index=True)`
- **Cache** expensive reads with `flask-caching` (at least in-memory for start)
- **Defer** heavy work to a task queue (Celery/RQ) rather than blocking the request
