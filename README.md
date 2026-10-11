# Portfolio

The portfolio is a React single page app. Its profile, projects, skills, and experience are defined in `frontend/src/App.jsx`, so browsing pages does not request portfolio data from the server. Django serves the React app shell for direct URLs and provides one API endpoint for sending contact form email.

## Run locally

Install the dependencies and start Django:

```sh
pip install -r requirements.txt
python manage.py runserver
```

For frontend development, run Vite in a second terminal:

```sh
cd frontend
npm install
npm run dev
```

Vite proxies only `/api/` to Django. The React router handles page changes in the browser; Django's catch-all serves the app shell when a page URL is opened directly.

## Contact email

The only backend operation is `POST /api/contact/`. Copy `.env.example` to `.env`, then replace its example `SECRET_KEY`, host, recipient, and SMTP values with your own. Django loads `.env` with `python-dotenv`; process environment variables take precedence. `CONTACT_EMAIL` is the inbox that receives submissions. Without SMTP configuration, Django uses the console email backend for local development. For SMTP, port 465 usually uses `EMAIL_USE_SSL=True` and `EMAIL_USE_TLS=False`; port 587 usually uses `EMAIL_USE_TLS=True` and `EMAIL_USE_SSL=False`.

The endpoint accepts JSON with `name`, `email`, `subject`, and `message`. It validates the fields and emails the submission without storing it in a database.

## Build frontend assets

```sh
cd frontend
npm run build
```

Vite writes the production assets to `static/frontend/`, which Django references in `templates/index.html`.
