import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function BarChart({ title, labels, datasets, options = {} }) {
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
      borderWidth: 1,
      backgroundColor: dataset.backgroundColor || `hsla(${index * 137.5}, 70%, 50%, 0.7)`,
      borderColor: dataset.borderColor || `hsl(${index * 137.5}, 70%, 50%)`,
      ...dataset,
    })),
  };

  return (
    <div style={{ height: '300px', width: '100%' }}>
      <Bar options={defaultOptions} data={data} />
    </div>
  );
}

export default BarChart;
