import numpy as np

import matplotlib
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


Base.classes.keys()
engine.execute('SELECT * FROM station LIMIT 5').fetchall()
engine.execute('SELECT * FROM measurement LIMIT 5').fetchall()

# Save reference to the table
stat = Base.classes.station
meas = Base.classes.measurement

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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/measurements"
    )


@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results = session.query(stat.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/measurements")
def measurments():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data including the station, prcp, tobs"""
    # Query all measurements
    results = session.query(meas.station, meas.date, meas.prcp, meas.tobs).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_measures = []
    for station, date, prcp, tobs in results:
        meas_dict = {}
        meas_dict["station"] = station
        meas_dict["date"] = date
        meas_dict["prcp"] = prcp
        meas_dict["tobs"] = tobs
        all_measures.append(meas_dict)

    return jsonify(all_measures)

lstdates=['09-26','09-27','09-28','09-29','09-30']

@app.route("/api/v1.0/dailynorms")
def daily_normals():
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    session = Session(engine)
    
    
    lstdaynorm=[]
    my_dict = {}
    for i in lstdates:
        sel = [func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)]
    
        dn=session.query(*sel).filter(func.strftime("%m-%d", meas.date) == i).all()
        lstdaynorm.append(dn)
        my_dict[i] = list(dn[0][0:]) # extract elements of tuple excluding date from list and convert it to list

    session.close()
    return jsonify(my_dict)

if __name__ == '__main__':
    app.run(debug=True)
