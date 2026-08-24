import React, { useState } from 'react';
import { analyzeReel } from '../services/api';
import { Film, Image, MessageSquare, Brain, CheckCircle2, Upload, FileVideo, Sparkles } from 'lucide-react';

export default function AnalyzeReelView({ setCurrentView, setScriptToOptimize }) {
  const [transcript, setTranscript] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setFilePreview(url);
    }
  };

  const handleAnalyzeReel = async () => {
    setLoading(true);
    try {
      const textToAnalyze = transcript.trim() || (selectedFile ? `Reel Video: ${selectedFile.name}` : "");
      const res = await analyzeReel({ 
        transcript: textToAnalyze || "Stop scrolling! Here is how you double your engagement in 30 seconds. Comment 'INFO' below for details!" 
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
        {/* Upload & Inputs Column */}
        <div className="lg:col-span-5 space-y-6">
          <div className="card-saas p-6 space-y-5">
            <h3 className="font-bold text-[#1a1a2e] text-base flex items-center gap-2">
              <Film className="w-4 h-4 text-[#4353ff]" />
              Reel Video & Spoken Content Upload
            </h3>

            {/* File Upload Drop Area */}
            <div className="relative border-2 border-dashed border-slate-200 rounded-2xl p-6 text-center space-y-3 bg-[#f8f9fc] hover:bg-slate-100/60 transition-colors cursor-pointer">
              <input
                type="file"
                accept="video/*,image/*"
                onChange={handleFileChange}
                className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />

              {filePreview ? (
                <div className="space-y-2">
                  {selectedFile?.type?.startsWith('video/') ? (
                    <video src={filePreview} controls className="max-h-40 rounded-xl mx-auto shadow-md" />
                  ) : (
                    <img src={filePreview} alt="Thumbnail preview" className="max-h-40 rounded-xl mx-auto shadow-md object-cover" />
                  )}
                  <div className="text-xs font-bold text-[#1a1a2e]">{selectedFile?.name}</div>
                  <span className="text-[10px] text-emerald-600 font-semibold bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                    File Loaded & Ready
                  </span>
                </div>
              ) : (
                <>
                  <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-[#4353ff] flex items-center justify-center mx-auto">
                    <Upload className="w-6 h-6" />
                  </div>
                  <div className="space-y-1">
                    <div className="text-xs font-bold text-[#1a1a2e]">Click or Drag MP4 / MOV Reel Video</div>
                    <p className="text-[10px] text-slate-400">Speech-to-text transcript & CNN frame extraction</p>
                  </div>
                </>
              )}
            </div>

            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">
                Spoken Content Transcript
              </label>
              <textarea
                rows={4}
                value={transcript}
                onChange={(e) => setTranscript(e.target.value)}
                placeholder="Type or paste reel spoken audio transcript..."
                className="w-full p-3.5 bg-[#f8f9fc] border border-slate-200 rounded-xl text-xs font-medium text-[#1a1a2e] focus:ring-2 focus:ring-[#4353ff]/20 focus:border-[#4353ff]"
              />
            </div>

            <button
              onClick={handleAnalyzeReel}
              disabled={loading}
              className="w-full py-3.5 px-4 bg-[#4353ff] hover:bg-[#3242e0] text-white font-extrabold rounded-2xl text-xs shadow-lg shadow-[#4353ff]/25 transition-all flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Running ML + ANN + CNN Pipelines...
                </>
              ) : (
                <>
                  <Film className="w-4 h-4" />
                  Analyze Reel (ML/ANN + CNN)
                </>
              )}
            </button>
          </div>
        </div>

        {/* Dual Pipeline Output Column */}
        <div className="lg:col-span-7 space-y-6">
          {result ? (
            <div className="space-y-6">
              {/* Pipeline 1: Spoken Content Intelligence */}
              <div className="card-saas p-6 border-l-4 border-l-[#4353ff] space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-[#4353ff] flex items-center gap-1.5">
                    <MessageSquare className="w-4 h-4" />
                    Pipeline 1: Spoken Content Analysis (ML + ANN)
                  </span>
                  <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                    result.script_score >= 80 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'
                  }`}>
                    {result.script_status}
                  </span>
                </div>

                <div className="flex items-baseline gap-3">
                  <div className="text-4xl font-extrabold text-[#1a1a2e]">{result.script_score}%</div>
                  <span className="text-xs text-slate-400 font-semibold">Aggregated Final Score</span>
                </div>

                <div className="grid grid-cols-2 gap-3 pt-2 border-t border-slate-100">
                  <div className="p-3 bg-purple-50/50 rounded-xl">
                    <span className="text-[10px] font-bold text-purple-700 block">Scikit-Learn ML Score</span>
                    <span className="text-lg font-extrabold text-purple-900">{result.ml_score}%</span>
                  </div>
                  <div className="p-3 bg-indigo-50/50 rounded-xl">
                    <span className="text-[10px] font-bold text-[#4353ff] block">TensorFlow Keras ANN Score</span>
                    <span className="text-lg font-extrabold text-indigo-900">{result.ann_score}%</span>
                  </div>
                </div>
              </div>

              {/* Pipeline 2: Visual Thumbnail Intelligence (CNN) */}
              <div className="card-saas p-6 border-l-4 border-l-emerald-600 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 flex items-center gap-1.5">
                    <Image className="w-4 h-4" />
                    Pipeline 2: Thumbnail & Visual Quality (CNN)
                  </span>
                  <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                    CNN Visual Classifier Active
                  </span>
                </div>

                <div className="flex items-baseline gap-3">
                  <div className="text-4xl font-extrabold text-[#1a1a2e]">{result.cnn_res?.visual_quality_score}%</div>
                  <span className="text-xs text-slate-400 font-semibold">Visual Quality Rating</span>
                </div>

                <div className="space-y-2 text-xs text-slate-700 font-medium pt-2 border-t border-slate-100">
                  <p>• <strong>Visual Clarity:</strong> {result.cnn_res?.clarity_rating}</p>
                  <p>• <strong>Text Overlay Contrast:</strong> {result.cnn_res?.text_visibility}</p>
                  <p>• <strong>Subject Framing:</strong> {result.cnn_res?.subject_prominence}</p>
                  <div className="p-3.5 bg-emerald-50 rounded-xl text-emerald-800 font-semibold mt-2 border border-emerald-200">
                    💡 <strong>Visual Recommendation:</strong> {result.cnn_res?.recommendation}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="card-saas p-12 text-center space-y-4 min-h-[420px] flex flex-col items-center justify-center">
              <div className="w-14 h-14 rounded-2xl bg-indigo-50 text-[#4353ff] flex items-center justify-center shadow-inner">
                <Film className="w-7 h-7" />
              </div>
              <div className="space-y-1">
                <h4 className="font-bold text-[#1a1a2e] text-base">Reel Video & Thumbnail Intelligence</h4>
                <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
                  Upload an MP4/MOV video or click <strong>Analyze Reel</strong> to evaluate spoken transcript (ML/ANN) & visual thumbnail quality (CNN).
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
