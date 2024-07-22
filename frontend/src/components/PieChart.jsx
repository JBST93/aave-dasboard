import React, { useEffect, useState } from 'react';
import axios from '../api/axios';
import { PieChart, Pie, Cell, Tooltip } from 'recharts';

const COLORS = [
  '#0088FE',
  '#00C49F',
  '#FFBB28',
  '#FF8042',
  '#845EC2',
  '#D65DB1',
  '#FF6F91',
  '#FF9671',
  '#FFC75F',
  '#F9F871',
];

const PieChartMktShare = () => {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('api/stablecoin_info');
        const dataset = response.data.stablecoin_info;

        // Sort the dataset by supply in descending order
        const sortedData = dataset.sort(
          (a, b) => (b.supply || 0) - (a.supply || 0)
        );

        // Get the top 5 stablecoins
        const top5 = sortedData.slice(0, 4).map((item, index) => ({
          name: item.token,
          value: item.supply || 0, // Ensure there's a default value if supply is missing
        }));

        // Sum the supplies of the remaining stablecoins and group them as "Others"
        const othersSupply = sortedData
          .slice(4)
          .reduce((sum, item) => sum + (item.supply || 0), 0);
        const others = {
          name: 'Others',
          value: othersSupply,
        };

        setChartData([...top5, others]);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <PieChart
      width={600}
      height={400}
    >
      <Pie
        data={chartData}
        labelLine={false}
        label={({ name }) => name}
        outerRadius={150}
        fill="#8884d8"
        dataKey="value"
      >
        {chartData.map((entry, index) => (
          <Cell
            key={`cell-${index}`}
            fill={COLORS[index % COLORS.length]}
          />
        ))}
      </Pie>
    </PieChart>
  );
};

export default PieChartMktShare;
