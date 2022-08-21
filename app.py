from flask import Flask, render_template, request, redirect, session
import json
import folium

app = Flask(__name__)
app.secret_key = "mykey"


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
        return render_template("content.html")


@app.route("/test")
def test():
    # print session datas
    print(session["data"])

    # optimize data as dict
    received_data = eval(session["data"])
    print(received_data, type(received_data))

    # use like as node.js
    return render_template("test.html", data=received_data, map_id=session["map_id"])


@app.route("/foli")
def foli():
    # use like as node.js
    return render_template("foli_test.html")


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

    return foli_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
