# django-svelte-ecommerce

A production-ready, modern e-commerce platform built with:

* **Django + Django REST Framework** (backend, API, OAuth2, Railway-ready)
* **SvelteKit** (frontend, SEO friendly, Vercel-ready)
* **PostgreSQL** (Supabase)

## Live Demo

Frontend: [https://django-svelte-ecommerce.vercel.app](https://django-svelte-ecommerce.vercel.app)

Backend: [https://django-svelte-ecommerce-production.up.railway.app](https://django-svelte-ecommerce-production.up.railway.app)

Test user credentials:
Please reach out to me for test user credentials or create your own by using the [registration form](https://django-svelte-ecommerce.vercel.app/register) on the frontend.

<u>*Disclaimer:*</u> This live demo is running on free-tier infrastructure across multiple global regions and providers. As a result, response times may vary and performance is not guaranteed. This environment is intended for testing and evaluation purposes only and *should not be used for production workloads.*

## Monorepo Structure

```
.
├── backend/      # Django project & API backend
├── frontend/     # SvelteKit app (SSR frontend)
```

## Local Development

**Prerequisites:**

* Python 3.10+
* Node.js 18+
* Supabase account

### Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Edit .env file as needed
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data # To seed sample data using Faker library # Optional
```
Open /o/applications/ and add an application. Copy the client id and client secret and replace it in .env file.
client type: ```public``` \
Authorization grant type: ```authorization code``` \
Redirect URI list: 
```
<your-backend-url>/oauth2-redirect.html
<your-frontend-url>/auth/callback
```
Finally, run the server:
```
python manage.py runserver
```

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```


## Deployment

### Backend (Railway)
- Connect your GitHub repo to Railway.
- Choose root directory as `backend`.
- In Railway environment variables, set as per [backend/.env.example](./backend/.env.example):
  - DJANGO_SECRET_KEY
  - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT (Supabase Postgres)
  - CLIENT_ID, CLIENT_SECRET
  - BACKEND_PROD_URL, FRONTEND_PROD_URL
- In Railway Start Command:
  ```
  gunicorn ecomm.wsgi:application
  ```

### Frontend (Vercel)
- Connect your repo to Vercel.
- Choose root directory as `frontend`.
- In Vercel environment variables, set as per [frontend/.env.example](./frontend/.env.example):
  - VITE_BACKEND_BASE_URL
  - VITE_CLIENT_ID
  - VITE_FRONTEND_BASE_URL
- Build command: `npm run build` # This is the default build command
- Output directory: `build` # This is the default output director

### Database (Supabase)
- Use Supabase Postgres in production.
- Provide DB credentials via Railway environment variables above.
- Use the shared pooler connection variables if you're connecting using Railway/Render

---