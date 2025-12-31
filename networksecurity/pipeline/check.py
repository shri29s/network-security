from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.logging.logger import logging

if __name__ == "__main__":
    try:
        trainingConfig = TrainingPipelineConfig()
        dataIngestionConfig = DataIngestionConfig(trainingConfig)
        dataIngestion = DataIngestion(dataIngestionConfig)
        dataIngestionArtifact = dataIngestion.initiateDataIngestion()
        print(dataIngestionArtifact)
        print()

        dataValidationConfig = DataValidationConfig(trainingConfig)
        dataValidation = DataValidation(dataValidationConfig, dataIngestionArtifact)
        dataValidationArtifact = dataValidation.initiate_data_validation()
        print(dataValidationArtifact)
        print()

        dataTransformationConfig = DataTransformationConfig(trainingConfig)
        dataTransformation = DataTransformation(dataTransformationConfig, dataValidationArtifact)
        dataTransformationArtifact = dataTransformation.initiate_data_transformation()
        print(dataTransformationArtifact)
        print()

        modelTrainerConfig = ModelTrainerConfig(trainingConfig)
        modelTrainer = ModelTrainer(modelTrainerConfig, dataTransformationArtifact)
        modelTrainerArtifact = modelTrainer.initiate_model_training()
        print(modelTrainerArtifact)
        print()
    except Exception as e:
        print(e)