import React from 'react';
import { 
  LayoutDashboard, 
  Microscope, 
  Sparkles, 
  Film, 
  BookOpen, 
  FolderKanban, 
  MessageSquareText, 
  BarChart3, 
  FileText, 
  Settings,
  Zap,
  CheckCircle2,
  ChevronRight
} from 'lucide-react';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'generate', label: 'Generate Script', icon: Sparkles },
  { id: 'analyze', label: 'Analyze Script', icon: Microscope },
  { id: 'reel', label: 'Analyze Reel', icon: Film },
  { id: 'library', label: 'Viral Library', icon: BookOpen },
  { id: 'scripts', label: 'My Workspace', icon: FolderKanban },
  { id: 'advisor', label: 'AI Advisor', icon: MessageSquareText },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
  { id: 'reports', label: 'Reports', icon: FileText },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ currentView, setCurrentView }) {
  return (
    <aside className="w-64 bg-white border-r border-slate-200/80 flex flex-col h-screen sticky top-0 z-30 font-sans">
      {/* Brand Logo Header (Memberstack Style) */}
      <div className="p-6 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-[#4353ff] text-white flex items-center justify-center shadow-lg shadow-[#4353ff]/20">
            <Zap className="w-5 h-5 fill-current" />
          </div>
          <div>
            <h1 className="font-extrabold text-lg tracking-tight text-[#1a1a2e] flex items-center gap-1.5">
              ViralIQ
              <span className="text-[9px] font-extrabold uppercase tracking-wider bg-indigo-50 text-[#4353ff] border border-indigo-100 px-1.5 py-0.5 rounded-full">
                PRO
              </span>
            </h1>
            <p className="text-xs text-slate-400 font-medium">Script Optimization SaaS</p>
          </div>
        </div>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2">
          Platform Overview
        </div>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl font-semibold text-xs transition-all duration-200 ${
                isActive
                  ? 'bg-[#4353ff] text-white shadow-md shadow-[#4353ff]/25'
                  : 'text-[#1a1a2e] hover:text-[#4353ff] hover:bg-slate-50'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 transition-colors ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {isActive && <ChevronRight className="w-3.5 h-3.5 text-white/80" />}
            </button>
          );
        })}
      </nav>

      {/* Clean Memberstack-Style Pro Plan Widget */}
      <div className="p-4 m-3 bg-[#f8f9fc] rounded-2xl border border-slate-200/80 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-extrabold uppercase text-[#1a1a2e] flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
            Active Plan
          </span>
          <span className="text-[10px] font-bold text-[#4353ff] bg-indigo-50 px-2 py-0.5 rounded-full">
            Unlimited
          </span>
        </div>
        <p className="text-[11px] text-slate-500 leading-tight">
          AI Candidate Optimizer & Multi-Model Evaluation Active.
        </p>
      </div>
    </aside>
  );
}
