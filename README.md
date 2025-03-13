# Solar Panel Analysis
 

## Background and Overview
As part of our ongoing efforts to optimize renewable energy output, our team conducted an in-depth analysis of solar panel generation and weather sensor data collected from two solar farms in India. Over a 34-day period, data was recorded at 15-minute intervals to capture detailed operational metrics.

### Data Collection & Structure:

#### Power Generation Data:
 Data is collected at the inverter level, where each inverter monitors multiple strings of solar panels. This granular approach allows us to assess the performance of individual inverters and identify any discrepancies or areas for maintenance.  

#### Weather Sensor Data:
Weather measurements are captured at the plant level via a single, strategically placed array of sensors. This setup provides an overview of environmental conditions impacting the entire solar farm, ensuring that our energy generation forecasts account for real-time weather variations.

By integrating these datasets, we can develop robust models to predict future power output, identify efficiency trends, and ultimately enhance our operational strategies.

## Executive Summary



## Project Goals
Analysis aims to achieve the following objectives:
1. Forecast Future Power Generation
    - Develop accurate predictive models to forecast solar power generation for the next few days.
    - This will support improved grid management and energy distribution planning.
2. Optimize Maintence Scheduling:
    - Detect performance patterns that indicate when panels may require cleaning or routine maintenance, ensuring that overall effiency is maintained and downtime is minimized.
3. Identifying Faulty or Underperforming Panels:
    - Analyze the data to pinpoint panels that are malfunctioning or underperforming, enabling targeted interventions to enhance system reliablity and energy output.

## Data Structure Overview
![power generation table](images/power_output_table.png)
![weather data table](images/weather_sensors_table.png)

## Insights Deep Dive
### 2. Optimize Maintenance Scheduling
![Heatmap of correlation between weather variables and power generation](notebooks/output2/weekly_data_correlation_heatmap.png)
![daily yield of all inverters for plant 1](notebooks/output2/daily_yield_over_time.png)
![Heatmap of correlation between weather variables and power generation after removal of week 24](notebooks/output2/weekly_data_correlation_heatmap.png)
![daily yield of all inverters for plant 1 removed week 24](notebooks/output2/daily_yield_over_time2.png)

### 3. Indentifying Faulty or Underperforming Panels
 - Plant 1 consists of 22 inverters, with 3 underperforming relative to the standard deviation of the plant’s average daily yield. These inverters are generating approximately 3% less energy than expected, resulting in a daily yield reduction of 274.7 kWh. Over a month, this could lead to a total energy loss of ~8,241 kWh, significantly impacting overall plant efficiency and potential revenue.
![Average daily yield of all inverters for plant 1](output/average_daily_yield.png)
- In contrast, Plant 2 is experiencing a significantly more drastic performance issue. Four underperforming solar panels are generating 23% less energy than expected, leading to a daily yield reduction of 3,202.95 kWh—over 11 times the loss observed in Plant 1. If left unresolved, this could result in a staggering ~96,088.5 kWh loss per month, posing a substantial threat to operational efficiency and profitability
![Average daily yield of all inverters for plant 2](output/average_daily_yield2.png)

![composite table of average daily yield of underperforming inverters from both plants](output/composite_table.png)
- Plant 1 has a moderate efficiency loss (3%, 274.7 kWh/day), requiring monitoring and maintenance checks.
- Plant 2 has a severe efficiency loss (23%, 3,202.95 kWh/day), demanding urgent investigation and   corrective actions.




## Recommendations

## Technical Details

## Caveats and Assumptions




