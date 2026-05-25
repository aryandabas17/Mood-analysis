"use client";
import { useState, useEffect } from 'react';
import * as faceapi from 'face-api.js';

export function useFaceApi() {
  const [modelsLoaded, setModelsLoaded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadModels = async () => {
      try {
        const MODEL_URL = '/models';
        await Promise.all([
          faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
          faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL),
        ]);
        setModelsLoaded(true);
      } catch (err) {
        console.error(err);
        setError("Failed to load biometric AI models.");
      }
    };
    loadModels();
  }, []);

  return { modelsLoaded, error };
}
