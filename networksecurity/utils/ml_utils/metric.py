from sklearn.metrics import f1_score, precision_score, recall_score
from networksecurity.entity.artifact_entity import ClassificationMetric

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

def get_classification_report(y_true, y_pred) -> ClassificationMetric:
    try:
        logging.info("Calculating f1, precision and recall score of the model")
        f1 = f1_score(y_true=y_true, y_pred=y_pred)
        prec = precision_score(y_true=y_true, y_pred=y_pred)
        recall = recall_score(y_true=y_true, y_pred=y_pred)

        return ClassificationMetric(
            f1_score=f1,
            precision=prec,
            recall=recall
        )
    except Exception as e:
        raise NetworkSecurityException(e)
