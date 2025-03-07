import pandas as pd
import os
import numpy as np
from data_access.candles_data_access import CandlesDataAccess

class Utils:

    def __init_ (self):
        self.candles_data_access = CandlesDataAccess

    def __convertCsvToParquet(self , month, year):
        csv = self.candles_data_access.get1sCsvPath(month , year)
        parquet = self.candles_data_access.get1sParquetPath(month , year)
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
        _1sData = self.__convertCsvToParquet(self , month, year)
        return _1sData

