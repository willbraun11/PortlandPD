# Master function list for Portland Police Data Case Study
# imports:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import folium
from folium.plugins import MarkerCluster


def join_csv_dataframes(filepath_list=['data/CAD-2012.csv', 
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

def make_datetime_column(df, column_with_date_string):
    df2 = df.copy()
    date_series = pd.to_datetime(df[column_with_date_string])
    df2[column_with_date_string] = date_series
    return df2

def make_blank_map(coord_list, zoom_start):
    map = folium.Map(location=coord_list, zoom_start=zoom_start)
    return map

def plot_clustered_folium_points(map, df, lat_col, long_col,                                                     max_records=500):
    mc = MarkerCluster().add_to(map)

 
    # add a marker for every record in the filtered data, use a clustered view
    for each in df[0:max_records].iterrows():
        if math.isnan(each[1][lat_col]) or math.isnan(each[1][long_col]):
            continue
        else:
            folium.Marker(location = [each[1][lat_col],each[1][long_col]],
                        clustered_marker = True).add_to(mc)

    return map


def neighborhood_correcter(df):
    neighborhood_correcter = {'Ardenwald': 'Ardenwald-Johnson Creek', 
                          'Argay':'Argay Terrace',
                         'Brooklyn':'Brooklyn Action Corps',
                         'Buckman East': 'Buckman Community Association',
                         'Buckman West': 'Buckman Community Association',
                         'Centennial':'Centennial Community Association',
                         'Cully':'Cully Association of Neighbors',
                         'Downtown':'Portland Downtown',
                         'Goose Hollow':'Goose Hollow Foothills League',
                         'Hayden Island':'Hayden Island Neighborhood Network',
                         'Hosford-Abernethy':'Hosford-Abernethy Neighborhood District Assn.',
                         'Irvington':'Irvington Community Association',
                         'Lloyd':'Lloyd District Community Association',
                         'Mt Scott-Arletta':'Mt. Scott Arletta',
                         'Mt Tabor':'Mt. Tabor',
                         'Northwest':'Northwest District Association',
                         'Old Town/Chinatown':'Old Town Community Association',
                         'Parkrose Heights':'Parkrose Heights Association of Neighbors',
                         'Pearl':'Pearl District',
                         'Sabin':'Sabin Community Association',
                         'Sellwood-Moreland':'Sellwood-Moreland Improvement League',
                         'Southwest Hills':'Southwest Hills Residential League',
                         'St Johns':'St. Johns',
                         'Sumner':'Sumner Association of Neighbors',
                         'Sunderland':'Sunderland Association of Neighbors',
                         'Wilkes':'Wilkes Community Group'}
    # police just list Parkrose Heights, neighborhoods has both Parkrose and 
    # Parkrose Heights Association of Neighbors
    # MC Unclaimed #11, 13, 14, 5
    df['Neighborhood'].map(neighborhood_correcter).fillna(df['col1'])
    return df