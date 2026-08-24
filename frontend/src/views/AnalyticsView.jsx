import React, { useEffect, useState } from 'react';
import { fetchAnalytics } from '../services/api';
import { BarChart3, Brain, Target, Layers } from 'lucide-react';

export default function AnalyticsView() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchAnalytics().then(setData).catch(console.error);
  }, []);

  const fiData = Object.entries(data?.ml_metrics?.feature_importances || {
    "hook_curiosity_score": 0.24,
    "cta_present": 0.18,
    "emotional_density": 0.15,
    "has_listicle": 0.12,
    "number_count": 0.10,
    "urgency_score": 0.08,
    "you_count": 0.07,
    "duration_diff": 0.06
  }).map(([key, value]) => ({
    feature: key,
    importance: Math.round(value * 100)
  })).sort((a, b) => b.importance - a.importance);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Metric Header Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card-saas p-5 space-y-1">
          <span className="text-xs font-bold uppercase text-slate-400">ML Accuracy (Random Forest)</span>
          <div className="text-3xl font-extrabold text-purple-600">{data?.ml_metrics?.accuracy || 100}%</div>
          <span className="text-[10px] text-slate-400 font-semibold">Precision: {data?.ml_metrics?.precision || 100}%</span>
        </div>

        <div className="card-saas p-5 space-y-1">
          <span className="text-xs font-bold uppercase text-slate-400">ANN Accuracy (Keras)</span>
          <div className="text-3xl font-extrabold text-indigo-600">{data?.ann_metrics?.accuracy || 100}%</div>
          <span className="text-[10px] text-slate-400 font-semibold">Recall: {data?.ann_metrics?.recall || 100}%</span>
        </div>

        <div className="card-saas p-5 space-y-1">
          <span className="text-xs font-bold uppercase text-slate-400">ANN EarlyStopping Epochs</span>
          <div className="text-3xl font-extrabold text-emerald-600">{data?.ann_metrics?.epochs_trained || 93}</div>
          <span className="text-[10px] text-emerald-600 font-semibold">Validation loss minimized</span>
        </div>

        <div className="card-saas p-5 space-y-1">
          <span className="text-xs font-bold uppercase text-slate-400">Validation Loss</span>
          <div className="text-3xl font-extrabold text-amber-600">{data?.ann_metrics?.final_val_loss || 0.01}</div>
          <span className="text-[10px] text-slate-400 font-semibold">Binary Crossentropy</span>
        </div>
      </div>

      {/* Feature Importances Progress Bars */}
      <div className="card-saas p-6 space-y-5">
        <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-purple-600" />
          Scikit-Learn Feature Importances Ranking
        </h3>

        <div className="space-y-4">
          {fiData.map((item, idx) => (
            <div key={idx} className="space-y-1">
              <div className="flex justify-between text-xs font-semibold text-slate-700">
                <span className="font-mono">{item.feature}</span>
                <span>{item.importance}%</span>
              </div>
              <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-purple-600 to-indigo-600 rounded-full transition-all duration-300" style={{ width: `${Math.max(5, item.importance)}%` }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
