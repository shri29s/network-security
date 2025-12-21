from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation

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
    except Exception as e:
        print(e)