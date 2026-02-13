/**
 * TrendChart Component
 * Line chart showing risk trend over time
 */

import { TrendingUp } from 'lucide-react';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

const TrendChart = ({ trendData }) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border border-slate-200 rounded-lg p-3 shadow-lg">
          <p className="text-slate-500 text-xs font-medium mb-1">{label}</p>
          <p className="text-slate-900 font-bold">Avg Risk: {payload[0].value.toFixed(1)}</p>
          {payload[1] && <p className="text-rose-600 text-sm">Alerts: {payload[1].value}</p>}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 h-full shadow-sm">
      <h3 className="text-lg font-semibold text-slate-900 mb-6 flex items-center gap-2">
        <TrendingUp className="text-slate-500" size={20} />
        Risk Trend (Last 24 Hours)
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={trendData}>
          <defs>
            <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#0f172a" stopOpacity={0.1}/>
              <stop offset="95%" stopColor="#0f172a" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
          <XAxis 
            dataKey="timestamp" 
            stroke="#94a3b8"
            tick={{ fill: '#64748b', fontSize: 11 }}
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => {
              // Show only hour
              const parts = value.split(' ');
              return parts[1] ? parts[1].substring(0, 5) : value;
            }}
          />
          <YAxis 
            stroke="#94a3b8"
            tick={{ fill: '#64748b', fontSize: 11 }}
            tickLine={false}
            axisLine={false}
            domain={[0, 100]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area 
            type="monotone" 
            dataKey="average_risk" 
            stroke="#0f172a" 
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#colorRisk)"
            activeDot={{ r: 6, fill: '#0f172a', stroke: '#ffffff', strokeWidth: 2 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendChart;
