/**
 * RiskChart Component
 * Pie chart showing risk distribution
 */

import { PieChart as PieChartIcon } from 'lucide-react';
import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';

const RiskChart = ({ stats }) => {
  const data = [
    { name: 'Low Risk', value: stats.low_risk, color: '#10b981' }, // Emerald 500
    { name: 'Medium Risk', value: stats.medium_risk, color: '#f59e0b' }, // Amber 500
    { name: 'High Risk', value: stats.high_risk, color: '#f43f5e' }, // Rose 500
  ];

  const COLORS = ['#10b981', '#f59e0b', '#f43f5e'];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border border-slate-200 rounded-lg p-3 shadow-lg">
          <p className="text-slate-900 font-semibold">{payload[0].name}</p>
          <p className="text-slate-600">{payload[0].value} logs</p>
          <p className="text-slate-400 text-xs">
            {stats.total_logs > 0 ? ((payload[0].value / stats.total_logs) * 100).toFixed(1) : 0}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 h-full shadow-sm">
      <h3 className="text-lg font-semibold text-slate-900 mb-6 flex items-center gap-2">
        <PieChartIcon className="text-slate-500" size={20} />
        Risk Distribution
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => percent > 0 ? `${(percent * 100).toFixed(0)}%` : ''}
            outerRadius={100}
            innerRadius={60}
            paddingAngle={5}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="transparent" />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            verticalAlign="bottom" 
            height={36}
            iconType="circle"
            formatter={(value) => <span className="text-slate-600 font-medium ml-1">{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RiskChart;
