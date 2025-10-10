import { ReactNode } from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StatCardProps {
  icon: ReactNode;
  label: string;
  value: number | string;
  change?: number;
  color: string;
  description?: string;
}

export default function StatCard({ 
  icon, 
  label, 
  value, 
  change, 
  color, 
  description 
}: StatCardProps) {
  const isPositiveChange = change && change > 0;
  const isNegativeChange = change && change < 0;
  
  return (
    <div className="bg-white rounded-lg shadow p-6 border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className={`p-3 rounded-lg ${color} bg-opacity-10`}>
            {icon}
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600">{label}</p>
            <p className="text-2xl font-semibold text-gray-900">{value}</p>
            {description && (
              <p className="text-xs text-gray-500 mt-1">{description}</p>
            )}
          </div>
        </div>
        {change !== undefined && (
          <div className="flex items-center text-sm">
            {isPositiveChange ? (
              <>
                <TrendingUp className="w-4 h-4 mr-1 text-green-500" />
                <span className="text-green-600">+{change}%</span>
              </>
            ) : isNegativeChange ? (
              <>
                <TrendingDown className="w-4 h-4 mr-1 text-red-500" />
                <span className="text-red-600">{change}%</span>
              </>
            ) : (
              <span className="text-gray-500">No change</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
