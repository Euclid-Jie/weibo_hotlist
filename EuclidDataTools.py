# -*- coding: utf-8 -*-
# @Time    : 2023/3/11 10:45
# @Author  : Euclid-Jie
# @File    : EuclidDataTools.py
import pandas as pd
from pathlib import Path


class EuclidCsvTools:
    """
    this class include tools used to precess csv file
    """

    def __init__(self, subFolder: str = None, FileName: str = "DemoOut.csv"):
        # para init
        self.subFolder = subFolder
        self.FileName = FileName
        self.FullFilePath: Path = None
        self.FullFolderPath: Path = None

    def path_clear(self):
        """
        get the full folder path and full file path
        :return:
        """
        if self.subFolder:
            self.FullFolderPath = Path("./", self.subFolder)
            self.FullFilePath = Path(self.subFolder, self.FileName)
        else:
            self.FullFolderPath = Path("./")
            self.FullFilePath = Path("./", self.FileName)
        print("文件将存储在: {}".format(self.FullFilePath))

    def saveCsvFile(self, df, append=False, **kawrgs):
        """
        save data to csv
        :param df: pd.DataFrame
        :param append: True(append save) or False(overwrite)
        :return:
        """
        if not self.FullFilePath:
            self.path_clear()

        self.FullFolderPath.mkdir(parents=True, exist_ok=True)
        if append:
            self.writeDf2Csv(df, self.FullFilePath, kawrgs)
        else:
            df.to_csv(
                self.FullFilePath,
                encoding=kawrgs.get("encoding", "utf_8_sig"),
                index=False,
            )

    @classmethod
    def writeDf2Csv(cls, df, FullFilePath, **kawrgs):
        if Path(FullFilePath).exists():
            # write after a exist file without header
            df.to_csv(
                FullFilePath,
                mode="a",
                encoding=kawrgs.get("encoding", "utf_8_sig"),
                header=False,
                index=False,
            )
        else:
            # write out a new file with header
            df.to_csv(
                FullFilePath,
                mode="w",
                encoding=kawrgs.get("encoding", "utf_8_sig"),
                header=True,
                index=False,
            )


class CsvClient(EuclidCsvTools):
    def __init__(self, subFolder: str = None, FileName: str = "DemoOut.csv"):
        """
        :param subFolder:
        :param FileName:
        """
        super().__init__(subFolder=subFolder, FileName=FileName)
        if FileName[-4:] != ".csv":
            self.FileName = self.FileName + ".csv"
        self.path_clear()

    def insert_one(self, data, **kwargs):
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        elif isinstance(data, pd.DataFrame):
            pass
        else:
            raise TypeError("传入参数仅支出dict和pd.DataFrame")
        self.saveCsvFile(df=data, append=True, kwargs=kwargs)
