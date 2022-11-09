import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Get date 12 months ago
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    
    # Query the date and precipitations for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date > query_date).\
            order_by(Measurement.date).all()

    session.close()

    # Create a dictionary where the date is the key and the precipitation is the value. 
    # Jasonify the results. 
    prcp_dict = {}
    for date, prcp in results:
        prcp_dict[date] = prcp

    return jsonify(prcp_dict)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the number of rows for each station
    station_count = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()

    session.close()
    
    # Create a dictionary where the station is the key and the number of rows is the value. 
    # Jasonify the results. 
    station_dict = {}
    for station, count in station_count:
       station_dict[station] = count

    return jsonify(station_dict)



@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Get date 12 months ago
    query_date = dt.date(2017, 8, 18) - dt.timedelta(days = 365)

    # Query the date and temperature for specified station over the last 12 months
    station_temp = session.query(Measurement.date, Measurement.tobs).\
            where(Measurement.station == "USC00519281").\
            filter(Measurement.date > query_date).\
            order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary where the date is the key and the temperature is the value. 
    # Jasonify the results. 
    temp_dict = {}
    for date, temp in station_temp:
        temp_dict[date] = temp

    return jsonify(temp_dict)





# @app.route("/api/v1.0/<start>")
# def start():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     start = dt.date(<start>)

#     station_stats = session.query(Measurement.station, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#             where(Measurement.station == "USC00519281").all().\
#             filter(Measurement.date >= start)

#     session.close()

#     start_dict = { }
#     for station, min, avg, max in station_stats:
#         start_dict["Station"] = station
#         start_dict["Min Temp"] = min
#         start_dict["Avg Temp"] = avg
#         start_dict["Max Temp"] = max

#     return jsonify(start_dict)
 



# @app.route("/api/v1.0/<start>/<end>")
# def start_end():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     start = dt.date(<start>)
#     end = dt.date(<end>)

#     station_stats = session.query(Measurement.station, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#             where(Measurement.station == "USC00519281").all().\
#             filter(Measurement.date >= start).\
#             filter(Measurement.date <= end)

#     session.close()

#     start_end_dict = { }
#     for station, min, avg, max in station_stats:
#         start_end_dict["Station"] = station
#         start_end_dict["Min Temp"] = min
#         start_end_dict["Avg Temp"] = avg
#         start_end_dict["Max Temp"] = max

#     return jsonify(start_end_dict)


if __name__ == '__main__':
    app.run(debug=True)
