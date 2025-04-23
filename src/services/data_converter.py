import pandas as pd
import os
import numpy as np
from data_paths.path_provider import PathProvider

class DataConverter:

    def __init__ (self, path_provider:PathProvider):
        self.path_provider = path_provider

    def __convertCsvToParquet(self,month, year):
        csv = self.path_provider.get1sCsvPath(month , year)
        parquet = self.path_provider.get1sParquetPath(month , year)
        if not os.path.exists(parquet):
            df = pd.read_csv(csv, usecols=[0, 1])
            df.to_parquet(parquet, index=False)
        else:
            df = pd.read_parquet(parquet)
        data1s = df.to_numpy()
        np.set_printoptions(
            formatter={
                "float_kind": lambda x: (
                    "{:.2f}".format(x) if x % 1 else "{:.0f}".format(x)
                )
            }
        )
        return data1s
    
    def get1sData (self, month, year):
        _1sData = self.__convertCsvToParquet(month, year)
        return _1sData

