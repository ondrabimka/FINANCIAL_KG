from enum import Enum

import pandas as pd


class Files(Enum):
    """
    Enum class for the names of the files in the data directory
    """

    INSIDER_HOLDER = "insider_holder.csv"
    INSIDER_TRANSACTION = "insider_transaction.csv"
    INSTITUTION = "institution.csv"
    MUTUAL_FUND = "mutual_fund.csv"
    TICKER_INFO = "info.csv"


class DataReader:
    """
    Class to read the data from the csv files in the data directory

    Attributes
    ----------
    data_path : Path
        Path to the data directory
    """

    def __init__(self, data_path):
        """
        Parameters
        ----------
        data_path : Path
            Path to the data directory
        """
        self.data_path = data_path

    def read_all_files(self, file: Files):
        """
        Read all the files with the given name in the data directory

        Parameters
        ----------
        file : Files
            Name of the file to read
        """
        dfs = []
        for directory in self.get_all_directories():
            for file_dir in self.get_all_files_w_name(directory, file):
                print("FILE IN LOOP:", file_dir)
                dfs.append(self.read_df(file_dir))
        return pd.concat(dfs, ignore_index=True)

    @staticmethod
    def read_df(dir):
        """
        Read the csv file in the given directory and return the dataframe

        Parameters
        ----------
        dir : Path
            Path to the csv file
        """

        df = pd.read_csv(dir)
        date = str(dir).split("/")[-2].replace("data_", "")
        df["date"] = pd.to_datetime(date)
        return df

    @staticmethod
    def get_all_files_w_name(files_path, file):
        """Get all files in the directory with the given name

        Parameters
        ----------
        files_path : Path
            Path to the directory
        file : str
            Name of the file to search for
        """
        print("PATH:", files_path)
        print("FILE:", file)
        print("FILE VAL:", file.value)
        return [x for x in files_path.iterdir() if x.name == file.value]

    def get_all_directories(self):
        """Get all directories in the data directory"""
        return [x for x in self.data_path.iterdir() if x.is_dir()]
