import React, { useState, useEffect } from 'react';
import { AlertTriangle, CheckCircle, XCircle, Filter, Bell, BellOff, TrendingDown, Activity, Server, Database, Cloud } from 'lucide-react';

const AlertIntelligenceApp = () => {
  const [alerts, setAlerts] = useState([]);
  const [filteredAlerts, setFilteredAlerts] = useState([]);
  const [noiseReduction, setNoiseReduction] = useState(true);
  const [selectedSeverity, setSelectedSeverity] = useState('all');
  const [selectedSource, setSelectedSource] = useState('all');
  const [correlationEnabled, setCorrelationEnabled] = useState(true);

  // Mock alert data generator
  const generateMockAlerts = () => {
    const sources = ['Prometheus', 'Datadog', 'New Relic', 'Grafana', 'PagerDuty'];
    const severities = ['critical', 'warning', 'info'];
    const clientNames = ['Client A - E-commerce', 'Client B - FinTech', 'Client C - Healthcare', 'Client D - Retail'];
    const alertTypes = [
      { type: 'CPU High', message: 'CPU usage above 90%', icon: Activity },
      { type: 'Memory Leak', message: 'Memory usage trending up', icon: TrendingDown },
      { type: 'Disk Full', message: 'Disk usage above 85%', icon: Server },
      { type: 'Database Slow', message: 'Query response time > 5s', icon: Database },
      { type: 'Service Down', message: 'Service health check failed', icon: XCircle },
      { type: 'API Latency', message: 'API response time elevated', icon: Cloud }
    ];

    const mockAlerts = [];
    for (let i = 0; i < 50; i++) {
      const alertType = alertTypes[Math.floor(Math.random() * alertTypes.length)];
      const isDuplicate = Math.random() > 0.7;
      
      mockAlerts.push({
        id: i + 1,
        timestamp: new Date(Date.now() - Math.random() * 3600000).toISOString(),
        source: sources[Math.floor(Math.random() * sources.length)],
        severity: severities[Math.floor(Math.random() * severities.length)],
        client: clientNames[Math.floor(Math.random() * clientNames.length)],
        type: alertType.type,
        message: alertType.message,
        host: `server-${Math.floor(Math.random() * 20) + 1}`,
        isDuplicate: isDuplicate,
        correlationGroup: isDuplicate ? Math.floor(i / 3) : null,
        icon: alertType.icon,
        status: 'active'
      });
    }
    return mockAlerts;
  };

  useEffect(() => {
    const mockAlerts = generateMockAlerts();
    setAlerts(mockAlerts);
  }, []);

  useEffect(() => {
    let filtered = [...alerts];

    // Apply noise reduction (remove duplicates)
    if (noiseReduction) {
      const seen = new Map();
      filtered = filtered.filter(alert => {
        const key = `${alert.type}-${alert.host}-${alert.client}`;
        if (seen.has(key)) {
          return false;
        }
        seen.set(key, true);
        return true;
      });
    }

    // Apply severity filter
    if (selectedSeverity !== 'all') {
      filtered = filtered.filter(alert => alert.severity === selectedSeverity);
    }

    // Apply source filter
    if (selectedSource !== 'all') {
      filtered = filtered.filter(alert => alert.source === selectedSource);
    }

    setFilteredAlerts(filtered);
  }, [alerts, noiseReduction, selectedSeverity, selectedSource]);

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-300';
      case 'warning': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'info': return 'bg-blue-100 text-blue-800 border-blue-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const stats = {
    total: alerts.length,
    filtered: filteredAlerts.length,
    reduced: alerts.length - filteredAlerts.length,
    critical: filteredAlerts.filter(a => a.severity === 'critical').length,
    warning: filteredAlerts.filter(a => a.severity === 'warning').length,
    info: filteredAlerts.filter(a => a.severity === 'info').length
  };

  const correlatedGroups = correlationEnabled 
    ? filteredAlerts.reduce((acc, alert) => {
        const key = `${alert.type}-${alert.client}`;
        if (!acc[key]) acc[key] = [];
        acc[key].push(alert);
        return acc;
      }, {})
    : null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">Alert Intelligence Platform</h1>
              <p className="text-slate-400">MSP Multi-Tenant Alert Management & Noise Reduction</p>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setNoiseReduction(!noiseReduction)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                  noiseReduction 
                    ? 'bg-green-600 text-white hover:bg-green-700' 
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                {noiseReduction ? <BellOff size={20} /> : <Bell size={20} />}
                {noiseReduction ? 'Noise Reduction: ON' : 'Noise Reduction: OFF'}
              </button>
              <button
                onClick={() => setCorrelationEnabled(!correlationEnabled)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                  correlationEnabled 
                    ? 'bg-purple-600 text-white hover:bg-purple-700' 
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                Correlation: {correlationEnabled ? 'ON' : 'OFF'}
              </button>
            </div>
          </div>
        </div>

        {/* Stats Dashboard */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm mb-1">Total Alerts</p>
                <p className="text-3xl font-bold text-white">{stats.total}</p>
              </div>
              <Bell className="text-slate-500" size={32} />
            </div>
          </div>
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm mb-1">After Filtering</p>
                <p className="text-3xl font-bold text-white">{stats.filtered}</p>
              </div>
              <Filter className="text-blue-500" size={32} />
            </div>
          </div>
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm mb-1">Noise Reduced</p>
                <p className="text-3xl font-bold text-green-400">{stats.reduced}</p>
              </div>
              <TrendingDown className="text-green-500" size={32} />
            </div>
          </div>
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm mb-1">Critical</p>
                <p className="text-3xl font-bold text-red-400">{stats.critical}</p>
              </div>
              <AlertTriangle className="text-red-500" size={32} />
            </div>
          </div>
          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm mb-1">Warning</p>
                <p className="text-3xl font-bold text-yellow-400">{stats.warning}</p>
              </div>
              <AlertTriangle className="text-yellow-500" size={32} />
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 mb-6">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <Filter className="text-slate-400" size={20} />
              <span className="text-white font-medium">Filters:</span>
            </div>
            <div className="flex items-center gap-2">
              <label className="text-slate-400 text-sm">Severity:</label>
              <select
                value={selectedSeverity}
                onChange={(e) => setSelectedSeverity(e.target.value)}
                className="bg-slate-700 text-white border border-slate-600 rounded px-3 py-1 text-sm"
              >
                <option value="all">All</option>
                <option value="critical">Critical</option>
                <option value="warning">Warning</option>
                <option value="info">Info</option>
              </select>
            </div>
            <div className="flex items-center gap-2">
              <label className="text-slate-400 text-sm">Source:</label>
              <select
                value={selectedSource}
                onChange={(e) => setSelectedSource(e.target.value)}
                className="bg-slate-700 text-white border border-slate-600 rounded px-3 py-1 text-sm"
              >
                <option value="all">All Sources</option>
                <option value="Prometheus">Prometheus</option>
                <option value="Datadog">Datadog</option>
                <option value="New Relic">New Relic</option>
                <option value="Grafana">Grafana</option>
                <option value="PagerDuty">PagerDuty</option>
              </select>
            </div>
          </div>
        </div>

        {/* Alert List */}
        <div className="bg-slate-800 border border-slate-700 rounded-lg overflow-hidden">
          <div className="p-4 bg-slate-750 border-b border-slate-700">
            <h2 className="text-xl font-bold text-white">
              {correlationEnabled ? 'Correlated Alert Groups' : 'Alert Feed'}
            </h2>
          </div>
          <div className="p-4 max-h-[600px] overflow-y-auto">
            {correlationEnabled && correlatedGroups ? (
              Object.entries(correlatedGroups).map(([groupKey, groupAlerts]) => (
                <div key={groupKey} className="mb-6 bg-slate-750 rounded-lg border border-slate-600 overflow-hidden">
                  <div className="bg-slate-700 px-4 py-3 border-b border-slate-600">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="bg-purple-600 rounded p-2">
                          {React.createElement(groupAlerts[0].icon, { size: 20, className: "text-white" })}
                        </div>
                        <div>
                          <h3 className="text-white font-semibold">{groupAlerts[0].type}</h3>
                          <p className="text-slate-400 text-sm">{groupAlerts[0].client}</p>
                        </div>
                      </div>
                      <span className="bg-purple-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                        {groupAlerts.length} alert{groupAlerts.length > 1 ? 's' : ''}
                      </span>
                    </div>
                  </div>
                  <div className="divide-y divide-slate-600">
                    {groupAlerts.slice(0, 3).map(alert => (
                      <div key={alert.id} className="p-4 hover:bg-slate-700 transition-colors">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <span className={`px-2 py-1 rounded text-xs font-medium border ${getSeverityColor(alert.severity)}`}>
                                {alert.severity.toUpperCase()}
                              </span>
                              <span className="text-slate-400 text-sm">{alert.source}</span>
                              <span className="text-slate-500 text-sm">•</span>
                              <span className="text-slate-400 text-sm">{alert.host}</span>
                            </div>
                            <p className="text-white mb-1">{alert.message}</p>
                            <p className="text-slate-500 text-sm">
                              {new Date(alert.timestamp).toLocaleString()}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                    {groupAlerts.length > 3 && (
                      <div className="p-3 bg-slate-700 text-center">
                        <span className="text-slate-400 text-sm">
                          +{groupAlerts.length - 3} more alert{groupAlerts.length - 3 > 1 ? 's' : ''} in this group
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              ))
            ) : (
              filteredAlerts.map(alert => (
                <div key={alert.id} className="mb-3 bg-slate-750 rounded-lg border border-slate-600 p-4 hover:border-slate-500 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3 flex-1">
                      <div className={`p-2 rounded ${
                        alert.severity === 'critical' ? 'bg-red-600' :
                        alert.severity === 'warning' ? 'bg-yellow-600' : 'bg-blue-600'
                      }`}>
                        {React.createElement(alert.icon, { size: 20, className: "text-white" })}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span className={`px-2 py-1 rounded text-xs font-medium border ${getSeverityColor(alert.severity)}`}>
                            {alert.severity.toUpperCase()}
                          </span>
                          <span className="text-white font-medium">{alert.type}</span>
                          <span className="text-slate-500 text-sm">•</span>
                          <span className="text-slate-400 text-sm">{alert.source}</span>
                        </div>
                        <p className="text-slate-300 mb-2">{alert.message}</p>
                        <div className="flex items-center gap-4 text-sm text-slate-400">
                          <span>Client: {alert.client}</span>
                          <span>•</span>
                          <span>Host: {alert.host}</span>
                          <span>•</span>
                          <span>{new Date(alert.timestamp).toLocaleString()}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AlertIntelligenceApp;