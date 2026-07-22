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

    @staticmethod
    def _is_missing(value) -> bool:
        if value is None:
            return True
        if isinstance(value, float) and pd.isna(value):
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        return False

    def _load_or_create_unique_node(self, node_cls, unique_field: str, payload: dict, context: str):
        unique_value = payload.get(unique_field)
        if self._is_missing(unique_value):
            logger.error(f"Cannot upsert {context}: missing unique field '{unique_field}'")
            return None

        try:
            return node_cls(**{unique_field: unique_value}).load(self.memgraph)
        except Exception:
            pass

        try:
            node = node_cls(**payload)
            node.save(self.memgraph)
            return node
        except Exception as e:
            logger.error(f"Error upserting {context} ({unique_field}={unique_value}): {e}")
            return None

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
        data = pd.read_csv(self.file_path / "insider_holder.csv").replace({np.nan: None})
        for _, row in data.iterrows():
            row_data = row.to_dict()
            insider_holder = self._load_or_create_unique_node(
                InsiderHolder,
                "name",
                {"name": row_data.get("name"), "position": row_data.get("position")},
                "insider holder",
            )

            if insider_holder is not None:
                try:
                    ticker = Ticker(ticker=row_data["ticker"]).load(self.memgraph)
                    relationship = Holds_IHT(_start_node_id=ticker._id, _end_node_id=insider_holder._id, **row_data)
                    relationship.save(self.memgraph)
                except Exception as e:
                    logger.error(f"Error creating relationship between {row_data['ticker']} and {row_data['name']}: {e}")
        logger.info("Uploaded insider holder data")

    def upload_insider_transaction_data(self):
        data = pd.read_csv(self.file_path / "insider_transaction.csv").replace({np.nan: None})
        for _, row in data.iterrows():
            row_data = row.to_dict()
            insider = None
            insider_transaction = None
            insider = self._load_or_create_unique_node(
                InsiderHolder,
                "name",
                {"name": row_data.get("name"), "position": row_data.get("position")},
                "insider holder",
            )

            try:
                insider_transaction_payload = {
                    "shares": row_data.get("shares"),
                    "value": row_data.get("value"),
                    "transaction_text": row_data.get("transaction_text"),
                    "position": row_data.get("position"),
                    "transaction": row_data.get("transaction"),
                    "startDate": row_data.get("startDate"),
                    "ownership": row_data.get("ownership"),
                }
                insider_transaction = InsiderTransaction(**insider_transaction_payload)
                insider_transaction.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error uploading insider transaction {row_data.get('name'), row_data.get('startDate')}: {e}, for index {_}")

            if insider is not None and insider_transaction is not None:
                try:
                    relationship = Created(_start_node_id=insider._id, _end_node_id=insider_transaction._id)
                    relationship.save(self.memgraph)
                except Exception as e:
                    logger.error(f"Error creating relationship between {row_data.get('name')} and {row_data.get('ticker')}: {e}")

            if insider_transaction is not None:
                try:
                    ticker = Ticker(ticker=row_data["ticker"]).load(self.memgraph)
                    relationship = Involves(_start_node_id=insider_transaction._id, _end_node_id=ticker._id)
                    relationship.save(self.memgraph)
                except Exception as e:
                    logger.error(f"Error creating relationship between {row_data.get('ticker')} and {row_data.get('name')}: {e}")

        logger.info("Uploaded insider transaction data")

    def upload_institution_data(self):
        data = pd.read_csv(self.file_path / "institution.csv").replace({np.nan: None})
        for _, row in data.iterrows():
            row_data = row.to_dict()
            institution = self._load_or_create_unique_node(
                Institution,
                "name",
                {"name": row_data.get("name")},
                "institution",
            )

            if institution is not None:
                try:
                    ticker = Ticker(ticker=row_data["ticker"]).load(self.memgraph)
                    relationship = Holds_IT(
                        _start_node_id=institution._id,
                        _end_node_id=ticker._id,
                        shares=row_data.get("shares"),
                        dateReported=row_data.get("dateReported"),
                        pctHeld=row_data.get("pctHeld"),
                        value=row_data.get("value"),
                    )
                    relationship.save(self.memgraph)
                except Exception as e:
                    logger.error(f"Error creating relationship between {row_data['ticker']} and {row_data['name']}: {e}")

        logger.info("Uploaded institution data")

    def upload_mutual_fund_data(self):
        data = pd.read_csv(self.file_path / "mutual_fund.csv").replace({np.nan: None})
        for _, row in data.iterrows():
            row_data = row.to_dict()
            mutual_fund = self._load_or_create_unique_node(
                MutualFund,
                "name",
                {"name": row_data.get("name")},
                "mutual fund",
            )

            if mutual_fund is not None:
                try:
                    ticker = Ticker(ticker=row_data["ticker"]).load(self.memgraph)
                    relationship = Holds_MT(
                        _start_node_id=mutual_fund._id,
                        _end_node_id=ticker._id,
                        shares=row_data.get("shares"),
                        dateReported=row_data.get("dateReported"),
                        pctHeld=row_data.get("pctHeld"),
                        value=row_data.get("value"),
                    )
                    relationship.save(self.memgraph)
                except Exception as e:
                    logger.error(f"Error creating relationship between {row_data['ticker']} and {row_data['name']}: {e}")

        logger.info("Uploaded mutual fund data")

    def upload_news_data(self):
        data = pd.read_csv(self.file_path / "news.csv").replace({np.nan: None})
        for _, row in data.iterrows():
            row_data = row.to_dict()
            news = self._load_or_create_unique_node(
                News,
                "uuid",
                {
                    "uuid": row_data.get("uuid"),
                    "title": row_data.get("title"),
                    "publisher": row_data.get("publisher"),
                    "link": row_data.get("link"),
                    "providerPublishTime": row_data.get("providerPublishTime"),
                    "summary": row_data.get("summary"),
                    "description": row_data.get("description"),
                },
                "news",
            )

            if news is not None:
                try:
                    ticker = Ticker(ticker=row_data["ticker"]).load(self.memgraph)
                    relationship = About_NT(_start_node_id=news._id, _end_node_id=ticker._id)
                    relationship.save(self.memgraph)
                except Exception as e:
                    logger.error(f"Error creating relationship between {row_data['title']} and {row_data['ticker']}: {e}")

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
