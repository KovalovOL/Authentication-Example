
# 🔐 Authentication via JWT

## 📁 `auth_router`

This module contains 3 endpoints:

* **`register_user`** — Registers a new user and saves them to the database.
* **`login_user`** — Authenticates the user, creates a JWT token, and stores it in a cookie.
* **`get_current_user_via_cookie`** — Retrieves the current user based on the JWT stored in the cookie.

## 🔐 `security.py`

This file contains key security-related functions:

* `hash_password(password: str)`: Hashes a plain password.
* `verify_password(plain: str, hashed: str)`: Verifies a password against its hash.
* `create_access_token(data: dict)`: Generates a JWT token with the given payload.

> 🔒 These are the core functions responsible for password encryption and token generation.

<img src="/docs/security.png">

## ⚙️ `dependencies.py`

This file contains helper functions that are used with FastAPI’s `Depends()` mechanism.
These typically handle tasks like retrieving the current user, managing the database session, etc.

<img src="/docs/dependencies.png"/>
