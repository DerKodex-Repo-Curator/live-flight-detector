import requests
import json
import time
from datetime import datetime
from neo4j_connection import Neo4jConnection
import pandas as pd
import numpy as np

class FlightDataCollector:
    def __init__(self):
        self.neo4j = Neo4jConnection()
        self.api_url = "https://opensky-network.org/api/states/all"
        self.flight_data = []
    
    def fetch_live_flights(self):
        """Fetch live flight data from OpenSky API"""
        try:
            # Add delay to avoid rate limiting
            time.sleep(2)
            response = requests.get(self.api_url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get('states', [])
            elif response.status_code == 429:
                print("Rate limited by OpenSky API. Returning empty data.")
                return []
            else:
                print(f"API Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching flight data: {e}")
            return []
    
    def process_flight_data(self, states):
        """Process and clean flight data"""
        processed_flights = []
        
        for state in states:
            if len(state) >= 17:  # Ensure we have all required fields
                flight_data = {
                    'icao24': state[0],
                    'callsign': state[1].strip() if state[1] else 'UNKNOWN',
                    'origin_country': state[2],
                    'time_position': state[3],
                    'last_contact': state[4],
                    'longitude': state[5],
                    'latitude': state[6],
                    'baro_altitude': state[7],
                    'on_ground': state[8],
                    'velocity': state[9],
                    'true_track': state[10],
                    'vertical_rate': state[11],
                    'sensors': state[12],
                    'geo_altitude': state[13],
                    'squawk': state[14],
                    'spi': state[15],
                    'position_source': state[16]
                }
                processed_flights.append(flight_data)
        
        return processed_flights
    
    def store_in_neo4j(self, flights):
        """Store flight data in Neo4j database"""
        if not self.neo4j.driver:
            print("⚠️ Neo4j not connected, skipping storage")
            return
        
        for flight in flights:
            try:
                self.neo4j.create_flight_node(flight)
                print(f"Stored flight: {flight['callsign']}")
            except Exception as e:
                print(f"Error storing flight {flight['callsign']}: {e}")
    
    def collect_and_store(self):
        """Main method to collect and store flight data"""
        print("Collecting live flight data...")
        states = self.fetch_live_flights()
        
        if states:
            processed_flights = self.process_flight_data(states)
            self.store_in_neo4j(processed_flights)
            # Store the latest data (keep last 1000 flights)
            self.flight_data = processed_flights[-1000:] if len(processed_flights) > 1000 else processed_flights
            print(f"Collected {len(processed_flights)} flights")
        else:
            print("No flight data received - using sample data")
            # Create sample flight data if API fails
            self.flight_data = self.create_sample_flight_data()
    
    def get_flight_statistics(self):
        """Calculate basic statistics from collected flight data"""
        if not self.flight_data:
            return {
                'total_flights': 0,
                'flights_in_air': 0,
                'flights_on_ground': 0,
                'avg_altitude': 0,
                'avg_velocity': 0
            }
        
        df = pd.DataFrame(self.flight_data)
        
        stats = {
            'total_flights': int(len(df)),
            'flights_in_air': int((~df['on_ground']).sum()),
            'flights_on_ground': int(df['on_ground'].sum()),
            'avg_altitude': float(df['baro_altitude'].mean()) if df['baro_altitude'].notna().any() else 0,
            'avg_velocity': float(df['velocity'].mean()) if df['velocity'].notna().any() else 0
        }
        
        return stats
    
    def create_sample_flight_data(self):
        """Create sample flight data for demonstration"""
        import random
        sample_flights = []
        airlines = ['UAL', 'DAL', 'AAL', 'SWA', 'JBU', 'AFR', 'BAW', 'DLH', 'KLM', 'EZY']
        countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Spain', 'Italy', 'Netherlands']
        
        for i in range(50):
            flight = {
                'icao24': f'abc{i:03d}',
                'callsign': f'{random.choice(airlines)}{random.randint(100, 9999)}',
                'origin_country': random.choice(countries),
                'time_position': int(time.time()),
                'last_contact': int(time.time()),
                'longitude': random.uniform(-180, 180),
                'latitude': random.uniform(-90, 90),
                'baro_altitude': random.uniform(0, 40000),
                'on_ground': random.choice([True, False]),
                'velocity': random.uniform(0, 500),
                'true_track': random.uniform(0, 360),
                'vertical_rate': random.uniform(-2000, 2000),
                'sensors': [],
                'geo_altitude': random.uniform(0, 40000),
                'squawk': f'{random.randint(1000, 7777)}',
                'spi': False,
                'position_source': 0
            }
            sample_flights.append(flight)
        
        print(f"Created {len(sample_flights)} sample flights")
        return sample_flights
    
    def close(self):
        self.neo4j.close()
