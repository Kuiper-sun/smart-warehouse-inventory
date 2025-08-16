import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend
);

const Dashboard = ({ inventoryData, error }) => {
  if (error) {
    return <div style={{ padding: '20px', color: 'red' }}><h1>Error</h1><p>{error}</p></div>;
  }

  const chartData = {
    labels: inventoryData.map(d => new Date(d.last_scanned).toLocaleString()),
    datasets: [{
      label: 'Quantity Scanned',
      data: inventoryData.map(d => d.quantity),
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      fill: true,
    }]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Recent Inventory Movements' },
    },
    scales: {
      x: { title: { display: true, text: 'Scan Time' } },
      y: { title: { display: true, text: 'Quantity' } }
    }
  };

  return (
    <div style={{ fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h1>Smart Warehouse Dashboard</h1>
      <div style={{ width: '80%', margin: 'auto' }}>
        {inventoryData.length > 0 ? (
          <Line data={chartData} options={options} />
        ) : (
          <p>No inventory data available. Send some data to the API endpoint.</p>
        )}
      </div>
    </div>
  );
};

export async function getServerSideProps() {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
    // Important: Use http://webserver inside the container, not localhost
    const containerApiUrl = 'http://webserver/api/inventory';
    const res = await fetch(containerApiUrl);

    if (!res.ok) {
      throw new Error(`Failed to fetch data from API: ${res.status} ${res.statusText}`);
    }
    const data = await res.json();
    return { props: { inventoryData: data.slice(0, 50).reverse() } };
  } catch (error) {
    console.error("Error in getServerSideProps:", error);
    return { props: { inventoryData: [], error: error.message } };
  }
}

export default Dashboard; 
