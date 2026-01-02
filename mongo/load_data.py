import os
from dotenv import load_dotenv
import pymongo
import json

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import pandas as pd
from networksecurity import constants

load_dotenv()

class DataETL:
    fileName = None
    records_json = None

    database = None
    collection = None
    client = None

    def __init__(self, fileName, database, collection):
        self.fileName = fileName

        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.database = self.client.get_database(database)
        self.collection = self.database.get_collection(collection)

    def convert_json(self):
        try:
            df = pd.read_csv(self.fileName)
            df.reset_index(drop=True, inplace=True)
        
            self.records_json = json.loads(df.T.to_json()).values()
            logging.info("Converted csv file to json list")
        except Exception as e:
            raise NetworkSecurityException(e)
    
    def push_mongo(self):
        try:
            self.collection.insert_many(self.records_json)
            logging.info("Loaded data into mongoDB")
            logging.info(f"{len(self.records_json)} rows inserted")
        except Exception as e:
            raise NetworkSecurityException(e)


if __name__ == "__main__":
    try:
        etlPipe = DataETL("./Network_Data/phisingData.csv", constants.DATA_INGESTION_DATABASE_NAME, constants.DATA_INGESTION_COLLECTION_NAME)
        etlPipe.convert_json() # Extract
        etlPipe.push_mongo() # Load
    except Exception as e:
        print(e)
        