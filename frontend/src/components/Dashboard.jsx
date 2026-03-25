import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Activity, AlertTriangle, CheckCircle, RefreshCw, Cpu, HardDrive, Clock, Search } from 'lucide-react';

export default function Dashboard() {
  const [data, setData] = useState([]);
  const [status, setStatus] = useState('healthy'); // healthy, degraded, self_healing
  const [events, setEvents] = useState([]);
  const [anomalyScore, setAnomalyScore] = useState(0);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      
      if (payload.event === 'self_healing_started') {
        setStatus('self_healing');
        setEvents(prev => [{ id: Date.now(), time: new Date().toLocaleTimeString(), type: 'warning', text: 'Self-healing triggered: Restarting services...' }, ...prev].slice(0, 10));
      } else if (payload.event === 'self_healing_completed') {
        setStatus('healthy');
        setEvents(prev => [{ id: Date.now(), time: new Date().toLocaleTimeString(), type: 'success', text: 'Self-healing completed: System restored.' }, ...prev].slice(0, 10));
      } else if (payload.metrics) {
        const newPoint = {
          time: new Date(payload.timestamp * 1000).toLocaleTimeString(),
          cpu: payload.metrics.cpu_percent.toFixed(1),
          memory: payload.metrics.memory_percent.toFixed(1),
          latency: payload.metrics.request_latency_ms.toFixed(1),
          isAnomaly: payload.is_anomaly
        };
        
        setData(prev => {
          const newData = [...prev, newPoint];
          if (newData.length > 20) newData.shift();
          return newData;
        });

        setStatus(payload.system_status);
        setAnomalyScore(payload.anomaly_score.toFixed(3));
        
        if (payload.is_anomaly && status === 'healthy') {
          setEvents(prev => [{ id: Date.now(), time: new Date().toLocaleTimeString(), type: 'error', text: `Critical Anomaly Detected! ML Score: ${payload.anomaly_score.toFixed(3)}` }, ...prev].slice(0, 10));
        }
      }
    };

    return () => ws.close();
  }, [status]);

  const getStatusColor = () => {
    if (status === 'healthy') return 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';
    if (status === 'degraded') return 'text-rose-400 bg-rose-400/10 border-rose-400/20 animate-pulse';
    return 'text-amber-400 bg-amber-400/10 border-amber-400/20 animate-pulse';
  };

  const getStatusIcon = () => {
    if (status === 'healthy') return <CheckCircle className="w-5 h-5 mr-2" />;
    if (status === 'degraded') return <AlertTriangle className="w-5 h-5 mr-2" />;
    return <RefreshCw className="w-5 h-5 mr-2 animate-spin" />;
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 flex-1">
        
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-400 text-sm font-medium">System Status</h3>
            <Activity className="text-blue-400 w-5 h-5" />
          </div>
          <div className={`inline-flex items-center px-4 py-2 rounded-lg border ${getStatusColor()} font-medium transition-colors duration-500`}>
            {getStatusIcon()}
            <span className="capitalize">{status.replace('_', ' ')}</span>
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-gray-400 text-sm font-medium">ML Anomaly Score</h3>
            <Search className="text-purple-400 w-5 h-5" />
          </div>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-bold text-gray-100">{anomalyScore}</span>
            <span className="text-sm text-gray-500 mb-1">threshold: 0.5</span>
          </div>
          <div className="w-full bg-gray-800 h-1.5 mt-4 rounded-full overflow-hidden">
            <div 
              className={`h-full rounded-full transition-all duration-500 ${anomalyScore > 0.5 ? 'bg-rose-500' : 'bg-emerald-500'}`} 
              style={{ width: `${Math.min(Math.max((anomalyScore / 2) * 100, 5), 100)}%` }} 
            />
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-gray-400 text-sm font-medium">Avg CPU</h3>
            <Cpu className="text-sky-400 w-5 h-5" />
          </div>
          <div className="text-3xl font-bold text-gray-100">
            {data.length > 0 ? data[data.length - 1].cpu : '--'}%
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-gray-400 text-sm font-medium">Avg Latency</h3>
            <Clock className="text-amber-400 w-5 h-5" />
          </div>
          <div className="text-3xl font-bold text-gray-100">
            {data.length > 0 ? data[data.length - 1].latency : '--'}ms
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-96">
        <div className="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl flex flex-col">
          <h2 className="text-lg font-medium text-gray-200 mb-4 flex items-center">
            <Activity className="w-5 h-5 mr-2 text-indigo-400" />
            Live Telemetry stream
          </h2>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                <XAxis dataKey="time" stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
                <YAxis stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.5rem' }}
                  itemStyle={{ color: '#E5E7EB' }}
                />
                <ReferenceLine y={85} label="CPU Critical" stroke="#EF4444" strokeDasharray="3 3" />
                <Line type="monotone" dataKey="cpu" stroke="#38BDF8" strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line type="monotone" dataKey="memory" stroke="#A78BFA" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl flex flex-col">
          <h2 className="text-lg font-medium text-gray-200 mb-4 flex items-center">
            <HardDrive className="w-5 h-5 mr-2 text-indigo-400" />
            Remediation Logs
          </h2>
          <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
            {events.length === 0 ? (
              <div className="text-gray-500 text-sm flex items-center justify-center h-full">No events logged</div>
            ) : (
                events.map(ev => (
                  <div key={ev.id} className="p-3 rounded-lg border border-gray-800 bg-gray-950/50 flex flex-col gap-1">
                    <span className="text-xs text-gray-500">{ev.time}</span>
                    <span className={`text-sm ${ev.type === 'error' ? 'text-rose-400' : ev.type === 'warning' ? 'text-amber-400' : 'text-emerald-400'}`}>
                      {ev.text}
                    </span>
                  </div>
                ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
