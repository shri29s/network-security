from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.model_selection import RandomizedSearchCV

import mlflow
import pandas as pd
import os

class NetworkModel:
    def __init__(self, preprocessor, model):
        self.preprocessor = preprocessor
        self.model = model

    def predict(self, X):
        try:
            X_transformed = self.preprocessor.transform(X)
            y_pred = self.model.predict(X_transformed)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e)
        
def evaluate_models(X_train, y_train, models: dict, params: dict, cv_result_dir: str):
    report = list()
    os.makedirs(cv_result_dir, exist_ok=True)

    mlflow.set_experiment("Model_selection_randomizedsearch")

    for model_name, model in models.items():
        logging.info(f"Running grid search cv for model: {model_name}")
        
        with mlflow.start_run(run_name=model_name):
            rscv = RandomizedSearchCV(model, params[model_name], scoring="f1", n_jobs=-1, verbose=1)
            rscv.fit(X_train, y_train)

            # Log best results only
            mlflow.log_params(rscv.best_params_)
            mlflow.log_metric("best_cv_f1", rscv.best_score_)
            logging.info(rscv.best_params_)
            
            cv_results_df = pd.DataFrame(rscv.cv_results_)
            csv_path = os.path.join(cv_result_dir, model_name + "_cv_results.csv")
            cv_results_df.to_csv(csv_path, index=False)
            mlflow.log_artifact(csv_path)

            mlflow.sklearn.log_model(
                rscv.best_estimator_,
                name="model"
            )

            report.append((model_name, rscv.best_params_, rscv.best_score_))

    # print(report)
    return report
