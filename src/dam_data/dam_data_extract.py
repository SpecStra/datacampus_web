import pandas as pd
import numpy as np
import requests as req
import json
import shutil
import os
import xmltodict

service_key = "LIIWzrgvlxdPCYxvuESJSwDhvcgpPNu8JxmBmmW70YHK7NroVZLfoI%2BW39rQ960XEp2dxvthJ9V5cuE3uJ%2FA7g%3D%3D"


# base_url = f"http://opendata.kwater.or.kr/openapi-data/service/pubd/dam/sluicePresentCondition/de/list?" \
#            f"type=JSON&damcode={dam_code}&stdt=2016-01-01&eddt=2022-06-30&numOfRows=30&pageNo=1&ServiceKey={service_key}"

"""

for i in epoch :
    base_url = f"http://opendata.kwater.or.kr/openapi-data/service/pubd/dam/sluicePresentCondition/de/list?" \
               f"type=JSON&damcode={dam_code}&stdt=2016-01-01&eddt=2022-06-30&numOfRows=30&pageNo={i}&ServiceKey={service_key}"

    print(base_url)
    r = req.get(base_url)
    print(r.text)
    print(json.dumps(xmltodict.parse(r.text), indent=4))
"""

dam_code = [
    {
        "name" : "영천댐",
        "code" : "2012210"
    },
    {
        "name" : "운문댐",
        "code" : "2021210"
    },
    {
        "name" : "밀양댐",
        "code" : "2021110"
    },
    {
        "name" : "합천댐",
        "code" : "2015110"
    },
    {
        "name" : "남강댐",
        "code" : "2018110"
    },
    {
        "name" : "평화의댐",
        "code" : "1009710"
    },
    {
        "name" : "화천댐",
        "code" : "1010310"
    },
    {
        "name" : "춘천댐",
        "code" : "1010320"
    },
    {
        "name" : "소양강댐",
        "code" : "1012110"
    },
    {
        "name" : "의암댐",
        "code" : "1013310"
    },
    {
        "name" : "청평댐",
        "code" : "1015310"
    },
    {
        "name" : "횡성댐",
        "code" : "1006110"
    },
    {
        "name" : "팔당댐",
        "code" : "1017310"
    },
    {
        "name" : "충주댐",
        "code" : "1003110"
    },
    {
        "name" : "괴산댐",
        "code" : "1004310"
    },
]


epoch = range(1, 79)
for c in dam_code :
    name = c["name"]
    code = c["code"]

    obsryymtde = []
    inflowqy = []
    lowlevel = []
    prcptqy = []
    rsvwtqy = []
    rsvwtrt = []
    totdcwtrqy = []

    for i in epoch :
        base_url = f"http://opendata.kwater.or.kr/openapi-data/service/pubd/dam/sluicePresentCondition/de/list?" \
                   f"type=JSON&damcode={code}&stdt=2016-01-01&eddt=2022-06-30&numOfRows=30&pageNo={i}&ServiceKey={service_key}"

        print(base_url)
        r = req.get(base_url)
        # print(r.text)
        output = json.loads(json.dumps(xmltodict.parse(r.text), indent=4))


        # print(output, type(output))
        # print(output["response"]["body"]["items"]["item"])

        for j in output["response"]["body"]["items"]["item"] :
            obsryymtde.append(j["obsryymtde"])
            try:
                inflowqy.append(j["inflowqy"])
            except KeyError:
                print("inflowqy error, pass")
                inflowqy.append(np.nan)

            try:
                lowlevel.append(j["lowlevel"])
            except KeyError:
                print("lowlevel error, pass")
                lowlevel.append(np.nan)

            try:
                prcptqy.append(j["prcptqy"])
            except KeyError:
                print("prcptqy error, pass")
                prcptqy.append(np.nan)

            try :
                rsvwtqy.append(j["rsvwtqy"])
            except KeyError :
                print("rsvwtqy error, pass")
                rsvwtqy.append(np.nan)

            try :
                rsvwtrt.append(j["rsvwtrt"])
            except KeyError :
                print("rsvwtrt error, pass")
                rsvwtrt.append(np.nan)

            try :
                totdcwtrqy.append(j["totdcwtrqy"])
            except KeyError :
                print("totdcwtrqy error, pass")
                totdcwtrqy.append(np.nan)

        df = pd.DataFrame(data={
            "obsryymtde" : obsryymtde,
            "inflowqy" : inflowqy,
            "lowlevel" : lowlevel,
            "prcptqy" : prcptqy,
            "rsvwtqy" : rsvwtqy,
            "rsvwtrt" : rsvwtrt,
            "totdcwtrqy" : totdcwtrqy
        })

        df.to_csv(f"./{name}_{code}_data.csv", encoding="ANSI", index=False)