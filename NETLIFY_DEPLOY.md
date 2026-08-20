# Q-Shield Netlify Deployment

## Frontend build
The Next.js application is in `frontend/` and uses the App Router under `frontend/src/app/`.

Netlify settings:
- Base directory: `frontend`
- Build command: `npm run build`
- Publish directory: `.next`
- Node version: 20

These settings are also stored in the root `netlify.toml`.

## Local test
From the repository root:

```powershell
cd frontend
npm install
npm run build
npm run dev
```

Production test:

```powershell
npm run build
npm run start
```

## Backend
The FastAPI backend is separate and runs on port 8000:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_server.py
```

Backend docs: http://localhost:8000/docs

## Netlify environment variable
After deploying the backend, open Netlify:
Project configuration -> Environment variables

Add:

`NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-DOMAIN/api`

Do not put secrets in the frontend environment. `NEXT_PUBLIC_*` variables are exposed to the browser.

## Important
The frontend build can succeed without the backend, but dashboard, incidents, agents, simulator, and quantum API interactions require a running/deployed FastAPI backend.
