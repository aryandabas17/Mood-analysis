import mongoose from 'mongoose';

const EmotionLogSchema = new mongoose.Schema({
  emotion: {
    type: String,
    required: true,
    enum: ['happy', 'sad', 'angry', 'neutral', 'fear', 'surprise', 'disgust'],
  },
  confidence: { type: Number, required: true },
  timestamp: { type: Date, default: Date.now },
});

const SessionSchema = new mongoose.Schema(
  {
    username: { type: String, required: true, trim: true },
    startTime: { type: Date, default: Date.now },
    endTime: { type: Date },
    logs: [EmotionLogSchema],
  },
  { timestamps: true }
);

export default mongoose.model('Session', SessionSchema);
