import fs from 'fs/promises';
import path from 'path';
import { randomUUID } from 'crypto';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_FILE = path.join(__dirname, '..', 'data', 'sessions.json');

async function readAll() {
  try {
    const raw = await fs.readFile(DATA_FILE, 'utf-8');
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

async function writeAll(sessions) {
  await fs.mkdir(path.dirname(DATA_FILE), { recursive: true });
  await fs.writeFile(DATA_FILE, JSON.stringify(sessions, null, 2));
}

export const fileStore = {
  async create({ username }) {
    const sessions = await readAll();
    const session = {
      _id: randomUUID(),
      username,
      startTime: new Date().toISOString(),
      endTime: null,
      logs: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    sessions.push(session);
    await writeAll(sessions);
    return session;
  },

  async findById(id) {
    const sessions = await readAll();
    return sessions.find((s) => s._id === id) ?? null;
  },

  async pushLog(id, log) {
    const sessions = await readAll();
    const index = sessions.findIndex((s) => s._id === id);
    if (index === -1) return null;
    sessions[index].logs.push({
      emotion: log.emotion,
      confidence: log.confidence,
      timestamp: log.timestamp || new Date().toISOString(),
    });
    sessions[index].updatedAt = new Date().toISOString();
    await writeAll(sessions);
    return sessions[index];
  },
};
