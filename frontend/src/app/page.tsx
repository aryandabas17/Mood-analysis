"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { startSessionApi } from '@/utils/api';
import GlowCard from '@/components/GlowCard';

export default function LandingPage() {
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleStart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    try {
      const session = await startSessionApi(name);
      localStorage.setItem('sessionId', session._id);
      localStorage.setItem('username', name);
      router.push('/analyze');
    } catch (err) {
      alert("Terminal core error starting analytics framework sync.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tighter mb-4 bg-gradient-to-b from-white via-neutral-200 to-neutral-500 bg-clip-text text-transparent">
          AI-POWERED MOOD ANALYSIS
        </h1>
        <p className="text-gray-400 font-mono text-sm max-w-xl mx-auto mb-12">
          Quantum Neural Pipeline evaluation for sub-second facial biomechanical tracking and biometric state calculation.
        </p>
      </motion.div>

      <GlowCard className="w-full max-w-md">
        <form onSubmit={handleStart} className="space-y-6">
          <div className="text-left">
            <label className="block text-xs font-mono text-cyan-400 uppercase tracking-widest mb-2">Initialize User Interface Identity</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter subject identity tag..."
              className="w-full bg-black/50 border border-cyber-border rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan-500 font-mono text-sm tracking-wide transition-colors"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full relative group overflow-hidden rounded-xl bg-gradient-to-r from-cyan-500 to-fuchsia-600 p-px font-semibold shadow-lg transition-transform active:scale-98"
          >
            <span className="block px-4 py-3 rounded-[11px] bg-cyber-bg transition-colors group-hover:bg-transparent font-mono tracking-widest text-sm text-cyan-400 group-hover:text-white">
              {loading ? "INITIALIZING..." : "START TELEMETRY LINK"}
            </span>
          </button>
        </form>
      </GlowCard>
    </div>
  );
}
