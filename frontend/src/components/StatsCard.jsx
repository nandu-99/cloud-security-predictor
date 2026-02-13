/**
 * StatsCard Component
 * Reusable card for displaying dashboard statistics
 */



const StatsCard = ({ title, value, icon: Icon, subtitle, color = 'primary' }) => {
  const colorClasses = {
    primary: 'border-slate-200 bg-white hover:border-slate-300',
    success: 'border-slate-200 bg-white hover:border-emerald-200',
    warning: 'border-slate-200 bg-white hover:border-amber-200',
    danger: 'border-slate-200 bg-white hover:border-rose-200',
  };

  const iconColorClasses = {
    primary: 'text-slate-600 bg-slate-100',
    success: 'text-emerald-600 bg-emerald-50',
    warning: 'text-amber-600 bg-amber-50',
    danger: 'text-rose-600 bg-rose-50',
  };

  return (
    <div className={`border rounded-xl p-6 transition-all duration-300 hover:shadow-lg ${colorClasses[color]}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-slate-500 text-sm font-medium uppercase tracking-wide">{title}</p>
          <h3 className="text-3xl font-bold text-slate-900 mt-2">{value.toLocaleString()}</h3>
          {subtitle && (
            <p className="text-slate-400 text-xs mt-1">{subtitle}</p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${iconColorClasses[color]}`}>
          <Icon size={24} />
        </div>
      </div>
    </div>
  );
};

export default StatsCard;
