import React, { useState } from 'react';
import { analyzeScript } from '../services/api';
import { Microscope, Brain, Target, Sparkles, CheckCircle2, ArrowRight, Video, MessageSquare } from 'lucide-react';

export default function AnalyzeScriptView({ setCurrentView, setScriptToOptimize }) {
  const [title, setTitle] = useState("");
  const [hookText, setHookText] = useState("");
  const [bodyText, setBodyText] = useState("");
  const [ctaText, setCtaText] = useState("");
  
  const [category, setCategory] = useState("Real Estate");
  const [platform, setPlatform] = useState("Instagram Reels");
  const [duration, setDuration] = useState(30);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    // Combine 3 textboxes into full script
    const combinedScript = `Hook (0-3s): ${hookText}\nScript Body (3-25s): ${bodyText}\nCall To Action (25-30s): ${ctaText}`.trim();
    if (!combinedScript) return;

    setLoading(true);
    try {
      const res = await analyzeScript({
        title: title.trim() || "My Reel Script",
        script_text: combinedScript,
        category,
        audience: "General",
        platform,
        duration: Number(duration)
      });
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 font-sans">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Input Column - 3 Distinct Text Boxes */}
        <div className="lg:col-span-6 space-y-6">
          <div className="card-saas p-6 space-y-5">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-[#1a1a2e] text-base flex items-center gap-2">
                <Microscope className="w-4 h-4 text-[#4353ff]" />
                Structured Script Analyzer
              </h3>
              <span className="text-[10px] font-extrabold uppercase text-[#4353ff] bg-indigo-50 px-2.5 py-1 rounded-full">
                ML + ANN Active
              </span>
            </div>

            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">
                Script Title
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter title..."
                className="w-full p-3 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-semibold text-[#1a1a2e] focus:ring-2 focus:ring-[#4353ff]/20 focus:border-[#4353ff]"
              />
            </div>

            {/* 1. Hook Text Box */}
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-[#4353ff] mb-1 flex items-center gap-1.5">
                🪝 1. Hook (First 0 - 3 Seconds)
              </label>
              <textarea
                rows={2}
                value={hookText}
                onChange={(e) => setHookText(e.target.value)}
                placeholder="Type your opening hook line here..."
                className="w-full p-3 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-medium text-[#1a1a2e] focus:ring-2 focus:ring-[#4353ff]/20 focus:border-[#4353ff]"
              />
            </div>

            {/* 2. Script Body Text Box */}
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-purple-600 mb-1 flex items-center gap-1.5">
                🎬 2. Main Script Body (3 - 25 Seconds)
              </label>
              <textarea
                rows={4}
                value={bodyText}
                onChange={(e) => setBodyText(e.target.value)}
                placeholder="Type your main value-driven body text here..."
                className="w-full p-3 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-medium text-[#1a1a2e] focus:ring-2 focus:ring-[#4353ff]/20 focus:border-[#4353ff]"
              />
            </div>

            {/* 3. CTA Text Box */}
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-emerald-600 mb-1 flex items-center gap-1.5">
                📢 3. Call To Action / CTA (25 - 30 Seconds)
              </label>
              <textarea
                rows={2}
                value={ctaText}
                onChange={(e) => setCtaText(e.target.value)}
                placeholder="Type your CTA (e.g. comment 'HOME' for DM details)..."
                className="w-full p-3 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-medium text-[#1a1a2e] focus:ring-2 focus:ring-[#4353ff]/20 focus:border-[#4353ff]"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Category</label>
                <select value={category} onChange={(e) => setCategory(e.target.value)} className="w-full p-2.5 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-semibold text-[#1a1a2e]">
                  <option>Real Estate</option>
                  <option>Finance & Wealth</option>
                  <option>Tech & AI</option>
                  <option>Fitness & Health</option>
                  <option>E-commerce</option>
                  <option>Education</option>
                </select>
              </div>
              <div>
                <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Target Duration</label>
                <input type="number" value={duration} onChange={(e) => setDuration(e.target.value)} className="w-full p-2.5 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-semibold text-[#1a1a2e]" />
              </div>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={loading || (!hookText.trim() && !bodyText.trim() && !ctaText.trim())}
              className="w-full py-3.5 px-4 bg-[#4353ff] hover:bg-[#3242e0] text-white font-extrabold rounded-2xl text-xs shadow-lg shadow-[#4353ff]/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Calculating Predictions & Feature Vectors...
                </>
              ) : (
                <>
                  <Brain className="w-4 h-4" />
                  Analyze Script Performance
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Diagnosis Column */}
        <div className="lg:col-span-6 space-y-6">
          {result ? (
            <div className="space-y-6">
              {/* Score Header Card */}
              <div className={`card-saas p-6 border-l-4 ${
                result.final_score >= 80 ? 'border-l-emerald-500' : 'border-l-amber-500'
              }`}>
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Overall Predicted Performance</span>
                    <div className="text-4xl font-extrabold text-[#1a1a2e] tracking-tight mt-1">{result.final_score}%</div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    result.final_score >= 80 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'
                  }`}>
                    {result.status}
                  </span>
                </div>
              </div>

              {/* Dual Model Score Split */}
              <div className="grid grid-cols-2 gap-4">
                <div className="card-saas p-5 bg-purple-50/50 border-purple-100">
                  <span className="text-xs font-bold text-purple-700">Quality Score</span>
                  <div className="text-3xl font-extrabold text-purple-900 mt-1">{result.ml_score}%</div>
                  <span className="text-[10px] text-purple-600 font-semibold">Structure & Keywords</span>
                </div>
                <div className="card-saas p-5 bg-indigo-50/50 border-indigo-100">
                  <span className="text-xs font-bold text-[#4353ff]">Retention Score</span>
                  <div className="text-3xl font-extrabold text-indigo-900 mt-1">{result.ann_score}%</div>
                  <span className="text-[10px] text-indigo-600 font-semibold">Viewer Pacing</span>
                </div>
              </div>

              {/* Clean Human Analysis Cards */}
              <div className="card-saas p-6 space-y-4">
                <h4 className="font-bold text-[#1a1a2e] text-sm flex items-center gap-2">
                  <Brain className="w-4 h-4 text-[#4353ff]" />
                  Script Analysis Breakdown
                </h4>
                
                <div className="space-y-3 text-xs text-slate-700 font-medium">
                  <div className="p-3 bg-[#f8f9fc] rounded-xl border border-slate-100 space-y-1">
                    <span className="font-bold text-[#4353ff] block">🪝 Hook Analysis</span>
                    <p>{result.analysis_data?.hook_critique || "Hook is clear and direct."}</p>
                  </div>
                  <div className="p-3 bg-[#f8f9fc] rounded-xl border border-slate-100 space-y-1">
                    <span className="font-bold text-purple-600 block">⏱️ Body Pacing</span>
                    <p>{result.analysis_data?.body_pacing || "Good information flow and value delivery."}</p>
                  </div>
                  <div className="p-3 bg-[#f8f9fc] rounded-xl border border-slate-100 space-y-1">
                    <span className="font-bold text-emerald-600 block">🎯 CTA Conversion</span>
                    <p>{result.analysis_data?.cta_strength || "Call to action provides clear next step."}</p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="card-saas p-12 text-center space-y-4 min-h-[420px] flex flex-col items-center justify-center">
              <div className="w-14 h-14 rounded-2xl bg-indigo-50 text-[#4353ff] flex items-center justify-center shadow-inner">
                <Brain className="w-7 h-7" />
              </div>
              <div className="space-y-1">
                <h4 className="font-bold text-[#1a1a2e] text-base">Awaiting Script Input</h4>
                <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
                  Enter your Hook, Script Body, and CTA on the left and click <strong>Analyze Script Performance</strong>.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
