# Testing Reference — pytest Patterns for Flask

## Fixtures (conftest.py)

```python
# tests/conftest.py
from __future__ import annotations
import pytest
from app import create_app
from app.extensions import db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def db(app):
    """Provide a clean DB transaction per test — rolls back after each test."""
    connection = _db.engine.connect()
    transaction = connection.begin()
    _db.session.bind = connection
    yield _db
    _db.session.remove()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def registered_user(db):
    from app.services.user_service import UserService
    from app.repositories.user_repository import UserRepository
    svc = UserService(UserRepository())
    return svc.register(email='test@example.com', raw_password='Passw0rd!', name='Test')
```

## Unit Tests — Service

```python
# tests/unit/test_user_service.py
import pytest
from unittest.mock import MagicMock
from app.services.user_service import UserService
from app.exceptions import DuplicateEmailError, InvalidCredentialsError

@pytest.fixture()
def repo():
    return MagicMock()

@pytest.fixture()
def service(repo):
    return UserService(repo)

class TestRegister:
    def test_creates_user_when_email_is_new(self, service, repo):
        repo.find_by_email.return_value = None
        service.register('new@example.com', 'Passw0rd!', 'Alice')
        repo.create.assert_called_once()

    def test_raises_on_duplicate_email(self, service, repo):
        repo.find_by_email.return_value = MagicMock()  # already exists
        with pytest.raises(DuplicateEmailError):
            service.register('dup@example.com', 'Passw0rd!', 'Alice')

class TestAuthenticate:
    def test_raises_on_wrong_password(self, service, repo):
        from werkzeug.security import generate_password_hash
        user = MagicMock()
        user.password = generate_password_hash('CorrectPw', method='pbkdf2:sha256', salt_length=16)
        repo.find_by_email.return_value = user
        with pytest.raises(InvalidCredentialsError):
            service.authenticate('a@b.com', 'WrongPw')

    def test_raises_on_unknown_email(self, service, repo):
        repo.find_by_email.return_value = None
        with pytest.raises(InvalidCredentialsError):
            service.authenticate('nobody@example.com', 'pw')
```

## Integration Tests — Routes (HTTP Layer)

```python
# tests/integration/test_auth_routes.py
import pytest

class TestRegisterRoute:
    def test_get_renders_form(self, client):
        r = client.get('/register')
        assert r.status_code == 200
        assert b'Register' in r.data

    def test_post_valid_redirects_to_secrets(self, client):
        r = client.post('/register', data={
            'name': 'Alice', 'email': 'alice@example.com',
            'password': 'Passw0rd!',
        }, follow_redirects=True)
        assert r.status_code == 200
        assert b'secrets' in r.data.lower()

    def test_post_duplicate_email_shows_error(self, client, registered_user):
        r = client.post('/register', data={
            'name': 'Bob', 'email': 'test@example.com',
            'password': 'Passw0rd!',
        })
        assert b'already registered' in r.data

class TestLoginRoute:
    def test_correct_credentials_redirects(self, client, registered_user):
        r = client.post('/login', data={
            'email': 'test@example.com', 'password': 'Passw0rd!',
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_wrong_password_shows_error(self, client, registered_user):
        r = client.post('/login', data={
            'email': 'test@example.com', 'password': 'WrongPw',
        })
        assert r.status_code in (200, 401)

class TestProtectedRoutes:
    def test_secrets_requires_login(self, client):
        r = client.get('/secrets', follow_redirects=False)
        assert r.status_code == 302
        assert '/login' in r.headers['Location']
```

## Test Naming Convention

```
tests/
├── conftest.py
├── unit/
│   ├── test_user_service.py
│   └── test_file_service.py
└── integration/
    ├── test_auth_routes.py
    └── test_file_routes.py
```

## pytest.ini / pyproject.toml markers

```toml
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "unit: pure unit tests (no DB, no HTTP)",
    "integration: tests that hit the DB or HTTP layer",
]
```

## Coverage Target

- Service layer: **≥ 90%** branch coverage
- Routes: **≥ 80%** (at minimum happy path + auth failure + invalid input)
- Models: **≥ 70%** (constraint + relationship tests)

Run with: `pytest --cov=app --cov-report=term-missing`
