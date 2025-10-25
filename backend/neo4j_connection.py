from neo4j import GraphDatabase
from config import Config

class Neo4jConnection:
    def __init__(self):
        try:
            print(f"Connecting to Neo4j at {Config.NEO4J_URI}")
            self.driver = GraphDatabase.driver(
                Config.NEO4J_URI,
                auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD)
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            print("✅ Neo4j connection successful")
        except Exception as e:
            print(f"❌ Neo4j connection failed: {e}")
            self.driver = None
    
    def close(self):
        if self.driver:
            self.driver.close()
    
    def execute_query(self, query, parameters=None):
        if not self.driver:
            return []
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return list(result)  # Convert to list to avoid consumption issues
        except Exception as e:
            print(f"Neo4j query error: {e}")
            return []
    
    def create_flight_node(self, flight_data):
        query = """
        MERGE (f:Flight {icao24: $icao24})
        SET f.callsign = $callsign,
            f.origin_country = $origin_country,
            f.time_position = $time_position,
            f.last_contact = $last_contact,
            f.longitude = $longitude,
            f.latitude = $latitude,
            f.baro_altitude = $baro_altitude,
            f.on_ground = $on_ground,
            f.velocity = $velocity,
            f.true_track = $true_track,
            f.vertical_rate = $vertical_rate,
            f.sensors = $sensors,
            f.geo_altitude = $geo_altitude,
            f.squawk = $squawk,
            f.spi = $spi,
            f.position_source = $position_source
        RETURN f
        """
        return self.execute_query(query, flight_data)
    
    def create_airport_node(self, airport_data):
        query = """
        MERGE (a:Airport {icao: $icao})
        SET a.name = $name,
            a.city = $city,
            a.country = $country,
            a.latitude = $latitude,
            a.longitude = $longitude
        RETURN a
        """
        return self.execute_query(query, airport_data)
    
    def create_route_relationship(self, flight_icao, origin_icao, destination_icao):
        query = """
        MATCH (f:Flight {icao24: $flight_icao})
        MATCH (origin:Airport {icao: $origin_icao})
        MATCH (dest:Airport {icao: $destination_icao})
        MERGE (f)-[:DEPARTS_FROM]->(origin)
        MERGE (f)-[:ARRIVES_AT]->(dest)
        RETURN f, origin, dest
        """
        return self.execute_query(query, {
            'flight_icao': flight_icao,
            'origin_icao': origin_icao,
            'destination_icao': destination_icao
        })
