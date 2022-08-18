import folium

buStation_corr = [37.48662382, 126.723325411]
tile_option = "Stamen Toner"
ex_popup = "<i>Bupyeong Station<br>Hello</i>"
ex_tooltip = "Hello, Station!"

# folium 객체 생성
foli_map = folium.Map(location=buStation_corr, zoom_start=15, tiles=tile_option)
folium.Marker(buStation_corr, popup=ex_popup, tooltip=ex_tooltip,
              icon=folium.Icon(color="red", icon="fire")).add_to(foli_map)
foli_map.save("./templates/temp/map1.html")