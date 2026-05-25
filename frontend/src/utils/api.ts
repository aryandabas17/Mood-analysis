import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api',
});

export const startSessionApi = async (username: string) => {
  const res = await api.post('/emotions/session/start', { username });
  return res.data;
};

export const logEmotionApi = async (sessionId: string, emotion: string, confidence: number) => {
  const res = await api.post(`/emotions/session/${sessionId}/log`, { emotion, confidence });
  return res.data;
};

export const getSessionApi = async (sessionId: string) => {
  const res = await api.get(`/emotions/session/${sessionId}`);
  return res.data;
};

export const getDownloadUrl = (sessionId: string) => {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';
  return `${base}/emotions/session/${sessionId}/download`;
};
