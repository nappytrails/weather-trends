import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template, jsonify, request, redirect


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/titanic.sqlite")

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


@app.route("/names")
def locationNames():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns the list of choices for dropdown"""
    # Query to fetch the list of location names
    results = session.query(ContentChoice.locationName, ContentChoice.shortName, 
                            ContentChoice.latitude, ContentChoice.longitude).all()

    session.close()

    # Convert list of tuples into normal list
    all_location_names = [locationName[0] for locationName in results]
    all_short_names = [shortName[0] for shortName in results]
    all_latitudes = [latitude[0] for latitude in results]
    all_longitudes = [longitude[0] for longitude in results]

    dropdownChoices = [{
        "locationNames" : all_location_names,
        "shortNames" : all_short_names,
        "latitudes" : all_latitudes,
        "longitudes" : all_longitudes
    }]

    return jsonify(dropdownChoices)


# @app.route("/api/pals")
# def pals():
#     results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()

#     hover_text = [result[0] for result in results]
#     lat = [result[1] for result in results]
#     lon = [result[2] for result in results]

#     pet_data = [{
#         "type": "scattergeo",
#         "locationmode": "USA-states",
#         "lat": lat,
#         "lon": lon,
#         "text": hover_text,
#         "hoverinfo": "text",
#         "marker": {
#             "size": 50,
#             "line": {
#                 "color": "rgb(8,8,8)",
#                 "width": 1
#             },
#         }
#     }]

#     return jsonify(pet_data)


if __name__ == '__main__':
    app.run(debug=True)
