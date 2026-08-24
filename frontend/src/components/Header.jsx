import React from 'react';
import { Search, Bell, Sparkles, ShieldCheck, Zap, User } from 'lucide-react';

export default function Header({ currentView, setCurrentView, title, subtitle }) {
  return (
    <header className="h-20 bg-white/95 backdrop-blur-md border-b border-slate-200/80 px-8 flex items-center justify-between sticky top-0 z-30 font-sans shadow-sm">
      {/* Brand & Top Navigation Bar */}
      <div className="flex items-center gap-8">
        <button
          onClick={() => setCurrentView('landing')}
          className="flex items-center gap-3 hover:opacity-80 transition-opacity"
        >
          <div className="w-10 h-10 rounded-2xl bg-[#4353ff] text-white flex items-center justify-center shadow-lg shadow-[#4353ff]/20">
            <Zap className="w-5 h-5 fill-current" />
          </div>
          <span className="font-extrabold text-xl tracking-tight text-[#1a1a2e]">
            ViralIQ
          </span>
        </button>

        {/* Top Navbar Links across all views */}
        <nav className="hidden lg:flex items-center gap-6 text-xs font-bold text-slate-600">
          <button 
            onClick={() => setCurrentView('landing')}
            className={`transition-colors ${currentView === 'landing' ? 'text-[#4353ff]' : 'hover:text-[#4353ff]'}`}
          >
            Home
          </button>
          <button 
            onClick={() => setCurrentView('generate')}
            className={`transition-colors ${currentView === 'generate' ? 'text-[#4353ff]' : 'hover:text-[#4353ff]'}`}
          >
            Script Generator
          </button>
          <button 
            onClick={() => setCurrentView('analyze')}
            className={`transition-colors ${currentView === 'analyze' ? 'text-[#4353ff]' : 'hover:text-[#4353ff]'}`}
          >
            Script Analyzer
          </button>
          <button 
            onClick={() => setCurrentView('reel')}
            className={`transition-colors ${currentView === 'reel' ? 'text-[#4353ff]' : 'hover:text-[#4353ff]'}`}
          >
            Reel Analyzer
          </button>
          <button 
            onClick={() => setCurrentView('library')}
            className={`transition-colors ${currentView === 'library' ? 'text-[#4353ff]' : 'hover:text-[#4353ff]'}`}
          >
            Viral Library
          </button>
          <button 
            onClick={() => setCurrentView('scripts')}
            className={`transition-colors ${currentView === 'scripts' ? 'text-[#4353ff]' : 'hover:text-[#4353ff]'}`}
          >
            Workspace
          </button>
          <button 
            onClick={() => setCurrentView('analytics')}
            className={`transition-colors ${currentView === 'analytics' ? 'text-[#4353ff]' : 'hover:text-[#4353ff]'}`}
          >
            Analytics
          </button>
        </nav>
      </div>

      {/* Header Right Actions */}
      <div className="flex items-center gap-4">
        {/* System Status Pill */}
        <div className="hidden sm:flex items-center gap-2 bg-emerald-50 text-emerald-700 border border-emerald-200 px-3.5 py-1.5 rounded-full text-xs font-semibold">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>AI Engine Connected</span>
        </div>

        <button
          onClick={() => setCurrentView('generate')}
          className="py-2.5 px-4 bg-[#4353ff] hover:bg-[#3242e0] text-white font-extrabold rounded-2xl text-xs transition-all shadow-md shadow-[#4353ff]/20 flex items-center gap-1.5"
        >
          <Sparkles className="w-3.5 h-3.5" />
          Launch Studio
        </button>
      </div>
    </header>
  );
}
