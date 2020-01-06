import pandas as pd
import numpy as np

def join_7_dataframes(filepath_list=['data/CAD-2012.csv', 
    'data/CAD-2013.csv',
    'data/CAD-2014.csv',
    'data/CAD-2015.csv',
    'data/CAD-2016.csv',
    'data/CAD-2017.csv',
    'data/CAD-2018.csv',
    'data/CAD-2019.csv']
    ):
    
    """
    Left join 7 DataFrames from the data directory into a new single dataframe.
    """
    all_dfs = []
    for filepath in filepath_list:
       all_dfs.append(pd.read_csv(filepath))

    new_df = pd.concat(all_dfs)
    return new_df