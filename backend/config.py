import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NEO4J_URI = os.getenv('NEO4J_URI', 'neo4j://127.0.0.1:7687')
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'Qwer@857')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    FLIGHT_API_KEY = os.getenv('FLIGHT_API_KEY', '')
    FLIGHT_API_URL = os.getenv('FLIGHT_API_URL', 'https://opensky-network.org/api')
