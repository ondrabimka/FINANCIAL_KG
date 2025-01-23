import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from gqlalchemy import Memgraph

from db.models import About_NT, Created, Holds_IHT, Holds_IT, Holds_MT, InsiderHolder, InsiderTransaction, Institution, Involves, MutualFund, News, Ticker
from utils import DATA_DIR, setup_custom_logger

logger = setup_custom_logger(__name__)

load_dotenv()


class DataUploader:

    """
    A class that uploads data to the database. Based on: https://memgraph.com/blog/jupyter-translate-data-to-graph-database

    Parameters
    ----------
    data_path : str
        The path to the data directory.

    Attributes
    ----------
    file_path : Path
        The path to the data file.
    memgraph : Memgraph
        The Memgraph object.
    """

    def __init__(self, data_path=pd.Timestamp.now().strftime("%Y-%m-%d")):
        self.file_path = DATA_DIR / f"data_{data_path}"
        if not self.file_path.exists():
            logger.error(f"Data directory {self.file_path} does not exist")
            raise FileNotFoundError(f"Data directory {self.file_path} does not exist")
        self.memgraph = Memgraph(os.getenv("QUICK_CONNECT_MG_HOST"), int(os.getenv("QUICK_CONNECT_MG_PORT")))

    def delete_all_data(self):
        logger.info("Deleting all data from the database")
        self.memgraph.execute("MATCH (n) DETACH DELETE n")

    def upload_ticker_data(self):
        data = pd.read_csv(self.file_path / "ticker_info.csv").replace({np.nan: None})
        for _, row in data.iterrows():
            try:
                ticker = Ticker(**row.to_dict())
                ticker.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error uploading ticker {row['ticker']}: {e}")
        logger.info("Uploaded ticker data")

    def upload_insider_holder_data(self):
        data = pd.read_csv(self.file_path / "insider_holder.csv")
        for _, row in data.iterrows():
            try:
                insider_holder = InsiderHolder(**row.to_dict())
                insider_holder.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error uploading insider holder {row['name']}: {e}")

            try:
                ticker = Ticker(ticker=row["ticker"]).load(self.memgraph)
                relationship = Holds_IHT(_start_node_id=ticker._id, _end_node_id=insider_holder._id, **row.to_dict())
                relationship.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error creating relationship between {row['ticker']} and {row['name']}: {e}")
        logger.info("Uploaded insider holder data")

    def upload_insider_transaction_data(self):
        data = pd.read_csv(self.file_path / "insider_transaction.csv")
        for _, row in data.iterrows():
            try:
                insider = InsiderHolder(**row.to_dict())
                insider = insider.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error uploading insider holder {row['name']}: {e}, for index {_}")

            try:
                insider_transaction = InsiderTransaction(**row.to_dict())
                insider_transaction.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error uploading insider transaction {row['name'], row['startDate']}: {e}, for index {_}")

            try:
                relationship = Created(_start_node_id=insider._id, _end_node_id=insider_transaction._id)
                relationship.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error creating relationship between {row['name']} and {row['ticker']}: {e}")

            try:
                ticker = Ticker(ticker=row["ticker"]).load(self.memgraph)
                relationship = Involves(_start_node_id=insider_transaction._id, _end_node_id=ticker._id)
                relationship.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error creating relationship between {row['ticker']} and {row['name']}: {e}")

        logger.info("Uploaded insider transaction data")

    def upload_institution_data(self):
        data = pd.read_csv(self.file_path / "institution.csv")
        for _, row in data.iterrows():
            try:
                institution = Institution(**row.to_dict())
                institution.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error uploading institution {row['name']}: {e}")

            try:
                ticker = Ticker(ticker=row["ticker"]).load(self.memgraph)
                relationship = Holds_IT(_start_node_id=institution._id, _end_node_id=ticker._id, shares=row["shares"])
                relationship.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error creating relationship between {row['ticker']} and {row['name']}: {e}")

        logger.info("Uploaded institution data")

    def upload_mutual_fund_data(self):
        data = pd.read_csv(self.file_path / "mutual_fund.csv")
        for _, row in data.iterrows():
            try:
                mutual_fund = MutualFund(**row.to_dict())
                mutual_fund.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error uploading mutual fund {row['name']}: {e}")

            try:
                ticker = Ticker(ticker=row["ticker"]).load(self.memgraph)
                relationship = Holds_MT(_start_node_id=mutual_fund._id, _end_node_id=ticker._id, shares=row["shares"])
                relationship.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error creating relationship between {row['ticker']} and {row['name']}: {e}")

        logger.info("Uploaded mutual fund data")

    def upload_news_data(self):
        data = pd.read_csv(self.file_path / "news.csv")
        for _, row in data.iterrows():
            try:
                news = News(**row.to_dict())
                news.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error creating news {row['title']}: {e}")

            try:
                ticker = Ticker(ticker=row["ticker"]).load(self.memgraph)
                relationship = About_NT(_start_node_id=news._id, _end_node_id=ticker._id)
                relationship.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error creating relationship between {row['title']} and {row['name']}: {e}")

    def reupload_all_data(self):
        logger.info("Reuploading all data")
        self.delete_all_data()
        self.upload_ticker_data()
        self.upload_insider_holder_data()
        self.upload_insider_transaction_data()
        self.upload_institution_data()
        self.upload_mutual_fund_data()
        self.upload_news_data()
        logger.info("Finished reuploading all data")

    def upload_all_data(self):
        logger.info("Uploading all data")
        self.upload_ticker_data()
        self.upload_insider_holder_data()
        self.upload_insider_transaction_data()
        self.upload_institution_data()
        self.upload_mutual_fund_data()
        self.upload_news_data()
        logger.info("Finished uploading all data")


if __name__ == "__main__":
    uploader = DataUploader()
    uploader.upload_all_data()
