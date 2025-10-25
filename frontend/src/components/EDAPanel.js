import React from 'react';

const EDAPanel = ({ edaData, onFetchEda }) => {
  return (
    <div>
      <div className="row mb-3">
        <div className="col-12">
          <button className="btn btn-primary" onClick={onFetchEda}>
            Refresh EDA Analysis
          </button>
        </div>
      </div>

      {Object.keys(edaData).length > 0 ? (
        <div className="row">
          <div className="col-md-6">
            <div className="card mb-3">
              <div className="card-header">
                <h5>Basic Statistics</h5>
              </div>
              <div className="card-body">
                {edaData.basic_stats && (
                  <div className="row text-center">
                    <div className="col-6 mb-2">
                      <div className="border rounded p-2">
                        <h6 className="text-primary">{edaData.basic_stats.total_flights}</h6>
                        <small>Total Flights</small>
                      </div>
                    </div>
                    <div className="col-6 mb-2">
                      <div className="border rounded p-2">
                        <h6 className="text-success">{edaData.basic_stats.flights_in_air}</h6>
                        <small>In Air</small>
                      </div>
                    </div>
                    <div className="col-6 mb-2">
                      <div className="border rounded p-2">
                        <h6 className="text-warning">{edaData.basic_stats.flights_on_ground}</h6>
                        <small>On Ground</small>
                      </div>
                    </div>
                    <div className="col-6 mb-2">
                      <div className="border rounded p-2">
                        <h6 className="text-info">{Math.round(edaData.basic_stats.avg_altitude || 0)}</h6>
                        <small>Avg Altitude</small>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="card mb-3">
              <div className="card-header">
                <h5>Country Distribution</h5>
              </div>
              <div className="card-body">
                {edaData.country_distribution && (
                  <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                    {Object.entries(edaData.country_distribution)
                      .slice(0, 15)
                      .map(([country, count]) => (
                        <div key={country} className="d-flex justify-content-between mb-1">
                          <span>{country}</span>
                          <span className="badge bg-primary">{count}</span>
                        </div>
                      ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="card">
              <div className="card-header">
                <h5>Altitude Distribution</h5>
              </div>
              <div className="card-body">
                {edaData.altitude_distribution && (
                  <div>
                    {Object.entries(edaData.altitude_distribution).map(([stat, value]) => (
                      <div key={stat} className="d-flex justify-content-between">
                        <span>{stat}</span>
                        <span>{Math.round(value * 100) / 100}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="card">
              <div className="card-header">
                <h5>Velocity Distribution</h5>
              </div>
              <div className="card-body">
                {edaData.velocity_distribution && (
                  <div>
                    {Object.entries(edaData.velocity_distribution).map(([stat, value]) => (
                      <div key={stat} className="d-flex justify-content-between">
                        <span>{stat}</span>
                        <span>{Math.round(value * 100) / 100}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="text-center text-muted py-5">
          <h5>No EDA Data Available</h5>
          <p>Click "Refresh EDA Analysis" to generate statistical analysis</p>
        </div>
      )}
    </div>
  );
};

export default EDAPanel;
