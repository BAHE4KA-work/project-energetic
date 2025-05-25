import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';

interface DeviationData {
  range: string;
  count: number;
}

interface DeviationBarChartProps {
  data: DeviationData[];
  isUserSpecific?: boolean; // <- новое поле
}

export const DeviationBarChart: React.FC<DeviationBarChartProps> = ({ data, isUserSpecific = false }) => {
  const maxValue = Math.max(...data.map(d => d.count));
  const roundedMax = Math.ceil(maxValue / 5) * 5;
  const step = roundedMax / 8;

  const yTicks = Array.from({ length: 9 }, (_, i) => Math.round(step * i));

  return (
    <div style={{
      width: '100%',
      height: 482,
      background: '#F0F3F4',
      borderRadius: 32,
      padding: '24px',
      paddingBottom: '48px',
    }}>
      <h3 style={{
        fontFamily: 'Roboto',
        fontWeight: 500,
        fontSize: '18px',
        marginBottom: '8px',
      }}>
        {isUserSpecific ? 'Показатель отклонения от нормы (по пользователю)' : 'Показатель отклонение от нормы (общая аналитика)'}
      </h3>

      <span style={{
        fontSize: 12,
        fontFamily: 'Inter',
        color: '#555',
        marginBottom: '12px',
        display: 'inline-block',
      }}>
        Кол-во нарушений
      </span>

      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data}>
          <CartesianGrid stroke="#ccc" strokeWidth={1} />
          <XAxis
            dataKey="range"
            tick={{
              fill: '#555',
              textAnchor: 'middle',
              fontFamily: 'Inter',
              fontSize: 12,
              fontWeight: 400,
              dy: 8,
            }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            ticks={yTicks}
            domain={[0, roundedMax]}
            tickFormatter={(v) => `${v}`}
            tick={{
              fill: '#555',
              textAnchor: 'end',
              fontFamily: 'Inter',
              fontSize: 12,
              fontWeight: 400,
              dx: -8,
            }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip formatter={(value: number) => `${value} нарушений`} />
          <Bar
            dataKey="count"
            radius={[8, 8, 0, 0]}
            fill="#5B49ED"
            barSize={54}
            isAnimationActive={true}
            animationDuration={1200}
            animationEasing="ease-out"
          />
        </BarChart>
      </ResponsiveContainer>

      <div style={{
        marginTop: '12px',
        textAlign: 'center',
        fontFamily: 'Inter',
        fontSize: '14px',
        fontWeight: 400,
        color: '#555',
        marginBottom: '12px',
      }}>
        Отклонение от нормы %
      </div>
    </div>
  );
};
