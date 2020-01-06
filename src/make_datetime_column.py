import pandas as pd
import numpy as np

def make_datetime_column(df, column_with_date_string):
    df2 = df.copy()
    date_series = pd.to_datetime(df[column_with_date_string])
    df2[column_with_date_string] = date_series
    return df2