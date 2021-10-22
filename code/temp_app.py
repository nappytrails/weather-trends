

@app.route("/names")
def locationNames():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # initialize the lists - contentChoice Table
    all_location_names = []
    all_short_names = []
    all_latitudes = []
    all_longitudes = []
    all_cities = []

    # initialize the lists - dailyForecastTB Table
    daily_responseNumbers = []
    daily_startDateTimes = []
    daily_startDates = []
    daily_startTimes = []
    daily_endDateTimes = []
    daily_endDates = []
    daily_endTimes = []
    daily_isDaytimes = []
    daily_temperatures = []
    daily_temperatureUnits = []
    daily_temperatureTrends = []
    daily_windSpeeds = []
    daily_minWindSpeeds = []
    daily_maxWindSpeeds = []
    daily_windSpeedUnits = []
    daily_windDirections = []
    daily_icons = []
    daily_shortForecasts = []
    daily_detailedForecasts = []
    daily_retrievalDateTimes = []

    # initialize the lists - hourlyForecastTB Table
    hourly_responseNumbers = []
    hourly_startDateTimes = []
    hourly_startDates = []
    hourly_startTimes = []
    hourly_endDateTimes = []
    hourly_endDates = []
    hourly_endTimes = []
    hourly_isDaytimes = []
    hourly_temperatures = []
    hourly_temperatureUnits = []
    hourly_temperatureTrends = []
    hourly_windSpeeds = []
    hourly_hourWindSpeeds = []
    hourly_windSpeedUnits = []
    hourly_windDirections = []
    hourly_icons = []
    hourly_shortForecasts = []

    """Returns the list of choices for dropdown"""
    # Query to fetch the list of location names
    resultsLocations = session.query(ContentChoice).all()

    # Query to fetch the list of Daily forecast for 7 days
    resultsDailyForecast = session.query(DailyForecastTB).all()

    # Query to fetch the list of Hourly forecast
    resultsHourlyForecast = session.query(HourlyForecastTB).all()

    session.close()

    for row in resultsLocations:
        all_location_names.append(row.locationName)
        all_short_names.append(row.shortName)
        all_latitudes.append(str(row.latitude))
        all_longitudes.append(str(row.longitude))
        all_cities.append(row.city)

    dropdownChoices = [{
        "locationNames" : all_location_names,
        "shortNames" : all_short_names,
        "city" : all_cities,
        "latitudes" : all_latitudes,
        "longitudes" : all_longitudes
    }]

    print("--------------")

    for row in resultsDailyForecast:
        daily_responseNumbers.append(int(row.responseNumber))
        # Since the startDateTime is in GMT, we might not need it for the index.html. So commenting this line
        # daily_startDateTimes.append(row.startDateTime)
        daily_startDates.append(str(row.startDate))
        daily_startTimes.append(str(row.startTime))
        # Since the endDateTime is in GMT, we might not need it for the index.html. So commenting this line
        # daily_endDateTimes.append(row.endDateTime)
        daily_endDates.append(str(row.endDate))
        daily_endTimes.append(str(row.endTime))
        # Will we need isDaytime for any of the reporting?
        # daily_isDaytimes.append(row.isDaytime)
        daily_temperatures.append(str(row.temperature))
        # we have all units as F; do we have to send it as part of JSON
        daily_temperatureUnits.append(row.temperatureUnit)
        # temperatureTrend always seem to be None and also not used for visualization. So commenting this line
        # daily_temperatureTrends.append(row.temperatureTrend)
        daily_windSpeeds.append(row.windSpeed)
        daily_minWindSpeeds.append(str(row.minWindSpeed))
        daily_maxWindSpeeds.append(str(row.maxWindSpeed))
        daily_windSpeedUnits.append(row.windSpeedUnit)
        daily_windDirections.append(row.windDirection)
        daily_icons.append(row.icon)
        daily_shortForecasts.append(row.shortForecast)
        daily_detailedForecasts.append(row.detailedForecast)
        daily_retrievalDateTimes.append(row.retrievalDateTime)

    dailyForecastJson = [{
            "number" : daily_responseNumbers,
            # "startDateTime" : daily_startDateTimes,
            "startDate" : daily_startDates,
            "startTime" : daily_startTimes,
            # "endDateTime" : daily_endDateTimes,
            "endDate" : daily_endDates,
            "endTime" : daily_endTimes,
            # "isDayTime" : daily_isDaytimes,
            "temperature" : daily_temperatures,
            "temperatureUnit" : daily_temperatureUnits,
            # "temperatureTrend" : daily_temperatureTrends,
            "windSpeed" : daily_windSpeeds,
            "minimumWindSpeed" : daily_minWindSpeeds,
            "maximumWindSpeed" : daily_maxWindSpeeds,
            "windSpeedUnit" : daily_windSpeedUnits,
            "windDirection" : daily_windDirections,
            "icon" : daily_icons,
            "shortForecast" : daily_shortForecasts,
            "detailedForecast" : daily_detailedForecasts,
            "retrievalDateTime" : daily_retrievalDateTimes
    }]

    for row in resultsHourlyForecast:
        hourly_responseNumbers.append(int(row.responseNumber))
        # Since the startDateTime is in GMT, we might not need it for the index.html. So commenting this line
        # hourly_startDateTimes.append(row.startDateTime)
        hourly_startDates.append(str(row.startDate))
        hourly_startTimes.append(str(row.startTime))
        # Since the endDateTime is in GMT, we might not need it for the index.html. So commenting this line
        # hourly_endDateTimes.append(row.endDateTime)
        hourly_endDates.append(str(row.endDate))
        hourly_endTimes.append(str(row.endTime))
         # Will we need isDaytime for any of the reporting?
        # hourly_isDaytimes.append(row.isDaytime)
        hourly_temperatures.append(str(row.temperature))
        # # we have all units as F; do we have to send it as part of JSON
        hourly_temperatureUnits.append(row.temperatureUnit)
        # # temperatureTrend always seem to be None and also not used for visualization. So commenting this line
        hourly_temperatureTrends.append(row.temperatureTrend)
        hourly_windSpeeds.append(row.windSpeed)
        hourly_hourWindSpeeds.append(str(row.hourWindSpeed))
        hourly_windSpeedUnits.append(row.windSpeedUnit)
        hourly_windDirections.append(row.windDirection)
        hourly_icons.append(row.icon)
        hourly_shortForecasts.append(row.shortForecast)

    hourlyForecastJson = [{
            "number" : hourly_responseNumbers,
            # "startDateTime" : hourly_startDateTimes,
            "startDate" : hourly_startDates,
            "startTime" : hourly_startTimes,
            # "endDateTime" : hourly_endDateTimes,
            "endDate" : hourly_endDates,
            "endTime" : hourly_endTimes,
            # "isDayTime" : hourly_isDaytimes,
            "temperature" : hourly_temperatures,
            "temperatureUnit" : hourly_temperatureUnits,
            # "temperatureTrend" : hourly_temperatureTrends,
            "windSpeed" : hourly_windSpeeds,
            "hourWindSpeed" : hourly_hourWindSpeeds,
            "hourWindSpeedUnit" : hourly_windSpeedUnits,
            "windDirection" : daily_windDirections,
            "icon" : daily_icons,
            "shortForecast" : daily_shortForecasts
    }]

    dropdownChoices.append(dailyForecastJson)
    dropdownChoices.append(hourlyForecastJson)

    # print("--------------")
    # print(resultsLocations)
    # print("--------------")
    # print(dropdownChoices)
    print(dropdownChoices)

    return jsonify(dropdownChoices)
