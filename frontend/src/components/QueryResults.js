import React from 'react';

const QueryResults = ({ simpleQueries, complexQueries, onFetchSimple, onFetchComplex }) => {
  return (
    <div>
      <div className="row mb-3">
        <div className="col-md-6">
          <button className="btn btn-primary w-100" onClick={onFetchSimple}>
            Execute Simple Queries
          </button>
        </div>
        <div className="col-md-6">
          <button className="btn btn-success w-100" onClick={onFetchComplex}>
            Execute Complex Queries
          </button>
        </div>
      </div>

      <div className="row">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5>Simple Neo4j Queries</h5>
            </div>
            <div className="card-body">
              {Object.keys(simpleQueries).length > 0 ? (
                Object.entries(simpleQueries).map(([queryName, result]) => (
                  <div key={queryName} className="mb-3">
                    <h6>{queryName.replace(/_/g, ' ').toUpperCase()}</h6>
                    <div className="border rounded p-2 bg-light">
                      <pre className="mb-0">
                        {JSON.stringify(result, null, 2)}
                      </pre>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-muted">Click "Execute Simple Queries" to see results</p>
              )}
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5>Complex Neo4j Queries</h5>
            </div>
            <div className="card-body">
              {Object.keys(complexQueries).length > 0 ? (
                Object.entries(complexQueries).map(([queryName, result]) => (
                  <div key={queryName} className="mb-3">
                    <h6>{queryName.replace(/_/g, ' ').toUpperCase()}</h6>
                    <div className="border rounded p-2 bg-light">
                      <pre className="mb-0">
                        {JSON.stringify(result, null, 2)}
                      </pre>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-muted">Click "Execute Complex Queries" to see results</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QueryResults;
