import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import axios from 'axios';
import DroneMap from './Map';
import './Dashboard.css';

const socket = io('http://localhost:5000');

const Dashboard = () => {
  const [droneStatus, setDroneStatus] = useState({});
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const fetchStatus = async () => {
      const response = await axios.get('http://localhost:5000/api/drone/status');
      setDroneStatus(response.data);
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 1000);
    return () => clearInterval(interval);
  }, []);

  const sendCommand = (command) => {
    socket.emit('drone_command', { command });
  };

  return (
    <div className="dashboard">
      <aside className="status-panel">
        <h2 className="status-title">Drone Telemetry</h2>
        <div className="status-grid">
          <div className="status-item">
            <span className="status-label">Battery</span>
            <span className="status-value">{droneStatus.battery}%</span>
          </div>
          <div className="status-item">
            <span className="status-label">Altitude</span>
            <span className="status-value">{droneStatus.altitude}m</span>
          </div>
          <div className="status-item">
            <span className="status-label">Angle</span>
            <span className="status-value">{droneStatus.angle}°</span>
          </div>
          <div className="status-item">
            <span className="status-label">Pressure</span>
            <span className="status-value">{droneStatus.pressure}hPa</span>
          </div>
          <div className="status-item">
            <span className="status-label">Temperature</span>
            <span className="status-value">{droneStatus.temperature}°C</span>
          </div>
          <div className="status-item">
            <span className="status-label">Height</span>
            <span className="status-value">{droneStatus.height}m</span>
          </div>
        </div>
        <div className="telemetry">
          <div className="gauge">
            <div className="gauge-value">{droneStatus.battery}%</div>
            <div className="gauge-label">Battery</div>
          </div>
          <div className="gauge">
            <div className="gauge-value">{droneStatus.height}m</div>
            <div className="gauge-label">Altitude</div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <div className="map-container">
          <DroneMap />
        </div>

        <div className="controls-panel">
          <div className="flight-controls">
            <h3>Flight Controls</h3>
            <div className="direction-controls">
              <button className="control-button">↖</button>
              <button className="control-button" onClick={() => sendCommand('forward')}>↑</button>
              <button className="control-button">↗</button>
              <button className="control-button" onClick={() => sendCommand('left')}>←</button>
              <button className="control-button" onClick={() => sendCommand('up')}>⊙</button>
              <button className="control-button" onClick={() => sendCommand('right')}>→</button>
              <button className="control-button">↙</button>
              <button className="control-button" onClick={() => sendCommand('backward')}>↓</button>
              <button className="control-button">↘</button>
            </div>
          </div>

          <div className="emergency-controls">
            <h3>Emergency Controls</h3>
            <button className="control-button takeoff" onClick={() => sendCommand('takeoff')}>
              Take Off
            </button>
            <button className="control-button land" onClick={() => sendCommand('land')}>
              Emergency Land
            </button>
            <button className="control-button" onClick={() => sendCommand('flip')}>
              Flip
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
