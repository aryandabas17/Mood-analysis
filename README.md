# Mood Analysis

Real-time AI emotion detection SaaS platform with Next.js frontend and Node.js/Express backend. Face inference runs client-side via face-api.js (TensorFlow.js).

## Project Structure

```
mood_project/
├── backend/          # Express API + MongoDB
├── frontend/         # Next.js 14 app
└── README.md
```

## Quick Start

### 1. AI model weights

Model files are in `frontend/public/models/` (downloaded automatically during setup).

### 2. MongoDB

Copy `backend/.env.example` to `backend/.env` and set `MONGO_URI` to your MongoDB Atlas or local instance:

```
mongodb://127.0.0.1:27017/mood_analysis
```

### 3. Backend

```bash
cd backend
npm install
npm run dev
```

Runs on http://localhost:5001 (port 5000 may be in use on your machine)

**Local dev without MongoDB:** `backend/.env` sets `USE_FILE_DB=true` to persist sessions in `backend/data/sessions.json`. For production, set `USE_FILE_DB=false` and configure `MONGO_URI` for MongoDB Atlas.

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 (Next.js may use 3001 if 3000 is busy)

## Environment Variables

| Service  | Variable              | Description                    |
|----------|-----------------------|--------------------------------|
| Backend  | `MONGO_URI`           | MongoDB connection string      |
| Backend  | `PORT`                | API port (default 5000)        |
| Backend  | `CLIENT_URL`          | CORS origin (default :3000)    |
| Frontend | `NEXT_PUBLIC_API_URL` | Backend API base URL           |

## Production

- **Database:** MongoDB Atlas
- **Backend:** Render / Railway — `npm start`
- **Frontend:** Vercel — set `NEXT_PUBLIC_API_URL` to your deployed API
