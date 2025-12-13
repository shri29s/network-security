import logging
from datetime import datetime
import os

LOG_FILE = f"{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_FILE_PATH, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_FILE_PATH, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    # filemode="a",
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)