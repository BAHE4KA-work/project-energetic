import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Area, ResponsiveContainer, ReferenceLine,
} from 'recharts';

interface EnergyLineChartProps {
  data: { week: number; consumption: number }[];
  normalAverage?: number;
}

export const EnergyLineChart: React.FC<EnergyLineChartProps> = ({ data, normalAverage }) => {
  const max = Math.max(...data.map(d => d.consumption));
  const roundedMax = Math.ceil(max / 100) * 100;

  const step = Math.ceil(roundedMax / 6); // 6 промежутков = 7 делений
  const yTicks = Array.from({ length: 7 }, (_, i) => i * step);

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
        Потребление электроэнергии по неделям (ТНС Кубань энерго)
      </h3>

      <span style={{
        fontSize: 12,
        fontFamily: 'Inter',
        color: '#555',
        marginBottom: '12px',
        display: 'inline-block',
      }}>
        Тыс. кВт/ч
      </span>

      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data}>
          <defs>
            <linearGradient id="grayFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#CCCCCC" stopOpacity={0.6} />
              <stop offset="100%" stopColor="#CCCCCC" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid stroke="#ccc" strokeWidth={1} />
          <XAxis
            dataKey="week"
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
            domain={[0, roundedMax]}
            ticks={yTicks}
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
            tickFormatter={(v) => `${v}`}
          />
          <Tooltip formatter={(v: number) => `${v} кВт/ч`} />

          <Area type="linear" dataKey="consumption" stroke="none" fill="url(#grayFill)" />
          <Line type="linear" dataKey="consumption" stroke="#121212" strokeWidth={1.5} dot={false} />

          {normalAverage && (
            <ReferenceLine
              y={normalAverage}
              stroke="#50BF70"
              strokeDasharray="6 6"
              strokeWidth={2}
            />
          )}
        </LineChart>
      </ResponsiveContainer>

      <div style={{
        marginTop: '12px',
        textAlign: 'center',
        fontFamily: 'Inter',
        fontSize: '14px',
        fontWeight: 400,
        color: '#555',
      }}>
        Недели (март 2025 – май 2025)
      </div>
    </div>
  );
};
