import asyncio

import pandas as pd

from ticker_handler import TickerHandler
from utils import DATA_DIR, setup_custom_logger

logger = setup_custom_logger(__name__)


class AsyncDataDownloader:

    """
    A class that downloads data asynchronously.

    Parameters
    ----------
    tickers : list
        The list of tickers to download data for.

    Attributes
    ----------
    tickers : list
        The list of tickers to download data for.

    Methods
    -------
    get_data(ticker)
        Gets the data for the given ticker.
    save_data(data, file_path)
        Saves the data to the given file path.
    download_all_data()
        Downloads all data for the tickers.
    download_data_by_chunks(chunk_size=10, sleep_time=5)
        Downloads data for the tickers by chunks.
    """

    def __init__(self, tickers):
        self.tickers = tickers

    async def get_data(self, ticker):
        """
        Gets the data for the given ticker.

        Parameters
        ----------
        ticker : str
            The ticker to get data for.

        Returns
        -------
        tuple
            A tuple containing the dataframes for ticker info, insider holder, mutual fund, institution, and insider transaction.
        """

        logger.info(f"Getting data for ticker {ticker}")
        ticker_handler = TickerHandler(ticker)
        if not ticker_handler.is_valid_ticker():
            logger.info(f"Valid ticker {ticker}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        ticker_info = ticker_handler.prepare_ticker_info()
        insider_holder = ticker_handler.prepare_insider_roster_holders()
        mutual_fund = ticker_handler.prepare_mutualfund_holders()
        institution = ticker_handler.prepare_institutional_holders()
        insider_transaction = ticker_handler.prepare_insider_transactions()
        news = ticker_handler.prepare_news()

        # add ticker to the data
        ticker_info["ticker"] = ticker
        insider_holder["ticker"] = ticker
        mutual_fund["ticker"] = ticker
        institution["ticker"] = ticker
        insider_transaction["ticker"] = ticker
        news["ticker"] = ticker

        return ticker_info, insider_holder, mutual_fund, institution, insider_transaction, news

    async def save_data(self, data, file_name):
        """
        Saves the data to the given file path. The file path is created based on the current date.
        """
        current_date = pd.Timestamp.now().strftime("%Y-%m-%d")
        file_path = DATA_DIR / f"data_{current_date}" / file_name
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        data.to_csv(file_path, index=False)
        logger.info(f"Saved data to {file_path}")

    async def download_all_data(self):

        """
        Downloads all data for the tickers.
        """

        logger.info("Downloading all data for the tickers")
        tasks = []
        for ticker in self.tickers:
            tasks.append(self.get_data(ticker))

        # concat all dataframes separately
        all_data = await asyncio.gather(*tasks)
        all_ticker_info = pd.concat([data[0] for data in all_data])
        all_insider_holder = pd.concat([data[1] for data in all_data])
        all_mutual_fund = pd.concat([data[2] for data in all_data])
        all_institution = pd.concat([data[3] for data in all_data])
        all_insider_trade = pd.concat([data[4] for data in all_data])
        all_news = pd.concat([data[5] for data in all_data])

        # save all dataframes
        await self.save_data(all_ticker_info, "ticker_info.csv")
        await self.save_data(all_insider_holder, "insider_holder.csv")
        await self.save_data(all_mutual_fund, "mutual_fund.csv")
        await self.save_data(all_institution, "institution.csv")
        await self.save_data(all_insider_trade, "insider_transaction.csv")
        await self.save_data(all_news, "news.csv")

    async def download_data_by_chunks(self, chunk_size=4, sleep_time=2.5):

        """
        Downloads data for the tickers by chunks.

        Parameters
        ----------
        chunk_size : int
            The size of each chunk.
        sleep_time : int
            The time to sleep between each chunk.
        """

        logger.info(f"Downloading data for the tickers by chunks with chunk size {chunk_size} and sleep time {sleep_time}")
        chunks = [self.tickers[i : i + chunk_size] for i in range(0, len(self.tickers), chunk_size)]

        all_ticker_info = []
        all_insider_holder = []
        all_mutual_fund = []
        all_institution = []
        all_insider_transaction = []
        all_news = []

        for chunk in chunks:
            tasks = []
            for ticker in chunk:
                tasks.append(self.get_data(ticker))

            # concat all dataframes separately
            data_chunk = await asyncio.gather(*tasks)
            all_ticker_info.append(pd.concat([data[0] for data in data_chunk]))
            all_insider_holder.append(pd.concat([data[1] for data in data_chunk]))
            all_mutual_fund.append(pd.concat([data[2] for data in data_chunk]))
            all_institution.append(pd.concat([data[3] for data in data_chunk]))
            all_insider_transaction.append(pd.concat([data[4] for data in data_chunk]))
            all_news.append(pd.concat([data[5] for data in data_chunk]))

            # sleep for a while
            await asyncio.sleep(sleep_time)

        # save all dataframes
        await self.save_data(pd.concat(all_ticker_info), "ticker_info.csv")
        await self.save_data(pd.concat(all_insider_holder), "insider_holder.csv")
        await self.save_data(pd.concat(all_mutual_fund), "mutual_fund.csv")
        await self.save_data(pd.concat(all_institution), "institution.csv")
        await self.save_data(pd.concat(all_insider_transaction), "insider_transaction.csv")
        await self.save_data(pd.concat(all_news), "news.csv")


# %%
# tickers = ["MSFT", "AAPL", "GOOGL"]
# downloader = AsyncDataDownloader(tickers)
# asyncio.run(downloader.download_all_data())
