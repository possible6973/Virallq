import React, { useState } from 'react';
import { sendAiAdvisorChat } from '../services/api';
import { MessageSquareText, Send, Bot, User, Sparkles } from 'lucide-react';

export default function AiAdvisorView() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I am your **ViralIQ AI Advisor**. I evaluate your ML + ANN model metrics and script retention patterns. How can I assist your content strategy today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (textToSend) => {
    const query = textToSend || input;
    if (!query.trim()) return;

    const newMsgs = [...messages, { role: 'user', content: query }];
    setMessages(newMsgs);
    setInput('');
    setLoading(true);

    try {
      const res = await sendAiAdvisorChat({ message: query });
      setMessages([...newMsgs, { role: 'assistant', content: res.reply }]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <div className="card-saas p-6 space-y-4 flex flex-col h-[650px]">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-md shadow-indigo-500/20">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-base">ViralIQ AI Advisor</h3>
              <p className="text-xs text-slate-400">Context-Aware RAG Content Strategist</p>
            </div>
          </div>
          <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
            Model Aware
          </span>
        </div>

        {/* Suggested Queries */}
        <div className="flex flex-wrap gap-2 pt-1">
          {[
            "🪝 How to write a 3s viral hook?",
            "📉 Why did my script score below 80%?",
            "📢 3 high-converting CTAs",
            "🤖 Explain ML vs ANN model scores"
          ].map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(q)}
              className="px-3 py-1.5 bg-slate-50 hover:bg-indigo-50 hover:text-indigo-600 border border-slate-200/80 rounded-xl text-xs font-semibold text-slate-600 transition-colors"
            >
              {q}
            </button>
          ))}
        </div>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto space-y-4 p-2">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex gap-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {m.role === 'assistant' && (
                <div className="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-600 flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4" />
                </div>
              )}
              <div
                className={`max-w-md p-4 rounded-2xl text-xs font-medium leading-relaxed ${
                  m.role === 'user'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'bg-slate-100 text-slate-800 border border-slate-200/60'
                }`}
              >
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex items-center gap-2 text-xs font-semibold text-indigo-600">
              <div className="w-3 h-3 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
              Advisor thinking...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="pt-3 border-t border-slate-100 flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask AI Advisor about your scripts..."
            className="flex-1 p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-900 focus:ring-2 focus:ring-indigo-500/20"
          />
          <button
            onClick={() => handleSend()}
            className="p-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl shadow-md shadow-indigo-500/20 transition-all"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
