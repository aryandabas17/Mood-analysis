import Link from 'next/link';

export default function MainNav() {
  return (
    <nav className="fixed top-0 inset-x-0 h-20 bg-cyber-bg/50 backdrop-blur-md border-b border-cyber-border z-50 flex items-center justify-between px-8">
      <Link href="/" className="text-xl font-bold tracking-widest bg-gradient-to-r from-cyan-400 to-fuchsia-500 bg-clip-text text-transparent">
        MOOD_ANALYSIS //
      </Link>
      <div className="flex gap-6 text-sm text-gray-400 font-mono">
        <span className="text-emerald-400 flex items-center gap-2">● SYSTEM_ONLINE</span>
      </div>
    </nav>
  );
}
