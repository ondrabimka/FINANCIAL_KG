from datetime import datetime

import pandas as pd
import yfinance as yf

from utils import setup_custom_logger

logger = setup_custom_logger(__name__)


class TickerHandler(yf.Ticker):
    """
    A class that handles ticker information.

    Parameters
    ----------
    ticker : str
        The ticker symbol.

    Attributes
    ----------
    ticker : yf.Ticker
        The Yahoo Finance Ticker object.

    Methods
    -------
    prepare_ticker_info()
        Prepares the ticker information including company officers, insider purchases, and major holders.
    prepare_major_holders()
        Prepares the major holders information.
    prepare_insider_purchases()
        Prepares the insider purchases information.
    prepare_institutional_holders()
        Prepares the institutional holders information.
    prepare_mutualfund_holders()
        Prepares the mutual fund holders information.
    prepare_insider_transactions()
        Prepares the insider transactions information.
    prepare_insider_roster_holders()
        Prepares the insider roster holders information.
    prepare_news()
        Prepares news data.
    clean_name(name)
        Cleans the given name by removing titles and degrees and converting it to uppercase.
    count_number_of_shared_letters_ratio(name1, name2)
        Calculates the ratio of shared letters between two names.
    """

    def __init__(self, ticker):
        super(TickerHandler, self).__init__(ticker)
        self.ticker = yf.Ticker(ticker)

    def prepare_ticker_info(self):
        """
        Prepares the ticker information including company officers, insider purchases, and major holders.

        Returns
        -------
        pd.DataFrame
            The concatenated DataFrame containing the ticker information.
        """
        info = self.ticker.info
        try:
            info.pop("companyOfficers")
        except Exception as E:
            logger.info("no companyOfficers", E)
        # TODO: Include company officers. Map them maybe?
        # officers = info.pop('companyOfficers')
        # officers = pd.DataFrame(officers)
        # replace nan with empty string
        info = pd.DataFrame([info])
        info = info.infer_objects(copy=False).fillna("")
        return pd.concat([info, self.prepare_insider_purchases(), self.prepare_major_holders()], axis=1)

    def prepare_major_holders(self) -> pd.DataFrame:
        """
        Prepares the major holders information.

        Returns
        -------
        pd.DataFrame
            The major holders information.
        """
        try:
            major_holders = self.ticker.major_holders
            major_holders = major_holders.T
            major_holders = major_holders.reset_index(drop=True)
            major_holders = major_holders.infer_objects(copy=False).fillna("")
            return major_holders
        except Exception as E:
            logger.error("No major_holders found for: ", self.ticker.ticker, " with exception: ", E)
            return pd.DataFrame([])

    def prepare_insider_purchases(self) -> pd.DataFrame:
        """
        Prepares the insider purchases information.

        Returns
        -------
        pd.DataFrame
            The insider purchases information.
        """

        try:
            insider_purchases = self.ticker.insider_purchases
            insider_purchases = insider_purchases[["Insider Purchases Last 6m", "Shares"]].T
            insider_purchases.columns = insider_purchases.iloc[0]
            insider_purchases = insider_purchases[1:]
            insider_purchases.columns = [f"Insider {col}" for col in insider_purchases.columns]
            insider_purchases = insider_purchases.reset_index(drop=True)
            insider_purchases = insider_purchases.infer_objects(copy=False).fillna("")
            return insider_purchases
        except Exception as E:
            logger.error("No insider_transactions found for: ", self.ticker.ticker, " with exception: ", E)
            return pd.DataFrame([])

    def prepare_institutional_holders(self) -> pd.DataFrame:
        """
        Prepares the institutional holders information.

        Returns
        -------
        pd.DataFrame
            The institutional holders information.
        """

        try:
            institutional_holders = self.ticker.institutional_holders
            institutional_holders.columns = ["dateReported", "name", "pctHeld", "shares", "value"]
            return institutional_holders
        except Exception as E:
            logger.error("No institutional_holders found for: ", self.ticker.ticker, " with exception: ", E)
            return pd.DataFrame([])

    def prepare_mutualfund_holders(self) -> pd.DataFrame:
        """
        Prepares the mutual fund holders information.

        Returns
        -------
        pd.DataFrame
            The mutual fund holders information.
        """

        try:
            mutualfund_holders = self.ticker.mutualfund_holders
            mutualfund_holders.columns = ["dateReported", "name", "pctHeld", "shares", "value"]
            return mutualfund_holders
        except Exception as E:
            logger.error("No mutualfund_holders found for: ", self.ticker.ticker, " with exception: ", E)
            return pd.DataFrame([])

    def prepare_insider_transactions(self) -> pd.DataFrame:
        """
        Prepares the insider transactions information.

        Returns
        -------
        pd.DataFrame
            The insider transactions information.
        """
        try:
            insider_transactions = self.ticker.insider_transactions
            insider_transactions.columns = ["shares", "value", "url", "transaction_text", "name", "position", "transaction", "startDate", "ownership"]
            return insider_transactions
        except Exception as E:
            logger.error("No insider_transactions found for: ", self.ticker.ticker, " with exception: ", E)
            return pd.DataFrame([])

    def prepare_insider_roster_holders(self) -> pd.DataFrame:
        """
        Prepares the insider roster holders information.

        Returns
        -------
        pd.DataFrame
            The insider roster holders information.
        """

        try:
            insider_roster_holders = self.ticker.insider_roster_holders

            columns = [
                "name",
                "position",
                "mostRecentTransaction",
                "latestTransactionDate",
                "sharesOwnedDirectly",
                "positionDirectDate",
                "sharesOwnedIndirectly",
                "positionIndirectDate",
                "ticker",
            ]

            # Data formats can vary
            if (self.insider_roster_holders.shape[1]) == 9:
                insider_roster_holders.columns = columns
                return insider_roster_holders
            elif (self.insider_roster_holders.shape[1]) == 8:
                columns.remove("sharesOwnedIndirectly")
                insider_roster_holders.columns = columns
                return insider_roster_holders
            else:
                return pd.DataFrame([])

        except Exception as E:
            logger.error("No insider_roster_holders found for: ", self.ticker.ticker, " with exception: ", E)
            return pd.DataFrame([])

    def prepare_news(self):
        """
        Preates the news information for a given ticker.

        Returns
        -------
        pd.DataFrame
            News the news information for a given ticker.
        """

        try:
            news_list = list()

            for news in self.ticker.news:
                news_dict = dict()  # reset the dictionary for each iteration of the loop (each article)
                news_dict["uuid"] = news["uuid"]
                news_dict["title"] = news["title"]
                news_dict["publisher"] = news["publisher"]
                news_dict["link"] = news["link"]
                news_dict["providerPublishTime"] = datetime.fromtimestamp(news["providerPublishTime"]).strftime("%Y-%m-%d %H:%M:%S")
                news_list.append(news_dict)

            news_df = pd.DataFrame(data=news_list, columns=["uuid", "title", "publisher", "link", "providerPublishTime"])
            return news_df

        except Exception as E:
            logger.error("No news found for: ", self.ticker.ticker, " with exception: ", E)
            return pd.DataFrame([])

    def prepare_historical_data(self):
        pass

    @staticmethod
    def clean_name(name):
        """
        Cleans the given name by removing titles and degrees and converting it to uppercase.

        Parameters
        ----------
        name : str
            The name to clean.

        Returns
        -------
        str
            The cleaned name.
        """
        # Remove titles and degrees
        for title in ["Dr.", "Ms.", "Mr.", "Ph.D.", "PhD", "MD", "MS"]:
            name = name.replace(title, "")
        return name.upper().strip()

    @staticmethod
    def count_number_of_shared_letters_ratio(name1, name2):
        """
        Calculates the ratio of shared letters between two names.

        Parameters
        ----------
        name1 : str
            The first name.
        name2 : str
            The second name.

        Returns
        -------
        float
            The ratio of shared letters between the two names.
        """
        return len(set(name1) & set(name2)) / len(set(name1) | set(name2))
