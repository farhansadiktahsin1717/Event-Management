# Event Management System

A polished Django web application for discovering events, managing categories, organizing users by role, and presenting an event platform with a strong recruiter-friendly UI.

This project includes:

- a public landing page with a hero section, features, contact form, footer, and custom 404 page
- role-based access for `Admin`, `Organizer`, and `Participant`
- event CRUD, category management, profile management, and authentication
- search, filtering, and pagination across major list views
- demo content seeding with generated event posters and profile images

## Highlights

- Public homepage with event discovery and contact section
- Custom logo and responsive navigation
- Email-based account activation on signup
- Console email notifications for contact messages and RSVP confirmations
- Admin dashboard for user roles and group management
- Organizer dashboard for event oversight
- Participant dashboard for personal event activity
- Paginated event, participant, category, and admin user views
- Local SVG demo assets for events and user avatars

## Tech Stack

- Python 3.12+
- Django 6.0.2
- SQLite by default
- Pillow for image support
- `django-tailwind` and `theme` included in project dependencies
- Gunicorn, WhiteNoise, and `psycopg-binary` available for deployment-oriented setups

## Project Structure

```text
Event-Management/
|-- event_management/          # Django project settings, root URLs, 404 handler
|-- events/                    # Event models, views, templates, signals
|-- users/                     # Custom user model, auth flow, profiles, demo seed command
|-- categories/                # Category CRUD and templates
|-- media/                     # Uploaded and generated media assets
|-- requirements.txt
|-- manage.py
```

## Features

### Public Experience

- landing page with hero, highlights, event search, and contact form
- event cards with filtering by keyword, category, and date range
- custom 404 page
- responsive layout and mobile navigation

### Authentication and Users

- custom `User` model with profile picture and phone number
- signup, login, logout, password reset, password change
- email activation workflow on registration
- profile view and edit flow

### Role-Based Access

- `Admin` can manage roles, groups, categories, and participants
- `Organizer` can manage events and categories
- `Participant` can browse events and use the participant dashboard

### Event Management

- create, update, delete, and view events
- image-backed event posters
- category assignment
- event statistics on dashboards

### Demo Data

- reusable management command for groups, users, categories, events, posters, and avatars
- generated SVG event posters in `media/events/`
- generated SVG profile images in `media/profiles/`

## Quick Start

### 1. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Apply migrations

```powershell
python manage.py migrate
```

### 4. Run the development server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Demo Content

Seed the project with sample groups, users, categories, events, and generated media:

```powershell
python manage.py seed_demo_content
```

Seeded demo accounts share this password:

```text
DemoPass123!
```

Example seeded users:

- `admin_demo`
- `lina_organizer`
- `samir_organizer`
- `maya_participant`
- `arif_participant`
- `sara_participant`
- `tanvir_participant`
- `nabila_participant`
- `farhan_participant`

## Media and Email

- Event media is stored in `media/events/`
- Profile media is stored in `media/profiles/`
- Email uses Django's console backend by default, so messages appear in the terminal during development

## Running Tests

```powershell
python manage.py test events users categories
```

The current test suite covers:

- event list pagination
- contact form email flow
- custom 404 rendering
- participant pagination
- category pagination

## Important Note About the Current Database

If you are using the checked-in `db.sqlite3`, there is an existing schema mismatch in the RSVP join table:

- `events_event_participants` still points to `auth_user`
- the project now uses the custom `users_user` model

Because of that, the demo seeder safely skips attaching newly seeded participants to events when it detects the old table structure.

This does **not** stop the app from seeding:

- groups
- users
- categories
- events
- event posters
- profile images

If you want full RSVP integrity for the existing database, the join table should be repaired or recreated.

## Default Configuration

Important settings in [`event_management/settings.py`](./event_management/settings.py):

- `AUTH_USER_MODEL = "users.User"`
- `EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"`
- `MEDIA_ROOT = BASE_DIR / "media"`
- `LOGIN_URL = "users:login"`

## Main Routes

- `/` - public landing page and event browsing
- `/dashboard/` - organizer dashboard
- `/users/dashboard/` - role-based dashboard redirect
- `/users/dashboard/admin/` - admin dashboard
- `/users/dashboard/participant/` - participant dashboard
- `/categories/` - category management
- `/users/participants/` - participant directory

## Why This Project Stands Out

- It is more than a CRUD demo; it has a landing-page experience, role-based flows, and visual polish.
- It includes seedable content and generated media, which makes it easy to demo quickly.
- It shows practical Django skills across auth, custom users, forms, signals, pagination, templates, and management commands.

## Next Improvements

- repair the RSVP join table so new participants can be linked cleanly in the current database
- add export features for CSV or PDF
- switch to PostgreSQL for production deployments
- add test coverage for management commands and role flows

---

Built with Django and designed to present well in portfolios, demos, and recruiter reviews.
