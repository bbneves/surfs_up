# Importing dependencies to work with the dataset.
import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask dependency
from flask import Flask, jsonify

# Setting up SQLA: Engine, Automap Schema, Table reflection and table references for each class.
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Setting up FLASK

app = Flask(__name__)

# Welcome route showing: precipitation, stations, temperatures observed, stats for specific dates.
@app.route("/")

def welcome():
    
    return( '''
    Welcome to the Climate Analysis API! \n
    Available Routes: \n
    /api/v1.0/precipitation \n
    /api/v1.0/stations \n
    /api/v1.0/tobs \n
    /api/v1.0/temp/start/end \n
    ''')

# Precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
        
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

#Stations route
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Temperatures observed route
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Temp Stats for specific dates, e.g.: /api/v1.0/temp/2017-06-01/2017-06-30
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    
    return jsonify(temps)