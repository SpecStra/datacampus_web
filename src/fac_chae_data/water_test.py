import pandas as pd
import numpy as np
import requests as req
import json
import shutil
import os
from haversine import haversine, Unit

# 채수처리시설 주위에 공장이 몇개나 있는지 계산하는 코드입니다.

x_file = "gg_region.csv"
y_file = "fac_gold.csv"

fac_url = f"./{x_file}"
chae_url = f"./{y_file}"

fac_df = pd.read_csv(fac_url, encoding="cp949")
chae_df = pd.read_csv(chae_url, encoding="cp949")

# print(fac_df, chae_df)

"""
def return_latitude_m(lati):
    return round(lati / 111, 5)


def return_longitude_m(longi):
    return round(longi / 91.17, 5)

# print(fac_df.head()["Latitude"].apply(return_latitude))

for i in chae_df["Latitude"]:
    for j in fac_df["Latitude"][:50]:
        print(f"{return_latitude_m(round(i, 3) - round(j, 3))} km")
"""

limits_list = [3,5,7,10,15,20]

fac_lati = fac_df["Latitude"]
fac_longi = fac_df["Longitude"]
chae_lati = chae_df["Latitude"]
chae_longi = chae_df["Longitude"]

for i in range(0, len(fac_df)):
    mount_3 = []
    mount_5 = []
    mount_7 = []
    mount_10 = []
    mount_15 = []
    mount_20 = []

    current_fac_lati = fac_lati[i]
    current_fac_longi = fac_longi[i]
    fac = (current_fac_lati, current_fac_longi)

    for index, j in enumerate(range(0, len(chae_df))):
        current_chae_lati = chae_lati[j]
        current_chae_longi = chae_longi[j]
        chae = (current_chae_lati, current_chae_longi)

        result = round(haversine(fac, chae, unit=Unit.KILOMETERS), 5)
        new_obj = {
            "index": index,
            "KM": result
        }
        if result <= limits_list[0] :
            mount_3.append(new_obj)
        elif limits_list[0] < result <= limits_list[1] :
            mount_5.append(new_obj)
        elif limits_list[1] < result <= limits_list[2] :
            mount_7.append(new_obj)
        elif limits_list[2] < result <= limits_list[3] :
            mount_10.append(new_obj)
        elif limits_list[3] < result <= limits_list[4] :
            mount_10.append(new_obj)
        elif limits_list[4] < result <= limits_list[5] :
            mount_10.append(new_obj)

        #print(len(mount_3),len(mount_5),len(mount_10))

    output_3 = len(mount_3)
    output_5 = len(mount_3) + len(mount_5)
    output_7 = len(mount_3) + len(mount_5) + len(mount_7)
    output_10 = len(mount_3) + len(mount_5) + len(mount_7) + len(mount_10)
    output_15 = len(mount_3) + len(mount_5) + len(mount_7) + len(mount_10) + len(mount_15)
    output_20 = len(mount_3) + len(mount_5) + len(mount_7) + len(mount_10) + len(mount_15) + len(mount_20)

    # fac_df["fac_3"]
    # fac_df["fac_5"]
    # fac_df["fac_10"]

    fac_df.at[i, "fac_3"] = output_3
    fac_df.at[i, "fac_5"] = output_5
    fac_df.at[i, "fac_7"] = output_7
    fac_df.at[i, "fac_10"] = output_10
    fac_df.at[i, "fac_15"] = output_15
    fac_df.at[i, "fac_20"] = output_20


fac_df.to_csv(f"./{x_file}-{y_file}_distance_complete.csv", index=False, encoding="ANSI")