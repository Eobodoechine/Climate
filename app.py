import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta 
from dateutil.relativedelta import *

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement=Base.classes.measurement
station=Base.classes.station

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
        f"/api/v1.0/id<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/prcp")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data including the date,prcp"""
    # Query measurement
    results = session.query(measurement.prcp,measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurement
    all_measurement = []
    for prcp,date in results:
        precipitation_dict = {}
        precipitation_dict["prcp"] = prcp
        precipitation_dict["date"] = date
        all_measurement.append(precipitation_dict)

    return jsonify(all_measurement)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    rdate=session.query(measurement.date,measurement.prcp).order_by(measurement.date.desc()).first()
    ydate=rdate.date
    dt = datetime.strptime(ydate, "%Y-%m-%d")
    oprior = dt - timedelta(days=365)
    oyear = oprior.strftime("%Y-%m-%d")
    tray=session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).all()
    trayz=session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).first()
    scnt=session.query(measurement.station,measurement.tobs,measurement.date).group_by(measurement.date).\
    filter_by(station=trayz.station).filter(measurement.date >= oyear).all()

# Convert list of tuples into normal list
    all_tobs = list(np.ravel(scnt))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def tobs(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    TMIN=session.query(func.min(measurement.tobs)).filter(measurement.date >= start).all()
    TAVG=session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    TMAX=session.query(func.max(measurement.tobs)).filter(measurement.date >= start).all()


    """Return a list of all passenger names"""
    # Query all passengers
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(TMIN,TAVG,TMAX))

    return jsonify(all_names)

if __name__ == '__main__':
    app.run(debug=True)
    
    
