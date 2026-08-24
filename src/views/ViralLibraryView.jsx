import React, { useEffect, useState } from 'react';
import { fetchViralLibrary, addViralScript } from '../services/api';
import { BookOpen, Search, Sparkles, Plus, Eye, ThumbsUp, MessageSquare, Share2 } from 'lucide-react';

export default function ViralLibraryView({ setCurrentView, setScriptToOptimize }) {
  const [items, setItems] = useState([]);
  const [category, setCategory] = useState("All");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const loadData = () => {
    setLoading(true);
    fetchViralLibrary(category, search)
      .then(res => {
        setItems(res);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadData();
  }, [category, search]);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Search & Filter Header */}
      <div className="card-saas p-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="relative flex-1 md:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search topic, hook, or keyword..."
              className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-900 focus:ring-2 focus:ring-indigo-500/20"
            />
          </div>

          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800"
          >
            <option>All</option>
            <option>Real Estate</option>
            <option>Finance & Wealth</option>
            <option>Tech & AI</option>
            <option>Fitness & Health</option>
            <option>E-commerce</option>
            <option>Education & Career</option>
          </select>
        </div>

        <span className="text-xs font-bold text-slate-400">
          Showing {items.length} Benchmark Templates
        </span>
      </div>

      {/* Script Grid */}
      {loading ? (
        <div className="p-12 text-center text-indigo-600 font-semibold">Loading Library Knowledge...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {items.map((item) => (
            <div key={item.id} className="card-saas p-6 space-y-4 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-600 border border-indigo-200">
                    {item.category}
                  </span>
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                    ⚡ {item.engagement_rate}% ER
                  </span>
                </div>

                <h4 className="font-bold text-slate-900 text-base">{item.topic}</h4>
                <p className="text-xs text-slate-400 font-medium">Audience: {item.audience} • {item.duration}s</p>

                <div className="mt-3 p-3 bg-slate-50 border border-slate-200/80 rounded-xl space-y-1 text-xs">
                  <span className="font-bold text-indigo-600">🪝 Hook:</span>
                  <p className="text-slate-800 font-medium italic">"{item.hook}"</p>
                  <p className="text-slate-600 pt-1 border-t border-slate-200/60 leading-relaxed">
                    {item.script_text}
                  </p>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400 font-semibold">
                <div className="flex items-center gap-3">
                  <span>👁️ {item.views?.toLocaleString()}</span>
                  <span>❤️ {item.likes?.toLocaleString()}</span>
                  <span>💬 {item.comments?.toLocaleString()}</span>
                </div>
                <button
                  onClick={() => {
                    if (setScriptToOptimize) setScriptToOptimize(item.hook);
                    setCurrentView('generate');
                  }}
                  className="py-1.5 px-3 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 font-bold rounded-lg text-xs transition-colors flex items-center gap-1"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  Use as Reference
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
