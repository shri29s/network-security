import pandas as pd
import os

from networksecurity.utils.utils import load_object
from networksecurity import constants
from networksecurity.utils.ml_utils.model import NetworkModel

from networksecurity.exception.exception import NetworkSecurityException

class BatchPrediction:
    def __init__(self):
        try:
            object_file_path = os.path.join(
                constants.FINAL_MODEL_DIR,
                constants.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_FILE_NAME
            )
            preprocessor = load_object(object_file_path)

            model_file_path = os.path.join(
                constants.FINAL_MODEL_DIR,
                constants.MODEL_TRAINER_TRAINED_MODEL_FILE_NAME
            )
            model = load_object(model_file_path)

            self.network_model = NetworkModel(preprocessor=preprocessor, model=model)
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def batch_prediction(self, file) -> pd.DataFrame:
        try:
            df = pd.read_csv(file)
            y_pred = self.network_model.predict(df)
            df['predicted'] = y_pred
            return df
        except Exception as e:
            raise NetworkSecurityException(e)
