# Mood Analysis

Real-time AI emotion detection web application with a Next.js frontend and Node.js/Express backend. Facial emotion inference runs **entirely in the browser** using [face-api.js](https://github.com/justadudewhohacks/face-api.js) and TensorFlow.js for low latency and minimal server compute.

## Features

- Live webcam face detection and emotion classification (happy, sad, angry, neutral, fear, surprise, disgust)
- Session-based emotion logging with confidence scores
- Dashboard with charts, session stats, and dominant mood summary
- CSV export of session history
- Futuristic dark UI with Framer Motion animations and Tailwind CSS
- Secure API (Helmet, rate limiting, CORS, error middleware)

## Project Structure

```
mood_project/
├── Golden Response/
│   ├── backend/                 # Express API + session storage
│   │   ├── config/              # MongoDB connection
│   │   ├── controllers/         # Session & emotion handlers
│   │   ├── middleware/          # Error handling, rate limiting
│   │   ├── models/              # Mongoose Session schema
│   │   ├── routes/              # REST API routes
│   │   ├── store/               # File-based store (local dev)
│   │   ├── data/                # sessions.json (file DB)
│   │   ├── server.js
│   │   └── package.json
│   └── frontend/                # Next.js 14 app
│       ├── public/models/       # face-api.js weight files
│       └── src/
│           ├── app/             # Landing, analyze, dashboard pages
│           ├── components/
│           ├── hooks/           # useFaceApi (model loading)
│           └── utils/           # API client (axios)
├── goldenresponse.py            # Embedded source + one-command runner
├── prompt.md                    # Original project specification
├── justification.md             # Evaluation verdict
└── README.md
```

## Quick Start (Recommended)

The fastest way to run the app is with `goldenresponse.py`, which extracts embedded source code, creates environment files, installs dependencies if needed, and starts both servers.

**Requirements:** [Node.js](https://nodejs.org/) (v18+), npm, Python 3.8+

```bash
python goldenresponse.py
```

This will:

1. Extract all backend/frontend source into `Golden Response/`
2. Create `backend/.env` and `frontend/.env.local` if missing
3. Run `npm install` in both folders (first time only)
4. Start the backend on **http://localhost:5001** and frontend on **http://localhost:3000**
5. Open the app in your browser

**Extract only (no servers):**

```bash
python goldenresponse.py --extract-only
```

## Manual Setup

### 1. AI model weights

face-api.js needs model weights in `Golden Response/frontend/public/models/`. If the binary shard files are missing, download them from the [face-api.js weights repo](https://github.com/justadudewhohacks/face-api.js/tree/master/weights) and place these four files in that folder:

- `tiny_face_detector_model-weights_manifest.json`
- `tiny_face_detector_model-shard1`
- `face_expression_model-weights_manifest.json`
- `face_expression_model-shard1`

### 2. Backend

```bash
cd "Golden Response/backend"
cp .env.example .env
npm install
npm run dev
```

Add to `backend/.env` for local development without MongoDB:

```env
PORT=5001
USE_FILE_DB=true
USE_MEMORY_DB=false
CLIENT_URL=http://localhost:3000
```

Sessions are stored in `backend/data/sessions.json` when `USE_FILE_DB=true`.

### 3. Frontend

```bash
cd "Golden Response/frontend"
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:5001/api
```

Then:

```bash
npm install
npm run dev
```

Open **http://localhost:3000**

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/emotions/session/start` | Start a new session (`username` in body) |
| `POST` | `/api/emotions/session/:sessionId/log` | Log emotion + confidence |
| `GET` | `/api/emotions/session/:sessionId` | Get session history |
| `GET` | `/api/emotions/session/:sessionId/download` | Download session as CSV |

## Environment Variables

| Service | Variable | Description |
|---------|----------|-------------|
| Backend | `PORT` | API port (default `5000`, use `5001` if 5000 is busy) |
| Backend | `MONGO_URI` | MongoDB connection string (production) |
| Backend | `USE_FILE_DB` | `true` = JSON file store in `data/sessions.json` |
| Backend | `USE_MEMORY_DB` | `true` = in-memory MongoDB (dev only) |
| Backend | `CLIENT_URL` | CORS origin (default `http://localhost:3000`) |
| Frontend | `NEXT_PUBLIC_API_URL` | Backend API base URL |

## Tech Stack

| Layer | Technologies |
|-------|----------------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Framer Motion, react-webcam, Recharts, Axios |
| Backend | Node.js, Express, Mongoose, Helmet, express-rate-limit |
| AI/ML | face-api.js, TensorFlow.js (client-side WebGL) |
| Database | MongoDB Atlas (production) or file-based JSON (local dev) |

## Production Deployment

1. **Database:** MongoDB Atlas — set `USE_FILE_DB=false` and configure `MONGO_URI`
2. **Backend:** Deploy `Golden Response/backend` to Render, Railway, or similar — run `npm start`
3. **Frontend:** Deploy `Golden Response/frontend` to Vercel or Netlify — set `NEXT_PUBLIC_API_URL` to your deployed API URL

## Repository

[https://github.com/aryandabas17/Mood-analysis](https://github.com/aryandabas17/Mood-analysis)
