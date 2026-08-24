import React, { useState } from 'react';
import { Settings, Key, Sliders, ShieldCheck } from 'lucide-react';

export default function SettingsView() {
  const [apiKey, setApiKey] = useState("");
  const [scoreMethod, setScoreMethod] = useState("weighted_average");
  const [mlWeight, setMlWeight] = useState(0.5);

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6 font-sans">
      {/* API Key Configuration */}
      <div className="card-saas p-6 space-y-4">
        <h3 className="font-bold text-[#1a1a2e] text-base flex items-center gap-2">
          <Key className="w-4 h-4 text-[#4353ff]" />
          Gemini API Configuration
        </h3>

        <div>
          <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">
            Custom GEMINI_API_KEY (Optional)
          </label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter custom Gemini API key..."
            className="w-full p-3 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-mono text-[#1a1a2e] focus:ring-2 focus:ring-[#4353ff]/20 focus:border-[#4353ff]"
          />
        </div>

        <div className="flex items-center gap-2 text-xs font-semibold text-emerald-600 bg-emerald-50 border border-emerald-200 p-3.5 rounded-xl">
          <ShieldCheck className="w-4 h-4" />
          <span>Server-Side API Key Active & Secured via Environment Variables</span>
        </div>
      </div>

      {/* Aggregation Settings */}
      <div className="card-saas p-6 space-y-4">
        <h3 className="font-bold text-[#1a1a2e] text-base flex items-center gap-2">
          <Sliders className="w-4 h-4 text-purple-600" />
          Score Aggregation Layer
        </h3>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Aggregation Method</label>
            <select value={scoreMethod} onChange={(e) => setScoreMethod(e.target.value)} className="w-full p-2.5 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-semibold text-[#1a1a2e]">
              <option value="weighted_average">Weighted Average</option>
              <option value="harmonic_mean">Harmonic Mean</option>
              <option value="min">Conservative (Min)</option>
              <option value="max">Optimistic (Max)</option>
            </select>
          </div>

          <div>
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">ML vs ANN Weight Ratio</label>
            <input type="range" min="0" max="1" step="0.05" value={mlWeight} onChange={(e) => setMlWeight(e.target.value)} className="w-full" />
            <span className="text-xs font-bold text-slate-700">{Math.round(mlWeight * 100)}% ML / {Math.round((1 - mlWeight) * 100)}% ANN</span>
          </div>
        </div>
      </div>
    </div>
  );
}
