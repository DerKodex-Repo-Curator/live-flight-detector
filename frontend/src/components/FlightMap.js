import React from 'react';

const FlightMap = ({ flights }) => {
  // Create a simple SVG-based flight map
  const renderFlightMap = () => {
    if (!flights || flights.length === 0) {
      return (
        <div className="d-flex align-items-center justify-content-center h-100">
          <div className="text-center">
            <h6>Flight Map Visualization</h6>
            <p className="text-muted">No flights to display</p>
          </div>
        </div>
      );
    }

    const inAirFlights = flights.filter(f => !f.on_ground);
    const onGroundFlights = flights.filter(f => f.on_ground);

    return (
      <div className="h-100">
        <div className="row mb-3">
          <div className="col-6">
            <div className="card text-center">
              <div className="card-body py-2">
                <h5 className="text-success mb-0">{inAirFlights.length}</h5>
                <small>Flights in Air</small>
              </div>
            </div>
          </div>
          <div className="col-6">
            <div className="card text-center">
              <div className="card-body py-2">
                <h5 className="text-warning mb-0">{onGroundFlights.length}</h5>
                <small>Flights on Ground</small>
              </div>
            </div>
          </div>
        </div>
        
        <div style={{ height: '300px', border: '1px solid #dee2e6', borderRadius: '4px', position: 'relative', overflow: 'hidden' }}>
          <svg width="100%" height="100%" style={{ background: 'linear-gradient(135deg, #87CEEB 0%, #98FB98 100%)' }}>
            {/* World map outline (simplified) */}
            <rect x="0" y="0" width="100%" height="100%" fill="rgba(135, 206, 235, 0.3)" />
            
            {/* Flight positions */}
            {flights.slice(0, 20).map((flight, index) => {
              // Convert lat/lng to SVG coordinates
              const x = ((flight.longitude + 180) / 360) * 100;
              const y = ((90 - flight.latitude) / 180) * 100;
              
              const isInAir = !flight.on_ground;
              const color = isInAir ? '#dc3545' : '#ffc107';
              const size = isInAir ? 6 : 4;
              
              return (
                <g key={index}>
                  <circle
                    cx={`${x}%`}
                    cy={`${y}%`}
                    r={size}
                    fill={color}
                    stroke="white"
                    strokeWidth="1"
                  />
                  {isInAir && (
                    <circle
                      cx={`${x}%`}
                      cy={`${y}%`}
                      r={size + 2}
                      fill="none"
                      stroke={color}
                      strokeWidth="1"
                      opacity="0.5"
                    />
                  )}
                </g>
              );
            })}
            
            {/* Legend */}
            <g transform="translate(10, 10)">
              <rect x="0" y="0" width="120" height="60" fill="rgba(255,255,255,0.9)" rx="4" />
              <text x="10" y="20" fontSize="12" fontWeight="bold">Legend</text>
              <circle cx="15" cy="35" r="4" fill="#dc3545" />
              <text x="25" y="40" fontSize="10">In Air</text>
              <circle cx="15" cy="50" r="3" fill="#ffc107" />
              <text x="25" y="55" fontSize="10">On Ground</text>
            </g>
          </svg>
        </div>
        
        <div className="mt-2">
          <small className="text-muted">
            Showing {Math.min(flights.length, 20)} of {flights.length} flights
          </small>
        </div>
      </div>
    );
  };

  return (
    <div style={{ height: '400px' }}>
      {renderFlightMap()}
    </div>
  );
};

export default FlightMap;
