from flask import Flask, jsonify, request
from flask_cors import CORS
from flight_data_collector import FlightDataCollector
from neo4j_connection import Neo4jConnection
import threading
import time
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global variables
flight_collector = None
neo4j_conn = None
is_collecting = False
collection_thread = None
last_api_call = 0

def initialize_connections():
    """Initialize connections with error handling"""
    global flight_collector, neo4j_conn
    try:
        flight_collector = FlightDataCollector()
        neo4j_conn = Neo4jConnection()
        print("✅ Connections initialized successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize connections: {e}")
        print("App will run but some features may not work")

def continuous_data_collection():
    """Background thread for continuous data collection"""
    global is_collecting
    while is_collecting:
        try:
            flight_collector.collect_and_store()
            time.sleep(120)  # Collect data every 2 minutes to avoid rate limits
        except Exception as e:
            print(f"Error in data collection: {e}")
            time.sleep(180)  # Wait 3 minutes on error

@app.route('/api/start-collection', methods=['POST'])
def start_collection():
    """Start continuous flight data collection"""
    global is_collecting, collection_thread
    
    if not is_collecting:
        is_collecting = True
        collection_thread = threading.Thread(target=continuous_data_collection)
        collection_thread.daemon = True
        collection_thread.start()
        return jsonify({'message': 'Data collection started', 'status': 'success'})
    else:
        return jsonify({'message': 'Data collection already running', 'status': 'info'})

@app.route('/api/stop-collection', methods=['POST'])
def stop_collection():
    """Stop continuous flight data collection"""
    global is_collecting
    is_collecting = False
    return jsonify({'message': 'Data collection stopped', 'status': 'success'})

@app.route('/api/collect-once', methods=['POST'])
def collect_once():
    """Collect flight data once"""
    global last_api_call
    try:
        if flight_collector is None:
            return jsonify({'message': 'Flight collector not initialized', 'status': 'error'})
        
        # Rate limiting: only allow one call every 30 seconds
        current_time = time.time()
        if current_time - last_api_call < 30:
            return jsonify({'message': 'Please wait 30 seconds between API calls to avoid rate limiting', 'status': 'error'})
        
        last_api_call = current_time
        flight_collector.collect_and_store()
        return jsonify({'message': 'Data collected successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}', 'status': 'error'})

@app.route('/api/flights', methods=['GET'])
def get_flights():
    """Get current flight data"""
    try:
        if flight_collector is None:
            return jsonify({'error': 'Flight collector not initialized', 'flights': [], 'count': 0}), 200
        
        # Check if we have cached flight data
        if hasattr(flight_collector, 'flight_data') and flight_collector.flight_data:
            return jsonify({'flights': flight_collector.flight_data[-50:], 'count': len(flight_collector.flight_data)})
        
        # Return empty data to avoid hanging on API calls
        return jsonify({'flights': [], 'count': 0, 'message': 'No cached flight data available. Use /api/collect-once to fetch new data.'})
    except Exception as e:
        return jsonify({'error': str(e), 'flights': [], 'count': 0}), 200

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify backend is working"""
    return jsonify({'message': 'Backend is working!', 'status': 'success'})

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get flight statistics"""
    try:
        if flight_collector is None:
            return jsonify({'error': 'Flight collector not initialized', 'total_flights': 0, 'flights_in_air': 0, 'flights_on_ground': 0, 'avg_altitude': 0}), 200
        
        stats = flight_collector.get_flight_statistics()
        return jsonify(stats)
    except Exception as e:
        print(f"Statistics error: {e}")
        return jsonify({'error': str(e), 'total_flights': 0, 'flights_in_air': 0, 'flights_on_ground': 0, 'avg_altitude': 0}), 200

# Neo4j Queries
@app.route('/api/queries/simple', methods=['GET'])
def get_simple_queries():
    """Execute 5 simple Neo4j queries"""
    queries = {
        'total_flights': "MATCH (f:Flight) RETURN count(f) as total_flights",
        'flights_by_country': "MATCH (f:Flight) RETURN f.origin_country as country, count(f) as flight_count ORDER BY flight_count DESC LIMIT 10",
        'flights_in_air': "MATCH (f:Flight) WHERE f.on_ground = false RETURN count(f) as flights_in_air",
        'avg_altitude': "MATCH (f:Flight) WHERE f.baro_altitude IS NOT NULL RETURN avg(f.baro_altitude) as avg_altitude",
        'unique_aircraft': "MATCH (f:Flight) RETURN count(DISTINCT f.icao24) as unique_aircraft"
    }
    
    results = {}
    for name, query in queries.items():
        try:
            result = neo4j_conn.execute_query(query)
            results[name] = [dict(record) for record in result]
        except Exception as e:
            results[name] = {'error': str(e)}
    
    return jsonify(results)

@app.route('/api/queries/complex', methods=['GET'])
def get_complex_queries():
    """Execute 5 complex Neo4j queries"""
    queries = {
        'flight_routes': """
            MATCH (f:Flight)-[:DEPARTS_FROM]->(origin:Airport)
            MATCH (f)-[:ARRIVES_AT]->(dest:Airport)
            RETURN origin.name as origin, dest.name as destination, count(f) as route_count
            ORDER BY route_count DESC LIMIT 10
        """,
        'busiest_airports': """
            MATCH (f:Flight)-[:DEPARTS_FROM|ARRIVES_AT]->(a:Airport)
            RETURN a.name as airport, count(f) as flight_count
            ORDER BY flight_count DESC LIMIT 10
        """,
        'altitude_distribution': """
            MATCH (f:Flight)
            WHERE f.baro_altitude IS NOT NULL
            RETURN 
                CASE 
                    WHEN f.baro_altitude < 10000 THEN 'Low (<10k ft)'
                    WHEN f.baro_altitude < 30000 THEN 'Medium (10k-30k ft)'
                    ELSE 'High (>30k ft)'
                END as altitude_range,
                count(f) as flight_count
            ORDER BY flight_count DESC
        """,
        'velocity_analysis': """
            MATCH (f:Flight)
            WHERE f.velocity IS NOT NULL AND f.velocity > 0
            RETURN 
                avg(f.velocity) as avg_velocity,
                max(f.velocity) as max_velocity,
                min(f.velocity) as min_velocity,
                count(f) as total_flights
        """,
        'country_aircraft_types': """
            MATCH (f:Flight)
            WHERE f.callsign IS NOT NULL AND f.callsign <> 'UNKNOWN'
            WITH f.origin_country as country, 
                 substring(f.callsign, 0, 2) as airline_code,
                 count(f) as flight_count
            RETURN country, airline_code, flight_count
            ORDER BY country, flight_count DESC
        """
    }
    
    results = {}
    for name, query in queries.items():
        try:
            result = neo4j_conn.execute_query(query)
            results[name] = [dict(record) for record in result]
        except Exception as e:
            results[name] = {'error': str(e)}
    
    return jsonify(results)

@app.route('/api/eda', methods=['GET'])
def get_eda_data():
    """Get data for Exploratory Data Analysis"""
    try:
        if flight_collector is None:
            return jsonify({'error': 'Flight collector not initialized'}), 200
        
        # Use cached flight data instead of fetching new data
        if not hasattr(flight_collector, 'flight_data') or not flight_collector.flight_data:
            return jsonify({'error': 'No flight data available. Use /api/collect-once first.'}), 200
        
        # Convert to DataFrame for analysis
        import pandas as pd
        df = pd.DataFrame(flight_collector.flight_data)
        
        # Statistical analysis
        eda_results = {
            'basic_stats': {
                'total_flights': len(df),
                'avg_altitude': float(df['baro_altitude'].mean()) if df['baro_altitude'].notna().any() else 0,
                'avg_velocity': float(df['velocity'].mean()) if df['velocity'].notna().any() else 0,
                'flights_on_ground': int(df['on_ground'].sum()),
                'flights_in_air': int((~df['on_ground']).sum()),
                'max_altitude': float(df['baro_altitude'].max()) if df['baro_altitude'].notna().any() else 0,
                'min_altitude': float(df['baro_altitude'].min()) if df['baro_altitude'].notna().any() else 0,
                'max_velocity': float(df['velocity'].max()) if df['velocity'].notna().any() else 0,
                'min_velocity': float(df['velocity'].min()) if df['velocity'].notna().any() else 0
            },
            'altitude_distribution': df['baro_altitude'].describe().to_dict() if df['baro_altitude'].notna().any() else {},
            'velocity_distribution': df['velocity'].describe().to_dict() if df['velocity'].notna().any() else {},
            'country_distribution': df['origin_country'].value_counts().to_dict(),
            'airline_distribution': df['callsign'].str[:3].value_counts().head(10).to_dict(),
            'altitude_ranges': {
                'low_altitude': int((df['baro_altitude'] < 10000).sum()),
                'medium_altitude': int(((df['baro_altitude'] >= 10000) & (df['baro_altitude'] < 30000)).sum()),
                'high_altitude': int((df['baro_altitude'] >= 30000).sum())
            }
        }
        
        return jsonify(eda_results)
    except Exception as e:
        print(f"EDA error: {e}")
        return jsonify({'error': str(e)}), 200

if __name__ == '__main__':
    print("Starting Live Flight Detector Backend...")
    print("Available endpoints:")
    print("- POST /api/start-collection - Start continuous data collection")
    print("- POST /api/stop-collection - Stop data collection")
    print("- POST /api/collect-once - Collect data once")
    print("- GET /api/flights - Get current flights")
    print("- GET /api/statistics - Get flight statistics")
    print("- GET /api/queries/simple - Execute simple Neo4j queries")
    print("- GET /api/queries/complex - Execute complex Neo4j queries")
    print("- GET /api/eda - Get EDA data")
    
    # Initialize connections
    initialize_connections()
    
    app.run(debug=True, host='0.0.0.0', port=9000)
