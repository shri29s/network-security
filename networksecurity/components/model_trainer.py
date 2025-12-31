from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity import constants
from networksecurity.entity.artifact_entity import ModelTrainerArtifact, ClassificationMetric, DataTransformationArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.utils import load_numpy_array, save_object
from networksecurity.utils.ml_utils.model import evaluate_models
from networksecurity.utils.ml_utils.metric import get_classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

import mlflow
import dagshub
dagshub.init(repo_owner='shri29s', repo_name='network-security', mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e)

    def train_model(self, X_train, y_train):
        logging.info("Preparing models to train")
        models = {
            "logistic": LogisticRegression(n_jobs=-1, verbose=1),
            "k-neighbors": KNeighborsClassifier(n_jobs=-1),
            "decision": DecisionTreeClassifier(),
            "adaboost": AdaBoostClassifier(),
            "gradient": GradientBoostingClassifier(),
            "random": RandomForestClassifier(n_jobs=-1, verbose=1)
        }
        logging.info(f"List of models considered: {models}")

        param_grids = {
            "logistic": {
                # "penalty": ["l1", "l2", "elasticnet"],
                # "C": [0.001, 0.01, 0.1, 1, 10, 100],
                # "solver": ["saga"],  # supports l1, l2, elasticnet
                # "max_iter": [1000],
                # "l1_ratio": [0.0, 0.5, 1.0]  # used only for elasticnet
            },

            "k-neighbors": {
                "n_neighbors": [3, 5, 7, 9, 11, 15],
                # "weights": ["uniform", "distance"],
                # "metric": ["euclidean", "manhattan", "minkowski"]
            },

            "decision": {
                # "criterion": ["gini", "entropy", "log_loss"],
                "max_depth": [None, 5, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 5],
                # "max_features": [None, "sqrt", "log2"]
            },

            "adaboost": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.05, 0.1, 0.5, 1.0],
                # "algorithm": ["SAMME", "SAMME.R"]
            },

            "gradient": {
                "n_estimators": [100, 200, 300],
                "learning_rate": [0.01, 0.05, 0.1],
                "max_depth": [3, 5, 7],
                # "min_samples_split": [2, 5, 10],
                # "min_samples_leaf": [1, 2, 5],
                # "subsample": [0.6, 0.8, 1.0]
            },

            "random": {
                "n_estimators": [100, 200, 300],
                "criterion": ["gini", "entropy", "log_loss"],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 5],
                # "max_features": ["sqrt", "log2"]
            }
        }

        logging.info("Evaluating the models for f1 score.")
        model_report = evaluate_models(X_train=X_train, y_train=y_train, models=models, params=param_grids, cv_result_dir=self.config.cv_result_dir)
        model_report.sort(key=lambda a: a[2], reverse=True)

        logging.info("Picking the best model")
        best_model_record = model_report[0]
        logging.info(f"Best model: {best_model_record}")

        best_model_name = best_model_record[0]
        best_params = best_model_record[1]

        model_class_map = {
            "logistic": LogisticRegression,
            "k-neighbors": KNeighborsClassifier,
            "decision": DecisionTreeClassifier,
            "adaboost": AdaBoostClassifier,
            "gradient": GradientBoostingClassifier,
            "random": RandomForestClassifier
        }

        best_model = model_class_map[best_model_name]()
        best_model.set_params(**best_params)
        return best_model
     
    def initiate_model_training(self) -> ModelTrainerArtifact:
        try:
            logging.info("Initiating model training")
            train_array_path = self.data_transformation_artifact.transformed_train_file_path
            test_array_path = self.data_transformation_artifact.transformed_test_file_path

            logging.info("Loading train and test numpy array")
            train_array = load_numpy_array(train_array_path)
            test_array = load_numpy_array(test_array_path)

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            best_model = self.train_model(X_train=X_train, y_train=y_train)
            best_model.fit(X_train, y_train)
            logging.info("Fitting the best model with train data")

            logging.info("Predicting for train and test data.")
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            train_report = get_classification_report(y_true=y_train, y_pred=y_train_pred)
            logging.info(f"Train report: {train_report}")
            test_report = get_classification_report(y_true=y_test, y_pred=y_test_pred)
            logging.info(f"Test report: {test_report}")

            mlflow.set_experiment("Best_model")
            with mlflow.start_run(run_name="final_model_run"):
                mlflow.log_metric("train_f1", train_report.f1_score)
                mlflow.log_metric("train_precision", train_report.precision)
                mlflow.log_metric("train_recall", train_report.recall)

                mlflow.log_metric("test_f1", test_report.f1_score)
                mlflow.log_metric("test_precision", test_report.precision)
                mlflow.log_metric("test_recall", test_report.recall)

                mlflow.sklearn.log_model(
                    best_model,
                    artifact_path="model"
                )

            save_object(self.config.model_file_path, best_model)

            return ModelTrainerArtifact(
                trained_model_file_path=self.config.model_file_path,
                train_metric=train_report,
                test_metric=test_report
            )
        except Exception as e:
            raise NetworkSecurityException(e)