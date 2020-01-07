from functions import *

df = start_with_combined()
table = choro_table(df)
date_range = ['2018-10-01']
png_list = ['TestFunction1.png']

make_and_screenshot(table, date_range, png_list)


