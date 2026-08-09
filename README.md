# OPES EDGE

OPES EDGE (One Platform for Every Solution) is a practical Express and SQLite platform for community and sustainable-development services.

## Stack

- Node.js and Express
- SQLite with `better-sqlite3`
- EJS-compatible server-rendered HTML views
- Bootstrap and custom CSS
- `express-session` for local session authentication

## Run Locally

1. Install dependencies with `npm install`.
2. Copy `.env.example` to `.env` and set a private `SESSION_SECRET`.
3. Start the server with `npm start`.
4. Open `http://localhost:5000`.

Always open pages through the Express URL above. Files inside `views/` contain EJS templates and must not be opened directly with a static preview or `file://` URL, because that bypasses server-side rendering and displays template tags literally in the browser.

Use `npm run dev` during development and `npm test` for the foundation tests.

## Architecture

- `routes/` defines URL surfaces.
- `controllers/` coordinates requests and views.
- `models/` owns SQLite queries.
- `middleware/` contains sessions, authentication, CSRF, logging, and errors.
- `views/` contains server-rendered pages and shared partials.
- `public/` contains browser assets.
- `config/database.js` is the single SQLite connection and schema owner.

The application remains a single monolith so it stays understandable and achievable for a student engineering project.

## Core Domains

1. Agriculture Management
2. Education
3. Healthcare Services
4. Community Services & Development
5. Energy Management
6. Water Management

Employment and governance routes remain scaffolded extensions and should not take priority over the six core domains.

## Current Foundation Flows

- Public landing page and domain pages
- Registration with validation and hashed passwords
- Login, logout, session regeneration, and protected dashboard access
- Session-backed CSRF protection for state-changing forms
- Health and database status endpoints
- Consistent 404 and server-error pages

The SQLite database is runtime data and is intentionally excluded from source control. Database schema changes belong in `config/database.js` until a migration workflow is needed.
