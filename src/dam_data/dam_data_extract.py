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
        "name" : "백제보",
        "code" : "3012602"
    },
    {
        "name" : "세종보",
        "code" : "3010601"
    },
    {
        "name" : "공주보",
        "code" : "3012601"
    }
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

        df.to_csv(f"./download/{name}_{code}_data.csv", encoding="ANSI", index=False)