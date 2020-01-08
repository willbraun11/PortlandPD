# A history of Marijuana Legalization in Portland, OR:
Oregon was the first state to decriminalize marijuana in the United States in 1973.  The Oregon Decriminalizaion Bill made possession of 1 ounce or less a violation (not a crime) punishable by a fine of $500-1000.  In 1986 - 26 years before Colorado and Washington became the first states to legalize marijuana - a Bill sought to legalize marijuana in Oregon.  It failed to pass with only 26.33% support from voters.  In 1997, House Bill 3643 was passed and recriminalized possession of less than an ounce to a Class C misdemeanor.

A bill proposing to legalize marijuana in 2012 failed to pass by a margin of 53% against - 47% for.

Finally in 2014 Oregon became the 5th state to pass legislation to legalize recreational use of marijuana and allow for state-controlled sale of cannabis. 

The legalization of marijuana in Oregon officially took effect on July 1st, 2015.  On October 1st, 2015, Oregon Governor Kate Brown signed an emergency bill declaring marijuana sales legal to recreational consumers (Paris, Achen).   

## The Dataset
While searching for datasets I came across the ["Police Data Initative"](https://www.policedatainitiative.org/).  This initiative serves to:
*<center>"promotes the use of open data to encourage joint problem solving, innovation, enhanced understanding, and accountability <br /> between communities and the law enforcement agencies that serve them." (https://www.policedatainitiative.org/) </center>* 

Over 130 US Police Agencies have voluntarily joined the Initiative and release datasets that summarize some of their activities.  Searching the data-sets of these 130 Agencies reveals that some Agencies are much more thorough in their compilation and release of data than others.  Portland PD is particularly generous with their information and releases [data-sets](https://www.portlandoregon.gov/police/71673) pertaining to Dispatched Calls, Traffic Stops, Uses of Force, Officer Involved Shootings, Traffic Stops, and others.  Portland PD was also of particular interest due to the recent legalization of marijuana and its' potential impact on crime trends.  

Further analysis could combine many of these data-sets to identify trends across data-sets.  This study pertains to the Dispatched Calls data-set which contains 7 csv files each containing roughly 30,000 rows and 14 columns - with each row representing one dispatched police call.  The columns include values for lat and long, call category ('Vice', 'Assault', 'Community Assist', etc...), response time, priority, and neighborhood.

## Data Pipeline
The World Bank investment data was easily accessed by csv file which I imported into a PostgreSQL database table. The EIA's data was much less straightforward. Detailed data for all countries was not available through a single API, so I found a bulk download (csv) of different series IDs available in all of the EIA's data. I imported these series keys into a Mongo database because each series had a different schema. I then queried the Mongo database to call individual country APIs to gather all the renewable energy generation and capacity data for all countries. To calculate generation/capacity ratios I also added columns of data to one of the Postgres tables with capacity converted to expected generation based on projections of the availability factor of renewable energy sources (kW => kWh). I created columns of varying availability factors and ultimately used a conservative estimate of 75% availability. Most renewable energy sources typically have availability of 80%-98%.

## Data Analysis
The primary focus of early data analysis was to determine if there were any significant impacts of the legalization of marijuana on criminal trends.



### Maybe Useful...
Since the early 2000's, surveys maintained by the Drug Enforcement Administration and the National Organization for the Reform of Marijuana Laws show that the rate of Oregon citizens who use cannabis is between 30-40% higher than the national average.  Oregon ranks in the top 20th percentile for marijuana use in several different age ranges (DEA, Portland Business Journal, NORML).

# References
https://en.wikipedia.org/wiki/Cannabis_in_Oregon#Legal_history
 
"Oregon Marijuana Statistics". National Organization for the Reform of Marijuana Laws. 2008-12-05. Archived from the original on April 15, 2008. Retrieved 2008-12-17.

"Oregon marijuana use among highest in U.S." Portland Business Journal. 2006-04-06. Archived from the original on 2008-02-25. Retrieved 2008-12-17.

"DEA Briefs and Background, Drugs and Drug Abuse, State Factsheets, Oregon". Drug Enforcement Administration. Archived from the original on August 22, 2008. Retrieved 2008-12-18.

Aachen, Paris (March 30, 2016). "New marijuana law clears way for recreational, medical sales in same place". Portland Tribune. Archived from the original on February 11, 2017. Retrieved 2017-02-08.

https://www.policedatainitiative.org/








# REFERENCE #
# Impact of Private Investments in Global Generation and Capacity of Renewable Energy
In the US, approximately 29% of global warming emissions are created by energy sources, mostly from fossil fuels. Most renewable energy sources generate little to no global warming emissions, even when considering a full lifecycle assessment. The International Energy Agency estimates that energy demand will increase by 70% by 2040 if current trends continue. Renewable energy needs to be a global priority. 

## Data Sources
While exploring data available in the renewable energy space I was intrigued by the U.S. Energy Information Association's plethora of demand, generation, capacity, and projection data surrounding both renewable and non-renewable energy sources. After finding The World Bank's compilation of private investments in global renewable energy in developing countries from 1980 to 2016 I decided to analyze both data sources together.

## Data Pipeline
The World Bank investment data was easily accessed by csv file which I imported into a PostgreSQL database table. The EIA's data was much less straightforward. Detailed data for all countries was not available through a single API, so I found a bulk download (csv) of different series IDs available in all of the EIA's data. I imported these series keys into a Mongo database because each series had a different schema. I then queried the Mongo database to call individual country APIs to gather all the renewable energy generation and capacity data for all countries. To calculate generation/capacity ratios I also added columns of data to one of the Postgres tables with capacity converted to expected generation based on projections of the availability factor of renewable energy sources (kW => kWh). I created columns of varying availability factors and ultimately used a conservative estimate of 75% availability. Most renewable energy sources typically have availability of 80%-98%.

## Data Analysis
The private investment data included 60 different attributes including several I was interested in around government/policy support and percent private investment vs public. Unfortunately after reviewing the data I determined most of these facets had too many null values to be of use. The EIA data simply provided country name and generation/capacity level by year. I used Psycopg2 to access the data I had stored in Postgres and did much of my analysis with Pandas. Unfortunately I didn't find a high correlation in number of projects or amount of investment in relation to capacity change year over year.

### Highest Private Investments
<p align="center">
  <img src="https://github.com/vanessapolliard/renewable-energy-generation/blob/master/images/top16countries.png">
</p>


The private investment data was limited to countries categorized as low- and middle-income under World Bank classification. After grouping the investment data by country I was surprised to find that, of the 85 countries in the data, Brazil had by far the highest level of private investments in renewable energy. 

### Largest Capacity Impact per $ Invested
<p align="center">
  <img src="https://github.com/vanessapolliard/renewable-energy-generation/blob/master/images/capacityperusd.png">
</p>

Using purely the investment data I found the capacity/$ rate for each renewable energy technology category. It appears that water-related resources have a slightly higher yield in comparison to the other tech categories. After reviewing this grouping I was surprised to see Natural Gas (nonrenewable) as a tech category, but after reviewing the data found that this refers to CSP (concentrated solar power) which is more comparable to natural gas than solar power.

### Investments by Income Class
<p align="center">
  <img src="https://github.com/vanessapolliard/renewable-energy-generation/blob/master/images/privateinvestmentbyincome.png">
</p>

Unsurprisingly the majority of private investments occurred in upper-middle income level countries. Brazil being in that category may be a factor to why there is such a large difference. 

### Trends in Capacity
<p align="center">
  <img src="https://github.com/vanessapolliard/renewable-energy-generation/blob/master/images/top16capacity.png">
</p>

I reviewed generation trends in comparison to number of private renewable energy projects from 1980-2016 to see if generation increased significantly when more projects occurred.

### Trends in Generation/Capacity Ratio
![Capacity Impact per $ Invested](https://github.com/vanessapolliard/renewable-energy-generation/blob/master/images/top16ratio.png)

Because generation typically increased with capacity I didn't find any impact from private projects.

### Capacity Change YOY
![Capacity Change YOY](https://github.com/vanessapolliard/renewable-energy-generation/blob/master/images/capacityyoy.png)

Capacity change is typically positive with a few exceptions for all top 16 countries. Unfortunately I didn't find a correlation between private investment project count or amount in year over year capacity change.

## Resources
Data used in this analysis was sourced from:
* [The World Bank Data Catalog](https://datacatalog.worldbank.org/dataset/private-participation-renewable-energy)
* [U.S. Energy Information Association API](https://www.eia.gov/opendata/qb.php?category=2134384)

Other citations:
* [Benefits of Renewable Energy Use](https://www.ucsusa.org/clean-energy/renewable-energy/public-benefits-of-renewable-power)
* [U.S. Energy Information Association API](https://www.eia.gov/opendata/qb.php?category=2134384)