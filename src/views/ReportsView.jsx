import React, { useEffect, useState } from 'react';
import { fetchUserScripts, generateReport } from '../services/api';
import { FileText, Download, Sparkles } from 'lucide-react';

export default function ReportsView() {
  const [scripts, setScripts] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [reportMd, setReportMd] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUserScripts().then(res => {
      setScripts(res);
      if (res.length > 0) setSelectedId(res[0].id);
    }).catch(console.error);
  }, []);

  const handleGenerateReport = async () => {
    if (!selectedId) return;
    setLoading(true);
    try {
      const res = await generateReport({ script_id: Number(selectedId) });
      setReportMd(res.report_markdown);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <div className="card-saas p-6 space-y-4">
        <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
          <FileText className="w-4 h-4 text-indigo-600" />
          Generate Performance Report
        </h3>

        <div className="flex gap-3">
          <select
            value={selectedId}
            onChange={(e) => setSelectedId(e.target.value)}
            className="flex-1 p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800"
          >
            {scripts.map((s) => (
              <option key={s.id} value={s.id}>#{s.id} — {s.title}</option>
            ))}
          </select>

          <button
            onClick={handleGenerateReport}
            disabled={loading}
            className="py-2.5 px-5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs transition-all"
          >
            {loading ? 'Generating...' : 'Generate Report'}
          </button>
        </div>
      </div>

      {reportMd && (
        <div className="card-saas p-6 space-y-4 animate-fadeIn">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <span className="text-xs font-bold uppercase text-slate-400">Generated Markdown Audit Report</span>
            <a
              href={`data:text/markdown;charset=utf-8,${encodeURIComponent(reportMd)}`}
              download="ViralIQ_Script_Report.md"
              className="py-1.5 px-3 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 font-bold rounded-lg text-xs flex items-center gap-1.5 transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              Download (.md)
            </a>
          </div>

          <div className="p-4 bg-slate-900 text-slate-100 rounded-xl font-mono text-xs leading-relaxed whitespace-pre-wrap">
            {reportMd}
          </div>
        </div>
      )}
    </div>
  );
}
