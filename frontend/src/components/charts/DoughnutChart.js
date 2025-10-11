import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

function DoughnutChart({ title, labels, data: chartData, options = {} }) {
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: !!title,
        text: title,
      },
    },
    ...options,
  };

  const data = {
    labels,
    datasets: [{
      data: chartData,
      backgroundColor: chartData.map((_, index) => `hsla(${index * 137.5}, 70%, 50%, 0.7)`),
      borderColor: chartData.map((_, index) => `hsl(${index * 137.5}, 70%, 50%)`),
      borderWidth: 1,
    }],
  };

  return (
    <div style={{ height: '300px', width: '100%' }}>
      <Doughnut options={defaultOptions} data={data} />
    </div>
  );
}

export default DoughnutChart;
