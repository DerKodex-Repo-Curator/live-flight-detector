import React from 'react';

const ControlPanel = ({ isCollecting, onStartCollection, onStopCollection, onCollectOnce }) => {
  return (
    <div className="card mb-3">
      <div className="card-header">
        <h5>Data Collection Control</h5>
      </div>
      <div className="card-body">
        <div className="row">
          <div className="col-md-4">
            <button 
              className={`btn btn-success w-100 ${isCollecting ? 'disabled' : ''}`}
              onClick={onStartCollection}
              disabled={isCollecting}
            >
              {isCollecting ? 'Collecting...' : 'Start Collection'}
            </button>
          </div>
          <div className="col-md-4">
            <button 
              className="btn btn-danger w-100"
              onClick={onStopCollection}
              disabled={!isCollecting}
            >
              Stop Collection
            </button>
          </div>
          <div className="col-md-4">
            <button 
              className="btn btn-primary w-100"
              onClick={onCollectOnce}
            >
              Collect Once
            </button>
          </div>
        </div>
        <div className="mt-2">
          <small className="text-muted">
            Status: {isCollecting ? '🟢 Collecting data every 30 seconds' : '🔴 Not collecting'}
          </small>
        </div>
      </div>
    </div>
  );
};

export default ControlPanel;
