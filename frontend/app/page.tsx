'use client'
import ChatPanel from '@/components/ChatPanel'
import NurseScene from '@/components/NurseScene'

export default function HomePage() {
  return (
    <main className="flex h-screen w-screen overflow-hidden">
      {/* LEFT SIDE: 3D Hologram */}
      <section className="w-1/2 h-full relative border-r border-white/10 bg-black/20">
        <div className="absolute top-8 left-8 z-20 glass rounded-2xl p-4">
          <h2 className="text-xl font-bold text-white tracking-wider">MIKA OS</h2>
          <div className="flex items-center gap-2 mt-2">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs text-white/70 uppercase tracking-widest">Neural Link Active</span>
          </div>
        </div>
        <NurseScene />
      </section>

      {/* RIGHT SIDE: Chat Interface */}
      <section className="w-1/2 h-full">
        <ChatPanel />
      </section>
    </main>
  )
}