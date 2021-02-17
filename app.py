# import stuff
from flask import Flask, jsonify
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# flask setup
app = Flask(__name__)

# flask routes
# home listing all possible routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate APP API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[input start_date format without brackets:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[input start_date format:yyyy-mm-dd without brackets]/[input end_date format:yyyy-mm-dd]<br/>"
    )
# convert query results to a dictionary using date and prcp as value
# return JSON representation of dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session link
    session = Session(engine)

    # query precipitation data
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").\
    filter(measurement.date <= "2017-08-23").all()

    # close session
    session.close()

    # convert query data to a dictionary
    precip = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        precip.append(prcp_dict)

    """Return data as json"""
    return jsonify(precip)


# return JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def station_list():

    # create session link
    session = Session(engine)

    # query station data
    active_stations = session.query(station.name).all()

    # close session
    session.close()

     # Convert list of tuples into normal list
    all_stations = list(np.ravel(active_stations))

    return jsonify(all_stations)


# query dates and temps of most active station for last year of data (determined from prev analysis to be 'USC00519281')
# return JSON list of tobs for the previous year
@app.route("/api/v1.0/tobs")
def tobs():

    # create session link
    session = Session(engine)

    """Return a tob list for last year of data for USCO519281"""
    # query tobs from most active station in last year
    max_station_tobs = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USCO519281').\
    filter(measurement.date >= "2016-08-23").filter(measurement.date <= "2017-08-23").all()

    # close the session
    session.close()
   
    # convert the list to a dictionary
    max_tobs = []
    for date,tobs in max_station_tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        max_tobs.append(tobs_dict)

    return jsonify(max_tobs)

# return a JSON list of min, avg, max temp for given start or end range
# for just a start date (start_date as input)
@app.route("/api/v1.0/<start_date>")
def start(start_date):

    # create session link
    session = Session(engine)

    """Get min, avg, max temp for given start date."""
    # query the data
    info = session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()

    # close the session
    session.close()
            
       # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs = []
    for min, avg, max in info:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)
               
    
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
 
    # create session link
    session = Session(engine)

    """Get min, avg, max temp for given start and end dates."""
    # query the data
    info = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    # close the session
    session.close()
    
    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_end_date_tobs = []
    for min, avg, max in info:
        start_end_date_tobs_dict = {}
        start_end_date_tobs_dict["min_temp"] = min
        start_end_date_tobs_dict["avg_temp"] = avg
        start_end_date_tobs_dict["max_temp"] = max
        start_end_date_tobs.append(start_end_date_tobs_dict) 
    return jsonify(start_end_date_tobs)
               
# debug
if __name__ == "__main__":
    app.run(debug=True)