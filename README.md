# User-Authentication-App

A terminal-based user registration and login system written in Python, with email OTP verification, bcrypt password hashing, and a MySQL backend.

## Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Security](#security)
- [Limitations](#limitations)
- [License](#license)

## Features
- Account registration with name and email format validation
- Email-based OTP verification on signup — a 6-digit code, valid for 3 minutes, with a resend option if it expires or is entered incorrectly
- Polished HTML (plus plain-text fallback) verification email
- Passwords hashed with bcrypt (cost factor 12) — never stored in plain text
- Password confirmation on signup, checked with a constant-time comparison
- Login verified against the stored bcrypt hash, with a single generic error message covering both a wrong password and an unregistered email
- All configuration centralized in `config.py`, loaded from a `.env` file
- Modular design — auth, database, email, and OTP logic each live in their own module

## How It Works

**Registration**
1. Choose `REGISTER` at the prompt
2. Enter a name and email (email format is checked with a regex)
3. A 6-digit OTP is emailed to that address, valid for 3 minutes
4. Enter the OTP — an incorrect or expired code can be resent
5. Once verified, set and confirm a password
6. The account is created with the password stored as a bcrypt hash

**Login**
1. Choose `LOGIN` at the prompt
2. Enter your email and password
3. The entered password is checked against the stored hash with `bcrypt.checkpw`
4. A wrong password and an unregistered email both return the same message, so a login attempt can't be used to find out which emails are registered

## Tech Stack
| Purpose | Library |
|---|---|
| Password hashing | `bcrypt` |
| Database | `mysql-connector-python` (MySQL) |
| Email delivery | `smtplib` (standard library) |
| Config / secrets loading | `python-dotenv` |
| OTP generation & secure comparisons | `secrets` (standard library) |
| Masked password input | `stdiomask` |
| Timed OTP input | `inputimeout` |

## Project Structure
```
.
├── main.py            # Entry point — orchestrates the register/login flow
├── auth.py            # Input prompts, password hashing/validation, email format check
├── database.py        # MySQL connection and queries
├── email_service.py   # Builds and sends the OTP email
├── otp.py              # OTP generation, timed input, verification
├── config.py           # Loads and exposes all environment variables
└── .env                # Local secrets (not committed)
```

## Prerequisites
- Python 3.8+
- A running MySQL server you can create a database and table in
- An email account with SMTP access (e.g., Gmail with an [app password](https://support.google.com/accounts/answer/185833) — regular account passwords won't work if 2-Step Verification is on)

## Installation
```bash
git clone <https://github.com/HerinP/User-Authenticator-App>
cd <repository-folder>

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install bcrypt mysql-connector-python python-dotenv stdiomask inputimeout
```

## Configuration
Create a `.env` file in the project root:
```env
# Database
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASS=your_mysql_password
DB_NAME=authenticate_app

# SMTP (used to send the OTP email)
SERVER_HOST=smtp.gmail.com
SERVER_PORT=587
SCRIPT_EMAIL=your_email@gmail.com
SCRIPT_EMAIL_PASS=your_app_password
```
`DB_NAME` can be whatever you'd like to call the database — `authenticate_app` above is just an example. `SERVER_PORT=587` matches the code's use of `starttls()`; don't use port 465 (implicit SSL) without also changing the connection code. Add `.env` to `.gitignore` so it's never committed.

## Database Setup
The app expects a `user` table with `name`, `email`, and `password_hash` columns, inferred from the queries in `database.py`:
```sql
CREATE DATABASE IF NOT EXISTS authenticate_app;
USE authenticate_app;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);
```
`email` is marked `UNIQUE` so duplicate accounts can't slip in at the database level, and `password_hash` is sized to exactly fit a bcrypt hash, which is always 60 characters. Adjust to match your actual schema if it differs.

## Usage
```bash
python main.py
```
Then follow the prompts to register a new account or log in to an existing one.

## Security
A few deliberate choices worth calling out:
- Passwords are hashed with **bcrypt** (cost factor 12), never stored in plain text
- OTPs are generated with `secrets.randbelow`, a cryptographically secure generator, not `random`
- OTP and password-confirmation checks use `secrets.compare_digest` for constant-time comparison, avoiding timing attacks
- OTPs expire after 3 minutes, limiting the window for guessing
- Database queries are parameterized (`%s` placeholders) — no SQL-injection surface
- Credentials are loaded from environment variables via `python-dotenv`, never hardcoded in source

## Limitations
- CLI only — no web or GUI interface
- MySQL-specific — `database.py` is written directly against `mysql-connector-python`, so switching databases means rewriting that module
- No password reset or account recovery flow
- No login rate-limiting — repeated password guesses against an account aren't throttled (OTP entry is self-limiting, since a wrong guess requires a freshly emailed code)
- No password strength requirements — any non-empty password is accepted
- Registration reveals whether an email is already registered (login does not have this issue)
- No account management — no way to update an email, change a password, or delete an account after signup
- Requires live MySQL and SMTP access to run — no offline or demo mode

## License
This project doesn't currently specify a license.
