
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster

st.title("광주광역시 광산구 음식물 스티커 판매처는?")

file_path = "광주광역시_광산구_음식물_스티커.csv"
df = pd.read_csv(file_path, encoding='cp949')

st.subheader("전체 목록")
st.dataframe(df[['사업장명', '주소']])

m = folium.Map([df["위도"].mean(), df["경도"].mean()], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

for index, row in df.iterrows():
   
    circle_marker = folium.CircleMarker(
        location=[row["위도"], row["경도"]],
        radius=5,
        tooltip=row["사업장명"],
        fill=True,
        color='blue',
        fill_color='blue'
    ).add_to(marker_cluster)
    
   
    popup_html = f"""
        <b>사업자명:</b> {row["사업장명"]} <br>
        <b>주소:</b> {row["주소"]} <br>
    """
    folium.Popup(popup_html, max_width=300).add_to(circle_marker)

 
    circle_marker.add_child(folium.ClickForMarker(popup=popup_html))


folium_static(m)


st.sidebar.subheader("선택된 사업장 정보")
selected_business = st.sidebar.empty()


js_click_handler = """
    function(element){
        var name = element.target.feature.properties.tooltip;
        var selected_business = document.getElementById('selected_business');
        selected_business.innerHTML = "<b>선택된 사업장 정보:</b><br><br>" + name;
    }
"""
m.get_root().html.add_child(folium.Element(js_click_handler))