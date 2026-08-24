import React, { useEffect, useState } from 'react';
import { fetchUserScripts, createScript, updateScript, deleteScript } from '../services/api';
import { FolderKanban, Plus, Trash2, Edit3, Save, X } from 'lucide-react';

export default function MyScriptsView() {
  const [scripts, setScripts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState(null);

  const [formTitle, setFormTitle] = useState("");
  const [formText, setFormText] = useState("");
  const [formCategory, setFormCategory] = useState("Real Estate");
  const [formAudience, setFormAudience] = useState("General");
  const [formPlatform, setFormPlatform] = useState("Instagram");
  const [formDuration, setFormDuration] = useState(30);

  const loadScripts = () => {
    setLoading(true);
    fetchUserScripts()
      .then(res => {
        setScripts(res);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadScripts();
  }, []);

  const handleCreate = async () => {
    if (!formTitle.trim() || !formText.trim()) return;
    try {
      await createScript({
        title: formTitle,
        script_text: formText,
        category: formCategory,
        audience: formAudience,
        platform: formPlatform,
        duration: Number(formDuration)
      });
      setFormTitle("");
      setFormText("");
      loadScripts();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (confirm("Are you sure you want to delete this script record from SQLite?")) {
      try {
        await deleteScript(id);
        loadScripts();
      } catch (err) {
        console.error(err);
      }
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Create Form */}
      <div className="card-saas p-6 space-y-4">
        <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
          <Plus className="w-4 h-4 text-indigo-600" />
          Create New Script Record (SQLite Create)
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Title</label>
            <input type="text" value={formTitle} onChange={(e) => setFormTitle(e.target.value)} placeholder="Script Title..." className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold" />
          </div>
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Category</label>
            <select value={formCategory} onChange={(e) => setFormCategory(e.target.value)} className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold">
              <option>Real Estate</option>
              <option>Finance & Wealth</option>
              <option>Tech & AI</option>
              <option>Fitness & Health</option>
              <option>E-commerce</option>
              <option>Education</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Duration (s)</label>
            <input type="number" value={formDuration} onChange={(e) => setFormDuration(e.target.value)} className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold" />
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Script Text</label>
          <textarea rows={3} value={formText} onChange={(e) => setFormText(e.target.value)} placeholder="Script content..." className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium" />
        </div>

        <button onClick={handleCreate} className="py-2.5 px-5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs shadow-md shadow-indigo-500/20 transition-all">
          Save Script Record
        </button>
      </div>

      {/* Script Records Table */}
      <div className="card-saas p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
            <FolderKanban className="w-4 h-4 text-indigo-600" />
            Stored User Script Records (SQLite Read, Update, Delete)
          </h3>
          <span className="text-xs font-bold text-slate-400">Total: {scripts.length}</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50 text-slate-400 font-bold uppercase text-[10px] tracking-wider border-b border-slate-100">
              <tr>
                <th className="py-3 px-4">ID</th>
                <th className="py-3 px-4">Title</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Platform</th>
                <th className="py-3 px-4">Duration</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {scripts.map((s) => (
                <tr key={s.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-slate-400">#{s.id}</td>
                  <td className="py-3.5 px-4 font-semibold text-slate-900">{s.title}</td>
                  <td className="py-3.5 px-4"><span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-600">{s.category}</span></td>
                  <td className="py-3.5 px-4">{s.platform}</td>
                  <td className="py-3.5 px-4">{s.duration}s</td>
                  <td className="py-3.5 px-4 text-right space-x-2">
                    <button onClick={() => handleDelete(s.id)} className="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg transition-colors">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
