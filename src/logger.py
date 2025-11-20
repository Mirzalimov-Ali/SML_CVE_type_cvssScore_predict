import logging 
import os

os.makedirs('logs', exist_ok=True)

def get_logger(file_name, save_file):
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(f"logs/{save_file}")

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger 