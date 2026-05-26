import './loadEnv.js';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { initStore } from './store/index.js';
import { apiLimiter } from './middleware/rateLimiter.middleware.js';
import { errorHandler } from './middleware/error.middleware.js';
import emotionRoutes from './routes/emotion.routes.js';

const app = express();

app.use(helmet());
app.use(cors({ origin: process.env.CLIENT_URL || 'http://localhost:3000' }));
app.use(express.json());

app.use('/api', apiLimiter);
app.use('/api/emotions', emotionRoutes);

app.use(errorHandler);

const PORT = process.env.PORT || 5000;

const startServer = async () => {
  await initStore();
  app.listen(PORT, () => console.log(`🛸 Cyber-Core Server running on port ${PORT}`));
};

startServer();
