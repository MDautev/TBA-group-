import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { FoodCatalog } from "./pages/FoodCatalog";
import { OrderTracking } from "./pages/OrderTracking";
import { Navbar } from "./components/Navbar";

export default function App() {
  const [user, setUser] = useState(null);

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navbar user={user} setUser={setUser} />
        <Routes>
          <Route path="/" element={<FoodCatalog />} />
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/orders" element={<OrderTracking user={user} />} />
        </Routes>
      </div>
    </Router>
  );
}
