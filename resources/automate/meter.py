from flask import current_app
from flask_restful import Resource
import pymongo
from datetime import datetime,timedelta
import numpy as np

class stimulate(Resource):
    def get(self):
            try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect["testing"]
                selectCollection = selectDb["testing"]
                selectCollection2 = selectDb["users"]
                selectCollection3 = selectDb["production"]

                try:
                    ls = list(selectCollection2.find())
                    date = datetime(2021,1,1,0,0,0)
                    minutes_to_add = 60
                    d1 = datetime(2020, 5, 13, 18, 0, 0)
                    d2 = datetime(2020, 5, 13, 22, 0, 0)
                    d3 = datetime(2020, 5, 13, 9, 0, 0)
                    d4 = datetime(2020, 5, 13, 17, 0, 0)
                    datetime_new = date
                    while(datetime_new !=datetime(2021,1,2,0,0,0)):
                        datetime_new = datetime_new + timedelta(minutes=minutes_to_add)
                        for i in ls:
                            dic ={}
                            dic2 ={}
                            if i[:2] == "HD":
                                if datetime_new.time() > d1.time() and datetime_new.time() < d2.time() :
                                    rn = np.random.uniform(0.445,0.465)
                                else:
                                    rn = np.random.uniform(0.405,0.425)
                                dic = {
                                    "userid": i,
                                    "time": datetime_new,
                                    "consumption": rn
                                }
                                avd = selectCollection2.find_one({"_id": i})
                                h = datetime_new.hour
                                avg = avd[str(h)]
                                if avg is None:
                                    avd1=avd
                                    avd1[str(h)] = rn
                                    newvalues={"$set":avd1}
                                    selectCollection2.update_one(avd,newvalues)
                                else:
                                    avd1=avd
                                    avd1[str(h)] = (avd1[str(h)] + rn)/2
                                    newvalues={"$set":avd1}
                                    selectCollection2.update_one(avd,newvalues)
                            elif i[:2]=="HS":
                                if datetime_new.time() > d1.time() and datetime_new.time() < d2.time() :
                                    rn = np.random.uniform(0.145,0.165)
                                else:
                                    rn = np.random.uniform(0.105,0.125)
                                pr = np.random.uniform(0.400,0.450)
                                dic = {
                                    "userid": i,
                                    "time": datetime_new,
                                    "consumption": rn,
                                }
                                dic2 = {
                                    "userid": i,
                                    "time": datetime_new,
                                    "production": pr
                                }
                            elif i[:2]=="CB":
                                if datetime_new.time() > d3.time() and datetime_new.time() < d4.time():
                                    dic = {
                                        "userid": i,
                                        "time": datetime_new,
                                        "consumption": 16.67,
                                    }
                            elif i[:2]=="HP":
                                dic = {
                                    "userid": i,
                                    "time": datetime_new,
                                    "consumption": 31.25,
                                }
                            elif i[:2]=="MY":
                                if datetime_new.time() > d3.time() and datetime_new.time() < d4.time():
                                    mac = selectCollection.find_one({"_id": i})
                                    if mac and mac["consumption"]!=0:
                                        rn = mac["consumption"]+(mac["consumption"]*0.30)
                                    else:
                                        rn = 0.3
                                else:
                                    rn =0

                                dic = {
                                        "userid": i,
                                        "time": datetime_new,
                                        "consumption": rn
                                    }
                            try:
                                selectCollection.insert_one(dic)
                                if dic2 !={}:
                                    selectCollection3.insert_one(dic2)
                            except Exception as e:
                                return {"code": 213, "message": "data Not inserted : " + str(e)},213
                except Exception as e:
                    return {"code": 211, "message": "Not found or bad request : " + str(e)},211

            except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210
