# Data processing

Download csv from grafana dashboard - needed to do in stages since grafana limit on data points it can show. e.g. downloaded oct 2023 to mar 2024, april 24 to july 24 and then aug 24 to spet 24.

Opened in visual studio and merged into one.

NOTE: after processing data noticed that we had a couple of instances where the high tide was showing as being permanent between 2 high tides - usually when an object has been shifted into view of the sensor - so manually went and removed those

e.g. I added the data with the marker ** below to create an artificial low water (Look on Grafana at dates 21st Sept 2024 or 10th April 2024 to see the errors this is fixing)

```
2024-09-21 04:40:12,490
2024-09-21 04:50:13,565
2024-09-21 05:00:13,665
2024-09-21 05:10:13,765 **
2024-09-21 05:20:13,865 **
2024-09-21 15:40:13,885 **
2024-09-21 15:50:13,765 **
2024-09-21 16:00:13,665
2024-09-21 16:10:12,555
2024-09-21 16:20:13,470
```

The file _Maxbotix-Sonar-height-data-2023_10-2024-09.csv_ has been cleaned and can be used with the scripts. Note: updated June 2025 - noticed some values were creating double counts of flood events when the the two consecutive values were the same - the value were edited so that they end in 1 (e.g. 600, 600 become 600, 601). Similarly a few readings oscillated so these were also adjusted to be consistent (e.g. 650, 640, 645, 635, 645 become 650, 640, 636, 635, 645 - smoothing the curve). This was done to ensure that the flood events were not double counted on one event.

## Scripts

[high-tides.ipynb](/data/high-tides.ipynb) - the high tides script looks for all instances of high tide and returns when in the day they occured - in theory should be 2 a day. Data is output in [high-tides.csv](/data/high-tides.csv)

[flooding-high-tides.ipynb](/data/flooding-high-tides.ipynb) -  this script uses the sonar data (_Maxbotix-Sonar-height-data-2023_10-2024-09.csv_) to return two sets of data with the dates of all the high tides that touched the floor boards and above the floor boards. They prepend the counts to the csv files with the larger number being touching floor boards and the smaller number being above the floor boards. 

[minutes-under-water.ipynb](/data/minutes-under-water.ipynb) - The time under water script shows how many minutes the floor boards were under water and produces the monthly totals graphs shown below.

[flood-event-plots.ipynb](/data/flood-event-plots.ipynb) - takes the flood events data and plots them as charts

[duration-average.ipynb](/data/duration-average.ipynb) - calculates the average duration of each flood and standard deviation

- Average duration: 54.49 minutes
- Standard deviation of duration: 24.54 minutes

[proportion-floods-daytime.ipynb](/data/proportion-floods-daytime.ipynb) - calculates the numbers of floods occuring between 2 times - e.g. 9am to 6pm

The proportion of rows between 8 AM and 7 PM is: 46.79%

[stats-for-events.ipynb](/data/stats-for-events.ipynb) - calculating and significant differences in the human observed vs underfloor flood events


## Data from October 2023 to September 2024

109 flooding tides [data](/data/109-flooding-high-tides-touching-floorboards.csv)

32 flooding tides visible above floor boards [data](/data/32-flooding-high-tides.csv)

![minutes flooded](/data/mins-under-water-830.png)

![minutes flooded](/data/mins-under-water-570.png)

![touching floor board flood events per month](/data/109-flooding-high-tides-touching-floorboards.png)

![above floor board flood events per month](/data/32-flooding-high-tides-above-floorboards.png)