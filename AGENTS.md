# OPES EDGE Development Instructions

## Project Context

OPES EDGE (One Platform for Every Solution) is a student engineering project for a unified community and sustainable-development platform.

Preserve the existing technology direction:

- Node.js with CommonJS modules
- Express for the web server
- SQLite through `better-sqlite3`
- Server-rendered views using the existing EJS configuration
- Bootstrap and the existing custom CSS for the frontend
- MVC-style separation using `routes/`, `controllers/`, `models/`, `middleware/`, `utils/`, `views/`, and `public/`

The application is a single practical monolith. Do not introduce React, MongoDB, ESP32, Arduino, GraphQL, microservices, or other new platforms unless the user explicitly approves the change and the existing architecture genuinely requires it.

The six core OPES EDGE domains are:

1. Agriculture Management
2. Education
3. Healthcare Services
4. Community Services & Development
5. Energy Management
6. Water Management

Employment and governance files exist in the scaffold, but do not expand them ahead of the six core domains without an explicit requirement.

## General Change Rules

- Inspect the nearby implementation, route, model, view, and tests before editing.
- Preserve working behavior and useful existing work.
- Make the smallest focused change that solves the request.
- Do not rewrite the project, replace the architecture, or perform unrelated cleanup.
- Do not create duplicate routes, controllers, models, views, stylesheets, helpers, or page variants.
- Reuse existing modules, layouts, partials, styles, and utilities where appropriate.
- Keep one clear owner for each behavior and data-access responsibility.
- Keep public APIs, URL conventions, database contracts, and user-facing behavior stable unless the task requires a deliberate change.
- Use ASCII by default and match the surrounding file style.
- Do not commit changes or modify unrelated user work.

## Naming and Structure

- Use `camelCase` for JavaScript variables and functions.
- Use `PascalCase` for classes or constructor-like types when needed.
- Use descriptive file names that match the existing suffix conventions, such as `agricultureController.js` and `userModel.js`.
- Keep route definitions in `routes/`, request/response orchestration in `controllers/`, SQL and persistence in `models/`, and cross-cutting behavior in `middleware/`.
- Keep shared browser behavior in `public/js/` and shared styles in the existing CSS files.
- Prefer one model per domain responsibility rather than embedding SQL throughout controllers or routes.
- Use consistent URL prefixes and naming across all six domains.
- Keep authentication and authorization separate from domain-specific business logic.

## Backend and Database

- Use parameterized SQLite statements; never interpolate user input into SQL.
- Validate and normalize input at the request boundary before persistence.
- Hash passwords with a maintained password-hashing library before storing them. Never log or persist plaintext passwords.
- Enforce authentication and role authorization through reusable middleware.
- Do not expose stack traces, SQL statements, secrets, or sensitive user data in responses or logs.
- Treat `.env` values as configuration and provide safe development fallbacks only where appropriate. Never add real secrets to source control.
- Keep database initialization and schema changes explicit, repeatable, and documented.
- Use transactions for related writes that must succeed or fail together.
- Handle expected database errors and return stable user-facing error responses.
- Keep the SQLite database file as runtime data, not source code, unless a task explicitly requires a fixture or migration artifact.

## Views, UI, and Accessibility

- Use the existing server-rendered view approach consistently; do not mix competing rendering strategies without a clear reason.
- Reuse shared navigation, footer, sidebar, and layout components instead of copying markup between pages.
- Keep the six domains visually and behaviorally consistent while allowing domain-specific content.
- Maintain responsive layouts for mobile, tablet, and desktop viewports.
- Use semantic HTML, logical heading order, labels for form controls, keyboard-accessible interactions, visible focus states, and sufficient color contrast.
- Do not rely on color, emoji, hover, or icons alone to communicate meaning.
- Provide meaningful link and button labels, useful image alt text, and accessible error/status messages.
- Preserve stable layouts so loading, validation, and long content do not cause avoidable shifting or overlap.
- Reuse the existing Bootstrap and custom CSS conventions before adding new styling patterns.

## Security and Reliability

- Apply least privilege to authenticated actions and administrative features.
- Protect state-changing requests against CSRF when form workflows are implemented.
- Configure secure, HTTP-only, appropriately scoped cookies for non-development environments.
- Avoid open redirects, unsafe file paths, unrestricted input, and reflected or stored XSS.
- Do not add external services or client dependencies without a concrete project need and explicit approval.
- Keep health and diagnostic endpoints free of sensitive implementation details.
- Add graceful error handling and a consistent 404 response for new route surfaces.

## Documentation and Decisions

- Update `README.md` when setup, commands, routes, roles, database schema, or user workflows change materially.
- Document important architectural decisions and non-obvious tradeoffs near the relevant code or in `docs/`.
- Record database schema changes, authentication assumptions, and domain workflow decisions.
- Keep documentation aligned with the implementation; do not describe planned features as completed.

## Validation Before Completion

Before considering a change complete:

1. Run the narrowest relevant test or executable check.
2. Run the application or targeted route check when server behavior changed.
3. Check affected views at mobile and desktop sizes when UI behavior changed.
4. Check authentication, authorization, validation, and error paths for security-sensitive changes.
5. Run the available project checks and confirm there are no new errors.
6. Review the diff for accidental duplication, unrelated edits, secrets, debug output, and broken links.

If the project lacks a suitable test, add a focused test or state the remaining validation gap clearly. Do not claim a feature is complete when only the happy path has been checked.
