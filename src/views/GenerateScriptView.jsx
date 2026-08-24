import React, { useState } from 'react';
import { enhancePrompt, generateCandidates } from '../services/api';
import { Sparkles, Copy, Check, Play, Trophy, Layers, Video, ArrowRight } from 'lucide-react';

export default function GenerateScriptView({ scriptToOptimize }) {
  // Clean initial state (no unwanted pre-filled text)
  const [informalText, setInformalText] = useState(scriptToOptimize || "");
  const [category, setCategory] = useState("Real Estate");
  const [audience, setAudience] = useState("First-time Buyers");
  const [platform, setPlatform] = useState("Instagram Reels");
  const [duration, setDuration] = useState(30);

  const [batchSize, setBatchSize] = useState(3);
  const [targetScore, setTargetScore] = useState(80);
  const [maxBatches, setMaxBatches] = useState(3);

  const [enhancing, setEnhancing] = useState(false);
  const [enhancedPrompt, setEnhancedPrompt] = useState("");
  const [copied, setCopied] = useState(false);

  const [generating, setGenerating] = useState(false);
  const [optimizationResult, setOptimizationResult] = useState(null);

  // OPTIONAL Prompt Enhancement
  const handleEnhance = async () => {
    if (!informalText.trim()) return;
    setEnhancing(true);
    try {
      const res = await enhancePrompt({
        informal_prompt: informalText,
        category,
        audience,
        platform,
        duration: Number(duration)
      });
      setEnhancedPrompt(res.enhanced_prompt);
    } catch (err) {
      console.error(err);
    } finally {
      setEnhancing(false);
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Direct Generation (Enhancer is purely OPTIONAL)
  const handleGenerate = async () => {
    if (!informalText.trim() && !enhancedPrompt.trim()) return;
    
    setGenerating(true);
    // Use enhanced prompt if generated, otherwise use raw user input directly!
    const promptToUse = enhancedPrompt.trim() ? enhancedPrompt : informalText;

    try {
      const res = await generateCandidates({
        enhanced_prompt: promptToUse,
        category,
        batch_size: Number(batchSize),
        target_score: Number(targetScore),
        max_batches: Number(maxBatches)
      });
      setOptimizationResult(res.optimization_result);
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const best = optimizationResult?.global_best;

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 font-sans">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Input & Prompt Controls Column */}
        <div className="lg:col-span-5 space-y-6">
          <div className="card-saas p-6 space-y-4">
            <h3 className="font-bold text-[#1a1a2e] text-base flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#4353ff]" />
              AI Script Studio Generator
            </h3>

            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">
                Script Topic or Idea
              </label>
              <textarea
                rows={3}
                value={informalText}
                onChange={(e) => setInformalText(e.target.value)}
                placeholder="Type your script topic here (e.g. 2BHK flat under 50 Lakhs in Surat)..."
                className="w-full p-3.5 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-medium text-[#1a1a2e] focus:ring-2 focus:ring-[#4353ff]/20 focus:border-[#4353ff] transition-all"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
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
                <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Platform</label>
                <select value={platform} onChange={(e) => setPlatform(e.target.value)} className="w-full p-2.5 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-semibold text-[#1a1a2e]">
                  <option>Instagram Reels</option>
                  <option>YouTube Shorts</option>
                  <option>TikTok</option>
                </select>
              </div>
            </div>

            {/* Direct Generation Primary Button */}
            <button
              onClick={handleGenerate}
              disabled={generating || (!informalText.trim() && !enhancedPrompt.trim())}
              className="w-full py-3.5 px-4 bg-[#4353ff] hover:bg-[#3242e0] text-white font-extrabold rounded-2xl text-xs shadow-lg shadow-[#4353ff]/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {generating ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Generating High-Converting Reel Script...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-current text-white" />
                  Generate Reel Script Now
                </>
              )}
            </button>

            {/* OPTIONAL Prompt Enhancer Helper Button */}
            <div className="pt-2 border-t border-slate-100">
              <button
                onClick={handleEnhance}
                disabled={enhancing || !informalText.trim()}
                className="w-full py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-[#1a1a2e] font-bold rounded-xl text-xs transition-all flex items-center justify-center gap-2 text-slate-600 hover:text-[#4353ff]"
              >
                {enhancing ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-[#4353ff] border-t-transparent rounded-full animate-spin" />
                    Enhancing Prompt...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-3.5 h-3.5 text-[#4353ff]" />
                    ✨ Enhance Prompt (Optional Helper)
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Enhanced Prompt Preview (Optional) */}
          {enhancedPrompt && (
            <div className="card-saas p-6 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-[#4353ff]">Enhanced Prompt Preview (Optional)</span>
                <button onClick={() => handleCopy(enhancedPrompt)} className="text-xs font-semibold text-slate-500 hover:text-slate-900 flex items-center gap-1">
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                  {copied ? 'Copied' : 'Copy'}
                </button>
              </div>
              <textarea
                rows={6}
                value={enhancedPrompt}
                onChange={(e) => setEnhancedPrompt(e.target.value)}
                className="w-full p-3.5 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-mono leading-relaxed text-[#1a1a2e]"
              />
            </div>
          )}

          {/* Advanced Optimization Options */}
          <div className="card-saas p-5 space-y-3">
            <h4 className="font-bold text-[#1a1a2e] text-[11px] uppercase tracking-wider flex items-center gap-2">
              <Layers className="w-3.5 h-3.5 text-[#4353ff]" />
              Optimization Batch Parameters
            </h4>
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-[10px] font-bold text-slate-400">Candidates</label>
                <input type="number" value={batchSize} onChange={(e) => setBatchSize(e.target.value)} className="w-full p-2 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-semibold text-[#1a1a2e]" />
              </div>
              <div>
                <label className="block text-[10px] font-bold text-slate-400">Target Score</label>
                <input type="number" value={targetScore} onChange={(e) => setTargetScore(e.target.value)} className="w-full p-2 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-semibold text-[#1a1a2e]" />
              </div>
              <div>
                <label className="block text-[10px] font-bold text-slate-400">Max Batches</label>
                <input type="number" value={maxBatches} onChange={(e) => setMaxBatches(e.target.value)} className="w-full p-2 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-semibold text-[#1a1a2e]" />
              </div>
            </div>
          </div>
        </div>

        {/* Output Column */}
        <div className="lg:col-span-7 space-y-6">
          {best ? (
            <div className="space-y-6">
              {/* Winner Header Card */}
              <div className="card-saas p-6 border-l-4 border-l-emerald-500 bg-gradient-to-br from-white via-[#f8f9fc] to-indigo-50/20">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-2xl bg-emerald-600 text-white flex items-center justify-center shadow-md shadow-emerald-500/20">
                      <Trophy className="w-5 h-5" />
                    </div>
                    <div>
                      <span className="text-[11px] font-extrabold uppercase tracking-wider text-emerald-700">Winning Reel Script</span>
                      <h3 className="text-2xl font-extrabold text-[#1a1a2e]">Score: {best.final_score}%</h3>
                    </div>
                  </div>
                  <div>
                    <button
                      onClick={() => handleCopy(best.script_text)}
                      className="py-2.5 px-4 bg-[#4353ff] hover:bg-[#3242e0] text-white font-bold rounded-xl text-xs shadow-md shadow-[#4353ff]/20 flex items-center gap-1.5"
                    >
                      <Copy className="w-3.5 h-3.5" />
                      Copy Winning Script
                    </button>
                  </div>
                </div>

                {/* Structured Script Output Box */}
                <div className="mt-6 space-y-4">
                  <div className="p-5 bg-[#1a1a2e] text-white rounded-2xl space-y-2 border border-slate-800 shadow-md">
                    <div className="flex items-center justify-between text-xs font-bold text-slate-300">
                      <span className="flex items-center gap-1.5 text-amber-400">
                        <Video className="w-4 h-4" />
                        Script Output Breakdown
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono">Ready to Record</span>
                    </div>
                    <div className="text-xs leading-relaxed font-sans text-slate-100 whitespace-pre-wrap">
                      {best.script_text}
                    </div>
                  </div>
                </div>
              </div>

              {/* Candidate Evaluation Table */}
              <div className="card-saas p-6 space-y-4">
                <h4 className="font-bold text-[#1a1a2e] text-sm">Batch Progression & Candidate Scores</h4>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-600">
                    <thead className="bg-[#f8f9fc] text-slate-400 font-bold uppercase text-[10px] tracking-wider border-b border-slate-100">
                      <tr>
                        <th className="py-3 px-4">Batch</th>
                        <th className="py-3 px-4">Candidate</th>
                        <th className="py-3 px-4">Quality Score</th>
                        <th className="py-3 px-4">Retention Rating</th>
                        <th className="py-3 px-4">Final Score</th>
                        <th className="py-3 px-4">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 font-medium">
                      {optimizationResult?.all_candidates?.map((c, idx) => (
                        <tr key={idx} className={c.final_score === best.final_score ? 'bg-emerald-50/60 font-bold' : ''}>
                          <td className="py-3 px-4">#{c.batch_number}</td>
                          <td className="py-3 px-4">#{c.candidate_number}</td>
                          <td className="py-3 px-4 text-purple-600">{c.ml_score}%</td>
                          <td className="py-3 px-4 text-[#4353ff]">{c.ann_score}%</td>
                          <td className="py-3 px-4 text-[#1a1a2e] font-bold">{c.final_score}%</td>
                          <td className="py-3 px-4">
                            <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700">
                              {c.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          ) : (
            <div className="card-saas p-12 text-center space-y-4 min-h-[420px] flex flex-col items-center justify-center">
              <div className="w-14 h-14 rounded-2xl bg-indigo-50 text-[#4353ff] flex items-center justify-center shadow-inner">
                <Sparkles className="w-7 h-7" />
              </div>
              <div className="space-y-1">
                <h4 className="font-bold text-[#1a1a2e] text-base">Generate High-Converting Reel Scripts</h4>
                <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
                  Enter your topic above and click <strong>Generate Reel Script Now</strong> to generate AI candidates instantly.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
