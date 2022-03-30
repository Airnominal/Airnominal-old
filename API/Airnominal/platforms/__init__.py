from os import stat
from urllib import response
from flask import Blueprint, request, jsonify, make_response
from json import dumps
from schema import Optional, Or, Schema, SchemaError
from ..database import Measurement, Station, Sensor, MeasurementType
from ..utils import returnError
from secrets import token_urlsafe
from ..database import Session
from datetime import datetime
from dateutil import parser
import msgpack
class PlatformsHandler:
    def __init__(self):
        self.session =  Session()
        self.reg = Blueprint('platforms', __name__)
        self.registerRouts()
    def registerRouts(self):
        @self.reg.route("", methods = ['GET'])
        def getStations():
            l = []
            for s in self.session.query(Station).all():
                a = {
                    "id" : str(s.id),
                    "name" : s.name,
                    "sensors" : []
                }
                for sen in s.sensors:
                    a["sensors"].append({
                        "name": sen.modelname,
                        "mes_type": sen.MeasurementType.name,
                        "unit": sen.MeasurementType.unit
                    })
                l.append(a)
            response = make_response(
                jsonify(l
                ),
                200,
            )
            return response
        @self.reg.route("/new", methods = ['POST'])
        def registerNewStation():
            schema = Schema({
                "name": str,
                "sensors": [
                    {
                        "name": str,
                        "mes_type": str,
                    }
                ],
            }, ignore_extra_keys=True)
            try:
                con = schema.validate(request.json)
            except Exception as err:
                print(err)
                return returnError("schema not validated")
            key = token_urlsafe()
            station = Station(name = con["name"])
            station.set_password(key)
            s = []
            for i in con["sensors"]:
                m = self.session.query(MeasurementType).filter(MeasurementType.name == i["mes_type"]).all()
                if not m:
                    return returnError(i["mes_type"] + " measurement type does not exist")
                m = m[0]
                sensor = Sensor(modelname = i["name"])
                s.append(sensor)
                station.sensors.append(sensor)
                m.sensors.append(sensor)
            self.session.add(station)
            for i in s:
                self.session.add(i)
            self.session.commit()
            response = make_response(
                jsonify(
                    {
                        "success": True,
                        "config" : dumps(
                            {
                                "id": str(station.id),
                                "key": key,
                                "sensors" : [{"name": i.modelname, "id": i.id} for i in s]
                            }
                        )
                    }
                ),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        @self.reg.route("/measurement/type", methods = ['GET'])
        def getAlltypes():
            m = self.session.query(MeasurementType).all()
            response = make_response(
                jsonify(
                    [{"name": i.name, "unit": i.unit} for i in m]
                ),
                200,
            )
            return response
        @self.reg.route("/new/type", methods = ['POST'])
        def newMeasurementType():
            schema = Schema({
                "name": str,
                "unit": str
            })
            try:
                con = schema.validate(request.json)
            except Exception as err:
                print(err)
                return returnError("schema not validated")
            m = self.session.query(MeasurementType).filter(MeasurementType.name == con["name"]).all()
            print(m)
            if m:
                return returnError("already exists")
            m = MeasurementType(name=con["name"], unit=con["unit"])
            self.session.add(m)
            response = make_response(
                jsonify(
                    {
                        "success": True,
                    }
                ),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            self.session.commit()
            return response
        @self.reg.route("/new/mes", methods = ['POST'])
        def submitMeasurements():
            schema = Schema([{
                "id": str,
                "key": str,
                "sen": [
                    {
                        "sen_id": str,
                        "mes": [
                            {
                                "value": Or(int, float),
                                "lon": float,
                                "lat": float,
                                Optional("isoTime") : str,
                                Optional("unixTime") : int
                            }
                        ],
                    }
                ],
            }])

            if type(request.json) != list:
                j = [request.json]
            else:
                j = request.json
            try:
                print(request, j)
                con = schema.validate(j)
            except Exception as error:
                print(error)
                return returnError("First schema not validated")
            for stat in con:
                s = self.session.query(Station).filter(Station.id == int(stat["id"])).all()
                if not s:
                    return returnError("Station id " + stat["id"] + " does not exist")
                s = s[0]
                if not s.is_correct_password(stat["key"]):
                    return returnError("Wrong password")
                for sen in stat["sen"]:
                    se = self.session.query(Sensor).filter(Sensor.id == int(sen["sen_id"])).all()
                    if not sen:
                        return returnError("Sensor id " + sen["sen_id"] + " does not exist")
                    se = se[0]
                    for mes in sen["mes"]:
                        time = None
                        if "isoTime" in mes.keys():
                            try:
                                time = parser.parse(mes["isoTime"])
                            except:
                                return returnError(mes["isoTime"] + " is not valid iso format timestamp")
                        elif "unixTime" in mes.keys():
                            try:
                                time = datetime.utcfromtimestamp(mes["unixTime"])
                            except:
                                return returnError(mes["unixTime"] + " is not valid unix format timestamp")
                        else:
                            time = datetime.now()
                        m = Measurement(value = mes["value"], datetime=time, lon=mes["lon"], lat=mes["lat"])
                        self.session.add(m)
                        se.measurements.append(m)
            response = make_response(
                jsonify(
                    {
                        "success": True,
                    }
                ),
                200,
            )
            self.session.commit()
            response.headers["Content-Type"] = "application/json"
            return response
        @self.reg.route("/mes/msG", methods = ['POST'])
        def shortMSGPCKapi():
            schema = Schema([{
                "k": str, #key, po nove v base 64 da vzame manj placa
                "iST": str, # id Station, zapisano v base 64 da vzame manj placa
                "iSE": str, # id Senzorja, spet v base 64
                "v":  Or(int, float),# value, kjer postaja je
                "lat": Or(int, float), # latitude
                "lon" : Or(int, float), # longitude
            }])
            pckg = msgpack.unpackb(request.get_data(), raw=False)
            print(pckg)
            try:
                con = schema.validate(pckg)
            except Exception as error:
                print(error)
                return returnError("First schema not validated")
            for stat in con:
                try:
                    s = self.session.query(Station).filter(Station.id == int(stat["iST"])).all()
                    if not s:
                        return returnError("Station id " + stat["iST"] + " does not exist")
                    s = s[0]
                    if not s.is_correct_password(stat["k"]):
                        return returnError("Wrong password")
                    se = self.session.query(Sensor).filter(Sensor.id == int(stat["iSE"])).all()
                    if not se:
                        return returnError("Sensor id " + se["sen_id"] + " does not exist")
                    se = se[0]
                    time = None
                    '''
                    if "isoTime" in mes.keys():
                        try:
                            time = parser.parse(mes["isoTime"])
                        except:
                            return returnError(mes["isoTime"] + " is not valid iso format timestamp")
                    elif "unixTime" in mes.keys():
                        try:
                            time = datetime.utcfromtimestamp(mes["unixTime"])
                        except:
                            return returnError(mes["unixTime"] + " is not valid unix format timestamp")
                    else:
                    '''
                    time = datetime.now()
                    m = Measurement(value = stat["v"], datetime=time, lon=stat["lon"], lat=stat["lat"])
                    self.session.add(m)
                    se.measurements.append(m)
                except Exception as e:
                    print(e)
            response = make_response(
                jsonify(
                    {
                        "success": True,
                    }
                ),
                200,
            )
            self.session.commit()
            response.headers["Content-Type"] = "application/json"
            return response
        @self.reg.route("/ping")
        def ping():
            response = make_response("PONG", 200)
            response.headers["Content-Type"] = "plain/text"
            return response


















