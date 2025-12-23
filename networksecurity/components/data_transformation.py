from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact

from networksecurity import constants
from networksecurity.utils import utils

import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e)

    @staticmethod
    def read_df(filePath) -> pd.DataFrame:
        try:
            logging.info(f"Reading dataframe from path: {filePath}")
            return pd.read_csv(filePath)
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def get_preprocessor_object(self) -> Pipeline:
        try:
            logging.info(f"Creating preprocessor object with params: {constants.DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            imputer = KNNImputer(**constants.DATA_TRANSFORMATION_IMPUTER_PARAMS)
            pipeline = Pipeline([("imputer", imputer)])
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation")
            train_df = DataTransformation.read_df(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_df(self.data_validation_artifact.valid_test_file_path)

            input_features_train = train_df.drop(constants.TARGET_COLUMN, axis=1)
            target_feature_train = train_df[constants.TARGET_COLUMN]
            target_feature_train.replace(-1, 0, inplace=True)

            input_features_test = test_df.drop(constants.TARGET_COLUMN, axis=1)
            target_feature_test = test_df[constants.TARGET_COLUMN]
            target_feature_test.replace(-1, 0, inplace=True)

            preprocessor = self.get_preprocessor_object()
            transformed_input_features_train = preprocessor.fit_transform(input_features_train)
            transformed_input_features_test = preprocessor.transform(input_features_test)

            transformed_train_df = np.concat([transformed_input_features_train, np.reshape(target_feature_train, (np.shape(transformed_input_features_train)[0], 1))], axis=1)
            transformed_test_df = np.concat([transformed_input_features_test, np.reshape(target_feature_test, (np.shape(transformed_input_features_test)[0], 1))], axis=1)

            # save the objects
            logging.info("Saving the numpy arrays and preprocessor object")
            utils.save_numpy_array(self.data_transformation_config.data_transformation_train_file_path, transformed_train_df)
            utils.save_numpy_array(self.data_transformation_config.data_transformation_test_file_path, transformed_test_df)
            utils.save_object(self.data_transformation_config.data_transformation_transformed_object_file_path, preprocessor)

            logging.info("Data transformation completed successfully")
            return DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.data_transformation_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformation_test_file_path,
                transformed_object_file_path=self.data_transformation_config.data_transformation_transformed_object_file_path
            )
        except Exception as e:
            raise NetworkSecurityException(e)