import pandas as pd
import numpy as np
import requests as req
import json
import shutil
import os

"""
en_type = "JSON"
service_key = "LIIWzrgvlxdPCYxvuESJSwDhvcgpPNu8JxmBmmW70YHK7NroVZLfoI%2BW39rQ960XEp2dxvthJ9V5cuE3uJ%2FA7g%3D%3D"
base_url = f"http://apis.data.go.kr/B550624/fctryRegistPrdctnInfo/getFctryPrdctnService?serviceKey={service_key}&numOfRows=10&pageNo=1&cmpnyNm=삼성전자&type={en_type}"

print(base_url)

"rnAdres": "충청남도 아산시 배방읍 배방로 158",
"frstFctryRegistDe": "19941109",
"indutyNm": "메모리용 전자집적회로 제조업 외 1 종",
"""


def create_source():
    all_file = os.listdir("./fac_data")

    source = {
        "name": ["회사명"],
        "address": ["공장대표주소"],
        "type": ["업종명"],
        "product": ["생산품"]
    }

    df = pd.read_csv(f"./fac_data/{all_file[0]}", encoding="cp949")
    name = df[source["name"]]
    address = df[source["address"]]
    typerz = df[source["type"]]
    product = df[source["product"]]

    dfs = pd.concat([name, address, typerz, product], axis=1)

    for i in all_file[1:]:
        print(i)
        path = f"./fac_data/{i}"
        for_df = pd.read_csv(path, encoding="cp949")

        for_name = for_df[source["name"]]
        for_address = for_df[source["address"]]
        for_typerz = for_df[source["type"]]
        for_product = for_df[source["product"]]

        dfs2 = pd.concat([for_name, for_address, for_typerz, for_product], axis=1)
        dfs = pd.concat([dfs, dfs2])

    print(dfs)
    # dfs.to_csv("./박기범_낙동강주변공장정보.csv", index=False, encoding="ANSI")


newnew_df = pd.read_csv("./박기범_낙동강주변공장정보.csv", encoding="cp949")
newnew_df = newnew_df[newnew_df["address"].notna()]
# newnew_df.to_csv("./박기범_낙동강주변공장정보_exceptNA.csv", index=False, encoding="ANSI")


"""
df = pd.read_csv(f"./fac_data/{all_file[1]}", encoding="cp949")

name = df[source["name"]]
address = df[source["address"]]
typerz = df[source["type"]]

dfs2 = pd.concat([name, address, typerz], axis=1)
print(pd.concat([dfs,dfs2]))
"""
