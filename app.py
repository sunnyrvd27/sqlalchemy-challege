# Import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt


# Import flask
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

# creating an app
app = Flask(__name__)

# defining the home page
@app.route("/")
def index():
    print("Index")
    return (
        f"Welcome to the Index!<br/>"
        f"Available routes are as follows<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date ==> 'Start Date is user specified in YYYY-MM-DD format'<br/>"
        f"/api/v1.0/start-date/end-date ==>'Start Date & End Date is user specified in YYYY-MM-DD format'<br/>"
    )

# Return a JSON list of stations from the dataset. (/api/v1.0/stations)
@app.route("/api/v1.0/precipitation")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    date_one_year = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query all passengers
    results = session.query(Measurement.date, func.round(func.avg(Measurement.prcp),2)).filter(Measurement.date >= date_one_year).group_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

# Return a JSON list of stations from the dataset. (/api/v1.0/stations)
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Return a JSON list of temperature observations (TOBS) for the previous year for station USC00519281 (/api/v1.0/tobs)
@app.route("/api/v1.0/tobs")
def temperatures():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    all_temperatures = list(np.ravel(results))

    return jsonify(all_temperatures)

@app.route("/api/v1.0/<start>")
def Start(start):

    session = Session(engine)
  
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()  

    session.close() 

    startdate = list(np.ravel(result))

    return jsonify(startdate)

@app.route("/api/v1.0/<start>/<end>")
def StartEnd(start,end):

    session = Session(engine)
  
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)). \
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()  

    session.close() 

    startdate = list(np.ravel(result))

    return jsonify(startdate)

if __name__ =="__main__":
    app.run(debug=True)