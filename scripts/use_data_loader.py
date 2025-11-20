from src.data_loader import DataLoader
from src.logger import get_logger

logger = get_logger("use_data_loader", "data_loader.log")

loader = DataLoader()
merged_df = loader.load_and_merge()

loader.save_merged(merged_df)
logger.info(f'datasets are merged')