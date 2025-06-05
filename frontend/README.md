# SvelteKit Frontend

Modern, SEO-friendly SvelteKit app for the django-svelte-ecommerce platform.

## Features

* Product/category listing and detail pages (SSR, SEO)
* OAuth2 login (via Django backend)
* Responsive UI (TailwindCSS)
* Ready for deployment on Vercel

## Development

```bash
npm install
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173)

## API Integration

* Configure API base URL in `.env` or via `src/lib/api.js`
* Attach Bearer token (OAuth2) for authenticated requests

## Build & Deploy

```bash
npm run build
```

* Deploy on [Vercel](https://vercel.com/) for best SSR support.

---

**Project structure:**

```
src/
  routes/      # SvelteKit file-based routing
  lib/         # Shared code (API, auth helpers)
  app.html     # HTML shell
```

---