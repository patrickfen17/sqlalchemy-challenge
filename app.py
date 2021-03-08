import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/[start_date] as yyyy-mm-dd<br/>"
        f"/api/v1.0/[start_date]/[end_date] as yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query measurements for precipitation data
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Convert the query results to a dictionary
    precipt_scores = list(np.ravel(results))

    return jsonify(precipt_scores)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(station.station).all()

    session.close()

    # Turn query results into a list of stations
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(measurement.date, measurement.tobs, measurement.prcp).\
        filter(measurement.date >= "2016-08-23").\
        filter(measurement.station == "USC00519281").\
        order_by(measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temps
    all_temps = []
    for date, tobs, prcp in results:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Temp"] = tobs
        temp_dict["Prcp"] = prcp
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # When given the start date only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
              filter(measurement.date >= start_date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    start_temps = []
    for min, avg, max in results:
        start_temps_dict = {}
        start_temps_dict["Min Temp"] = min
        start_temps_dict["Avg Temp"] = avg
        start_temps_dict["Max Temp"] = max
        start_temps.append(start_temps_dict)

    return jsonify(start_temps)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # When given the start and end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
              filter(measurement.date >= start_date).\
              filter(measurement.date <= end_date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    start_end_temps = []
    for min, avg, max in results:
        start_end_temps_dict = {}
        start_end_temps_dict["Min Temp"] = min
        start_end_temps_dict["Avg Temp"] = avg
        start_end_temps_dict["Max Temp"] = max
        start_end_temps.append(start_end_temps_dict)

    return jsonify(start_end_temps)

    session.close()

if __name__ == '__main__':
    app.run(debug=True)
