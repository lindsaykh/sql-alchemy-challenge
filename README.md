# sql-alchemy-challenge
UNC CH BC HW

The jupyter notebook titled "climate_finished" uses SQLAlchemy to access a sqlite database
of Hawaiian weather data (temperature, precipitation, and date). The most recent date in the 
data set is determined and the last 12 months of data are retrieved for analysis.

A plot of precipitation (in inches) by date is made using Matplotlib and summary statistics
are printed using the Pandas describe function.

Analysis of stations in the dataset is done next. The number of stations, most active stations,
and lowest, highest, and avg temperature obtained from the most active station. Finally, a histogram
of 12 months of temperature data from the most active station is plotted using Matplotlib.

The app.py file in this repo first lists available routes. One route lists all precipitation values,
another the stations, another the last year of temperature data from the most active station, and finally
two routes give min/max/avg temp data based on either the input start date or the start/end date.

References:

https://github.com/goldenb85/sqlalchemy-challenge/blob/master/climate_starter.ipynb