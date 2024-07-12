# %% https://memgraph.com/blog/jupyter-translate-data-to-graph-database
import asyncio

import pandas as pd

from src.ticker_handler import TickerHandler


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
        ticker_handler = TickerHandler(ticker)
        ticker_info = ticker_handler.prepare_ticker_info()
        insider_holder = ticker_handler.prepare_insider_roster_holders()
        mutual_fund = ticker_handler.prepare_mutualfund_holders()
        institution = ticker_handler.prepare_institutional_holders()
        insider_trade = ticker_handler.prepare_insider_transactions()

        # add ticker to the data
        ticker_info["ticker"] = ticker
        insider_holder["ticker"] = ticker
        mutual_fund["ticker"] = ticker
        institution["ticker"] = ticker
        insider_trade["ticker"] = ticker

        return ticker_info, insider_holder, mutual_fund, institution, insider_trade

    async def save_data(self, data, file_path):
        data.to_csv(file_path, index=False)

    async def download_all_data(self):
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

        # save all dataframes
        await self.save_data(all_ticker_info, "ticker_info.csv")
        await self.save_data(all_insider_holder, "insider_holder.csv")
        await self.save_data(all_mutual_fund, "mutual_fund.csv")
        await self.save_data(all_institution, "institution.csv")
        await self.save_data(all_insider_trade, "insider_trade.csv")

    async def download_data_by_chunks(self, chunk_size=10, sleep_time=5):
        chunks = [self.tickers[i : i + chunk_size] for i in range(0, len(self.tickers), chunk_size)]

        all_data = []
        all_ticker_info = []
        all_insider_holder = []
        all_mutual_fund = []
        all_institution = []
        all_insider_trade = []

        for chunk in chunks:
            tasks = []
            for ticker in chunk:
                tasks.append(self.get_data(ticker))

            # concat all dataframes separately
            data = await asyncio.gather(*tasks)
            all_data.append(data)
            all_ticker_info.append(pd.concat([data[0] for data in data]))
            all_insider_holder.append(pd.concat([data[1] for data in data]))
            all_mutual_fund.append(pd.concat([data[2] for data in data]))
            all_institution.append(pd.concat([data[3] for data in data]))
            all_insider_trade.append(pd.concat([data[4] for data in data]))

            # sleep for a while
            await asyncio.sleep(sleep_time)

        # save all dataframes
        await self.save_data(pd.concat(all_ticker_info), "ticker_info.csv")
        await self.save_data(pd.concat(all_insider_holder), "insider_holder.csv")
        await self.save_data(pd.concat(all_mutual_fund), "mutual_fund.csv")
        await self.save_data(pd.concat(all_institution), "institution.csv")
        await self.save_data(pd.concat(all_insider_trade), "insider_trade.csv")


# %%
tickers = ["MSFT", "AAPL", "GOOGL"]
downloader = AsyncDataDownloader(tickers)
asyncio.run(downloader.download_all_data())
