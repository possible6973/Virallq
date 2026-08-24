import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';

import LandingView from './views/LandingView';
import DashboardView from './views/DashboardView';
import AnalyzeScriptView from './views/AnalyzeScriptView';
import GenerateScriptView from './views/GenerateScriptView';
import AnalyzeReelView from './views/AnalyzeReelView';
import ViralLibraryView from './views/ViralLibraryView';
import MyScriptsView from './views/MyScriptsView';
import AiAdvisorView from './views/AiAdvisorView';
import AnalyticsView from './views/AnalyticsView';
import ReportsView from './views/ReportsView';
import SettingsView from './views/SettingsView';

const VIEW_TITLES = {
  landing: { title: "Welcome to ViralIQ", subtitle: "The AI Script Optimization Platform for Short-Form Video Creators." },
  dashboard: { title: "Executive Dashboard", subtitle: "Real-time script performance predictions, optimization analytics, and viral patterns." },
  analyze: { title: "Script Intelligence & Performance Analysis", subtitle: "Evaluate any reel script using trained ML and ANN AI models." },
  generate: { title: "AI Script Generator Studio", subtitle: "Prompt Engineering + Gemini LLM Candidate Generation + Multi-Candidate Evaluation." },
  reel: { title: "Analyze Reel (Video & Visual Intelligence)", subtitle: "Dual Pipeline: Spoken Content Transcript & Thumbnail Visual Quality Classifier." },
  library: { title: "Viral Script Knowledge Library", subtitle: "Benchmark repository of high-performing reel templates." },
  scripts: { title: "My Scripts Management", subtitle: "Full Create, Read, Update, and Delete operations for user script records." },
  advisor: { title: "AI Script Advisor", subtitle: "Chat with an AI content strategist aware of your script history." },
  analytics: { title: "Model Analytics & Feature Importances", subtitle: "Empirical performance metrics and accuracy curves." },
  reports: { title: "Script Performance Reports", subtitle: "Generate and download executive script performance audit reports." },
  settings: { title: "System Configuration & Settings", subtitle: "Configure Gemini API credentials and score aggregation parameters." },
};

export default function App() {
  const [currentView, setCurrentView] = useState('landing');
  const [scriptToOptimize, setScriptToOptimize] = useState('');

  if (currentView === 'landing') {
    return <LandingView setCurrentView={setCurrentView} />;
  }

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <DashboardView setCurrentView={setCurrentView} setScriptToAnalyze={setScriptToOptimize} />;
      case 'analyze':
        return <AnalyzeScriptView setCurrentView={setCurrentView} setScriptToOptimize={setScriptToOptimize} />;
      case 'generate':
        return <GenerateScriptView scriptToOptimize={scriptToOptimize} />;
      case 'reel':
        return <AnalyzeReelView />;
      case 'library':
        return <ViralLibraryView setCurrentView={setCurrentView} setScriptToOptimize={setScriptToOptimize} />;
      case 'scripts':
        return <MyScriptsView />;
      case 'advisor':
        return <AiAdvisorView />;
      case 'analytics':
        return <AnalyticsView />;
      case 'reports':
        return <ReportsView />;
      case 'settings':
        return <SettingsView />;
      default:
        return <DashboardView setCurrentView={setCurrentView} setScriptToAnalyze={setScriptToOptimize} />;
    }
  };

  const headerInfo = VIEW_TITLES[currentView] || VIEW_TITLES.dashboard;

  return (
    <div className="min-h-screen flex bg-slate-50">
      <Sidebar currentView={currentView} setCurrentView={setCurrentView} />
      <div className="flex-1 flex flex-col min-w-0">
        <Header currentView={currentView} setCurrentView={setCurrentView} title={headerInfo.title} subtitle={headerInfo.subtitle} />
        <main className="flex-1 overflow-y-auto">
          {renderView()}
        </main>
      </div>
    </div>
  );
}
