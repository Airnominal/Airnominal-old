import json
from os import stat
import sched
from flask import Blueprint, request, jsonify, make_response, Response
from schema import Optional, Or, Schema, SchemaError
from sqlalchemy import func

from ..database import Measurement, Station, Sensor, MeasurementType
from ..utils import returnError
from secrets import token_hex
from ..database import Session
from datetime import datetime
from dateutil import parser
import ujson
import hashlib

class DisplayHandler:
    def __init__(self):
        self.session =  Session()
        self.reg = Blueprint('display', __name__)
        self.registerRouts()

    def handleRequest(self, only_latest=False):
        all_args = request.args.to_dict()
        schema = Schema({
            Optional("platform"): str,
            Optional("measurements"): str,
            Optional("from"): str,
            Optional("to"): str
        }, ignore_extra_keys=True)
        try:
            con = schema.validate(all_args)
        except Exception as err:
            print(err)
            return returnError("Schema not validated")
        
        if only_latest:
            mes = self.session.query(Measurement, func.max(Measurement.datetime)).group_by(Measurement.sensor_id)
        else:
            mes = self.session.query(Measurement)
        #proccess Stations
        if "platform" in con.keys():
            con["platform"] = [int(x) for x in con["platform"].split(",")]
            for i in con["platform"]:
                if not self.session.query(Station).filter(Station.id == i).all():
                    return returnError("Platform with ID " + str(i) + " does not exist")
            mes = mes.join(Sensor).join(Station).filter(Station.id.in_(con["platform"]))
        #proccess MesaurementType
        if "measurements" in con.keys():
            con["measurements"] = con["measurements"].split(",")
            for i in con["measurements"]:
                if not self.session.query(MeasurementType).filter(MeasurementType.name == i).all():
                    return returnError("No measurement type of " + str(i))
                mes = mes.join(MeasurementType).filter(MeasurementType.name.in_(con["measurements"]))
        #proccess DateTime
        try:
            if "from" in con.keys():
                con["from"] = parser.parse(con["from"])
                mes = mes.filter(Measurement.datetime >= con["from"])
            if "to" in con.keys():
                con["to"] = parser.parse(con["to"])
                mes = mes.filter(Measurement.datetime <= con["to"])
        except Exception as err:
            print(err)
            return returnError("date format not correct")
        l = []
        
        for m in mes.all():
            if only_latest:
                m = m[0]
            a = {
                "timestamp": m.datetime.isoformat(),
                "platform": m.Sensor.station_id,
                "coordinates": [m.lat, m.lon],
                "data": {
                    "name": m.Sensor.MeasurementType.name,
                    "unit": m.Sensor.MeasurementType.unit,
                    "value": m.value
                },
                "hash": str(m.id)
            }
            l.append(a)
        response = Response(
            response=ujson.dumps(l),
            status=200,
            mimetype='application/json'
        )
        return response

    def registerRouts(self):
        @self.reg.route("/measurements", methods = ['GET'])
        def historical_measurements():
            return self.handleRequest()

        @self.reg.route("/measurements/latest", methods = ['GET'])
        def latest_measurements():
            return self.handleRequest(only_latest=True)
