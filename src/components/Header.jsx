import React, { useState } from 'react';
import { Search, Bell, Sparkles, ShieldCheck, Zap, User, Menu, X, Home, FileText, BarChart3, Video, Library, Layout, Bot, Settings } from 'lucide-react';

export default function Header({ currentView, setCurrentView, title, subtitle }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'landing', label: 'Home', icon: Home },
    { id: 'generate', label: 'Script Generator', icon: Sparkles },
    { id: 'analyze', label: 'Script Analyzer', icon: FileText },
    { id: 'reel', label: 'Reel Analyzer', icon: Video },
    { id: 'library', label: 'Viral Library', icon: Library },
    { id: 'scripts', label: 'Workspace', icon: Layout },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'advisor', label: 'AI Advisor', icon: Bot },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const handleNavClick = (viewId) => {
    setCurrentView(viewId);
    setMobileMenuOpen(false);
  };

  return (
    <>
      <header className="h-16 md:h-20 bg-white/95 backdrop-blur-md border-b border-slate-200/80 px-4 md:px-8 flex items-center justify-between sticky top-0 z-40 font-sans shadow-sm">
        {/* Brand & Top Navigation Bar */}
        <div className="flex items-center gap-4 md:gap-8">
          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-2 rounded-xl text-slate-700 hover:bg-slate-100 transition-colors"
            aria-label="Toggle Navigation Menu"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>

          <button
            onClick={() => handleNavClick('landing')}
            className="flex items-center gap-2.5 hover:opacity-80 transition-opacity"
          >
            <div className="w-9 h-9 md:w-10 md:h-10 rounded-2xl bg-[#4353ff] text-white flex items-center justify-center shadow-lg shadow-[#4353ff]/20">
              <Zap className="w-4 h-4 md:w-5 md:h-5 fill-current" />
            </div>
            <span className="font-extrabold text-lg md:text-xl tracking-tight text-[#1a1a2e]">
              ViralIQ
            </span>
          </button>

          {/* Desktop Top Navbar Links */}
          <nav className="hidden lg:flex items-center gap-5 text-xs font-bold text-slate-600">
            {navItems.slice(0, 7).map((item) => (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`transition-colors py-1 ${
                  currentView === item.id ? 'text-[#4353ff] border-b-2 border-[#4353ff]' : 'hover:text-[#4353ff]'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Header Right Actions */}
        <div className="flex items-center gap-3">
          {/* System Status Pill */}
          <div className="hidden sm:flex items-center gap-2 bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1.5 rounded-full text-xs font-semibold">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>AI Connected</span>
          </div>

          <button
            onClick={() => handleNavClick('generate')}
            className="py-2 md:py-2.5 px-3.5 md:px-4 bg-[#4353ff] hover:bg-[#3242e0] text-white font-extrabold rounded-2xl text-xs transition-all shadow-md shadow-[#4353ff]/20 flex items-center gap-1.5"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Launch Studio</span>
          </button>
        </div>
      </header>

      {/* Mobile Drawer Menu Overlay */}
      {mobileMenuOpen && (
        <div className="lg:hidden fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex">
          <div className="w-4/5 max-w-xs bg-white h-full shadow-2xl flex flex-col p-6 font-sans overflow-y-auto">
            <div className="flex items-center justify-between pb-6 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-2xl bg-[#4353ff] text-white flex items-center justify-center shadow-md">
                  <Zap className="w-4 h-4 fill-current" />
                </div>
                <span className="font-extrabold text-lg text-[#1a1a2e]">ViralIQ</span>
              </div>
              <button
                onClick={() => setMobileMenuOpen(false)}
                className="p-2 rounded-xl text-slate-500 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <nav className="flex-1 py-6 space-y-1.5">
              {navItems.map((item) => {
                const IconComponent = item.icon;
                const active = currentView === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => handleNavClick(item.id)}
                    className={`w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-sm font-bold transition-all ${
                      active
                        ? 'bg-[#4353ff] text-white shadow-md shadow-[#4353ff]/20'
                        : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                    }`}
                  >
                    <IconComponent className={`w-5 h-5 ${active ? 'text-white' : 'text-slate-400'}`} />
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </nav>

            <div className="pt-4 border-t border-slate-100">
              <div className="bg-slate-50 p-4 rounded-2xl flex items-center gap-3 border border-slate-200/60">
                <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0" />
                <div>
                  <div className="text-xs font-bold text-slate-800">FastAPI & AI Active</div>
                  <div className="text-[10px] text-slate-500 font-semibold">Gemini + ML + ANN Pipeline</div>
                </div>
              </div>
            </div>
          </div>
          <div className="flex-1" onClick={() => setMobileMenuOpen(false)} />
        </div>
      )}
    </>
  );
}
