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

The file _Maxbotix-Sonar-height-data-2023_10-2024-09.csv_ has been cleaned and can be used with the scripts.

## Scripts

high-tides/ipynb - the high tides script looks for all instances of high tide and returns when in the day they occured - in theory shoyuld be 2 a day. Data is output in [high-tides.csv](/data/high-tides.csv)

The max height script then uses this data to return the dates of all the high tides that touched the floor boards.

minutes-under-water.ipynb - The time under water script shows how many minutes the floor boards were under water and produces the monthly totals graphs shown below.

## Data from October 2023 to September 2024

166 flooding tides [data](/data/166-flooding-high-tides-touching-floorboards.csv)

61 flooding tides visible above floor boards [data](/data/61-flooding-high-tides-visible.csv)

![minutes flooded](/data/mins-under-water-830.png)

![minutes flooded](/data/mins-under-water-570.png)
