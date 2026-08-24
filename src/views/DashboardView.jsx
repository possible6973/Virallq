import React, { useEffect, useState } from 'react';
import { fetchDashboard } from '../services/api';
import { 
  FileText, 
  Brain, 
  Target, 
  Trophy, 
  Sparkles, 
  ArrowUpRight,
  TrendingUp,
  Microscope,
  BookOpen,
  ChevronRight,
  Zap
} from 'lucide-react';

export default function DashboardView({ setCurrentView, setScriptToAnalyze }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard()
      .then(res => {
        setData(res);
        setLoading(false);
      })
      .catch(err => {
        console.error("Dashboard Fetch Error:", err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="flex items-center gap-3 text-[#4353ff] font-semibold text-xs">
          <div className="w-5 h-5 border-2 border-[#4353ff] border-t-transparent rounded-full animate-spin" />
          Loading Performance Dashboard...
        </div>
      </div>
    );
  }

  const metrics = [
    { label: 'Total Scripts', value: data?.total_scripts || 0, icon: FileText, change: 'Active Library', color: 'text-[#4353ff]', bg: 'bg-indigo-50' },
    { label: 'Reels Evaluated', value: data?.reels_analyzed || 0, icon: Brain, change: 'Dual AI Model', color: 'text-purple-600', bg: 'bg-purple-50' },
    { label: 'Average Score', value: `${data?.avg_score || 0}%`, icon: Target, change: 'Benchmark: 80%', color: 'text-amber-600', bg: 'bg-amber-50' },
    { label: 'Peak Score', value: `${data?.best_score || 0}%`, icon: Trophy, change: 'Highest Recorded', color: 'text-emerald-600', bg: 'bg-emerald-50' },
    { label: 'High Potential', value: data?.optimized_count || 0, icon: Sparkles, change: 'Optimized Candidates', color: 'text-blue-600', bg: 'bg-blue-50' },
  ];

  const pieCategories = [
    { name: 'Real Estate', percent: 35, color: 'bg-[#4353ff]' },
    { name: 'Finance & Wealth', percent: 25, color: 'bg-purple-600' },
    { name: 'Tech & AI', percent: 20, color: 'bg-emerald-600' },
    { name: 'Fitness & Health', percent: 12, color: 'bg-amber-500' },
    { name: 'Education', percent: 8, color: 'bg-pink-500' },
  ];

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto font-sans">
      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-xs font-semibold text-rose-700">
          ⚠️ Note: System offline fallback active.
        </div>
      )}

      {/* Memberstack Hero Banner */}
      <div className="card-saas p-8 bg-gradient-to-r from-[#1a1a2e] via-[#242442] to-[#4353ff] text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative overflow-hidden shadow-xl shadow-[#4353ff]/10">
        <div className="space-y-2 z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-xs font-semibold text-white">
            <Zap className="w-3.5 h-3.5 text-amber-300 fill-current" />
            AI Script Generation & Optimization Engine v2.0
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">
            Create Viral Reel Scripts in Seconds
          </h1>
          <p className="text-xs text-slate-200 leading-relaxed">
            Generate, analyze, and optimize short-form video scripts using Grammarly-style prompt enhancement, multi-candidate AI iteration, and quantitative score prediction.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3 z-10 w-full md:w-auto">
          <button
            onClick={() => setCurrentView('generate')}
            className="py-3 px-6 bg-white hover:bg-slate-100 text-[#4353ff] font-extrabold rounded-2xl text-xs transition-all shadow-lg shadow-black/10 flex items-center justify-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            Generate Scripts
          </button>
          <button
            onClick={() => setCurrentView('analyze')}
            className="py-3 px-6 bg-white/10 hover:bg-white/20 text-white font-bold rounded-2xl text-xs transition-all border border-white/20 flex items-center justify-center gap-2"
          >
            Analyze Draft
          </button>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-5">
        {metrics.map((m, idx) => {
          const Icon = m.icon;
          return (
            <div key={idx} className="card-saas p-5 flex flex-col justify-between">
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">{m.label}</span>
                <div className={`w-8 h-8 rounded-xl ${m.bg} ${m.color} flex items-center justify-center`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div>
                <div className="text-2xl font-extrabold text-[#1a1a2e] tracking-tight">{m.value}</div>
                <div className="text-[11px] font-semibold text-slate-500 mt-1 flex items-center gap-1">
                  <TrendingUp className="w-3 h-3 text-emerald-500" />
                  {m.change}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Charts & History Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Table Column */}
        <div className="lg:col-span-2 card-saas p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h3 className="font-bold text-[#1a1a2e] text-base">Recent Script Analyses</h3>
              <p className="text-xs text-slate-400">Quantitative evaluations and viral potential ratings</p>
            </div>
            <button 
              onClick={() => setCurrentView('analyze')}
              className="text-xs font-bold text-[#4353ff] hover:underline flex items-center gap-1"
            >
              Analyze New <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-[#f8f9fc] text-slate-400 font-bold uppercase text-[10px] tracking-wider border-b border-slate-100">
                <tr>
                  <th className="py-3 px-4">Script Title</th>
                  <th className="py-3 px-4">Quality Score</th>
                  <th className="py-3 px-4">Retention Rating</th>
                  <th className="py-3 px-4">Final Score</th>
                  <th className="py-3 px-4">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {data?.recent_predictions?.length > 0 ? (
                  data.recent_predictions.map((p, idx) => (
                    <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                      <td className="py-3.5 px-4 font-semibold text-[#1a1a2e]">{p.script_title || 'Untitled Script'}</td>
                      <td className="py-3.5 px-4 text-purple-600 font-bold">{p.ml_score}%</td>
                      <td className="py-3.5 px-4 text-[#4353ff] font-bold">{p.ann_score}%</td>
                      <td className="py-3.5 px-4">
                        <span className="font-extrabold text-[#1a1a2e]">{p.final_score}%</span>
                      </td>
                      <td className="py-3.5 px-4">
                        <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                          p.final_score >= 80 
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' 
                            : 'bg-amber-50 text-amber-700 border border-amber-200'
                        }`}>
                          {p.status}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="py-6 text-center text-slate-400">
                      No script analyses recorded yet. Run your first analysis!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Category Breakdown Progress Bars */}
        <div className="card-saas p-6 space-y-5 flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-[#1a1a2e] text-base">Category Distribution</h3>
            <p className="text-xs text-slate-400">Content niche breakdown</p>
          </div>

          <div className="space-y-4">
            {pieCategories.map((item, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex justify-between text-xs font-semibold text-slate-700">
                  <span>{item.name}</span>
                  <span>{item.percent}%</span>
                </div>
                <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div className={`h-full ${item.color} rounded-full`} style={{ width: `${item.percent}%` }} />
                </div>
              </div>
            ))}
          </div>

          <div className="pt-3 border-t border-slate-100 text-[11px] text-slate-400 font-medium">
            Based on benchmark high-conversion dataset
          </div>
        </div>
      </div>

      {/* Quick Actions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card-saas p-6 flex flex-col justify-between bg-gradient-to-br from-white to-slate-50">
          <div>
            <div className="w-10 h-10 rounded-2xl bg-[#4353ff] text-white flex items-center justify-center mb-4 shadow-md shadow-[#4353ff]/20">
              <Microscope className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-[#1a1a2e] text-lg">Analyze Draft Script</h4>
            <p className="text-xs text-slate-500 mt-1">Paste any raw draft to extract features and predict engagement score.</p>
          </div>
          <button
            onClick={() => setCurrentView('analyze')}
            className="mt-6 w-full py-3 px-4 bg-[#4353ff] hover:bg-[#3242e0] text-white font-extrabold rounded-2xl text-xs transition-all shadow-md shadow-[#4353ff]/20 flex items-center justify-center gap-2"
          >
            Launch Analyzer <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div className="card-saas p-6 flex flex-col justify-between bg-gradient-to-br from-white to-slate-50">
          <div>
            <div className="w-10 h-10 rounded-2xl bg-purple-600 text-white flex items-center justify-center mb-4 shadow-md shadow-purple-500/20">
              <Sparkles className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-[#1a1a2e] text-lg">AI Script Generator</h4>
            <p className="text-xs text-slate-500 mt-1">Enhance raw topics and discover peak scoring candidates automatically.</p>
          </div>
          <button
            onClick={() => setCurrentView('generate')}
            className="mt-6 w-full py-3 px-4 bg-purple-600 hover:bg-purple-700 text-white font-extrabold rounded-2xl text-xs transition-all shadow-md shadow-purple-500/20 flex items-center justify-center gap-2"
          >
            Launch Generator <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div className="card-saas p-6 flex flex-col justify-between bg-gradient-to-br from-white to-slate-50">
          <div>
            <div className="w-10 h-10 rounded-2xl bg-emerald-600 text-white flex items-center justify-center mb-4 shadow-md shadow-emerald-500/20">
              <BookOpen className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-[#1a1a2e] text-lg">Viral Library</h4>
            <p className="text-xs text-slate-500 mt-1">Explore high-engagement benchmark script templates and structural hooks.</p>
          </div>
          <button
            onClick={() => setCurrentView('library')}
            className="mt-6 w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold rounded-2xl text-xs transition-all shadow-md shadow-emerald-500/20 flex items-center justify-center gap-2"
          >
            Browse Library <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
