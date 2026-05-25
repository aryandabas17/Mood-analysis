import express from 'express';
import {
  startSession,
  saveEmotionData,
  getSessionHistory,
  downloadReport,
} from '../controllers/emotion.controller.js';

const router = express.Router();

router.post('/session/start', startSession);
router.post('/session/:sessionId/log', saveEmotionData);
router.get('/session/:sessionId', getSessionHistory);
router.get('/session/:sessionId/download', downloadReport);

export default router;
