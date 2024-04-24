import streamlit as st
import pandas as pd
from typing import List, Tuple

# 데이터
data = pd.read_csv('/Users/soo/Desktop/데이터/개인공부/참여형 봄꽃놀이 지도/02. 기상 데이터 수집 및 시각화/01. 기상청_2~3월 기상정보 크롤링/기상청 크롤링_2020~2024_2~3월 기온_서울.csv', encoding='utf-8')
data = data.drop('Unnamed: 0',axis=1)
data['년월일'] = pd.to_datetime(data['년월일'])
data['년월일'] = data['년월일'].dt.date
data_1 = data.copy()
data_1['년월일'] = pd.to_datetime(data_1['년월일'])

# 스트림릿
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Line

st.sidebar.header('2020 ~ 2024 2,3월 서울 지역별 기후 데이터')

Country = st.sidebar.multiselect(
    "🧭 '지역'을 선택해주세요.",
    options=data_1["지역명"].unique(),
    default=data_1["지역명"].unique()[0:2]
)

Year = st.sidebar.slider("📅 '연도'를 선택해주세요", 2020, 2024, (2020, 2024))
# Month = st.sidebar.multiselect("📅 '월'을 선택해주세요", options=[2, 3],default=[2, 3])
# Day = st.sidebar.slider("📅 '일'을 선택해주세요", 1, 31, (1, 31))

st.subheader('기온')
data_1=data_1.astype({'년월일':'str'})
if Country:
    data_1 = data_1[data_1["지역명"].isin(Country)]

if Year:
    data_1 = data_1[pd.to_datetime(data_1['년월일']).dt.year.between(Year[0], Year[1])]

# if Month:
#     data_1 = data_1[pd.to_datetime(data_1['년월일']).dt.month.isin(Month)]

# if Day:
#     data_1 = data_1[pd.to_datetime(data_1['년월일']).dt.day.between(Year[0], Year[1])]


st.write(data_1)


c = (
    Line()
    .add_xaxis(data_1['년월일'])
    .add_yaxis("최고 기온", data_1['최고기온(℃)'])
    .add_yaxis("최저 기온", data_1['최저기온(℃)'])
    .set_global_opts(title_opts=opts.TitleOpts(title=""))
)
st_pyecharts(c)
