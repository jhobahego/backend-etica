# TODO: Implement Role-Based Access Control and Authentication

This document outlines the steps required to implement user roles ("usuario", "admin") and JWT-based authentication using OAuth2 in the FastAPI application.

## 1. Update User Model (`models/Usuario.py`)

-   [x] Add a `rol` field to the `Usuario` model. Use an `Enum` for "usuario" and "admin" roles. Set a default role (e.g., "usuario").
-   [x] Add a `hashed_password` field to store the hashed password.
-   [x] Remove `num_cedula` from `ActualizarUsuario` if it shouldn't be updatable, or adjust logic accordingly. Consider if users should be able to update their own role.
-   [x] Ensure `ActualizarUsuario` allows updating relevant fields, potentially excluding `rol` and `hashed_password` unless handled by specific admin logic.

## 2. Implement Authentication Utilities (`auth.py`)

-   [ ] Create a new file `auth.py`.
-   [ ] Add functions for password hashing (`pwd_context` from `passlib.context`) and verification.
-   [ ] Add functions to create JWT access tokens (`create_access_token` using `jose.jwt`). Include expiration time from `.env`.
-   [ ] Add a function to verify and decode JWT tokens (`verify_token`).
-   [ ] Define `OAuth2PasswordBearer` instance.

## 3. Create Authentication Endpoint (`routes/auth.py`)

-   [ ] Create a new file `routes/auth.py` with an `APIRouter`.
-   [ ] Implement a `/token` (or `/login`) endpoint using `OAuth2PasswordRequestForm`.
    -   [ ] Authenticate the user by comparing the provided password hash with the stored hash.
    -   [ ] If authentication is successful, generate and return a JWT access token.
    -   [ ] Handle authentication failures.
-   [ ] Include this router in `main.py`.

## 4. Implement Authorization Dependencies (`dependencies.py`)

-   [ ] Create a new file `dependencies.py`.
-   [ ] Create a dependency `get_current_user`:
    -   [ ] Takes `token: str = Depends(oauth2_scheme)` (from `auth.py`).
    -   [ ] Decodes the token using `auth.verify_token`.
    -   [ ] Retrieves the user from the database based on the username/ID in the token payload.
    -   [ ] Raises `HTTPException` if the token is invalid or the user doesn't exist.
    -   [ ] Returns the user object.
-   [ ] Create a dependency `require_role(required_roles: List[str])`:
    -   [ ] Takes a list of allowed roles.
    -   [ ] Depends on `current_user: Usuario = Depends(get_current_user)`.
    -   [ ] Checks if `current_user.rol` is in `required_roles`.
    -   [ ] Raises `HTTPException` (403 Forbidden) if the user doesn't have the required role.

## 5. Protect Endpoints (`routes/usuarios.py`)

-   [ ] Modify the `POST /empleados` endpoint:
    -   [ ] Hash the user's password before saving.
    -   [ ] Set the default role to "usuario". Consider if this endpoint should be public or require admin privileges. The prompt implies user self-registration is allowed.
-   [ ] Apply dependencies to protect existing endpoints:
    -   [ ] `GET /empleados`: Add `Depends(require_role(["admin"]))`.
    -   [ ] `GET /empleados/{num_cedula}`:
        -   Add `current_user: Usuario = Depends(get_current_user)`.
        -   Check if `current_user.rol == "admin"` OR if `current_user.num_cedula == num_cedula`. Raise 403 if neither condition is met.
    -   [ ] `PUT /empleados/{usuario_id}`:
        -   Add `current_user: Usuario = Depends(get_current_user)`.
        -   Check if `current_user.rol == "admin"` OR if `str(current_user.usuario_id) == usuario_id`. Raise 403 if neither condition is met.
        -   Prevent users from updating their own `rol` unless explicitly allowed.
    -   [ ] `DELETE /empleados/{usuario_id}`: Add `Depends(require_role(["admin"]))`.

## 6. Seed Initial Admin User

-   [ ] Decide on a strategy to create the first admin user (e.g., a separate script, manual database insertion, a command-line command).
-   [ ] Document this process in `README.md`.

## 7. Update Documentation (`README.md`)

-   [ ] Document the new authentication flow (`/token` endpoint).
-   [ ] Explain the roles and permissions.
-   [ ] Document how to create the initial admin user.

## 8. Testing

-   [ ] Test all endpoints without authentication (should fail except possibly registration).
-   [ ] Test login endpoint with correct and incorrect credentials.
-   [ ] Test all endpoints with a "usuario" token, verifying they can access/modify only their own data and cannot access admin-only endpoints.
-   [ ] Test all endpoints with an "admin" token, verifying they have full access.
