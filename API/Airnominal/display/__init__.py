import json
from os import stat
import sched
from flask import Blueprint, request, jsonify, make_response
from schema import Optional, Or, Schema, SchemaError
from ..database import Measurement, Station, Sensor, MeasurementType
from ..utils import returnError
from secrets import token_hex
from ..database import Session
from datetime import datetime
from dateutil import parser
import hashlib

class DisplayHandler:
    def __init__(self):
        self.session =  Session()
        self.reg = Blueprint('display', __name__)
        self.registerRouts()
    def registerRouts(self):
        @self.reg.route("/measurements", methods = ['GET'])
        def graphAccess():
            all_args = request.args.to_dict()
            schema = Schema({
               Optional("platform"): str,
               "measurements": str,
               Optional("from"): str,
               Optional("to"): str
            })
            sen = self.session.query(Sensor)
            try:
                con = schema.validate(all_args)
            except:
                return returnError("Schema not validated")
            #proccess Stations
            if "platform" in con.keys():
                con["platform"] = [int(x) for x in con["platform"].split(",")]
                for i in con["platform"]:
                    if not self.session.query(Station).filter(Station.id == i).all():
                        return returnError("No measurement type of " + i)
                sen = sen.join(Station).filter(Station.id.in_(con["platform"]))
            #proccess MesaurementType
            con["measurements"] = con["measurements"].split(",")
            for i in con["measurements"]:
                if not self.session.query(MeasurementType).filter(MeasurementType.name == i).all():
                    return returnError("No measurement type of " + i)
                sen = sen.join(MeasurementType).filter(MeasurementType.name.in_(con["measurements"]))
            #proccess DateTime
            print(sen.all())
            mes = self.session.query(Measurement).filter(Measurement.sensor_id.in_([s.id for s in sen.all()]))
            try:
                if "from" in con.keys():
                    con["from"] = parser.parse(con["from"])
                    mes = mes.filter(Measurement.datetime >= con["from"])
                if "to" in con.keys():
                    con["to"] = parser.parse(con["to"])
                    mes = mes.filter(Measurement.datetime <= con["to"])
            except:
                return returnError("date format not correct")
            l = []
            for m in mes.all():
                a = {
                    "timestamp": m.datetime.isoformat(),
                    "platform": m.sensor_id,
                    "coordinates": [m.lat, m.lon],
                    "measurements": [{
                        m.Sensor.MeasurementType.name: {
                            "value" : m.value,
                            "unit": m.Sensor.MeasurementType.unit
                        }
                    }]
                }
                a["hash"] = hashlib.sha256(json.dumps(a).encode("utf-8")).hexdigest()
                l.append(a)
            response = make_response(
                jsonify(l),
                200,
            )
            return response

            
