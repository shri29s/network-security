from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import os
import pandas as pd
import numpy as np
import pymongo

from sklearn.model_selection import train_test_split

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv
load_dotenv(".env")

class DataIngestion:
    def __init__(self, dataIngestionConfig: DataIngestionConfig):
        self.config = dataIngestionConfig
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))

    def fetchMongoDB(self):
        try:
            collection = self.client.get_database(self.config.database_name).get_collection(self.config.collection_name)
            dataframe = pd.DataFrame(list(collection.find()))

            if "_id" in dataframe.columns.to_list():
                dataframe.drop("_id", axis=1, inplace=True)

            dataframe.replace("na", value=np.nan)

            logging.info("Data fetched from mongo DB")
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def export_feature_store(self, dataframe: pd.DataFrame):
        try:
            os.makedirs(os.path.dirname(self.config.feature_store_file_path), exist_ok=True)
            dataframe.to_csv(self.config.feature_store_file_path, index=False, header=True)
            logging.info("Feature store exported")
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def split_data(self, dataframe: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(
                dataframe,
                test_size=self.config.train_test_ratio
            )
            logging.info("Data splited into train and test dataframes")

            os.makedirs(os.path.dirname(self.config.training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.config.testing_file_path), exist_ok=True)

            train_df.to_csv(self.config.training_file_path, index=False, header=True)
            logging.info("Train file exported successfully")
            test_df.to_csv(self.config.testing_file_path, index=False, header=True)
            logging.info("Test file exported successfully")
        except Exception as e:
            raise NetworkSecurityException(e)

    def initiateDataIngestion(self):
        try:
            logging.info("Initiating data ingestion")
            dataframe = self.fetchMongoDB()
            self.export_feature_store(dataframe=dataframe)
            self.split_data(dataframe=dataframe)

            artifact = DataIngestionArtifact(
                self.config.feature_store_file_path,
                self.config.training_file_path,
                self.config.testing_file_path
            )
            logging.info("Data ingestion completed")
            return artifact
        except Exception as e:
            raise NetworkSecurityException(e)