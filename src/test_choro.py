from functions import *

df = start_with_combined()
table = list(choro_table(df))
date_range = ['2018-10-01']
png_list = ['TestFunction1.png']


def TEST_MAP(table, legend_name):
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
    legend_name = legend_name).add_to(map)
    return map

# legend_name=legend
# bins=[float(x) for x in bin_intervals
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

TEST_MAKE(table, '2018-01-01', png_list)


