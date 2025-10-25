import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import FlightMap from './components/FlightMap';
import FlightTable from './components/FlightTable';
import StatisticsPanel from './components/StatisticsPanel';
import QueryResults from './components/QueryResults';
import EDAPanel from './components/EDAPanel';
import ControlPanel from './components/ControlPanel';

function App() {
  const [flights, setFlights] = useState([]);
  const [statistics, setStatistics] = useState({});
  const [simpleQueries, setSimpleQueries] = useState({});
  const [complexQueries, setComplexQueries] = useState({});
  const [edaData, setEdaData] = useState({});
  const [isCollecting, setIsCollecting] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');

  // Fetch flights data
  const fetchFlights = async () => {
    try {
      const response = await axios.get('/api/flights');
      setFlights(response.data.flights || []);
    } catch (error) {
      console.error('Error fetching flights:', error);
    }
  };

  // Fetch statistics
  const fetchStatistics = async () => {
    try {
      const response = await axios.get('/api/statistics');
      setStatistics(response.data);
    } catch (error) {
      console.error('Error fetching statistics:', error);
    }
  };

  // Fetch simple queries
  const fetchSimpleQueries = async () => {
    try {
      const response = await axios.get('/api/queries/simple');
      setSimpleQueries(response.data);
    } catch (error) {
      console.error('Error fetching simple queries:', error);
    }
  };

  // Fetch complex queries
  const fetchComplexQueries = async () => {
    try {
      const response = await axios.get('/api/queries/complex');
      setComplexQueries(response.data);
    } catch (error) {
      console.error('Error fetching complex queries:', error);
    }
  };

  // Fetch EDA data
  const fetchEdaData = async () => {
    try {
      const response = await axios.get('/api/eda');
      setEdaData(response.data);
    } catch (error) {
      console.error('Error fetching EDA data:', error);
    }
  };

  // Start data collection
  const startCollection = async () => {
    try {
      await axios.post('/api/start-collection');
      setIsCollecting(true);
    } catch (error) {
      console.error('Error starting collection:', error);
    }
  };

  // Stop data collection
  const stopCollection = async () => {
    try {
      await axios.post('/api/stop-collection');
      setIsCollecting(false);
    } catch (error) {
      console.error('Error stopping collection:', error);
    }
  };

  // Collect data once
  const collectOnce = async () => {
    try {
      await axios.post('/api/collect-once');
      fetchFlights();
      fetchStatistics();
    } catch (error) {
      console.error('Error collecting data:', error);
    }
  };

  // Auto-refresh data every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchFlights();
      fetchStatistics();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  // Initial data fetch
  useEffect(() => {
    fetchFlights();
    fetchStatistics();
  }, []);

  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            🛩️ Live Flight Detector
          </a>
          <div className="navbar-nav">
            <button 
              className={`nav-link btn ${activeTab === 'dashboard' ? 'btn-primary' : 'btn-outline-primary'} me-2`}
              onClick={() => setActiveTab('dashboard')}
            >
              Dashboard
            </button>
            <button 
              className={`nav-link btn ${activeTab === 'queries' ? 'btn-primary' : 'btn-outline-primary'} me-2`}
              onClick={() => setActiveTab('queries')}
            >
              Neo4j Queries
            </button>
            <button 
              className={`nav-link btn ${activeTab === 'eda' ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => setActiveTab('eda')}
            >
              EDA Analysis
            </button>
          </div>
        </div>
      </nav>

      <div className="container-fluid mt-3">
        {activeTab === 'dashboard' && (
          <>
            <ControlPanel 
              isCollecting={isCollecting}
              onStartCollection={startCollection}
              onStopCollection={stopCollection}
              onCollectOnce={collectOnce}
            />
            
            <div className="row">
              <div className="col-md-8">
                <div className="card mb-3">
                  <div className="card-header">
                    <h5>Live Flight Map</h5>
                  </div>
                  <div className="card-body">
                    <FlightMap flights={flights} />
                  </div>
                </div>
                
                <div className="card">
                  <div className="card-header">
                    <h5>Flight Data Table</h5>
                  </div>
                  <div className="card-body">
                    <FlightTable flights={flights} />
                  </div>
                </div>
              </div>
              
              <div className="col-md-4">
                <StatisticsPanel statistics={statistics} />
              </div>
            </div>
          </>
        )}

        {activeTab === 'queries' && (
          <QueryResults 
            simpleQueries={simpleQueries}
            complexQueries={complexQueries}
            onFetchSimple={fetchSimpleQueries}
            onFetchComplex={fetchComplexQueries}
          />
        )}

        {activeTab === 'eda' && (
          <EDAPanel 
            edaData={edaData}
            onFetchEda={fetchEdaData}
          />
        )}
      </div>
    </div>
  );
}

export default App;
