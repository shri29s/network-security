import sys
from networksecurity.logging.logger import logging

class NetworkSecurityException(Exception):
    message: str
    traceback = None
    lineno: int
    filename: str

    def __init__(self, message):
        self.message = message
        _, _, self.traceback = sys.exc_info()
        self.lineno = self.traceback.tb_lineno
        self.filename = self.traceback.tb_frame.f_code.co_filename
        logging.error(self)

    def __str__(self):
        return f"Exception [msg: {self.message}, line: {self.lineno}, file: {self.filename}]"
    
if __name__ == "__main__":
    try:
        try:
            a = 1 / 0
        except Exception as e:
            raise NetworkSecurityException(e)
    except Exception as e:
        logging.error(e)
        print(e)