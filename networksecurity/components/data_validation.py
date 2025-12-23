from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

from networksecurity import constants
from networksecurity.utils.utils import read_yaml, write_yaml

from scipy.stats import ks_2samp # for making the drift report
import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig, ing_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = config
            self.data_ingestion_artifact = ing_artifact
            self._schema_config = read_yaml(constants.SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e)

    @staticmethod
    def read_df(filePath: str) -> pd.DataFrame:
        try:
            return pd.read_csv(filePath)
        except Exception as e:
            raise NetworkSecurityException(e)

    def validate_number_of_columns(self, df1: pd.DataFrame, df2: pd.DataFrame) -> bool:
        try:
            logging.info("Validating number of columns for both the train and test df")
            if(len(df1.columns) != len(self._schema_config.get("columns"))):
                logging.info("No. of columns invalid in train df")
                return False
            if(len(df2.columns) != len(self._schema_config.get("columns"))):
                logging.info("No. of columns invalid in test df")
                return False
            
            logging.info("Number of columns are same - valid")
            return True
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def check_numerical_columns(self, df: pd.DataFrame):
        try:
            logging.info("Checking numerical columns")
            num_cols: str = self._schema_config.get("numerical_columns")
            num_cols: list = num_cols.split(" ")
            col_list = list(df.columns)

            for col in num_cols:
                if col not in col_list:
                    return False
            
            logging.info("Numerical column test passed")
            return True
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def drift_report(self, initial_df: pd.DataFrame, current_df: pd.DataFrame, threshold = 0.05, drift_limit = 0.5):
        try:
            logging.info("Checking for data drift")
            drifted_columns_count = 0
            report = dict()
            for col in initial_df.columns:
                col1 = initial_df[col]
                col2 = current_df[col]

                result = ks_2samp(col1, col2)
                if float(result.pvalue) <= threshold:
                    report[col] = {
                        "pvalue": float(result.pvalue),
                        "drift_status": True
                    }
                    drifted_columns_count += 1
                else:
                    report[col] = {
                        "pvalue": float(result.pvalue),
                        "drift_status": False
                    }
                
            logging.info(f"No. of drifted columns: {drifted_columns_count}")
            write_yaml(self.data_validation_config.drift_report_path, report)
            return drifted_columns_count / len(initial_df.columns) <= drift_limit
        except Exception as e:
            raise NetworkSecurityException(e)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Initiating data validation")
            train_path = self.data_ingestion_artifact.train_path
            test_path = self.data_ingestion_artifact.test_path

            train_df = DataValidation.read_df(train_path)
            test_df = DataValidation.read_df(test_path)

            status = self.validate_number_of_columns(train_df, test_df)
            if not status:
                raise NetworkSecurityException("Data validation failed: Number of columns not matching.")
            
            status = self.check_numerical_columns(train_df)
            if not status:
                raise NetworkSecurityException("Data validation failed: Numerical column test failed for training dataset")
            
            status = self.check_numerical_columns(test_df)
            if not status:
                raise NetworkSecurityException("Data validation failed: Numerical column test failed for testing dataset")
            
            status = self.drift_report(train_df, test_df)
            if not status:
                raise NetworkSecurityException("Data validation failed: Too much drift in dataset")
            
            logging.info("Data validation is successful")
            return DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_path,
                valid_test_file_path=self.data_ingestion_artifact.test_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_path
            )
        except Exception as e:
            raise NetworkSecurityException(e)