"use client";
import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import Webcam from 'react-webcam';
import * as faceapi from 'face-api.js';
import { motion, AnimatePresence } from 'framer-motion';
import { useFaceApi } from '@/hooks/useFaceApi';
import { logEmotionApi } from '@/utils/api';
import GlowCard from '@/components/GlowCard';

export default function AnalyzePage() {
  const router = useRouter();
  const { modelsLoaded, error: modelError } = useFaceApi();
  const webcamRef = useRef<Webcam>(null);

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [currentEmotion, setCurrentEmotion] = useState<string>("Scanning...");
  const [confidence, setConfidence] = useState<number>(0);
  const [sysStatus, setSysStatus] = useState<string>("Awaiting Camera Authorization...");
  const [cameraError, setCameraError] = useState<boolean>(false);

  useEffect(() => {
    const id = localStorage.getItem('sessionId');
    if (!id) router.push('/');
    else setSessionId(id);
  }, [router]);

  useEffect(() => {
    if (!modelsLoaded || !sessionId) return;
    setSysStatus("Neural Array Active. Evaluating metrics...");

    const intervalId = setInterval(async () => {
      if (webcamRef.current?.video?.readyState === 4) {
        const video = webcamRef.current.video;
        const detection = await faceapi
          .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions())
          .withFaceExpressions();

        if (detection) {
          const expressions = detection.expressions;
          const topEmotion = Object.entries(expressions).reduce((a, b) =>
            a[1] > b[1] ? a : b
          );

          const emotionName = topEmotion[0];
          const score = Math.round(topEmotion[1] * 100);

          setCurrentEmotion(emotionName.toUpperCase());
          setConfidence(score);
          setSysStatus("Tracking target live.");

          if (score > 40) {
            logEmotionApi(sessionId, emotionName, score).catch((err) =>
              console.error("Telemetry update drop", err)
            );
          }
        } else {
          setCurrentEmotion("NO FACE PRESENT");
          setConfidence(0);
          setSysStatus("Awaiting clear visual tracking vector...");
        }
      }
    }, 500);

    return () => clearInterval(intervalId);
  }, [modelsLoaded, sessionId]);

  if (modelError) return <div className="text-red-500 font-mono p-8">{modelError}</div>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 min-h-[80vh] items-start">
      <div className="lg:col-span-2 space-y-6">
        <GlowCard className="overflow-hidden relative p-2 bg-black">
          {!cameraError ? (
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              onUserMediaError={() => {
                setCameraError(true);
                setSysStatus("Permission Denied.");
              }}
              className="w-full h-auto rounded-xl object-cover scale-x-[-1]"
            />
          ) : (
            <div className="aspect-video w-full flex items-center justify-center bg-red-950/20 rounded-xl border border-red-500/40 text-red-400 font-mono">
              [CRITICAL ERROR: WEBCAM FEED DISCONNECTED]
            </div>
          )}
          <div className="absolute top-6 left-6 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-md border border-cyber-border text-xs font-mono tracking-wider flex items-center gap-2">
            <span className={`h-2 w-2 rounded-full ${cameraError ? 'bg-red-500' : 'bg-cyan-400 animate-pulse'}`} />
            {sysStatus}
          </div>
        </GlowCard>
      </div>

      <div className="space-y-6">
        <GlowCard className="text-center py-12 relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,242,254,0.08),transparent_70%)]" />
          <h3 className="text-xs font-mono text-gray-400 uppercase tracking-widest mb-2">Calculated Target MoodState</h3>

          <AnimatePresence mode="wait">
            <motion.div
              key={currentEmotion}
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 1.1, opacity: 0 }}
              className="text-4xl font-mono font-black text-cyan-400 tracking-wide my-4 drop-shadow-[0_0_15px_rgba(0,242,254,0.4)]"
            >
              {currentEmotion}
            </motion.div>
          </AnimatePresence>

          <div className="mt-8 px-4">
            <div className="flex justify-between text-xs font-mono text-gray-400 mb-2">
              <span>CONFIDENCE ACCURACY</span>
              <span className="text-cyan-400">{confidence}%</span>
            </div>
            <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden border border-white/5">
              <motion.div
                animate={{ width: `${confidence}%` }}
                className="h-full bg-gradient-to-r from-cyan-400 to-fuchsia-500"
              />
            </div>
          </div>
        </GlowCard>

        <button
          onClick={() => router.push('/dashboard')}
          className="w-full bg-white text-black font-mono font-bold tracking-widest py-4 rounded-xl shadow-lg hover:bg-neutral-200 transition-colors text-sm"
        >
          TERMINATE & VIEW SYSTEM METRICS →
        </button>
      </div>
    </div>
  );
}
