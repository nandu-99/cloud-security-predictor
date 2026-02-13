/**
 * Dashboard Component
 * Main dashboard for Cloud Security Threat Predictor
 */

import { Activity, AlertTriangle, Bot, FileText, Loader2, Search, Shield, Zap } from 'lucide-react';
import { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import AlertModal from './AlertModal';
import AlertsTable from './AlertsTable';
import RiskChart from './RiskChart';
import StatsCard from './StatsCard';
import TrendChart from './TrendChart';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_logs: 0,
    total_alerts: 0,
    low_risk: 0,
    medium_risk: 0,
    high_risk: 0,
  });
  const [alerts, setAlerts] = useState([]);
  const [trendData, setTrendData] = useState([]);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);

  // Fetch dashboard data
  const fetchDashboardData = async () => {
    try {
      const [statsData, alertsData, trendDataResponse] = await Promise.all([
        apiService.getDashboardStats(),
        apiService.getAlerts(null, 100),
        apiService.getRiskTrend(24),
      ]);
      
      setStats(statsData);
      setAlerts(alertsData);
      setTrendData(trendDataResponse);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      showNotification('Failed to load dashboard data', 'error');
    }
  };

  // Initial load
  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Show notification
  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  // Action handlers
  const handleGenerateLogs = async () => {
    setLoading(true);
    try {
      const response = await apiService.generateLogs();
      showNotification(response.message, 'success');
      await fetchDashboardData();
    } catch (error) {
      showNotification(error.response?.data?.detail || 'Failed to generate logs', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleTrainModel = async () => {
    setLoading(true);
    try {
      const response = await apiService.trainModel();
      showNotification(response.message, 'success');
    } catch (error) {
      showNotification(error.response?.data?.detail || 'Failed to train model', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeLogs = async () => {
    setLoading(true);
    try {
      const response = await apiService.analyzeLogs();
      showNotification(`${response.message} - ${response.details.alerts_created} alerts created`, 'success');
      await fetchDashboardData();
    } catch (error) {
      showNotification(error.response?.data?.detail || 'Failed to analyze logs', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateAttack = async () => {
    setLoading(true);
    try {
      const response = await apiService.simulateAttack();
      showNotification(`🚨 ${response.message} - ${response.details.high_risk_alerts} high-risk alerts!`, 'warning');
      await fetchDashboardData();
    } catch (error) {
      showNotification(error.response?.data?.detail || 'Failed to simulate attack', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-slate-900 rounded-lg text-white">
                <Shield size={24} />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900 leading-tight">
                  Cloud Security Threat Predictor
                </h1>
                <p className="text-slate-500 text-xs font-medium">AI-Driven Behavioral Anomaly Detection</p>
              </div>
            </div>
            <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-full border border-emerald-100">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <span className="text-xs font-semibold uppercase tracking-wide">System Active</span>
            </div>
          </div>
        </div>
      </header>

      {/* Action Bar */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <button
            onClick={handleGenerateLogs}
            disabled={loading}
            className="group flex items-center justify-center gap-2 px-6 py-3 bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold rounded-xl transition-all shadow-sm hover:shadow"
          >
            <FileText size={18} className="text-slate-400 group-hover:text-slate-600 transition-colors" />
            Generate Logs
          </button>
          <button
            onClick={handleTrainModel}
            disabled={loading}
            className="group flex items-center justify-center gap-2 px-6 py-3 bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold rounded-xl transition-all shadow-sm hover:shadow"
          >
            <Bot size={18} className="text-slate-400 group-hover:text-amber-500 transition-colors" />
            Train Model
          </button>
          <button
            onClick={handleAnalyzeLogs}
            disabled={loading}
            className="group flex items-center justify-center gap-2 px-6 py-3 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-xl transition-all shadow-md hover:shadow-lg"
          >
            <Search size={18} className="text-slate-300 group-hover:text-white transition-colors" />
            Analyze Logs
          </button>
          <button
            onClick={handleSimulateAttack}
            disabled={loading}
            className="group flex items-center justify-center gap-2 px-6 py-3 bg-white border border-slate-200 hover:border-rose-200 hover:bg-rose-50 text-slate-700 hover:text-rose-700 font-semibold rounded-xl transition-all shadow-sm hover:shadow"
          >
            <Zap size={18} className="text-slate-400 group-hover:text-rose-500 transition-colors" />
            Simulate Attack
          </button>
        </div>
      </div>

      {/* Notification */}
      {notification && (
        <div className="max-w-7xl mx-auto px-6 mb-6">
          <div className={`p-4 rounded-xl border flex items-center gap-3 ${
            notification.type === 'success' ? 'bg-emerald-50 border-emerald-200 text-emerald-700' :
            notification.type === 'error' ? 'bg-rose-50 border-rose-200 text-rose-700' :
            'bg-amber-50 border-amber-200 text-amber-700'
          }`}>
             {notification.type === 'success' ? <Shield size={20} /> : <AlertTriangle size={20} />}
            <span className="font-medium">{notification.message}</span>
          </div>
        </div>
      )}

      {/* Loading Indicator */}
      {loading && (
        <div className="max-w-7xl mx-auto px-6 mb-6">
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex items-center gap-3 shadow-sm">
            <Loader2 className="animate-spin text-slate-900" size={24} />
            <span className="text-slate-600 font-medium">Processing request...</span>
          </div>
        </div>
      )}

      {/* Stats Cards */}
      <div className="max-w-7xl mx-auto px-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatsCard
            title="Total Logs"
            value={stats.total_logs}
            icon={FileText}
            subtitle="All activity logs"
            color="primary"
          />
          <StatsCard
            title="Total Alerts"
            value={stats.total_alerts}
            icon={AlertTriangle}
            subtitle="Medium + High risk"
            color="warning"
          />
          <StatsCard
            title="High Risk"
            value={stats.high_risk}
            icon={Zap}
            subtitle="Critical threats"
            color="danger"
          />
          <StatsCard
            title="Medium Risk"
            value={stats.medium_risk}
            icon={Activity}
            subtitle="Moderate concerns"
            color="warning"
          />
        </div>
      </div>

      {/* Charts */}
      <div className="max-w-7xl mx-auto px-6 mb-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <RiskChart stats={stats} />
          <TrendChart trendData={trendData} />
        </div>
      </div>

      {/* Alerts Table */}
      <div className="max-w-7xl mx-auto px-6 pb-12">
        <AlertsTable alerts={alerts} onAlertClick={setSelectedAlert} />
      </div>

      {/* Alert Modal */}
      {selectedAlert && (
        <AlertModal alert={selectedAlert} onClose={() => setSelectedAlert(null)} />
      )}
    </div>
  );
};

export default Dashboard;
