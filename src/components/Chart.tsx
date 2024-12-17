import React from 'react';

interface ChartProps {
  data: any[];
}

const Chart: React.FC<ChartProps> = ({ data }) => {
  return (
    <div>
      <h2>Chart Component</h2>
      {/* Example chart rendering */}
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default Chart;
