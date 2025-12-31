from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

class TrainingPipeline:
    def __init__(self):
        self.trainingConfig = TrainingPipelineConfig()

    def data_ingestion(self):
        try:
            logging.info("Initiating data ingestion")
            self.dataIngestionConfig = DataIngestionConfig(self.trainingConfig)
            dataIngestion = DataIngestion(self.dataIngestionConfig)
            dataIngestionArtifact = dataIngestion.initiateDataIngestion()
            logging.info("Data ingestion completed")
            return dataIngestionArtifact
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def data_validation(self, dataIngestionArtifact):
        try:
            logging.info("Initiating data validation")
            self.dataValidationConfig = DataValidationConfig(self.trainingConfig)
            dataValidation = DataValidation(self.dataValidationConfig, dataIngestionArtifact)
            dataValidationArtifact = dataValidation.initiate_data_validation()
            logging.info("Data validation completed")
            return dataValidationArtifact
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def data_transformation(self, dataValidationArtifact):
        try:
            self.dataTransformationConfig = DataTransformationConfig(self.trainingConfig)
            dataTransformation = DataTransformation(self.dataTransformationConfig, dataValidationArtifact)
            dataTransformationArtifact = dataTransformation.initiate_data_transformation()
            return dataTransformationArtifact
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def model_trainer(self, dataTransformationArtifact):
        try:
            self.modelTrainerConfig = ModelTrainerConfig(self.trainingConfig)
            modelTrainer = ModelTrainer(self.modelTrainerConfig, dataTransformationArtifact)
            modelTrainerArtifact = modelTrainer.initiate_model_training()
            return modelTrainerArtifact
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def run_pipeline(self):
        try:
            dataIngestionArtifact = self.data_ingestion()
            dataValidataionArtifact = self.data_validation(dataIngestionArtifact)
            dataTransformationArtifact = self.data_transformation(dataValidataionArtifact)
            modelTrainerArtifact = self.model_trainer(dataTransformationArtifact)
            return modelTrainerArtifact
        except Exception as e:
            raise NetworkSecurityException(e)
