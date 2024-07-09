import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster

# 페이지 제목 설정
st.title("광주광역시 광산구 음식물 스티커 판매처는?")

# CSV 파일 읽기 (파일 경로 확인 필요)
file_path = "광주광역시_광산구_음식물_스티커.csv"
df = pd.read_csv(file_path, encoding='cp949')

# 전체 목록 출력 (사업장명, 주소)
st.subheader("판매처 목록")

# 페이징을 위한 변수 설정
page_size = 10
page_number = st.number_input("페이지 번호 :", min_value=1, value=1)

# 페이지 번호에 맞게 데이터 슬라이싱
start_idx = (page_number - 1) * page_size
end_idx = start_idx + page_size
paged_df = df.iloc[start_idx:end_idx]

# 데이터프레임 출력
st.dataframe(paged_df[['사업장명', '주소']])

# 지도 생성
m = folium.Map([df["위도"].mean(), df["경도"].mean()], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# 데이터프레임에서 위치 정보를 이용해 지도에 마커 추가
for index, row in paged_df.iterrows():
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

    # 클릭 이벤트 처리
    circle_marker.add_child(folium.ClickForMarker(popup=popup_html))

# folium 지도를 Streamlit에 출력
folium_static(m)

# 사이드바에 선택된 사업장 정보 표시
st.sidebar.subheader("선택된 사업장 정보")
selected_business = st.sidebar.empty()

# JavaScript 코드를 사용하여 클릭 이벤트 처리
js_click_handler = """
    function(element){
        var name = element.target.feature.properties.tooltip;
        var selected_business = document.getElementById('selected_business');
        selected_business.innerHTML = "<b>선택된 사업장 정보:</b><br><br>" + name;
    }
"""
m.get_root().html.add_child(folium.Element(js_click_handler))
