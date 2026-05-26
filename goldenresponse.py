"""
Golden Response - complete embedded frontend and backend source code.

All project source files from Golden Response/backend and Golden Response/frontend
are stored in PROJECT_FILES. Use extract_all() to write them to disk.
"""

from __future__ import annotations

import os
import sys
import subprocess
import threading
import time
import webbrowser
import signal
from pathlib import Path
from typing import Dict

PROJECT_FILES: Dict[str, str] = {
    "backend/.env.example": "PORT=5000\nMONGO_URI=mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/mood_analysis?retryWrites=true&w=majority\nNODE_ENV=development\nCLIENT_URL=http://localhost:3000\n",
    "backend/config/db.js": "import mongoose from 'mongoose';\nimport { MongoMemoryServer } from 'mongodb-memory-server';\n\nlet memoryServer;\n\nexport const connectDB = async () => {\n  try {\n    let uri = process.env.MONGO_URI;\n    if (process.env.USE_MEMORY_DB === 'true') {\n      memoryServer = await MongoMemoryServer.create({\n        instance: { launchTimeout: 120000 },\n      });\n      uri = memoryServer.getUri('mood_analysis');\n      console.log('\ud83d\udce6 Using in-memory MongoDB (development)');\n    }\n    const conn = await mongoose.connect(uri);\n    console.log(`\ud83d\ude80 MongoDB Connected: ${conn.connection.host}`);\n  } catch (error) {\n    console.error(`\u274c MongoDB Connection Error: ${error.message}`);\n    process.exit(1);\n  }\n};\n",
    "backend/controllers/emotion.controller.js": "import { sessionStore } from '../store/index.js';\n\nexport const startSession = async (req, res, next) => {\n  try {\n    const { username } = req.body;\n    if (!username) {\n      res.status(400);\n      throw new Error('Username is required');\n    }\n    const session = await sessionStore.create({ username });\n    res.status(201).json(session);\n  } catch (error) {\n    next(error);\n  }\n};\n\nexport const saveEmotionData = async (req, res, next) => {\n  try {\n    const { sessionId } = req.params;\n    const { emotion, confidence } = req.body;\n\n    if (!emotion || confidence === undefined) {\n      res.status(400);\n      throw new Error('Invalid emotion dataset entry');\n    }\n\n    const session = await sessionStore.pushLog(sessionId, { emotion, confidence });\n\n    if (!session) {\n      res.status(404);\n      throw new Error('Session not found');\n    }\n\n    res.status(200).json({ success: true });\n  } catch (error) {\n    next(error);\n  }\n};\n\nexport const getSessionHistory = async (req, res, next) => {\n  try {\n    const { sessionId } = req.params;\n    const session = await sessionStore.findById(sessionId);\n\n    if (!session) {\n      res.status(404);\n      throw new Error('Session parameters not found');\n    }\n    res.status(200).json(session);\n  } catch (error) {\n    next(error);\n  }\n};\n\nexport const downloadReport = async (req, res, next) => {\n  try {\n    const { sessionId } = req.params;\n    const session = await sessionStore.findById(sessionId);\n    if (!session) {\n      res.status(404);\n      throw new Error('Session not found');\n    }\n\n    res.setHeader('Content-Type', 'text/csv');\n    res.setHeader('Content-Disposition', `attachment; filename=session-${sessionId}.csv`);\n\n    let csvContent = 'Timestamp,Emotion,Confidence\\n';\n    session.logs.forEach((log) => {\n      const ts = log.timestamp instanceof Date ? log.timestamp.toISOString() : new Date(log.timestamp).toISOString();\n      csvContent += `${ts},${log.emotion},${log.confidence}\\n`;\n    });\n\n    res.status(200).send(csvContent);\n  } catch (error) {\n    next(error);\n  }\n};\n",
    "backend/data/.gitkeep": "",
    "backend/loadEnv.js": "import dotenv from 'dotenv';\n\ndotenv.config();\n",
    "backend/middleware/error.middleware.js": "export const errorHandler = (err, req, res, next) => {\n  const statusCode = res.statusCode === 200 ? 500 : res.statusCode;\n  res.status(statusCode).json({\n    message: err.message,\n    stack: process.env.NODE_ENV === 'production' ? null : err.stack,\n  });\n};\n",
    "backend/middleware/rateLimiter.middleware.js": "import rateLimit from 'express-rate-limit';\n\nexport const apiLimiter = rateLimit({\n  windowMs: 15 * 60 * 1000,\n  max: 100,\n  standardHeaders: true,\n  legacyHeaders: false,\n  message: { message: 'Too many requests from this IP, please try again later.' },\n});\n",
    "backend/models/Session.model.js": "import mongoose from 'mongoose';\n\nconst EmotionLogSchema = new mongoose.Schema({\n  emotion: {\n    type: String,\n    required: true,\n    enum: ['happy', 'sad', 'angry', 'neutral', 'fear', 'surprise', 'disgust'],\n  },\n  confidence: { type: Number, required: true },\n  timestamp: { type: Date, default: Date.now },\n});\n\nconst SessionSchema = new mongoose.Schema(\n  {\n    username: { type: String, required: true, trim: true },\n    startTime: { type: Date, default: Date.now },\n    endTime: { type: Date },\n    logs: [EmotionLogSchema],\n  },\n  { timestamps: true }\n);\n\nexport default mongoose.model('Session', SessionSchema);\n",
    "backend/package.json": "{\n  \"name\": \"mood-analysis-backend\",\n  \"version\": \"1.0.0\",\n  \"type\": \"module\",\n  \"main\": \"server.js\",\n  \"scripts\": {\n    \"start\": \"node server.js\",\n    \"dev\": \"nodemon server.js\"\n  },\n  \"dependencies\": {\n    \"mongodb-memory-server\": \"^9.2.0\",\n    \"cors\": \"^2.8.5\",\n    \"dotenv\": \"^16.4.5\",\n    \"express\": \"^4.19.2\",\n    \"express-rate-limit\": \"^7.2.0\",\n    \"helmet\": \"^7.1.0\",\n    \"mongoose\": \"^8.3.1\"\n  },\n  \"devDependencies\": {\n    \"nodemon\": \"^3.1.0\"\n  }\n}\n",
    "backend/routes/emotion.routes.js": "import express from 'express';\nimport {\n  startSession,\n  saveEmotionData,\n  getSessionHistory,\n  downloadReport,\n} from '../controllers/emotion.controller.js';\n\nconst router = express.Router();\n\nrouter.post('/session/start', startSession);\nrouter.post('/session/:sessionId/log', saveEmotionData);\nrouter.get('/session/:sessionId', getSessionHistory);\nrouter.get('/session/:sessionId/download', downloadReport);\n\nexport default router;\n",
    "backend/server.js": "import './loadEnv.js';\nimport express from 'express';\nimport cors from 'cors';\nimport helmet from 'helmet';\nimport { initStore } from './store/index.js';\nimport { apiLimiter } from './middleware/rateLimiter.middleware.js';\nimport { errorHandler } from './middleware/error.middleware.js';\nimport emotionRoutes from './routes/emotion.routes.js';\n\nconst app = express();\n\napp.use(helmet());\napp.use(cors({ origin: process.env.CLIENT_URL || 'http://localhost:3000' }));\napp.use(express.json());\n\napp.use('/api', apiLimiter);\napp.use('/api/emotions', emotionRoutes);\n\napp.use(errorHandler);\n\nconst PORT = process.env.PORT || 5000;\n\nconst startServer = async () => {\n  await initStore();\n  app.listen(PORT, () => console.log(`\ud83d\udef8 Cyber-Core Server running on port ${PORT}`));\n};\n\nstartServer();\n",
    "backend/store/fileStore.js": "import fs from 'fs/promises';\nimport path from 'path';\nimport { randomUUID } from 'crypto';\nimport { fileURLToPath } from 'url';\n\nconst __dirname = path.dirname(fileURLToPath(import.meta.url));\nconst DATA_FILE = path.join(__dirname, '..', 'data', 'sessions.json');\n\nasync function readAll() {\n  try {\n    const raw = await fs.readFile(DATA_FILE, 'utf-8');\n    return JSON.parse(raw);\n  } catch {\n    return [];\n  }\n}\n\nasync function writeAll(sessions) {\n  await fs.mkdir(path.dirname(DATA_FILE), { recursive: true });\n  await fs.writeFile(DATA_FILE, JSON.stringify(sessions, null, 2));\n}\n\nexport const fileStore = {\n  async create({ username }) {\n    const sessions = await readAll();\n    const session = {\n      _id: randomUUID(),\n      username,\n      startTime: new Date().toISOString(),\n      endTime: null,\n      logs: [],\n      createdAt: new Date().toISOString(),\n      updatedAt: new Date().toISOString(),\n    };\n    sessions.push(session);\n    await writeAll(sessions);\n    return session;\n  },\n\n  async findById(id) {\n    const sessions = await readAll();\n    return sessions.find((s) => s._id === id) ?? null;\n  },\n\n  async pushLog(id, log) {\n    const sessions = await readAll();\n    const index = sessions.findIndex((s) => s._id === id);\n    if (index === -1) return null;\n    sessions[index].logs.push({\n      emotion: log.emotion,\n      confidence: log.confidence,\n      timestamp: log.timestamp || new Date().toISOString(),\n    });\n    sessions[index].updatedAt = new Date().toISOString();\n    await writeAll(sessions);\n    return sessions[index];\n  },\n};\n",
    "backend/store/index.js": "import Session from '../models/Session.model.js';\nimport { fileStore } from './fileStore.js';\n\nconst useFileStore = () => process.env.USE_FILE_DB === 'true';\n\nexport const sessionStore = {\n  async create({ username }) {\n    if (useFileStore()) return fileStore.create({ username });\n    return Session.create({ username, logs: [] });\n  },\n\n  async findById(id) {\n    if (useFileStore()) return fileStore.findById(id);\n    return Session.findById(id);\n  },\n\n  async pushLog(id, { emotion, confidence }) {\n    if (useFileStore()) {\n      return fileStore.pushLog(id, { emotion, confidence, timestamp: new Date() });\n    }\n    return Session.findByIdAndUpdate(\n      id,\n      { $push: { logs: { emotion, confidence, timestamp: new Date() } } },\n      { new: true, runValidators: true }\n    );\n  },\n};\n\nexport const initStore = async () => {\n  if (useFileStore()) {\n    console.log('\ud83d\udcc1 Using file-based session store (development)');\n    return;\n  }\n  const { connectDB } = await import('../config/db.js');\n  await connectDB();\n};\n",
    "frontend/next-env.d.ts": "/// <reference types=\"next\" />\n/// <reference types=\"next/image-types/global\" />\n\n// NOTE: This file should not be edited\n// see https://nextjs.org/docs/basic-features/typescript for more information.\n",
    "frontend/next.config.js": "/** @type {import('next').NextConfig} */\nconst nextConfig = {\n  reactStrictMode: true,\n};\n\nmodule.exports = nextConfig;\n",
    "frontend/package.json": "{\n  \"name\": \"mood-analysis-frontend\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\"\n  },\n  \"dependencies\": {\n    \"axios\": \"^1.6.8\",\n    \"face-api.js\": \"^0.22.2\",\n    \"framer-motion\": \"^11.1.7\",\n    \"lucide-react\": \"^0.371.0\",\n    \"next\": \"14.2.1\",\n    \"react\": \"^18.2.0\",\n    \"react-dom\": \"^18.2.0\",\n    \"react-webcam\": \"^7.2.0\",\n    \"recharts\": \"^2.12.5\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"^20.12.7\",\n    \"@types/react\": \"^18.2.79\",\n    \"@types/react-dom\": \"^18.2.25\",\n    \"autoprefixer\": \"^10.4.19\",\n    \"postcss\": \"^8.4.38\",\n    \"tailwindcss\": \"^3.4.3\",\n    \"typescript\": \"^5.4.5\"\n  }\n}\n",
    "frontend/postcss.config.js": "module.exports = {\n  plugins: {\n    tailwindcss: {},\n    autoprefixer: {},\n  },\n};\n",
    "frontend/public/models/face_expression_model-weights_manifest.json": "[{\"weights\":[{\"name\":\"dense0/conv0/filters\",\"shape\":[3,3,3,32],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.0057930146946626555,\"min\":-0.7125408074435067}},{\"name\":\"dense0/conv0/bias\",\"shape\":[32],\"dtype\":\"float32\"},{\"name\":\"dense0/conv1/depthwise_filter\",\"shape\":[3,3,32,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.006473719839956246,\"min\":-0.6408982641556684}},{\"name\":\"dense0/conv1/pointwise_filter\",\"shape\":[1,1,32,32],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.010509579321917366,\"min\":-1.408283629136927}},{\"name\":\"dense0/conv1/bias\",\"shape\":[32],\"dtype\":\"float32\"},{\"name\":\"dense0/conv2/depthwise_filter\",\"shape\":[3,3,32,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.005666389652326995,\"min\":-0.7252978754978554}},{\"name\":\"dense0/conv2/pointwise_filter\",\"shape\":[1,1,32,32],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.010316079270605948,\"min\":-1.1760330368490781}},{\"name\":\"dense0/conv2/bias\",\"shape\":[32],\"dtype\":\"float32\"},{\"name\":\"dense0/conv3/depthwise_filter\",\"shape\":[3,3,32,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.0063220320963392074,\"min\":-0.853474333005793}},{\"name\":\"dense0/conv3/pointwise_filter\",\"shape\":[1,1,32,32],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.010322785377502442,\"min\":-1.4658355236053466}},{\"name\":\"dense0/conv3/bias\",\"shape\":[32],\"dtype\":\"float32\"},{\"name\":\"dense1/conv0/depthwise_filter\",\"shape\":[3,3,32,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.0042531527724920535,\"min\":-0.5741756242864272}},{\"name\":\"dense1/conv0/pointwise_filter\",\"shape\":[1,1,32,64],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.010653339647779278,\"min\":-1.1825207009035}},{\"name\":\"dense1/conv0/bias\",\"shape\":[64],\"dtype\":\"float32\"},{\"name\":\"dense1/conv1/depthwise_filter\",\"shape\":[3,3,64,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.005166931012097527,\"min\":-0.6355325144879957}},{\"name\":\"dense1/conv1/pointwise_filter\",\"shape\":[1,1,64,64],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.011478300188101974,\"min\":-1.3888743227603388}},{\"name\":\"dense1/conv1/bias\",\"shape\":[64],\"dtype\":\"float32\"},{\"name\":\"dense1/conv2/depthwise_filter\",\"shape\":[3,3,64,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.006144821410085641,\"min\":-0.8479853545918185}},{\"name\":\"dense1/conv2/pointwise_filter\",\"shape\":[1,1,64,64],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.010541967317169788,\"min\":-1.3809977185492421}},{\"name\":\"dense1/conv2/bias\",\"shape\":[64],\"dtype\":\"float32\"},{\"name\":\"dense1/conv3/depthwise_filter\",\"shape\":[3,3,64,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.005769844849904378,\"min\":-0.686611537138621}},{\"name\":\"dense1/conv3/pointwise_filter\",\"shape\":[1,1,64,64],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.010939095534530341,\"min\":-1.2689350820055196}},{\"name\":\"dense1/conv3/bias\",\"shape\":[64],\"dtype\":\"float32\"},{\"name\":\"dense2/conv0/depthwise_filter\",\"shape\":[3,3,64,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.0037769308277204924,\"min\":-0.40790852939381317}},{\"name\":\"dense2/conv0/pointwise_filter\",\"shape\":[1,1,64,128],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.01188667194516051,\"min\":-1.4382873053644218}},{\"name\":\"dense2/conv0/bias\",\"shape\":[128],\"dtype\":\"float32\"},{\"name\":\"dense2/conv1/depthwise_filter\",\"shape\":[3,3,128,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.006497045825509464,\"min\":-0.8381189114907208}},{\"name\":\"dense2/conv1/pointwise_filter\",\"shape\":[1,1,128,128],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.011632198913424622,\"min\":-1.3377028750438316}},{\"name\":\"dense2/conv1/bias\",\"shape\":[128],\"dtype\":\"float32\"},{\"name\":\"dense2/conv2/depthwise_filter\",\"shape\":[3,3,128,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.005947182225246056,\"min\":-0.7969224181829715}},{\"name\":\"dense2/conv2/pointwise_filter\",\"shape\":[1,1,128,128],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.011436844339557722,\"min\":-1.4524792311238306}},{\"name\":\"dense2/conv2/bias\",\"shape\":[128],\"dtype\":\"float32\"},{\"name\":\"dense2/conv3/depthwise_filter\",\"shape\":[3,3,128,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.006665432686899222,\"min\":-0.8998334127313949}},{\"name\":\"dense2/conv3/pointwise_filter\",\"shape\":[1,1,128,128],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.01283421422920975,\"min\":-1.642779421338848}},{\"name\":\"dense2/conv3/bias\",\"shape\":[128],\"dtype\":\"float32\"},{\"name\":\"dense3/conv0/depthwise_filter\",\"shape\":[3,3,128,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.004711699953266218,\"min\":-0.6737730933170692}},{\"name\":\"dense3/conv0/pointwise_filter\",\"shape\":[1,1,128,256],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.010955964817720302,\"min\":-1.3914075318504784}},{\"name\":\"dense3/conv0/bias\",\"shape\":[256],\"dtype\":\"float32\"},{\"name\":\"dense3/conv1/depthwise_filter\",\"shape\":[3,3,256,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.00554193468654857,\"min\":-0.7149095745647656}},{\"name\":\"dense3/conv1/pointwise_filter\",\"shape\":[1,1,256,256],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.016790372250126858,\"min\":-2.484975093018775}},{\"name\":\"dense3/conv1/bias\",\"shape\":[256],\"dtype\":\"float32\"},{\"name\":\"dense3/conv2/depthwise_filter\",\"shape\":[3,3,256,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.006361540626077091,\"min\":-0.8142772001378676}},{\"name\":\"dense3/conv2/pointwise_filter\",\"shape\":[1,1,256,256],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.01777329678628959,\"min\":-1.7062364914838006}},{\"name\":\"dense3/conv2/bias\",\"shape\":[256],\"dtype\":\"float32\"},{\"name\":\"dense3/conv3/depthwise_filter\",\"shape\":[3,3,256,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.006900275922289082,\"min\":-0.8625344902861353}},{\"name\":\"dense3/conv3/pointwise_filter\",\"shape\":[1,1,256,256],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.015449936717164282,\"min\":-1.9003422162112067}},{\"name\":\"dense3/conv3/bias\",\"shape\":[256],\"dtype\":\"float32\"},{\"name\":\"fc/weights\",\"shape\":[256,7],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.004834276554631252,\"min\":-0.7203072066400565}},{\"name\":\"fc/bias\",\"shape\":[7],\"dtype\":\"float32\"}],\"paths\":[\"face_expression_model-shard1\"]}]",
    "frontend/public/models/tiny_face_detector_model-weights_manifest.json": "[{\"weights\":[{\"name\":\"conv0/filters\",\"shape\":[3,3,3,16],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.009007044399485869,\"min\":-1.2069439495311063}},{\"name\":\"conv0/bias\",\"shape\":[16],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.005263455241334205,\"min\":-0.9211046672334858}},{\"name\":\"conv1/depthwise_filter\",\"shape\":[3,3,16,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.004001977630690033,\"min\":-0.5042491814669441}},{\"name\":\"conv1/pointwise_filter\",\"shape\":[1,1,16,32],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.013836609615999109,\"min\":-1.411334180831909}},{\"name\":\"conv1/bias\",\"shape\":[32],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.0015159862590771096,\"min\":-0.30926119685173037}},{\"name\":\"conv2/depthwise_filter\",\"shape\":[3,3,32,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.002666276225856706,\"min\":-0.317286870876948}},{\"name\":\"conv2/pointwise_filter\",\"shape\":[1,1,32,64],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.015265831292844286,\"min\":-1.6792414422128714}},{\"name\":\"conv2/bias\",\"shape\":[64],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.0020280554598453,\"min\":-0.37113414915168985}},{\"name\":\"conv3/depthwise_filter\",\"shape\":[3,3,64,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.006100742489683862,\"min\":-0.8907084034938438}},{\"name\":\"conv3/pointwise_filter\",\"shape\":[1,1,64,128],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.016276211832083907,\"min\":-2.0508026908425725}},{\"name\":\"conv3/bias\",\"shape\":[128],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.003394414279975143,\"min\":-0.7637432129944072}},{\"name\":\"conv4/depthwise_filter\",\"shape\":[3,3,128,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.006716050119961009,\"min\":-0.8059260143953211}},{\"name\":\"conv4/pointwise_filter\",\"shape\":[1,1,128,256],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.021875603993733724,\"min\":-2.8875797271728514}},{\"name\":\"conv4/bias\",\"shape\":[256],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.0041141652009066415,\"min\":-0.8187188749804216}},{\"name\":\"conv5/depthwise_filter\",\"shape\":[3,3,256,1],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.008423839597141042,\"min\":-0.9013508368940915}},{\"name\":\"conv5/pointwise_filter\",\"shape\":[1,1,256,512],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.030007277283014035,\"min\":-3.8709387695088107}},{\"name\":\"conv5/bias\",\"shape\":[512],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.008402082966823203,\"min\":-1.4871686851277068}},{\"name\":\"conv8/filters\",\"shape\":[1,1,512,25],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.028336129469030042,\"min\":-4.675461362389957}},{\"name\":\"conv8/bias\",\"shape\":[25],\"dtype\":\"float32\",\"quantization\":{\"dtype\":\"uint8\",\"scale\":0.002268134028303857,\"min\":-0.41053225912299807}}],\"paths\":[\"tiny_face_detector_model-shard1\"]}]",
    "frontend/src/app/analyze/page.tsx": "\"use client\";\nimport { useEffect, useRef, useState } from 'react';\nimport { useRouter } from 'next/navigation';\nimport Webcam from 'react-webcam';\nimport * as faceapi from 'face-api.js';\nimport { motion, AnimatePresence } from 'framer-motion';\nimport { useFaceApi } from '@/hooks/useFaceApi';\nimport { logEmotionApi } from '@/utils/api';\nimport GlowCard from '@/components/GlowCard';\n\nexport default function AnalyzePage() {\n  const router = useRouter();\n  const { modelsLoaded, error: modelError } = useFaceApi();\n  const webcamRef = useRef<Webcam>(null);\n\n  const [sessionId, setSessionId] = useState<string | null>(null);\n  const [currentEmotion, setCurrentEmotion] = useState<string>(\"Scanning...\");\n  const [confidence, setConfidence] = useState<number>(0);\n  const [sysStatus, setSysStatus] = useState<string>(\"Awaiting Camera Authorization...\");\n  const [cameraError, setCameraError] = useState<boolean>(false);\n\n  useEffect(() => {\n    const id = localStorage.getItem('sessionId');\n    if (!id) router.push('/');\n    else setSessionId(id);\n  }, [router]);\n\n  useEffect(() => {\n    if (!modelsLoaded || !sessionId) return;\n    setSysStatus(\"Neural Array Active. Evaluating metrics...\");\n\n    const intervalId = setInterval(async () => {\n      if (webcamRef.current?.video?.readyState === 4) {\n        const video = webcamRef.current.video;\n        const detection = await faceapi\n          .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions())\n          .withFaceExpressions();\n\n        if (detection) {\n          const expressions = detection.expressions;\n          const topEmotion = Object.entries(expressions).reduce((a, b) =>\n            a[1] > b[1] ? a : b\n          );\n\n          const emotionName = topEmotion[0];\n          const score = Math.round(topEmotion[1] * 100);\n\n          setCurrentEmotion(emotionName.toUpperCase());\n          setConfidence(score);\n          setSysStatus(\"Tracking target live.\");\n\n          if (score > 40) {\n            logEmotionApi(sessionId, emotionName, score).catch((err) =>\n              console.error(\"Telemetry update drop\", err)\n            );\n          }\n        } else {\n          setCurrentEmotion(\"NO FACE PRESENT\");\n          setConfidence(0);\n          setSysStatus(\"Awaiting clear visual tracking vector...\");\n        }\n      }\n    }, 500);\n\n    return () => clearInterval(intervalId);\n  }, [modelsLoaded, sessionId]);\n\n  if (modelError) return <div className=\"text-red-500 font-mono p-8\">{modelError}</div>;\n\n  return (\n    <div className=\"grid grid-cols-1 lg:grid-cols-3 gap-8 min-h-[80vh] items-start\">\n      <div className=\"lg:col-span-2 space-y-6\">\n        <GlowCard className=\"overflow-hidden relative p-2 bg-black\">\n          {!cameraError ? (\n            <Webcam\n              audio={false}\n              ref={webcamRef}\n              screenshotFormat=\"image/jpeg\"\n              onUserMediaError={() => {\n                setCameraError(true);\n                setSysStatus(\"Permission Denied.\");\n              }}\n              className=\"w-full h-auto rounded-xl object-cover scale-x-[-1]\"\n            />\n          ) : (\n            <div className=\"aspect-video w-full flex items-center justify-center bg-red-950/20 rounded-xl border border-red-500/40 text-red-400 font-mono\">\n              [CRITICAL ERROR: WEBCAM FEED DISCONNECTED]\n            </div>\n          )}\n          <div className=\"absolute top-6 left-6 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-md border border-cyber-border text-xs font-mono tracking-wider flex items-center gap-2\">\n            <span className={`h-2 w-2 rounded-full ${cameraError ? 'bg-red-500' : 'bg-cyan-400 animate-pulse'}`} />\n            {sysStatus}\n          </div>\n        </GlowCard>\n      </div>\n\n      <div className=\"space-y-6\">\n        <GlowCard className=\"text-center py-12 relative overflow-hidden\">\n          <div className=\"absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,242,254,0.08),transparent_70%)]\" />\n          <h3 className=\"text-xs font-mono text-gray-400 uppercase tracking-widest mb-2\">Calculated Target MoodState</h3>\n\n          <AnimatePresence mode=\"wait\">\n            <motion.div\n              key={currentEmotion}\n              initial={{ scale: 0.9, opacity: 0 }}\n              animate={{ scale: 1, opacity: 1 }}\n              exit={{ scale: 1.1, opacity: 0 }}\n              className=\"text-4xl font-mono font-black text-cyan-400 tracking-wide my-4 drop-shadow-[0_0_15px_rgba(0,242,254,0.4)]\"\n            >\n              {currentEmotion}\n            </motion.div>\n          </AnimatePresence>\n\n          <div className=\"mt-8 px-4\">\n            <div className=\"flex justify-between text-xs font-mono text-gray-400 mb-2\">\n              <span>CONFIDENCE ACCURACY</span>\n              <span className=\"text-cyan-400\">{confidence}%</span>\n            </div>\n            <div className=\"w-full bg-white/5 h-2 rounded-full overflow-hidden border border-white/5\">\n              <motion.div\n                animate={{ width: `${confidence}%` }}\n                className=\"h-full bg-gradient-to-r from-cyan-400 to-fuchsia-500\"\n              />\n            </div>\n          </div>\n        </GlowCard>\n\n        <button\n          onClick={() => router.push('/dashboard')}\n          className=\"w-full bg-white text-black font-mono font-bold tracking-widest py-4 rounded-xl shadow-lg hover:bg-neutral-200 transition-colors text-sm\"\n        >\n          TERMINATE & VIEW SYSTEM METRICS \u2192\n        </button>\n      </div>\n    </div>\n  );\n}\n",
    "frontend/src/app/dashboard/page.tsx": "\"use client\";\nimport { useEffect, useState } from 'react';\nimport { useRouter } from 'next/navigation';\nimport { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';\nimport { getSessionApi, getDownloadUrl } from '@/utils/api';\nimport GlowCard from '@/components/GlowCard';\n\ninterface LogEntry {\n  emotion: string;\n  confidence: number;\n  timestamp: string;\n}\n\nexport default function DashboardPage() {\n  const router = useRouter();\n  const [data, setData] = useState<LogEntry[]>([]);\n  const [username, setUsername] = useState('');\n  const [sessionId, setSessionId] = useState<string | null>(null);\n\n  useEffect(() => {\n    const sId = localStorage.getItem('sessionId');\n    const user = localStorage.getItem('username');\n    if (!sId) router.push('/');\n\n    setSessionId(sId);\n    setUsername(user || 'Subject Unknown');\n\n    if (sId) {\n      getSessionApi(sId)\n        .then((res) => {\n          const formatted = res.logs.map((l: { emotion: string; confidence: number; timestamp: string }) => ({\n            emotion: l.emotion.toUpperCase(),\n            confidence: l.confidence,\n            timestamp: new Date(l.timestamp).toLocaleTimeString([], {\n              hour: '2-digit',\n              minute: '2-digit',\n              second: '2-digit',\n            }),\n          }));\n          setData(formatted);\n        })\n        .catch((err) => console.error(\"Failed downloading processing pipeline logs\", err));\n    }\n  }, [router]);\n\n  const emotionCounts = data.reduce<Record<string, number>>((acc, curr) => {\n    acc[curr.emotion] = (acc[curr.emotion] || 0) + 1;\n    return acc;\n  }, {});\n\n  const primaryEmotion =\n    Object.entries(emotionCounts).reduce(\n      (a, b) => (a[1] > b[1] ? a : b),\n      [\"N/A\", 0]\n    )[0] ?? \"N/A\";\n\n  return (\n    <div className=\"space-y-8 pb-16\">\n      <div className=\"flex flex-col md:flex-row justify-between items-start md:items-center gap-4\">\n        <div>\n          <h1 className=\"text-3xl font-bold font-mono tracking-tight\">\n            BIOMETRIC ENGINE INDEX // {username.toUpperCase()}\n          </h1>\n          <p className=\"text-sm text-gray-400 font-mono mt-1\">Telemetry Record Set: {sessionId}</p>\n        </div>\n        {sessionId && (\n          <a\n            href={getDownloadUrl(sessionId)}\n            className=\"px-5 py-2.5 bg-cyber-card border border-cyber-border rounded-xl font-mono text-xs tracking-wider text-cyan-400 hover:border-cyan-400/50 transition-colors\"\n          >\n            DOWNLOAD HISTORICAL LOGS (.CSV)\n          </a>\n        )}\n      </div>\n\n      <div className=\"grid grid-cols-1 md:grid-cols-3 gap-6\">\n        <GlowCard>\n          <div className=\"text-xs font-mono text-gray-400 mb-1\">AGGREGATED DOMINANT STATE</div>\n          <div className=\"text-3xl font-black font-mono text-fuchsia-400 tracking-wide\">{primaryEmotion}</div>\n        </GlowCard>\n        <GlowCard>\n          <div className=\"text-xs font-mono text-gray-400 mb-1\">ACQUIRED DATAPOINTS</div>\n          <div className=\"text-3xl font-black font-mono text-cyan-400 tracking-wide\">{data.length} frames</div>\n        </GlowCard>\n        <GlowCard>\n          <div className=\"text-xs font-mono text-gray-400 mb-1\">AVERAGE CORE CONFIDENCE</div>\n          <div className=\"text-3xl font-black font-mono text-emerald-400 tracking-wide\">\n            {data.length ? Math.round(data.reduce((acc, c) => acc + c.confidence, 0) / data.length) : 0}%\n          </div>\n        </GlowCard>\n      </div>\n\n      <GlowCard className=\"p-4\">\n        <div className=\"text-xs font-mono text-gray-400 mb-6 px-2 tracking-widest\">\n          REAL-TIME BIOMETRIC CONFIDENCE TIMELINE STRIP\n        </div>\n        <div className=\"w-full h-80\">\n          <ResponsiveContainer width=\"100%\" height=\"100%\">\n            <AreaChart data={data}>\n              <defs>\n                <linearGradient id=\"glowColor\" x1=\"0\" y1=\"0\" x2=\"0\" y2=\"1\">\n                  <stop offset=\"5%\" stopColor=\"#00f2fe\" stopOpacity={0.4} />\n                  <stop offset=\"95%\" stopColor=\"#00f2fe\" stopOpacity={0} />\n                </linearGradient>\n              </defs>\n              <XAxis\n                dataKey=\"timestamp\"\n                stroke=\"#333\"\n                tick={{ fill: '#666', fontFamily: 'monospace', fontSize: 10 }}\n              />\n              <YAxis stroke=\"#333\" domain={[0, 100]} tick={{ fill: '#666', fontFamily: 'monospace', fontSize: 10 }} />\n              <Tooltip\n                contentStyle={{\n                  backgroundColor: '#030014',\n                  borderColor: 'rgba(255,255,255,0.1)',\n                  borderRadius: '12px',\n                  fontFamily: 'monospace',\n                }}\n                itemStyle={{ color: '#00f2fe' }}\n              />\n              <Area\n                type=\"monotone\"\n                dataKey=\"confidence\"\n                stroke=\"#00f2fe\"\n                strokeWidth={2}\n                fillOpacity={1}\n                fill=\"url(#glowColor)\"\n              />\n            </AreaChart>\n          </ResponsiveContainer>\n        </div>\n      </GlowCard>\n    </div>\n  );\n}\n",
    "frontend/src/app/globals.css": "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n",
    "frontend/src/app/layout.tsx": "import type { Metadata } from \"next\";\nimport \"./globals.css\";\nimport MainNav from \"@/components/MainNav\";\n\nexport const metadata: Metadata = {\n  title: \"Mood Analysis // AI Neural Face Reader\",\n  description: \"Real-time biometric facial emotion evaluation engine\",\n};\n\nexport default function RootLayout({\n  children,\n}: Readonly<{\n  children: React.ReactNode;\n}>) {\n  return (\n    <html lang=\"en\" className=\"bg-cyber-bg text-white overflow-x-hidden\">\n      <body>\n        <div className=\"fixed inset-0 bg-[radial-gradient(circle_at_50%_120%,#1a0b36,transparent_60%)] -z-10\" />\n        <MainNav />\n        <main className=\"min-h-screen pt-20 px-4 md:px-8 max-w-7xl mx-auto\">\n          {children}\n        </main>\n      </body>\n    </html>\n  );\n}\n",
    "frontend/src/app/page.tsx": "\"use client\";\nimport { useState } from 'react';\nimport { useRouter } from 'next/navigation';\nimport { motion } from 'framer-motion';\nimport { startSessionApi } from '@/utils/api';\nimport GlowCard from '@/components/GlowCard';\n\nexport default function LandingPage() {\n  const [name, setName] = useState('');\n  const [loading, setLoading] = useState(false);\n  const router = useRouter();\n\n  const handleStart = async (e: React.FormEvent) => {\n    e.preventDefault();\n    if (!name.trim()) return;\n    setLoading(true);\n    try {\n      const session = await startSessionApi(name);\n      localStorage.setItem('sessionId', session._id);\n      localStorage.setItem('username', name);\n      router.push('/analyze');\n    } catch (err) {\n      alert(\"Terminal core error starting analytics framework sync.\");\n    } finally {\n      setLoading(false);\n    }\n  };\n\n  return (\n    <div className=\"flex flex-col items-center justify-center min-h-[80vh] text-center\">\n      <motion.div\n        initial={{ scale: 0.95, opacity: 0 }}\n        animate={{ scale: 1, opacity: 1 }}\n        transition={{ duration: 0.8 }}\n      >\n        <h1 className=\"text-5xl md:text-7xl font-extrabold tracking-tighter mb-4 bg-gradient-to-b from-white via-neutral-200 to-neutral-500 bg-clip-text text-transparent\">\n          AI-POWERED MOOD ANALYSIS\n        </h1>\n        <p className=\"text-gray-400 font-mono text-sm max-w-xl mx-auto mb-12\">\n          Quantum Neural Pipeline evaluation for sub-second facial biomechanical tracking and biometric state calculation.\n        </p>\n      </motion.div>\n\n      <GlowCard className=\"w-full max-w-md\">\n        <form onSubmit={handleStart} className=\"space-y-6\">\n          <div className=\"text-left\">\n            <label className=\"block text-xs font-mono text-cyan-400 uppercase tracking-widest mb-2\">Initialize User Interface Identity</label>\n            <input\n              type=\"text\"\n              required\n              value={name}\n              onChange={(e) => setName(e.target.value)}\n              placeholder=\"Enter subject identity tag...\"\n              className=\"w-full bg-black/50 border border-cyber-border rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan-500 font-mono text-sm tracking-wide transition-colors\"\n            />\n          </div>\n          <button\n            type=\"submit\"\n            disabled={loading}\n            className=\"w-full relative group overflow-hidden rounded-xl bg-gradient-to-r from-cyan-500 to-fuchsia-600 p-px font-semibold shadow-lg transition-transform active:scale-98\"\n          >\n            <span className=\"block px-4 py-3 rounded-[11px] bg-cyber-bg transition-colors group-hover:bg-transparent font-mono tracking-widest text-sm text-cyan-400 group-hover:text-white\">\n              {loading ? \"INITIALIZING...\" : \"START TELEMETRY LINK\"}\n            </span>\n          </button>\n        </form>\n      </GlowCard>\n    </div>\n  );\n}\n",
    "frontend/src/components/GlowCard.tsx": "\"use client\";\nimport { motion } from 'framer-motion';\n\nexport default function GlowCard({ children, className = \"\" }: { children: React.ReactNode; className?: string }) {\n  return (\n    <motion.div\n      initial={{ opacity: 0, y: 20 }}\n      animate={{ opacity: 1, y: 0 }}\n      transition={{ duration: 0.5 }}\n      className={`backdrop-blur-xl bg-cyber-card border border-cyber-border rounded-2xl p-6 shadow-[0_0_50px_-12px_rgba(0,242,254,0.15)] hover:border-cyan-500/30 transition-all duration-300 ${className}`}\n    >\n      {children}\n    </motion.div>\n  );\n}\n",
    "frontend/src/components/MainNav.tsx": "import Link from 'next/link';\n\nexport default function MainNav() {\n  return (\n    <nav className=\"fixed top-0 inset-x-0 h-20 bg-cyber-bg/50 backdrop-blur-md border-b border-cyber-border z-50 flex items-center justify-between px-8\">\n      <Link href=\"/\" className=\"text-xl font-bold tracking-widest bg-gradient-to-r from-cyan-400 to-fuchsia-500 bg-clip-text text-transparent\">\n        MOOD_ANALYSIS //\n      </Link>\n      <div className=\"flex gap-6 text-sm text-gray-400 font-mono\">\n        <span className=\"text-emerald-400 flex items-center gap-2\">\u25cf SYSTEM_ONLINE</span>\n      </div>\n    </nav>\n  );\n}\n",
    "frontend/src/hooks/useFaceApi.ts": "\"use client\";\nimport { useState, useEffect } from 'react';\nimport * as faceapi from 'face-api.js';\n\nexport function useFaceApi() {\n  const [modelsLoaded, setModelsLoaded] = useState(false);\n  const [error, setError] = useState<string | null>(null);\n\n  useEffect(() => {\n    const loadModels = async () => {\n      try {\n        const MODEL_URL = '/models';\n        await Promise.all([\n          faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),\n          faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL),\n        ]);\n        setModelsLoaded(true);\n      } catch (err) {\n        console.error(err);\n        setError(\"Failed to load biometric AI models.\");\n      }\n    };\n    loadModels();\n  }, []);\n\n  return { modelsLoaded, error };\n}\n",
    "frontend/src/utils/api.ts": "import axios from 'axios';\n\nconst api = axios.create({\n  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api',\n});\n\nexport const startSessionApi = async (username: string) => {\n  const res = await api.post('/emotions/session/start', { username });\n  return res.data;\n};\n\nexport const logEmotionApi = async (sessionId: string, emotion: string, confidence: number) => {\n  const res = await api.post(`/emotions/session/${sessionId}/log`, { emotion, confidence });\n  return res.data;\n};\n\nexport const getSessionApi = async (sessionId: string) => {\n  const res = await api.get(`/emotions/session/${sessionId}`);\n  return res.data;\n};\n\nexport const getDownloadUrl = (sessionId: string) => {\n  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';\n  return `${base}/emotions/session/${sessionId}/download`;\n};\n",
    "frontend/tailwind.config.ts": "import type { Config } from \"tailwindcss\";\n\nconst config: Config = {\n  content: [\n    \"./src/pages/**/*.{js,ts,jsx,tsx,mdx}\",\n    \"./src/components/**/*.{js,ts,jsx,tsx,mdx}\",\n    \"./src/app/**/*.{js,ts,jsx,tsx,mdx}\",\n  ],\n  theme: {\n    extend: {\n      colors: {\n        cyber: {\n          bg: '#030014',\n          card: 'rgba(255, 255, 255, 0.03)',\n          border: 'rgba(255, 255, 255, 0.08)',\n          glow: '#00f2fe',\n          neonPink: '#f355da',\n        },\n      },\n    },\n  },\n  plugins: [],\n};\nexport default config;\n",
    "frontend/tsconfig.json": "{\n  \"compilerOptions\": {\n    \"lib\": [\"dom\", \"dom.iterable\", \"esnext\"],\n    \"allowJs\": true,\n    \"skipLibCheck\": true,\n    \"strict\": true,\n    \"noEmit\": true,\n    \"esModuleInterop\": true,\n    \"module\": \"esnext\",\n    \"moduleResolution\": \"bundler\",\n    \"resolveJsonModule\": true,\n    \"isolatedModules\": true,\n    \"jsx\": \"preserve\",\n    \"incremental\": true,\n    \"plugins\": [{ \"name\": \"next\" }],\n    \"paths\": {\n      \"@/*\": [\"./src/*\"]\n    }\n  },\n  \"include\": [\"next-env.d.ts\", \"**/*.ts\", \"**/*.tsx\", \".next/types/**/*.ts\"],\n  \"exclude\": [\"node_modules\"]\n}\n",
}


def get_combined_code() -> str:
    sections = []
    for path, content in PROJECT_FILES.items():
        sections.append(f"# ===== FILE: {path} =====\n{content}\n")
    return "\n".join(sections).strip() + "\n"


COMBINED_CODE = get_combined_code()


def extract_all(output_dir: str = "Golden Response") -> None:
    base = Path(output_dir)
    for rel_path, content in PROJECT_FILES.items():
        target = base / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Safely handle surrogate pairs (like \ud83d\udce6) before encoding to UTF-8
            content = content.encode('utf-16', 'surrogatepass').decode('utf-16')
        except Exception:
            pass
        target.write_text(content, encoding="utf-8")


def check_command_exists(cmd: str) -> bool:
    """Checks if a command is available on the system path."""
    import shutil
    return shutil.which(cmd) is not None


def kill_process_tree(proc):
    """Terminates a process and all its children across Windows and Unix."""
    if not proc:
        return
    try:
        if os.name == 'nt':
            # On Windows, kill the process tree forcefully using taskkill
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )
        else:
            # On Unix, terminate process group
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except Exception:
        try:
            proc.terminate()
        except Exception:
            pass


def run_project(output_dir: str = "Golden Response") -> None:
    base = Path(output_dir).resolve()
    
    # 1. Verify Node.js and npm are installed
    if not check_command_exists("node") or not check_command_exists("npm"):
        print("\n\033[91m[Error] Node.js and npm are required to run this project.\033[0m")
        print("Please install Node.js from https://nodejs.org/ and try again.\n")
        sys.exit(1)
        
    print("\n\033[96m=== Setting up Environment ===\033[0m")
    
    # 2. Extract files
    print("Extracting embedded code files...")
    extract_all(str(base))
    
    # 3. Create backend env file if it doesn't exist
    backend_dir = base / "backend"
    backend_env = backend_dir / ".env"
    backend_env_example = backend_dir / ".env.example"
    
    if not backend_env.exists():
        if backend_env_example.exists():
            print("Creating backend/.env from .env.example...")
            content = backend_env_example.read_text(encoding="utf-8")
            lines = []
            for line in content.splitlines():
                if line.startswith("MONGO_URI="):
                    lines.append("MONGO_URI=mongodb://127.0.0.1:27017/mood_analysis")
                else:
                    lines.append(line)
            # Ensure USE_FILE_DB is true so it doesn't fail if mongo is missing
            if not any("USE_FILE_DB" in l for l in lines):
                lines.append("USE_FILE_DB=true")
            if not any("USE_MEMORY_DB" in l for l in lines):
                lines.append("USE_MEMORY_DB=false")
            backend_env.write_text("\n".join(lines) + "\n", encoding="utf-8")
        else:
            print("Creating default backend/.env...")
            backend_env.write_text(
                "PORT=5001\n"
                "MONGO_URI=mongodb://127.0.0.1:27017/mood_analysis\n"
                "USE_MEMORY_DB=false\n"
                "USE_FILE_DB=true\n"
                "NODE_ENV=development\n"
                "CLIENT_URL=http://localhost:3000\n",
                encoding="utf-8"
            )
            
    # 4. Create frontend env file if it doesn't exist
    frontend_dir = base / "frontend"
    frontend_env = frontend_dir / ".env.local"
    if not frontend_env.exists():
        print("Creating frontend/.env.local...")
        frontend_env.write_text("NEXT_PUBLIC_API_URL=http://localhost:5001/api\n", encoding="utf-8")

    # 5. Check and install dependencies
    backend_node_modules = backend_dir / "node_modules"
    if not backend_node_modules.exists():
        print("\033[93mInstalling backend dependencies (this might take a minute)...\033[0m")
        subprocess.run("npm install", shell=True, cwd=str(backend_dir), check=True)
        print("Backend dependencies installed.")
    else:
        print("Backend dependencies already installed.")

    frontend_node_modules = frontend_dir / "node_modules"
    if not frontend_node_modules.exists():
        print("\033[93mInstalling frontend dependencies (this might take a minute)...\033[0m")
        subprocess.run("npm install", shell=True, cwd=str(frontend_dir), check=True)
        print("Frontend dependencies installed.")
    else:
        print("Frontend dependencies already installed.")
        
    print("\n\033[92m=== Starting backend and frontend concurrently ===\033[0m")
    
    # 6. Run processes
    backend_cmd = "node server.js"
    backend_proc = None
    frontend_proc = None
    
    popen_kwargs = {}
    if os.name != 'nt':
        popen_kwargs['preexec_fn'] = os.setsid
        
    try:
        # Start Backend (writing directly to standard streams)
        print("Starting Cyber-Core Backend Server on port 5001...")
        backend_proc = subprocess.Popen(
            backend_cmd,
            shell=True,
            cwd=str(backend_dir),
            **popen_kwargs
        )
        
        # Start Frontend (writing directly to standard streams)
        print("Starting Next.js Frontend on http://localhost:3000...")
        frontend_proc = subprocess.Popen(
            "npm run dev",
            shell=True,
            cwd=str(frontend_dir),
            **popen_kwargs
        )
        
        # 7. Wait a few seconds, then open the browser
        def open_browser():
            time.sleep(5)
            print("\n\033[92m[System] Launching browser to http://localhost:3000...\033[0m\n", flush=True)
            webbrowser.open("http://localhost:3000")
            
        threading.Thread(target=open_browser, daemon=True).start()
        
        print("\n\033[92m=== Mood Analysis Project is Running ===\033[0m")
        print("\033[93mPress Ctrl+C to terminate both servers and stop the program.\033[0m\n", flush=True)
        
        # Keep main thread alive monitoring processes
        while True:
            be_status = backend_proc.poll()
            fe_status = frontend_proc.poll()
            
            if be_status is not None:
                print(f"\n\033[91m[System] Backend process exited with code {be_status}\033[0m", flush=True)
                break
            if fe_status is not None:
                print(f"\n\033[91m[System] Frontend process exited with code {fe_status}\033[0m", flush=True)
                break
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\033[93m[System] Shutdown signal received (Ctrl+C). Terminating processes...\033[0m", flush=True)
    finally:
        print("Stopping backend...", flush=True)
        kill_process_tree(backend_proc)
        print("Stopping frontend...", flush=True)
        kill_process_tree(frontend_proc)
        print("\033[92m[System] All servers successfully terminated.\033[0m", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--extract-only":
        extract_all()
        print(f"Embedded {len(PROJECT_FILES)} files extracted to Golden Response.")
    else:
        run_project()

