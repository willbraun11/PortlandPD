from functions import *

# First objective:  Make a png file of the Vice crimes for every month in the data set: Jan 2012 to Sept 2019

# Instantiate combined police call dataframe
df = start_with_combined()

# Need to create a df table of counts for every month:
# Start by getting the date_range of the df:
date_range = date_range_of_set(df, 'ReportMonthYear')

# Now split up the df by the range of dates:
df_split_by_date = split_df_by_date(df, date_range)

# Now convert the df's into smaller tables suitable for passing into the choropleth mapper:
choro_tables = [choro_table(i) for i in df_split_by_date]


# Now that we have the tables, and a list of date_ranges, we need a list of png output file names to pass to the make_and_screenshot function:
png_list = make_png_list('Vice_Crimes_by_Month', len(choro_tables))

# RE DEFINE TEST FUNCTIONS
def TEST_MAP(table, legend_name):
    bin_intervals = [0, 300, 500, 900, 1100, 1500, 6969]
    map = make_blank_map(11.5)
    portland_geo_data = r'/Users/will/Desktop/Portland/neighborhoods_regions.geojson'
    folium.Choropleth(
    geo_data = portland_geo_data,  
    data = table,
    columns = ['Neighborhood', 'Count'],
    key_on = 'properties.MAPLABEL',
    fill_color = 'YlOrRd', 
    fill_opacity = 0.7, 
    line_opacity = 0.3,
    legend_name = legend_name,
    bins=[float(x) for x in bin_intervals]).add_to(map)
    return map

def TEST_MAKE(tables, legends, output_png_names):
    output_html_names = make_html_list(output_png_names)
    

    for i in range(len(tables)):
        driver = webdriver.Chrome(executable_path='/Users/will/Desktop/chromedriver')
        driver.set_window_size(1100, 900)
        map = TEST_MAP(tables[i], legends[i])
        map.save(output_html_names[i])
        driver.get(f'file:///Users/will/dsi/PortlandPD/src/{output_html_names[i]}')
        time.sleep(3)
        driver.save_screenshot(output_png_names[i])
        os.remove(output_html_names[i])
        driver.quit()


# Now we are ready to pass these input into the main function...
TEST_MAKE(choro_tables, date_range, png_list)