from functions import *

# First objective:  Make a png file of the Vice crimes for every month in the data set: Jan 2012 to Sept 2019

# Instantiate combined police call dataframe
df = start_with_combined()

# Need to create a df table of counts for every month:
# Start by getting the date_range of the df:
date_range = date_range_of_set(df, 'ReportMonthYear')

# Now split up the df by the range of dates:
df_split_by_date = split_df_by_date(df, date_range)
half_the_dfs = df_split_by_date[::2]


# Run the full df:
# choro_tables = [choro_table(i) for i in df_split_by_date]


# Run only half the df:
choro_tables = [choro_table(i) for i in half_the_dfs]
date_range = date_range[::2]

# Now that we have the tables, and a list of date_ranges, we need a list of png output file names to pass to the make_and_screenshot function:
png_list = make_png_list('Total_Crimes_by_Month', len(choro_tables))


# Now we are ready to pass these input into the main function...
make_and_screenshot_with_bins(choro_tables, date_range, png_list)