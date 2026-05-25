"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';
import { getSessionApi, getDownloadUrl } from '@/utils/api';
import GlowCard from '@/components/GlowCard';

interface LogEntry {
  emotion: string;
  confidence: number;
  timestamp: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<LogEntry[]>([]);
  const [username, setUsername] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    const sId = localStorage.getItem('sessionId');
    const user = localStorage.getItem('username');
    if (!sId) router.push('/');

    setSessionId(sId);
    setUsername(user || 'Subject Unknown');

    if (sId) {
      getSessionApi(sId)
        .then((res) => {
          const formatted = res.logs.map((l: { emotion: string; confidence: number; timestamp: string }) => ({
            emotion: l.emotion.toUpperCase(),
            confidence: l.confidence,
            timestamp: new Date(l.timestamp).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
            }),
          }));
          setData(formatted);
        })
        .catch((err) => console.error("Failed downloading processing pipeline logs", err));
    }
  }, [router]);

  const emotionCounts = data.reduce<Record<string, number>>((acc, curr) => {
    acc[curr.emotion] = (acc[curr.emotion] || 0) + 1;
    return acc;
  }, {});

  const primaryEmotion =
    Object.entries(emotionCounts).reduce(
      (a, b) => (a[1] > b[1] ? a : b),
      ["N/A", 0]
    )[0] ?? "N/A";

  return (
    <div className="space-y-8 pb-16">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold font-mono tracking-tight">
            BIOMETRIC ENGINE INDEX // {username.toUpperCase()}
          </h1>
          <p className="text-sm text-gray-400 font-mono mt-1">Telemetry Record Set: {sessionId}</p>
        </div>
        {sessionId && (
          <a
            href={getDownloadUrl(sessionId)}
            className="px-5 py-2.5 bg-cyber-card border border-cyber-border rounded-xl font-mono text-xs tracking-wider text-cyan-400 hover:border-cyan-400/50 transition-colors"
          >
            DOWNLOAD HISTORICAL LOGS (.CSV)
          </a>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <GlowCard>
          <div className="text-xs font-mono text-gray-400 mb-1">AGGREGATED DOMINANT STATE</div>
          <div className="text-3xl font-black font-mono text-fuchsia-400 tracking-wide">{primaryEmotion}</div>
        </GlowCard>
        <GlowCard>
          <div className="text-xs font-mono text-gray-400 mb-1">ACQUIRED DATAPOINTS</div>
          <div className="text-3xl font-black font-mono text-cyan-400 tracking-wide">{data.length} frames</div>
        </GlowCard>
        <GlowCard>
          <div className="text-xs font-mono text-gray-400 mb-1">AVERAGE CORE CONFIDENCE</div>
          <div className="text-3xl font-black font-mono text-emerald-400 tracking-wide">
            {data.length ? Math.round(data.reduce((acc, c) => acc + c.confidence, 0) / data.length) : 0}%
          </div>
        </GlowCard>
      </div>

      <GlowCard className="p-4">
        <div className="text-xs font-mono text-gray-400 mb-6 px-2 tracking-widest">
          REAL-TIME BIOMETRIC CONFIDENCE TIMELINE STRIP
        </div>
        <div className="w-full h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="glowColor" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#00f2fe" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#00f2fe" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis
                dataKey="timestamp"
                stroke="#333"
                tick={{ fill: '#666', fontFamily: 'monospace', fontSize: 10 }}
              />
              <YAxis stroke="#333" domain={[0, 100]} tick={{ fill: '#666', fontFamily: 'monospace', fontSize: 10 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#030014',
                  borderColor: 'rgba(255,255,255,0.1)',
                  borderRadius: '12px',
                  fontFamily: 'monospace',
                }}
                itemStyle={{ color: '#00f2fe' }}
              />
              <Area
                type="monotone"
                dataKey="confidence"
                stroke="#00f2fe"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#glowColor)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </GlowCard>
    </div>
  );
}
