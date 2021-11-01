import numpy as np
import json
import sys
import random
import requests
import sqlalchemy
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from config import driver, username, password, host, port, database 
from slack_config import webhookURL
from refresh_from_api import refresh_from_api
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory


#################################################
# Database Setup
#################################################

connection_string = f"{driver}://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
ContentChoice = Base.classes.contentChoice
DailyForecastTB = Base.classes.dailyForecastTB
HourlyForecastTB = Base.classes.hourlyForecastTB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/data2")
@app.route("/data2/<homeLocation>", methods=["GET", "POST"])
def site_data(homeLocation=None):
    """Returns the data for the website"""

    homeLocation = request.form.get("campus") or "UCLA"

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to fetch the list of location names
    resultsLocations = session.query(ContentChoice).all()

    # if homeLocation == None:
    #     homeLocation = session.query(ContentChoice.shortName).filter_by(homePage = 'Y').one()
    #     print(homeLocation)

    # # Query to fetch the list of Daily forecast for 7 days
    # resultsDailyForecast = session.query(DailyForecastTB).filter_by(shortName = homeLocation).all()

    # # Query to fetch the list of Hourly forecast
    # resultsHourlyForecast = session.query(HourlyForecastTB).filter_by(shortName = homeLocation).all()
    
    # Query to fetch the list of Daily forecast for 7 days
    resultsDailyForecast = session.query(DailyForecastTB).all()

    # Query to fetch the list of Hourly forecast
    resultsHourlyForecast = session.query(HourlyForecastTB).all()

    content_choice = []
    for row in resultsLocations:
        choice = {}

        location = row.locationName
        short_name = row.shortName
        city = row.city
        latitude = row.latitude
        longitude = row.longitude

        choice["locationName"] = location
        choice["shortName"] = short_name
        choice["city"] = city
        choice["latitude"] = str(latitude)
        choice["longitude"] = str(longitude)

        content_choice.append(choice)

    daily_forecasts = []
    for row in resultsDailyForecast:
        day_forecast = {}

        day_forecast["daily_responseNumber"] = int(row.responseNumber)
        day_forecast["daily_responseName"] = row.responseName
        # Since the startDateTime is in GMT, we might not need it for the index.html. So commenting this line
        # day_forecast["daily_startDateTime"] = row.startDateTime
        day_forecast["daily_startDate"] = str(row.startDate)
        day_forecast["daily_startTime"] = str(row.startTime)
        # Since the endDateTime is in GMT, we might not need it for the index.html. So commenting this line
        # day_forecast["daily_endDateTime'] = str(row.endDateTime)
        day_forecast["daily_endDate"] = str(row.endDate)
        day_forecast["daily_endTimes"] = str(row.endTime)
        day_forecast["daily_isDaytime"] = row.isDaytime
        day_forecast["daily_temperature"] = int(row.temperature)
        # we have all units as F; do we have to send it as part of JSON
        day_forecast["daily_temperatureUnit"] = row.temperatureUnit
        # temperatureTrend always seem to be None and also not used for visualization. So commenting this line
        # day_forecast["daily_temperatureTrend"] = row.temperatureTrend)
        day_forecast["daily_windSpeed"] = row.windSpeed
        day_forecast["daily_minWindSpeed"] = int(row.minWindSpeed)
        day_forecast["daily_maxWindSpeed"] = str(row.maxWindSpeed)
        day_forecast["daily_windSpeedUnit"] = row.windSpeedUnit
        day_forecast["daily_windDirection"] = row.windDirection
        day_forecast["daily_icon"] = row.icon
        day_forecast["daily_shortForecast"] = row.shortForecast
        day_forecast["daily_detailedForecast"] = row.detailedForecast
        day_forecast["daily_retrievalDateTime"] = row.retrievalDateTime

        daily_forecasts.append(day_forecast)

    hourly_forecasts = []
    for row in resultsHourlyForecast:
        hour_forecast = {}

        hour_forecast["hourly_responseNumber"] = int(row.responseNumber)
        # Since the startDateTime is in GMT, we might not need it for the index.html. So commenting this line
        # hour_forecast["hourly_startDateTime"] = row.startDateTime
        hour_forecast["hourly_startDate"] = str(row.startDate)
        hour_forecast["hourly_startTime"] = str(row.startTime)
        # Since the endDateTime is in GMT, we might not need it for the index.html. So commenting this line
        # hour_forecast["hourly_endDateTime"] = row.endDateTime
        hour_forecast["hourly_endDate"] = str(row.endDate)
        hour_forecast["hourly_endTime"] = str(row.endTime)
        # Will we need isDaytime for any of the reporting?
        hour_forecast["hourly_isDaytime"] = row.isDaytime
        hour_forecast["hourly_temperature"] = int(row.temperature)
        # we have all units as F; do we have to send it as part of JSON
        # hour_forecast["hourly_temperatureUnits"] = row.temperatureUnit
        # temperatureTrend always seem to be None and also not used for visualization. So commenting this line
        # hour_forecast["hourly_temperatureTrend"] = row.temperatureTrend
        hour_forecast["hourly_windSpeed"] = row.windSpeed
        hour_forecast["hourly_hourWindSpeed"] = int(row.hourWindSpeed)
        hour_forecast["hourly_windSpeedUnit"] = row.windSpeedUnit
        hour_forecast["hourly_windDirection"] = row.windDirection
        hour_forecast["hourly_icon"] = row.icon
        hour_forecast["hourly_shortForecast"] = row.shortForecast

        hourly_forecasts.append(hour_forecast)

    session.close()

    data = {"locations" : content_choice, "dailyForecasts" : daily_forecasts, "hourlyForecasts" : hourly_forecasts}

    return jsonify(data)
    
@app.route("/refresh_data")
def refreshData():
    refresh_from_api()
    return render_template("index.html", code=302)


@app.route("/slack", methods=['POST'])
def slackMessage():
    inputMessage = request.form['message']
    if __name__ == '__main__':
        # message = ("Here's the weather for you in message!")
        title = (f"Here's today's weather update!")
        slack_data = {
            "username": "TyphoonsTuesday",
            "text": "Weather Forecast from TyphoonsTuesday",
            "icon_emoji": ":tornado:",
            "channel" : "#general",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            "title": title,
                            "value": inputMessage,
                            "short": "false",
                        }
                    ]
                }
            ]
        }
        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(webhookURL, data=json.dumps(slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
    
    return render_template("index.html", code=302)

if __name__ == '__main__':
    app.run(debug=True)
