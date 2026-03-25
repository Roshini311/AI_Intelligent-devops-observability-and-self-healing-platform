import React from 'react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen">
      <header className="bg-gray-900 border-b border-gray-800 p-4 sticky top-0 z-10 transition-all shadow-md shadow-blue-900/10">
        <div className="container mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-wide">
            Nexus AI Observability
          </h1>
          <span className="text-sm font-medium text-blue-400 bg-blue-400/10 px-3 py-1 rounded-full border border-blue-400/20">
            DevOps Self-Healing Platform
          </span>
        </div>
      </header>
      <main className="container mx-auto py-8 px-4">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
