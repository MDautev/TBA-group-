// src/pages/Dashboard.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

export function Dashboard({ user }) {
  const navigate = useNavigate();

  if (!user) {
    return (
      <div className="text-center">
        <h2>Please log in to continue</h2>
        <button onClick={() => navigate('/login')} className="p-2 bg-blue-500 text-white rounded mt-4">
          Login
        </button>
      </div>
    );
  }

  const renderClientDashboard = () => (
    <div className="dashboard-container client-dashboard">
      <h3 className="dashboard-title">Welcome, Client!</h3>
      <div className="dashboard-section">
        <p>Here you can browse products, place orders and track deliveries.</p>
      </div>
      <button onClick={() => alert("Place order")} className="dashboard-btn">
        Place Order
      </button>
    </div>
  );

  const renderStaffDashboard = () => (
    <div className="dashboard-container staff-dashboard">
      <h3 className="dashboard-title">Welcome, Staff!</h3>
      <div className="dashboard-section">
        <p>Manage restaurants and food items, as well as view orders.</p>
      </div>
      <button onClick={() => alert("Manage restaurants and products")} className="dashboard-btn">
        Manage
      </button>
    </div>
  );

  const renderDelivererDashboard = () => (
    <div className="dashboard-container deliverer-dashboard">
      <h3 className="dashboard-title">Welcome, Deliverer!</h3>
      <div className="dashboard-section">
        <p>View active deliveries, track orders and complete your tasks.</p>
      </div>
      <button onClick={() => alert("Manage deliveries")} className="dashboard-btn">
        Manage Deliveries
      </button>
    </div>
  );

  if (user.role === 'client') {
    return renderClientDashboard();
  } else if (user.role === 'staff') {
    return renderStaffDashboard();
  } else if (user.role === 'deliverer') {
    return renderDelivererDashboard();
  }

  return <div>Unknown role</div>;
}
