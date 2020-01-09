# Master function list for Portland Police Data Case Study
# imports:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import folium
from folium.plugins import MarkerCluster
from selenium import webdriver
import os
import time



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

def make_blank_map(zoom_start, location=[45.5236, -122.6750]):
    map = folium.Map(zoom_start=zoom_start, location=location)
    return map

def plot_clustered_folium_points(map, df, lat_col, long_col,                                                     max_records=500):
    mc = MarkerCluster().add_to(map)
    for each in df[0:max_records].iterrows():
        if math.isnan(each[1][lat_col]) or math.isnan(each[1][long_col]):
            continue
        else:
            folium.Marker(location = [each[1][lat_col],each[1][long_col]],
                        clustered_marker = True).add_to(mc)

    return map


def neighborhood_correcter(df):
    neighborhood_key = {'Ardenwald': 'Ardenwald-Johnson Creek', 
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
                         'Mt Scott-Arleta':'Mt. Scott-Arleta',
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
    df['Neighborhood'] = df['Neighborhood'].map(neighborhood_key).fillna(df['Neighborhood'])


def start_with_combined():
    df = pd.read_csv('/Users/will/Desktop/Portland/calls_for_service/CAD-combined.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    col_with_dates = 'ReportMonthYear'
    df = make_datetime_column(df, col_with_dates)
    df = df.sort_values(by='ReportMonthYear')
    neighborhood_correcter(df)
    return df

def choro_table(df):
    table = pd.DataFrame(df['Neighborhood'].value_counts().astype(float))
    table = table.reset_index()
    table.columns = ['Neighborhood', 'Count']
    return table

def split_df_by_date(df, date_list):
    lst_of_dfs = []
    for i in date_list:
        lst_of_dfs.append((df[df['ReportMonthYear'] == i]))
    return lst_of_dfs

def date_range_of_set(df, col_name_of_dates):
    date_array = df[col_name_of_dates].unique()
    date_range = [str(i) for i in date_array]
    date_range.sort()
    return [i[0:10] for i in date_range]


def make_vice_map(table, legend_name):
    bin_intervals = [0, 60, 120, 180, 240, 300, 360]
    map = make_blank_map(11.5)
    portland_geo_data = r'/Users/will/Desktop/Portland/neighborhoods_regions.geojson'
    folium.Choropleth(
    geo_data = portland_geo_data,  
    data = table,
    columns = ['Neighborhood', 'Count'],
    key_on = 'properties.MAPLABEL',
    fill_color = 'YlOrRd', 
    fill_opacity = 0.6, 
    line_opacity = 0.4,
    legend_name = legend_name,
    bins=[float(x) for x in bin_intervals],
    nan_fill_color='white').add_to(map)
    return map


def make_choro_map_with_bins(table, legend_name):
    bin_intervals = [0, 287, 574, 861, 1148, 1435, 1722]
    map = make_blank_map(11.5)
    portland_geo_data = r'/Users/will/Desktop/Portland/neighborhoods_regions.geojson'
    folium.Choropleth(
    geo_data = portland_geo_data,  
    data = table,
    columns = ['Neighborhood', 'Count'],
    key_on = 'properties.MAPLABEL',
    fill_color = 'YlOrRd', 
    fill_opacity = 0.6, 
    line_opacity = 0.4,
    legend_name = legend_name,
    bins=[float(x) for x in bin_intervals],
    nan_fill_color='white').add_to(map)
    return map
# Use for Vice: BuGn
# old color: YlOrRd
# other option: BuPu

def make_choro_map(table, legend_name):
    map = make_blank_map(11.5)
    portland_geo_data = r'/Users/will/Desktop/Portland/neighborhoods_regions.geojson'
    folium.Choropleth(
    geo_data = portland_geo_data,  
    data = table,
    columns = ['Neighborhood', 'Count'],
    key_on = 'properties.MAPLABEL',
    fill_color = 'YlOrRd', 
    fill_opacity = 0.6, 
    line_opacity = 0.4,
    legend_name = legend_name).add_to(map)
    return map

def make_and_screenshot_with_bins(tables, legend_names, output_png_names):
    output_html_names = make_html_list(output_png_names)
    

    for i in range(len(tables)):
        driver = webdriver.Chrome(executable_path='/Users/will/Desktop/chromedriver')
        driver.set_window_size(1100, 900)
        map = make_choro_map_with_bins(tables[i], legend_names[i])
        map.save(output_html_names[i])
        driver.get(f'file:///Users/will/dsi/PortlandPD/src/{output_html_names[i]}')
        time.sleep(3)
        driver.save_screenshot(output_png_names[i])
        os.remove(output_html_names[i])
        driver.quit()

def make_and_screenshot(tables, legend_names, output_png_names):
    output_html_names = make_html_list(output_png_names)
    

    for i in range(len(tables)):
        driver = webdriver.Chrome(executable_path='/Users/will/Desktop/chromedriver')
        driver.set_window_size(1100, 900)
        map = make_choro_map(tables[i], legend_names[i])
        map.save(output_html_names[i])
        driver.get(f'file:///Users/will/dsi/PortlandPD/src/{output_html_names[i]}')
        time.sleep(3)
        driver.save_screenshot(output_png_names[i])
        os.remove(output_html_names[i])
        driver.quit()

def make_png_list(base, num_values):
    png_list = []
    for i in range(num_values):
        if i<9:
            png_list.append(base + '0' + str(i+1) + '.png')
        else:
            png_list.append(base + str(i+1) + '.png')
    return png_list

def make_html_list(png_list):
    png_list = [name.strip('.png')+'.html' for name in png_list]
    return png_list




if __name__=="__main__":
    pass
    
        