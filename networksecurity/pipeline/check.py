from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from networksecurity.components.data_ingestion import DataIngestion

if __name__ == "__main__":
    try:
        trainingConfig = TrainingPipelineConfig()
        dataIngestionConfig = DataIngestionConfig(trainingConfig)
        dataIngestion = DataIngestion(dataIngestionConfig)
        dataIngestionArtifact = dataIngestion.initiateDataIngestion()
        print(dataIngestionArtifact)
    except Exception as e:
        print(e)