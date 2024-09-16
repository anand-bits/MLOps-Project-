import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.constants import DATABASE_NAME

import os
from pymongo.mongo_client import MongoClient
import certifi
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Retrieve MongoDB credentials from environment variables
username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')

# URL-encode the username and password
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Construct MongoDB URI
mongo_db_url = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.dyrzg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Certificate authority file for secure connections
ca = certifi.where()

class MongoDBClient:
    """
    Class Name: MongoDBClient
    Description: This class handles the connection to MongoDB. It connects to the specified MongoDB database and
                 raises exceptions if the connection fails.
    """

    # Class-level client to avoid multiple connections
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            # Check if the client is already created
            if MongoDBClient.client is None:
                if mongo_db_url is None:
                    raise Exception(f"MongoDB URL is not set in environment variables.")
                
                # Initialize MongoClient with TLS/SSL connection
                MongoDBClient.client = MongoClient(mongo_db_url, tlsCAFile=ca)

            # Set the client and the database
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

            logging.info("MongoDB connection successful.")

        except Exception as e:
            # Log the exception and raise a custom exception
            raise USvisaException(e, sys)

