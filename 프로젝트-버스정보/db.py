import sqlite3 
import streamlit as st

# 데이터베이스에 연결
con = sqlite3.connect('bus_csv copy.db', check_same_thread=False) # 안전성
cursor = con.cursor()

# 정류장 정보를 데이터 베이스에서 가져오기
def search_station(search_name):
    if search_name:
            # SQL 쿼리 실행
            cursor.execute('SELECT * FROM bus_station WHERE station_name LIKE ?', ('%' + search_name + '%',))
            results = cursor.fetchall()

            # 결과 출력
            if results:
                for row in results:
                    st.write("•  " + f"{row[2]}" + " :  " + f"**{row[1]}**")
            else:
                st.write("No matching results.")