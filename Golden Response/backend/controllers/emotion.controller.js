import { sessionStore } from '../store/index.js';

export const startSession = async (req, res, next) => {
  try {
    const { username } = req.body;
    if (!username) {
      res.status(400);
      throw new Error('Username is required');
    }
    const session = await sessionStore.create({ username });
    res.status(201).json(session);
  } catch (error) {
    next(error);
  }
};

export const saveEmotionData = async (req, res, next) => {
  try {
    const { sessionId } = req.params;
    const { emotion, confidence } = req.body;

    if (!emotion || confidence === undefined) {
      res.status(400);
      throw new Error('Invalid emotion dataset entry');
    }

    const session = await sessionStore.pushLog(sessionId, { emotion, confidence });

    if (!session) {
      res.status(404);
      throw new Error('Session not found');
    }

    res.status(200).json({ success: true });
  } catch (error) {
    next(error);
  }
};

export const getSessionHistory = async (req, res, next) => {
  try {
    const { sessionId } = req.params;
    const session = await sessionStore.findById(sessionId);

    if (!session) {
      res.status(404);
      throw new Error('Session parameters not found');
    }
    res.status(200).json(session);
  } catch (error) {
    next(error);
  }
};

export const downloadReport = async (req, res, next) => {
  try {
    const { sessionId } = req.params;
    const session = await sessionStore.findById(sessionId);
    if (!session) {
      res.status(404);
      throw new Error('Session not found');
    }

    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', `attachment; filename=session-${sessionId}.csv`);

    let csvContent = 'Timestamp,Emotion,Confidence\n';
    session.logs.forEach((log) => {
      const ts = log.timestamp instanceof Date ? log.timestamp.toISOString() : new Date(log.timestamp).toISOString();
      csvContent += `${ts},${log.emotion},${log.confidence}\n`;
    });

    res.status(200).send(csvContent);
  } catch (error) {
    next(error);
  }
};
