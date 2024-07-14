import logging

import numpy as np
import pandas as pd
from gqlalchemy import Memgraph

from src.db.models import Created, Holds_IHT, Holds_IT, Holds_MT, InsiderHolder, InsiderTransaction, Institution, MutualFund, Purchased, Ticker

logger = logging.getLogger(__name__)


class DataUploader:
    def __init__(self):
        self.memgraph = Memgraph()

    def delete_all_data(self):
        self.memgraph.execute("MATCH (n) DETACH DELETE n")

    def upload_ticker_data(self):
        data = pd.read_csv("data/ticker_info.csv").replace({np.nan: None})
        for _, row in data.iterrows():
            try:
                ticker = Ticker(**row.to_dict())
                ticker.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error uploading ticker {row['ticker']}: {e}")

    def upload_insider_holder_data(self):
        data = pd.read_csv("data/insider_holder.csv")
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

    def upload_insider_transaction_data(self):
        data = pd.read_csv("data/insider_transaction.csv")
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
                relationship = Purchased(_start_node_id=insider_transaction._id, _end_node_id=ticker._id)
                relationship.save(self.memgraph)
            except Exception as e:
                logger.error(f"Error creating relationship between {row['ticker']} and {row['name']}: {e}")

    def upload_institution_data(self):
        data = pd.read_csv("data/institution.csv")
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

    def upload_mutual_fund_data(self):
        data = pd.read_csv("data/mutual_fund.csv")
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

    def reupload_all_data(self):
        self.delete_all_data()
        self.upload_ticker_data()
        self.upload_insider_holder_data()
        self.upload_insider_transaction_data()
        self.upload_institution_data()
        self.upload_mutual_fund_data()

    def upload_all_data(self):
        self.upload_ticker_data()
        self.upload_insider_holder_data()
        self.upload_insider_transaction_data()
        self.upload_institution_data()
        self.upload_mutual_fund_data()


if __name__ == "__main__":
    uploader = DataUploader()
    uploader.upload_all_data()
