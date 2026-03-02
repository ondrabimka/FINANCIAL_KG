import asyncio

import pandas as pd

from db.upload import DataUploader
from download import AsyncDataDownloader
from utils import DATA_DIR, setup_custom_logger

logger = setup_custom_logger(__name__)

logger.info("Program started")
logger.info("----------------")
# tickers = os.getenv("TICKERS").split(",")
tickers = pd.read_csv(DATA_DIR / "nasdaq_screener_1721725526813.csv").dropna()
tickers = list(tickers["Symbol"])
logger.info("Getting data for the following tickers:")
logger.info(tickers)
downloader = AsyncDataDownloader(tickers)
asyncio.get_event_loop().run_until_complete(downloader.download_data_by_chunks())
logger.info("All data downloaded")
logger.info("Uploading data to the database")
uploader = DataUploader()
uploader.reupload_all_data()
logger.info("All data uploaded")
logger.info("Program finished")
