"use client";
import { motion } from 'framer-motion';

export default function GlowCard({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`backdrop-blur-xl bg-cyber-card border border-cyber-border rounded-2xl p-6 shadow-[0_0_50px_-12px_rgba(0,242,254,0.15)] hover:border-cyan-500/30 transition-all duration-300 ${className}`}
    >
      {children}
    </motion.div>
  );
}
