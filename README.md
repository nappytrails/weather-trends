# Weather Trends and Forecast




## By Typhoons Tuesday
---


## **Founders:** Erin Kinney, Sushma Kesamsetty, Ricky Lee
---




## **Objective**:
---


The purpose of this project is to create a website for school staffs to have an easy-to-use tools to alert parents on weather forcasts and promptly update them with newly updated information. 

School location(s), City and associated Longitude/Latitude values are configurable. Based on the list of schools in the DB table, Weather data is loaded and used for visualization.

For example, if the road condition is bad due to the weather, staffs can used our website to quickly make decision and alert the parents all on our website. We provide dropdown menus to pin locations easily and hourly and weekly weather trends by line charts and map. 

## **Libraries / Requirements:**
---

- JSON
- HTML/CSS
- JS
- JQuery
- Python
- Pandas
- D3
- PostgreSQL
- Flask
- Plotly
- Leaflet
- AWS
- Slack Incoming-Webhook Extension

## Data Source 
---

- https://www.weather.gov/documentation/services-web-api

## Data Collection Process:
---


We collected our weather forcast data by using api.weather.gov and extracted current weather datas using Pandas and JSON. To clean the data, we have used JSON and loaded them to PosgreSQL. 

## Visualization:
---
[**Map Visualization**](https://github.com/skesamsetty/weather-trends/blob/main/images/SiteMockup.png)

1. We used dropdowns to pin point locations.
2. Used Plotly to display Hourly and Wind Speed line charts
3. The map and markers to the map to display the weather forcast. Used L.circle functions and bindPopup to give more detailed information. 










