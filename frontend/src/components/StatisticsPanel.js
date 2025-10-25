import React from 'react';

const StatisticsPanel = ({ statistics }) => {
  return (
    <div className="card">
      <div className="card-header">
        <h5>Flight Statistics</h5>
      </div>
      <div className="card-body">
        <div className="row text-center">
          <div className="col-6 mb-3">
            <div className="border rounded p-2">
              <h6 className="text-primary">{statistics.total_flights || 0}</h6>
              <small className="text-muted">Total Flights</small>
            </div>
          </div>
          <div className="col-6 mb-3">
            <div className="border rounded p-2">
              <h6 className="text-success">{statistics.flights_in_air || 0}</h6>
              <small className="text-muted">In Air</small>
            </div>
          </div>
          <div className="col-6 mb-3">
            <div className="border rounded p-2">
              <h6 className="text-warning">{statistics.flights_on_ground || 0}</h6>
              <small className="text-muted">On Ground</small>
            </div>
          </div>
          <div className="col-6 mb-3">
            <div className="border rounded p-2">
              <h6 className="text-info">{Math.round(statistics.avg_altitude || 0)}</h6>
              <small className="text-muted">Avg Altitude (ft)</small>
            </div>
          </div>
        </div>
        
        {statistics.countries && Object.keys(statistics.countries).length > 0 && (
          <div className="mt-3">
            <h6>Top Countries</h6>
            <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
              {Object.entries(statistics.countries)
                .slice(0, 10)
                .map(([country, count]) => (
                  <div key={country} className="d-flex justify-content-between">
                    <span>{country}</span>
                    <span className="badge bg-secondary">{count}</span>
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatisticsPanel;
