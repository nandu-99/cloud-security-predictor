/**
 * AlertModal Component
 * Modal popup showing detailed alert information with explanations
 */


import { AlertOctagon, AlertTriangle, Check, ShieldAlert, X } from 'lucide-react';

const AlertModal = ({ alert, onClose }) => {
  if (!alert) return null;

  const getRiskColor = (level) => {
    switch (level) {
      case 'High': return 'text-rose-600';
      case 'Medium': return 'text-amber-600';
      case 'Low': return 'text-emerald-600';
      default: return 'text-slate-400';
    }
  };

  const getRiskBgColor = (level) => {
    switch (level) {
      case 'High': return 'bg-rose-50 border-rose-100';
      case 'Medium': return 'bg-amber-50 border-amber-100';
      case 'Low': return 'bg-emerald-50 border-emerald-100';
      default: return 'bg-slate-50 border-slate-100';
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center z-50 p-4 transition-all">
      <div className="bg-white border border-slate-200 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-slate-100 p-6 flex items-center justify-between z-10">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <ShieldAlert className="text-slate-700" size={24} />
              Security Alert Details
            </h2>
            <p className="text-slate-500 text-sm mt-1 font-mono">ID: #{alert.id}</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Risk Score */}
          <div className={`border rounded-xl p-5 ${getRiskBgColor(alert.risk_level)}`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-600 text-sm font-medium uppercase tracking-wide">Risk Assessment</p>
                <div className="flex items-center gap-2 mt-1">
                  <AlertTriangle size={24} className={getRiskColor(alert.risk_level)} />
                  <p className={`text-3xl font-bold ${getRiskColor(alert.risk_level)}`}>
                    {alert.risk_level} Risk
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-slate-500 text-sm uppercase tracking-wide">Risk Score</p>
                <p className="text-4xl font-bold text-slate-900">{alert.risk_score.toFixed(1)}</p>
                <p className="text-slate-400 text-xs font-medium">/ 100</p>
              </div>
            </div>
          </div>

          {/* Explanation Section */}
          <div className="bg-slate-50 rounded-xl p-5 border border-slate-100">
            <h3 className="text-base font-semibold text-slate-900 mb-3 flex items-center gap-2">
              <AlertOctagon size={18} className="text-slate-700" />
              AI Analysis
            </h3>
            <div className="space-y-2">
              {alert.explanation && alert.explanation.length > 0 ? (
                alert.explanation.map((reason, index) => (
                  <div key={index} className="flex items-start gap-3 text-slate-600 text-sm">
                    <span className="text-slate-400 mt-1.5">•</span>
                    <span className="leading-relaxed">{reason}</span>
                  </div>
                ))
              ) : (
                <p className="text-slate-400 text-sm italic">No detailed analysis available.</p>
              )}
            </div>
          </div>

          {/* Log Details */}
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
            <div className="bg-slate-50 px-5 py-3 border-b border-slate-100">
               <h3 className="text-sm font-semibold text-slate-900">Log Metadata</h3>
            </div>
            <div className="p-5 grid grid-cols-2 gap-6">
              <div>
                <p className="text-slate-400 text-xs uppercase font-medium mb-1">User ID</p>
                <p className="text-slate-900 font-mono text-sm bg-slate-50 inline-block px-2 py-1 rounded border border-slate-100">{alert.user_id}</p>
              </div>
              <div>
                <p className="text-slate-400 text-xs uppercase font-medium mb-1">Location</p>
                <p className="text-slate-700 text-sm font-medium">{alert.login_location}</p>
              </div>
              <div>
                <p className="text-slate-400 text-xs uppercase font-medium mb-1">Time</p>
                <p className="text-slate-700 text-sm">{alert.login_time}</p>
              </div>
              <div>
                <p className="text-slate-400 text-xs uppercase font-medium mb-1">Timestamp</p>
                <p className="text-slate-700 text-sm">
                  {new Date(alert.timestamp).toLocaleString()}
                </p>
              </div>
              <div>
                <p className="text-slate-400 text-xs uppercase font-medium mb-1">Failed Attempts</p>
                <p className="text-slate-900 font-semibold">{alert.failed_login_attempts}</p>
              </div>
              <div>
                <p className="text-slate-400 text-xs uppercase font-medium mb-1">Access Level</p>
                <p className="text-slate-700 capitalize text-sm">{alert.resource_access_level}</p>
              </div>
              <div>
                <p className="text-slate-400 text-xs uppercase font-medium mb-1">VMs Created</p>
                <p className="text-slate-900 font-semibold">{alert.vm_creation_count}</p>
              </div>
              <div>
                <p className="text-slate-400 text-xs uppercase font-medium mb-1">Privilege Change</p>
                <div className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-md text-sm font-medium ${alert.privilege_change ? 'bg-amber-50 text-amber-700' : 'bg-slate-50 text-slate-600'}`}>
                  {alert.privilege_change ? <AlertTriangle size={14} /> : <Check size={14} />}
                  {alert.privilege_change ? 'Detected' : 'None'}
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end pt-2">
            <button
              onClick={onClose}
              className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-xl transition-colors shadow-sm hover:shadow"
            >
              Close Details
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AlertModal;
