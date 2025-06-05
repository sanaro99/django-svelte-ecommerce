# django-svelte-ecommerce

A production-ready, modern e-commerce platform built with:

* **Django + Django REST Framework** (API backend, OAuth2, PostgreSQL)
* **SvelteKit** (frontend, SSR, SEO, Vercel-ready)
* **Docker Compose** (for orchestration and local dev)

## Monorepo Structure

```
.
├── backend/      # Django project & API backend
├── frontend/     # SvelteKit app (SSR frontend)
├── docker-compose.yml
```

## Local Development

**Prerequisites:**

* Python 3.10+
* Node.js 18+
* Docker & Docker Compose (for DB/containers)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Edit as needed
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### With Docker Compose

```bash
docker-compose up --build
```

## Deployment

* Backend: Deploy Django to your preferred host (supports Gunicorn/Uvicorn, Postgres)
* Frontend: Deploy SvelteKit via Vercel (recommended) or any Node host

---