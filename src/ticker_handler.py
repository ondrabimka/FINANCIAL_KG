import pandas as pd
import yfinance as yf


# %%
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
        # TODO: Include company officers. Map them maybe?
        # officers = info.pop('companyOfficers')
        # officers = pd.DataFrame(officers)
        return pd.concat([pd.DataFrame([info]), self.prepare_insider_purchases(), self.prepare_major_holders()], axis=1)

    def prepare_major_holders(self) -> pd.DataFrame:
        """
        Prepares the major holders information.

        Returns
        -------
        pd.DataFrame
            The major holders information.
        """
        major_holders = self.ticker.major_holders
        major_holders = major_holders.T
        major_holders = major_holders.reset_index(drop=True)
        return major_holders

    def prepare_insider_purchases(self) -> pd.DataFrame:
        """
        Prepares the insider purchases information.

        Returns
        -------
        pd.DataFrame
            The insider purchases information.
        """
        insider_purchases = self.ticker.insider_purchases
        insider_purchases = insider_purchases[["Insider Purchases Last 6m", "Shares"]].T
        insider_purchases.columns = insider_purchases.iloc[0]
        insider_purchases = insider_purchases[1:]
        insider_purchases.columns = [f"Insider {col}" for col in insider_purchases.columns]
        insider_purchases = insider_purchases.reset_index(drop=True)
        return insider_purchases

    def prepare_institutional_holders(self) -> pd.DataFrame:
        """
        Prepares the institutional holders information.

        Returns
        -------
        pd.DataFrame
            The institutional holders information.
        """
        institutional_holders = self.ticker.institutional_holders
        return institutional_holders

    def prepare_mutualfund_holders(self) -> pd.DataFrame:
        """
        Prepares the mutual fund holders information.

        Returns
        -------
        pd.DataFrame
            The mutual fund holders information.
        """
        mutualfund_holders = self.ticker.mutualfund_holders
        return mutualfund_holders

    def prepare_insider_transactions(self) -> pd.DataFrame:
        """
        Prepares the insider transactions information.

        Returns
        -------
        pd.DataFrame
            The insider transactions information.
        """
        insider_transactions = self.ticker.insider_transactions
        return insider_transactions

    def prepare_insider_roster_holders(self) -> pd.DataFrame:
        """
        Prepares the insider roster holders information.

        Returns
        -------
        pd.DataFrame
            The insider roster holders information.
        """
        insider_roster_holders = self.ticker.insider_roster_holders
        return insider_roster_holders

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
