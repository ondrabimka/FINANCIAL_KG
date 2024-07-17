import os

from dotenv import load_dotenv

from db.upload import DataUploader
from download import AsyncDataDownloader
from utils import setup_custom_logger

logger = setup_custom_logger(__name__)

load_dotenv()

logger.info("Program started")
logger.info("----------------")
tickers = os.getenv("TICKERS").split(",")
logger.info("Getting data for the following tickers:")
logger.info(tickers)
downloader = AsyncDataDownloader(tickers)
downloader.download_data_by_chunks()
logger.info("All data downloaded")
logger.info("Uploading data to the database")
uploader = DataUploader()
uploader.reupload_all_data()
logger.info("All data uploaded")
logger.info("Program finished")
