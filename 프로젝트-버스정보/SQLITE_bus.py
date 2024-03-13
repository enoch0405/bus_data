# 모듈 가져오기
import sqlite3
import streamlit as st
import requests
import json
from db import search_station 

# 데이터베이스에 연결
con = sqlite3.connect('bus_csv copy.db')
cursor = con.cursor()

# 버스 api
def take_bus(station_id):
    bus_info=[]
    service_key = 'Xhhtp6o3z4f7BOdsmlZ94BhZZKweTPbK9SwsaxHQmLhdWTYvOrFdAs4aSD6yPZZSJRh5VBGU2v+uABrSXp1bBQ=='
    url = 'http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid'    
    
    params = {
        'ServiceKey' : service_key,
        'arsId' : station_id,
        'resultType' : 'json',
        # 'stId' : 111000213
    }
    response = requests.get(url, params=params)
    bus_info = []
    if response.status_code == 200:
        decoded_content = response.content.decode('utf-8')
        json_data = json.loads(decoded_content)
        bus_list = json_data['msgBody']['itemList']

        for b in bus_list:
            bus = {}
            if b['routeType'] == '3':
                bus['image'] = 'static/bus_blue@400.png'
            elif b['routeType'] == '2' or b['routeType'] == '4':
                bus['image'] = 'static/bus_green@400.png'
            elif b['routeType'] == '6':
                bus['image'] = 'static/bus_red@400.png'
            elif b['routeType'] == '5':
                bus['image'] = 'static/bus_yellow@400.png'
            else:
                bus['image'] = 'static/bus_gray@400.png'
            
            bus['bus_number1'] = b['busRouteAbrv']
            bus['arrive_time1'] = b['arrmsgSec1']
            bus['current_station1'] = b['stationNm1']
            bus['arrive_time2'] = b['arrmsgSec2']
            bus['current_station2'] = b['stationNm2']
            bus['station_name'] = b['stNm']

            # print(bus['arrive_time1'])
            if bus['arrive_time1'] == '첫 번째 버스 운행종료':
                pass
            elif bus['arrive_time2'] == None:
                pass
            else:
                bus_info.append(bus)

        return bus_info

# 버스 정보 적기
def write_bus():
    station_id = st.text_input('Type the station ID')

    try:
        # st.write('예시 ) 강동경희대병원: 25178, 고덕역: 25140, 강남역: 22298, 23285, 서울역: 11164')
        # st.divider()
        if station_id:
            bus_list = take_bus(station_id)
            st.subheader(f"{bus_list[0]['station_name']}({station_id})")
            st.divider()
            for bus in bus_list:
            # 두 개의 열 생성
                col1, col2 = st.columns([4, 5])  # 첫 번째 열은 이미지를 위해 1/5, 두 번째 열은 텍스트를 위해 4/5의 너비를 가짐

                # 첫 번째 열: 이미지
                with col1:
                    st.image(bus['image'], width=300)

                # 두 번째 열: 텍스트
                with col2:
                    st.write(f"버스 번호 : **{bus['bus_number1']}**")
                    if bus['current_station1'] == None:
                        pass
                    else:
                        st.write(f"현재 정류장 : **{bus['current_station1']}**")
                    st.write(f"도착 예정 시간 : **{bus['arrive_time1']}**")
                st.divider()
    except:
        st.write('정보 없음')

# 사이드 검색창
def side_bar():
    st.title(":blue[*Bus*] Information 🚌")

    with st.sidebar:
        # 버스 검색하기
        search_name = st.text_input('Search the station ID')  
        search_station(search_name)

# 메인 검색창
def main():
    side_bar()
    write_bus()

main()