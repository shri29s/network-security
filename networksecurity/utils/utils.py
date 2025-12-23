from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import yaml
import os
import pickle

import numpy as np

def read_yaml(fileName: str) -> dict:
    try:
        logging.info(f"Reading from yaml file: {fileName}")
        with open(fileName, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e)
    
def write_yaml(fileName: str, content: object):
    try:
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        logging.info(f"Writing to yaml file: {fileName}")
        with open(fileName, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e)
    
def save_numpy_array(fileName: str, array): 
    try:
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        logging.info(f"Saving numpy array to file: {fileName}")
        with open(fileName, "wb") as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e)
    
def save_object(fileName: str, object: object): 
    try:
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        logging.info(f"Pickling object to file: {fileName}")
        with open(fileName, "wb") as file:
            pickle.dump(object, file)
    except Exception as e:
        raise NetworkSecurityException(e)