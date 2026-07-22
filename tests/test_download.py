import asyncio
import pathlib
import sys
import types
import unittest
from unittest.mock import patch

SRC_DIR = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

if "yfinance" not in sys.modules:
    sys.modules["yfinance"] = types.SimpleNamespace(Ticker=type("Ticker", (), {}))

import download  # noqa: E402


class FakeInvalidTickerHandler:
    def __init__(self, ticker):
        self.ticker = ticker

    def is_valid_ticker(self):
        return False


class TestAsyncDataDownloader(unittest.TestCase):
    def test_get_data_returns_empty_frames_for_invalid_ticker(self):
        downloader = download.AsyncDataDownloader(["INVALID"])

        with patch("download.TickerHandler", FakeInvalidTickerHandler):
            results = asyncio.run(downloader.get_data("INVALID"))

        self.assertEqual(len(results), 6)
        self.assertTrue(all(df.empty for df in results))


if __name__ == "__main__":
    unittest.main()
