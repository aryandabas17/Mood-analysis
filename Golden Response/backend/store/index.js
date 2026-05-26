import Session from '../models/Session.model.js';
import { fileStore } from './fileStore.js';

const useFileStore = () => process.env.USE_FILE_DB === 'true';

export const sessionStore = {
  async create({ username }) {
    if (useFileStore()) return fileStore.create({ username });
    return Session.create({ username, logs: [] });
  },

  async findById(id) {
    if (useFileStore()) return fileStore.findById(id);
    return Session.findById(id);
  },

  async pushLog(id, { emotion, confidence }) {
    if (useFileStore()) {
      return fileStore.pushLog(id, { emotion, confidence, timestamp: new Date() });
    }
    return Session.findByIdAndUpdate(
      id,
      { $push: { logs: { emotion, confidence, timestamp: new Date() } } },
      { new: true, runValidators: true }
    );
  },
};

export const initStore = async () => {
  if (useFileStore()) {
    console.log('📁 Using file-based session store (development)');
    return;
  }
  const { connectDB } = await import('../config/db.js');
  await connectDB();
};
