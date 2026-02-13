/**
 * AlertsTable Component
 * Table displaying security alerts with filtering
 */

import { AlertCircle, Eye, SlidersHorizontal } from 'lucide-react';
import { useState } from 'react';

const AlertsTable = ({ alerts, onAlertClick }) => {
  const [filterRisk, setFilterRisk] = useState('all');

  const filteredAlerts = alerts.filter(alert => {
    if (filterRisk === 'all') return true;
    return alert.risk_level.toLowerCase() === filterRisk;
  });

  const getRiskBadge = (level) => {
    const styles = {
      High: 'bg-rose-50 text-rose-700 border-rose-200',
      Medium: 'bg-amber-50 text-amber-700 border-amber-200',
      Low: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    };
    return styles[level] || 'bg-slate-100 text-slate-600 border-slate-200';
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
          <AlertCircle className="text-slate-500" size={20} />
          Recent Alerts
        </h3>
        
        {/* Filter */}
        <div className="flex items-center gap-2">
          <SlidersHorizontal size={16} className="text-slate-400" />
          <span className="text-slate-500 text-sm font-medium">Filter:</span>
          <select
            value={filterRisk}
            onChange={(e) => setFilterRisk(e.target.value)}
            className="bg-slate-50 border border-slate-200 text-slate-700 px-3 py-1.5 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-400 transition-all"
          >
            <option value="all">All Risks</option>
            <option value="high">High Risk</option>
            <option value="medium">Medium Risk</option>
            <option value="low">Low Risk</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        {filteredAlerts.length === 0 ? (
          <div className="text-center py-12 bg-slate-50 rounded-lg border border-dashed border-slate-200">
            <p className="text-slate-500 text-base font-medium">No alerts found</p>
            <p className="text-slate-400 text-sm mt-1">Run analysis to generate alerts</p>
          </div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-100">
                <th className="text-left text-slate-500 text-xs font-semibold uppercase tracking-wider py-4 px-4">Timestamp</th>
                <th className="text-left text-slate-500 text-xs font-semibold uppercase tracking-wider py-4 px-4">User ID</th>
                <th className="text-left text-slate-500 text-xs font-semibold uppercase tracking-wider py-4 px-4">Location</th>
                <th className="text-left text-slate-500 text-xs font-semibold uppercase tracking-wider py-4 px-4">Risk Score</th>
                <th className="text-left text-slate-500 text-xs font-semibold uppercase tracking-wider py-4 px-4">Risk Level</th>
                <th className="text-left text-slate-500 text-xs font-semibold uppercase tracking-wider py-4 px-4">Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredAlerts.slice(0, 10).map((alert) => (
                <tr 
                  key={alert.id} 
                  className="border-b border-slate-50 hover:bg-slate-50 transition-colors group"
                >
                  <td className="py-4 px-4 text-slate-600 text-sm">
                    {new Date(alert.timestamp).toLocaleString()}
                  </td>
                  <td className="py-4 px-4 text-slate-900 font-medium text-sm">
                    {alert.user_id}
                  </td>
                  <td className="py-4 px-4 text-slate-600 text-sm">
                    {alert.login_location}
                  </td>
                  <td className="py-4 px-4 text-slate-900 font-semibold">
                    {alert.risk_score.toFixed(1)}
                  </td>
                  <td className="py-4 px-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getRiskBadge(alert.risk_level)}`}>
                      {alert.risk_level}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <button
                      onClick={() => onAlertClick(alert)}
                      className="text-slate-400 hover:text-slate-900 transition-colors flex items-center gap-1 text-sm font-medium"
                    >
                      <Eye size={16} />
                      Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {filteredAlerts.length > 10 && (
        <p className="text-gray-500 text-sm text-center mt-4">
          Showing 10 of {filteredAlerts.length} alerts
        </p>
      )}
    </div>
  );
};

export default AlertsTable;
