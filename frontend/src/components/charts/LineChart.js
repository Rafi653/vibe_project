import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function LineChart({ title, labels, datasets, options = {} }) {
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
    scales: {
      y: {
        beginAtZero: true,
      },
    },
    ...options,
  };

  const data = {
    labels,
    datasets: datasets.map((dataset, index) => ({
      fill: dataset.fill !== undefined ? dataset.fill : false,
      tension: 0.3,
      borderColor: dataset.borderColor || `hsl(${index * 137.5}, 70%, 50%)`,
      backgroundColor: dataset.backgroundColor || `hsla(${index * 137.5}, 70%, 50%, 0.5)`,
      ...dataset,
    })),
  };

  return (
    <div style={{ height: '300px', width: '100%' }}>
      <Line options={defaultOptions} data={data} />
    </div>
  );
}

export default LineChart;
