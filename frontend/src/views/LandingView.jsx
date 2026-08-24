import React from 'react';
import { 
  Sparkles, 
  Play, 
  CheckCircle2, 
  ArrowRight, 
  Zap, 
  Trophy, 
  Brain, 
  Film, 
  BookOpen, 
  Layers, 
  ShieldCheck,
  Star,
  ChevronRight
} from 'lucide-react';

export default function LandingView({ setCurrentView }) {
  return (
    <div className="min-h-screen bg-[#f8f9fc] text-[#1a1a2e] font-sans selection:bg-[#4353ff] selection:text-white">
      {/* Top Navbar */}
      <header className="h-20 bg-white/90 backdrop-blur-md border-b border-slate-200/80 px-8 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-[#4353ff] text-white flex items-center justify-center shadow-lg shadow-[#4353ff]/20">
              <Zap className="w-5 h-5 fill-current" />
            </div>
            <span className="font-extrabold text-xl tracking-tight text-[#1a1a2e]">
              ViralIQ
            </span>
          </div>

          <nav className="hidden md:flex items-center gap-6 text-xs font-bold text-slate-600">
            <button onClick={() => setCurrentView('generate')} className="hover:text-[#4353ff] transition-colors">Script Generator</button>
            <button onClick={() => setCurrentView('analyze')} className="hover:text-[#4353ff] transition-colors">Analyzer</button>
            <button onClick={() => setCurrentView('library')} className="hover:text-[#4353ff] transition-colors">Viral Library</button>
            <button onClick={() => setCurrentView('analytics')} className="hover:text-[#4353ff] transition-colors">Analytics</button>
          </nav>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setCurrentView('dashboard')}
            className="py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-[#1a1a2e] font-bold rounded-xl text-xs transition-all"
          >
            Dashboard
          </button>
          <button
            onClick={() => setCurrentView('generate')}
            className="py-2.5 px-5 bg-[#4353ff] hover:bg-[#3242e0] text-white font-extrabold rounded-2xl text-xs transition-all shadow-md shadow-[#4353ff]/25 flex items-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            Launch AI Studio
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-8 max-w-7xl mx-auto text-center space-y-8">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-50 border border-indigo-100 text-xs font-bold text-[#4353ff] shadow-sm">
          <Sparkles className="w-3.5 h-3.5" />
          The AI Script Optimization Platform for Short-Form Video Creators
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-[#1a1a2e] max-w-4xl mx-auto leading-tight">
          Write & Optimize <span className="text-[#4353ff]">Viral Reel Scripts</span> in Seconds with AI
        </h1>

        <p className="text-base text-slate-500 max-w-2xl mx-auto leading-relaxed font-medium">
          Generate high-converting Instagram Reels, Shorts, and TikTok scripts using multi-candidate AI iteration, quantitative retention evaluation, and viral hook benchmark data.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <button
            onClick={() => setCurrentView('generate')}
            className="w-full sm:w-auto py-4 px-8 bg-[#4353ff] hover:bg-[#3242e0] text-white font-extrabold rounded-2xl text-sm transition-all shadow-xl shadow-[#4353ff]/25 flex items-center justify-center gap-3"
          >
            Start Generating Free <ArrowRight className="w-4 h-4" />
          </button>
          <button
            onClick={() => setCurrentView('library')}
            className="w-full sm:w-auto py-4 px-8 bg-white hover:bg-slate-50 text-[#1a1a2e] font-bold rounded-2xl text-sm transition-all border border-slate-200 shadow-sm flex items-center justify-center gap-2"
          >
            Explore Viral Library
          </button>
        </div>

        {/* Feature Badges */}
        <div className="pt-8 flex flex-wrap items-center justify-center gap-6 text-xs font-semibold text-slate-500">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            <span>Grammarly-Style Prompt Enhancer</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            <span>Multi-Candidate AI Optimization</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            <span>Quantitative Score Prediction</span>
          </div>
        </div>
      </section>

      {/* Live Features Grid */}
      <section className="py-16 px-8 max-w-7xl mx-auto space-y-12 border-t border-slate-200/80">
        <div className="text-center space-y-3">
          <h2 className="text-2xl font-extrabold text-[#1a1a2e]">Built for Creators & Marketing Agencies</h2>
          <p className="text-xs text-slate-400 font-medium max-w-lg mx-auto">
            Everything you need to turn raw video ideas into 80%+ engagement score short-form reel scripts.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="card-saas p-8 space-y-4 flex flex-col justify-between bg-white">
            <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-[#4353ff] flex items-center justify-center">
              <Sparkles className="w-6 h-6" />
            </div>
            <div className="space-y-2">
              <h3 className="text-lg font-bold text-[#1a1a2e]">AI Script Studio</h3>
              <p className="text-xs text-slate-500 leading-relaxed">
                Type your topic and let Gemini generate 3 to 5 candidate scripts. Automatically selects the winning peak candidate.
              </p>
            </div>
            <button
              onClick={() => setCurrentView('generate')}
              className="text-xs font-extrabold text-[#4353ff] hover:underline flex items-center gap-1 pt-2"
            >
              Try Generator <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div className="card-saas p-8 space-y-4 flex flex-col justify-between bg-white">
            <div className="w-12 h-12 rounded-2xl bg-purple-50 text-purple-600 flex items-center justify-center">
              <Brain className="w-6 h-6" />
            </div>
            <div className="space-y-2">
              <h3 className="text-lg font-bold text-[#1a1a2e]">Script Analyzer</h3>
              <p className="text-xs text-slate-500 leading-relaxed">
                Paste any raw draft to extract 15+ quantitative metrics, evaluate quality ratings, and get qualitative recommendations.
              </p>
            </div>
            <button
              onClick={() => setCurrentView('analyze')}
              className="text-xs font-extrabold text-purple-600 hover:underline flex items-center gap-1 pt-2"
            >
              Analyze Script <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div className="card-saas p-8 space-y-4 flex flex-col justify-between bg-white">
            <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <BookOpen className="w-6 h-6" />
            </div>
            <div className="space-y-2">
              <h3 className="text-lg font-bold text-[#1a1a2e]">Viral Benchmark Library</h3>
              <p className="text-xs text-slate-500 leading-relaxed">
                Access 50+ benchmark high-engagement reel script templates across Real Estate, Finance, Tech, Fitness, and E-commerce.
              </p>
            </div>
            <button
              onClick={() => setCurrentView('library')}
              className="text-xs font-extrabold text-emerald-600 hover:underline flex items-center gap-1 pt-2"
            >
              Browse Library <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-8 border-t border-slate-200/80 bg-white text-center text-xs text-slate-400 font-medium">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-xl bg-[#4353ff] text-white flex items-center justify-center">
              <Zap className="w-4 h-4 fill-current" />
            </div>
            <span className="font-bold text-[#1a1a2e]">ViralIQ SaaS</span>
          </div>
          <p>© 2026 ViralIQ Inc. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
