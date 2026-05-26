import type { Metadata } from "next";
import "./globals.css";
import MainNav from "@/components/MainNav";

export const metadata: Metadata = {
  title: "Mood Analysis // AI Neural Face Reader",
  description: "Real-time biometric facial emotion evaluation engine",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="bg-cyber-bg text-white overflow-x-hidden">
      <body>
        <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_120%,#1a0b36,transparent_60%)] -z-10" />
        <MainNav />
        <main className="min-h-screen pt-20 px-4 md:px-8 max-w-7xl mx-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
