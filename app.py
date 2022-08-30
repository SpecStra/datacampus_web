import random
from flask import Flask, render_template, request, redirect, session
import json
import folium
import pandas as pd
import hashlib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import datetime
import requests as req
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "mykey"
tile_option = "stamenterrain"

han_river_bo_url = "./resource/moduel_yet.csv"
han_region_json_url = "./resource/han_region_label.json"
with open(han_region_json_url, encoding="utf8") as f:
    han_region_json = json.load(f)

# news crwal module
crawl_url = "https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query=녹조"
r = req.get(crawl_url)
soup = BeautifulSoup(r.text, 'html.parser')
found = soup.select_one("#main_pack > section > div > div.group_news > ul").findAll("a", {"class": "news_tit"})
news_link = []
news_tilte = []
for i in found:
    news_link.append(i["href"])
    news_tilte.append(i["title"])

# 오염도 obj
infect_limit_list = [
    {
        "limit_value": 0,
        "color": "blue",
        "opacity": 0.7,
        "status" : "Clean"
    },
    {
        "limit_value": 1000,
        "color": "green",
        "opacity": 0.8,
        "status" : "Moderate"
    },
    {
        "limit_value": 10000,
        "color": "darkgreen",
        "opacity": 0.9,
        "status" : "Considerable"
    },
    {
        "limit_value": 1000000,
        "color": "red",
        "opacity": 1,
        "status" : "High"
    },
]


def cells_return_obj(cells) :
    round_cells = round(cells, 0)
    if infect_limit_list[0]["limit_value"] <= round_cells < infect_limit_list[1]["limit_value"] :
        print("situ 1")
        return infect_limit_list[0]
    elif infect_limit_list[1]["limit_value"] <= round_cells < infect_limit_list[2]["limit_value"] :
        print("situ 2")
        return infect_limit_list[1]
    elif infect_limit_list[2]["limit_value"] <= round_cells < infect_limit_list[3]["limit_value"] :
        print("situ 3")
        return infect_limit_list[2]

# randomForest model
def input_model(region, date):
    df = pd.read_csv(han_river_bo_url, encoding="cp949")
    input_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    latest_dates = df[df["region"] == 0].sort_values("date", ascending=False).head(1)
    latest_date = df[df["region"] == 0].sort_values("date", ascending=False).head(1)["date"].values[0]
    latest_date_datetype = datetime.datetime.strptime(latest_date, '%Y-%m-%d')
    print(input_date, latest_date_datetype)
    if input_date >= latest_date_datetype:  # 미래예측
        print(f"sequence 미래예측")
        list1 = []
        for i in latest_dates.columns[5:-1]:
            a = latest_dates[i].values[0]
            list1.append(a)
        season = (int(input_date.month) - 1) // 3
        input_data = [region, input_date.year, input_date.month, season]
        for i in list1:
            input_data.append(i)

    elif input_date < latest_date_datetype:  # 과거예측
        print(f"sequence 과거예측")
        original_data = df[(df["region"] == region) & (df["date"] == date)]
        list1 = []
        for i in original_data.columns[5:-1]:
            a = original_data[i].values[0]
            list1.append(a)
        season = (int(input_date.month) - 1) // 3
        input_data = [region, input_date.year, input_date.month, season]
        for i in list1:
            input_data.append(i)
    return input_data


def model(input_data):
    df = pd.read_csv(han_river_bo_url, encoding="cp949")
    X = df.drop(["date", "log_cells"], axis=1)
    y = df[['log_cells']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=19)  # 20%만 테스트데이터로
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # 예측
    input_data = np.array(input_data)
    y_pred = model.predict(input_data.reshape(1, -1))
    real_cell = np.expm1(y_pred)

    return real_cell

"""
def input_model(region, date):
    df = pd.read_csv(han_river_bo_url, encoding="cp949")
    input_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    latest_dates = df[df["region"] == 0].sort_values("date", ascending=False).head(1)
    latest_date = df[df["region"] == 0].sort_values("date", ascending=False).head(1)["date"].values[0]
    latest_date_datetype = datetime.datetime.strptime(latest_date, '%Y-%m-%d')
    if input_date >= latest_date_datetype:
        list1 = []
        for i in latest_dates.columns[5:]:
            a = latest_dates[i].values[0]
            list1.append(a)
        season = (int(input_date.month) - 1) // 3
        input_data = [region, date, input_date.year, input_date.month, season]
        for i in list1:
            input_data.append(i)
    elif input_date < latest_date_datetype:
        original_data = df[(df["region"] == region) & (df["date"] == date)]
        if len(original_data) == 0:
            input_data = 0
        else:
            list1 = []
            for i in original_data.columns[5:]:
                a = original_data[i].values[0]
                list1.append(a)
            season = (int(input_date.month) - 1) // 3
            input_data = [region, date, input_date.year, input_date.month, season]
            for i in list1:
                input_data.append(i)

    return input_data

def model(input_data):
    df = pd.read_csv("final_data_08_26.csv")
    le = LabelEncoder()
    df["date"] = le.fit_transform(df["date"])
    X = df.drop(["log_cells"], axis=1)
    y = df[['log_cells']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=19)

    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    model = RandomForestRegressor(random_state=19, n_estimators=100)
    model.fit(X_train, y_train)
    # 예측
    input_data = X.iloc[-1, :]
    input_data = np.array(input_data)
    y_pred = model.predict(input_data.reshape(1, -1))
    real_cell = np.expm1(y_pred)[0]

    return real_cell
"""
def use_model_return_cells(region, date):
    return model(input_model(region, date))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # export form data as form_data
        form_data = json.dumps(request.form)

        # send to session -> data -> inputName
        session["data"] = form_data

        # after redirected, session still go on
        return redirect("./test")
    else:
        return render_template("content.html", title="Home", news_tilte=news_tilte, news_link=news_link)


@app.route("/search", methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        today = str(datetime.datetime.today()).split(" ")[0]
        corr_json_url = "./src/folium_complex/resource/han_region_corr.json"
        with open(corr_json_url, encoding="utf8") as f:
            corr_dict = json.load(f)
        regions = []
        for i in corr_dict:
            regions.append(i["region"])

        return render_template("search.html", title="Search", today=today, regions=regions)
    else:
        session["search_date"] = request.form.get("date")
        session["search_region"] = request.form.get("region")
        # print(search_date, search_region)
        return redirect("/map")


@app.route("/data")
def datas(source=None):
    # folium 객체에 쓸 변수 선언
    # seoul_corr = source["corr"]
    buStation_corr = [37.48662382, 126.723325411]
    tile_option = "stamenterrain"
    ex_popup = "<i>Bupyeong Station<br>Hello</i>"
    ex_tooltip = "Hello, Station!"

    # folium 객체 생성
    foli_map = folium.Map(location=buStation_corr, zoom_start=15, tiles=tile_option)
    folium.Marker(buStation_corr, popup=ex_popup, tooltip=ex_tooltip,
                  icon=folium.Icon(color="red", icon="fire")).add_to(foli_map)
    foli_map.save("./templates/temp/map.html")

    # return foli_map._repr_html_()
    return render_template("./foli_test.html", title="Data")


@app.route("/map")
def map():
    soc = request.args.get("source")
    # han_corr = [37.422889, 127.281111]
    corr_json_url = "./src/folium_complex/resource/han_region_corr.json"
    with open(corr_json_url, encoding="utf8") as f:
        corr_dict = json.load(f)
    print(soc)

    if soc:
        if soc == "han":
            corr = [37.422889, 127.281111]
            wise_df_url = "./src/folium_complex/resource/han_wise_tested.csv"

        # print(corr_dict)
        wise_df = pd.read_csv(wise_df_url, encoding="cp949")

        foli_map = folium.Map(location=corr, zoom_start=11, tiles=tile_option)

        # print(corr_df.head())
        # 분석 데이터가 바뀔 경우 아래 슬라이싱 수정 필요.
        for i in wise_df.columns[9:26]:
            corr_name = i.split("＿")[1]
            corr_obj = list(filter(lambda x: x["region"] == corr_name, corr_dict))[0]
            corr = [corr_obj["latitude"], corr_obj["longitude"]]
            # print(corr_obj)
            rand_pick = infect_limit_list[random.randrange(0, 4)]
            rand_pick_status = rand_pick["status"]
            rand_cells = random.randrange(500, 1500)
            rand_pick_color = rand_pick["color"]
            ex_popup = f"<i>{corr_name}</i>"
            ex_tooltip = f"{corr_name} <br> 현재상태 : {rand_pick_status} <br> 유해남조류 수 : <p style=\"color: {rand_pick_color}\">{rand_cells*10}<p>"
            folium.Circle(tuple(corr), popup=ex_popup, tooltip=ex_tooltip, radius=rand_cells,
                          color=rand_pick_color, fill="darkgreen").add_to(foli_map)

            # print(wise_df[f"region_{corr_name}"] == 1)
            # print(wise_df[wise_df[i] == 1])

        foli_map.save("./templates/temp/han_map.html")

        return render_template("./foli_test.html", map_url="temp/han_map.html", title="Map")
    else:
        search_date = session.get("search_date")
        search_region = session.get("search_region")
        search_region_obj = list(filter(lambda x: x["region"] == search_region, han_region_json))[0]
        search_label = search_region_obj["label"]
        cells = model(input_model(search_label, search_date))
        search_obj = list(filter(lambda x: x["region"] == search_region, corr_dict))[0]
        search_corr = [search_obj["latitude"], search_obj["longitude"]]
        # 상태 설정 필요
        search_status = "Normal"

        # print(f"cells : {cells[0]}")
        limit_obj = cells_return_obj(cells[0])
        # print(limit_obj)

        # 날짜, 지역과 일치하는 y_predict값을 도출
        foli_map = folium.Map(location=search_corr, zoom_start=13, tiles=tile_option)
        search_popup = f""
        search_tooltip = f"유해남조류 수 : {round(cells[0], 0)} \n 상태 : {search_status}"
        folium.Circle(tuple(search_corr), radius=round(cells[0]/10), color=limit_obj["color"],
                      popup=search_popup, tooltip=search_tooltip,
                      fill="darkgreen").add_to(foli_map)
        hashed_filename = hashlib.sha256(f"{search_date}_{search_region}".encode("utf-8")).hexdigest()
        map_url = f"./templates/temp/searched/{hashed_filename}.html"
        foli_map.save(map_url)

        return render_template("./foli_test.html", map_url=f"temp/searched/{hashed_filename}.html", title="Map")


if __name__ == '__main__':
    app.run(debug=True)
