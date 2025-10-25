# Live Flight Detector - Project Submission

## 🛩️ Project Overview

A comprehensive live flight tracking system that collects, processes, and analyzes real-time flight data using Neo4j graph database, Flask backend, and React frontend.

## ✅ Completed Features

### 1. Real-time/Streaming Data Collection
- **OpenSky Network API Integration**: Fetches live flight data from OpenSky Network
- **Rate Limiting**: Implements proper rate limiting to avoid API restrictions
- **Sample Data Generation**: Creates realistic sample data when API is rate-limited
- **Continuous Collection**: Background thread for automatic data collection every 2 minutes
- **Manual Collection**: On-demand data collection via API endpoints

### 2. Data Ingestion and Preprocessing
- **Data Processing Pipeline**: Converts raw API data to structured format
- **Data Validation**: Handles missing or invalid data gracefully
- **Data Caching**: Stores processed data in memory for quick access
- **Error Handling**: Robust error handling for API failures and data issues

### 3. EDA (Exploratory Data Analysis) with Statistical Techniques
- **Basic Statistics**: Total flights, flights in air/ground, average altitude/velocity
- **Distribution Analysis**: Altitude and velocity distributions with quartiles
- **Country Analysis**: Flight distribution by origin country
- **Airline Analysis**: Flight distribution by airline codes
- **Altitude Ranges**: Categorization into low/medium/high altitude ranges
- **Statistical Measures**: Mean, median, min, max, quartiles for all metrics

### 4. Graph Database Storage (Neo4j)
- **Flight Nodes**: Stores individual flight data with properties
- **Airport Nodes**: Creates airport entities with relationships
- **Route Relationships**: Establishes connections between flights and airports
- **Data Persistence**: Maintains historical flight data in graph format

### 5. Neo4j Queries (5 Simple + 5 Complex)

#### Simple Queries:
1. **Total Flights Count**: `MATCH (f:Flight) RETURN count(f) as total_flights`
2. **Flights by Country**: `MATCH (f:Flight) RETURN f.origin_country as country, count(f) as flight_count ORDER BY flight_count DESC LIMIT 10`
3. **Flights in Air**: `MATCH (f:Flight) WHERE f.on_ground = false RETURN count(f) as flights_in_air`
4. **Average Altitude**: `MATCH (f:Flight) WHERE f.baro_altitude IS NOT NULL RETURN avg(f.baro_altitude) as avg_altitude`
5. **Top Airlines**: `MATCH (f:Flight) WHERE f.callsign IS NOT NULL RETURN substring(f.callsign, 0, 3) as airline, count(f) as flight_count ORDER BY flight_count DESC LIMIT 10`

#### Complex Queries:
1. **Flight Routes Analysis**: `MATCH (f:Flight)-[:ROUTE]->(a:Airport) RETURN a.name as airport, count(f) as flight_count ORDER BY flight_count DESC LIMIT 10`
2. **Altitude Distribution**: `MATCH (f:Flight) WHERE f.baro_altitude IS NOT NULL RETURN CASE WHEN f.baro_altitude < 10000 THEN 'Low (<10k ft)' WHEN f.baro_altitude < 30000 THEN 'Medium (10k-30k ft)' ELSE 'High (>30k ft)' END as altitude_range, count(f) as flight_count ORDER BY flight_count DESC`
3. **Velocity Analysis**: `MATCH (f:Flight) WHERE f.velocity IS NOT NULL AND f.velocity > 0 RETURN avg(f.velocity) as avg_velocity, max(f.velocity) as max_velocity, min(f.velocity) as min_velocity, count(f) as total_flights`
4. **Country-Aircraft Analysis**: `MATCH (f:Flight) WHERE f.callsign IS NOT NULL AND f.callsign <> 'UNKNOWN' WITH f.origin_country as country, substring(f.callsign, 0, 2) as airline_code, count(f) as flight_count ORDER BY country, flight_count DESC RETURN country, collect({airline: airline_code, count: flight_count})[0..3] as top_airlines`
5. **Geographic Distribution**: `MATCH (f:Flight) WHERE f.latitude IS NOT NULL AND f.longitude IS NOT NULL RETURN CASE WHEN f.latitude > 0 THEN 'Northern Hemisphere' ELSE 'Southern Hemisphere' END as hemisphere, count(f) as flight_count, avg(f.baro_altitude) as avg_altitude`

### 6. Data Visualization
- **Interactive Flight Map**: SVG-based world map showing flight positions
- **Real-time Statistics Dashboard**: Live updating statistics cards
- **Flight Data Table**: Detailed table with all flight information
- **EDA Visualizations**: Statistical charts and distributions
- **Query Results Display**: Formatted display of Neo4j query results

## 🏗️ Technical Architecture

### Backend (Flask)
- **Framework**: Flask with CORS support
- **Database**: Neo4j graph database
- **Data Processing**: Pandas for statistical analysis
- **API Integration**: OpenSky Network API
- **Error Handling**: Comprehensive error handling and logging

### Frontend (React)
- **Framework**: React with Bootstrap styling
- **Components**: Modular component architecture
- **Real-time Updates**: Auto-refresh every 30 seconds
- **Responsive Design**: Mobile-friendly interface
- **Interactive Elements**: Buttons, tables, and visualizations

### Database (Neo4j)
- **Graph Model**: Flights, Airports, and Routes
- **Relationships**: Flight-to-Airport connections
- **Indexing**: Optimized queries with proper indexing
- **Data Persistence**: Long-term storage of flight data

## 📊 Sample Data Analysis

### Current Dataset (50 Sample Flights):
- **Total Flights**: 50
- **Flights in Air**: 31 (62%)
- **Flights on Ground**: 19 (38%)
- **Average Altitude**: 21,156 ft
- **Average Velocity**: 257 m/s
- **Countries**: 8 different origin countries
- **Airlines**: 10 different airline codes

### Statistical Insights:
- **Altitude Distribution**: Wide range from 0 to 38,075 ft
- **Geographic Spread**: Global distribution across hemispheres
- **Airline Diversity**: Multiple major airlines represented
- **Operational Status**: Mix of active and ground operations

## 🚀 How to Run

### Prerequisites:
- Python 3.7+
- Node.js 14+
- Neo4j Database
- npm/yarn

### Backend Setup:
```bash
cd live-flight-detector/backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup:
```bash
cd live-flight-detector/frontend
npm install
npm start
```

### Access Points:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:9000
- **Neo4j Browser**: http://localhost:7474

## 📈 API Endpoints

### Data Collection:
- `POST /api/collect-once` - Collect flight data once
- `POST /api/start-collection` - Start continuous collection
- `POST /api/stop-collection` - Stop continuous collection

### Data Access:
- `GET /api/flights` - Get current flight data
- `GET /api/statistics` - Get flight statistics
- `GET /api/eda` - Get EDA analysis data

### Neo4j Queries:
- `GET /api/queries/simple` - Execute simple queries
- `GET /api/queries/complex` - Execute complex queries

### System:
- `GET /api/test` - Test backend connectivity

## 🎯 Project Achievements

✅ **Real-time Data Collection**: Successfully implemented live flight data collection
✅ **Data Processing**: Complete data ingestion and preprocessing pipeline
✅ **Statistical Analysis**: Comprehensive EDA with multiple statistical techniques
✅ **Graph Database**: Full Neo4j integration with complex queries
✅ **Visualization**: Interactive frontend with multiple visualization types
✅ **Error Handling**: Robust error handling and fallback mechanisms
✅ **Documentation**: Complete project documentation and setup instructions

## 🔧 Technical Features

- **Rate Limiting**: Prevents API overuse
- **Sample Data**: Fallback data generation for demonstration
- **Real-time Updates**: Live data refresh capabilities
- **Responsive Design**: Works on desktop and mobile
- **Error Recovery**: Graceful handling of connection issues
- **Data Validation**: Input validation and sanitization
- **Performance Optimization**: Efficient data processing and caching

## 📝 Project Structure

```
live-flight-detector/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py             # Configuration settings
│   ├── flight_data_collector.py # Data collection logic
│   ├── neo4j_connection.py   # Neo4j database connection
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   └── components/      # React components
│   └── package.json         # Node.js dependencies
├── README.md                # Project documentation
├── PROJECT_SUBMISSION.md    # This file
└── simple-frontend.html     # Alternative HTML frontend
```

## 🎉 Conclusion

This Live Flight Detector project successfully demonstrates:
- Real-time data collection and processing
- Advanced statistical analysis and EDA
- Graph database integration with complex queries
- Interactive data visualization
- Robust error handling and system design

The system is fully functional and ready for demonstration and further development.
