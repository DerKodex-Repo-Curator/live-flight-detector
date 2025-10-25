import React from 'react';

const FlightTable = ({ flights }) => {
  return (
    <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
      <table className="table table-striped table-hover">
        <thead className="table-dark sticky-top">
          <tr>
            <th>Callsign</th>
            <th>Country</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Altitude</th>
            <th>Velocity</th>
            <th>On Ground</th>
          </tr>
        </thead>
        <tbody>
          {flights.slice(0, 50).map((flight, index) => (
            <tr key={index}>
              <td>{flight.callsign || 'N/A'}</td>
              <td>{flight.origin_country || 'N/A'}</td>
              <td>{flight.latitude ? flight.latitude.toFixed(4) : 'N/A'}</td>
              <td>{flight.longitude ? flight.longitude.toFixed(4) : 'N/A'}</td>
              <td>{flight.baro_altitude ? `${Math.round(flight.baro_altitude)} ft` : 'N/A'}</td>
              <td>{flight.velocity ? `${Math.round(flight.velocity)} m/s` : 'N/A'}</td>
              <td>
                <span className={`badge ${flight.on_ground ? 'bg-success' : 'bg-primary'}`}>
                  {flight.on_ground ? 'Ground' : 'Air'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {flights.length === 0 && (
        <div className="text-center text-muted py-4">
          No flight data available. Click "Collect Once" to fetch data.
        </div>
      )}
    </div>
  );
};

export default FlightTable;
