import mongoose from 'mongoose';
import { MongoMemoryServer } from 'mongodb-memory-server';

let memoryServer;

export const connectDB = async () => {
  try {
    let uri = process.env.MONGO_URI;
    if (process.env.USE_MEMORY_DB === 'true') {
      memoryServer = await MongoMemoryServer.create({
        instance: { launchTimeout: 120000 },
      });
      uri = memoryServer.getUri('mood_analysis');
      console.log('📦 Using in-memory MongoDB (development)');
    }
    const conn = await mongoose.connect(uri);
    console.log(`🚀 MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error(`❌ MongoDB Connection Error: ${error.message}`);
    process.exit(1);
  }
};
