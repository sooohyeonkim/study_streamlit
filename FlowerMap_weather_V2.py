import streamlit as st
import pandas as pd
from typing import List, Tuple

# 데이터
data = pd.read_csv('../기상청 크롤링_2020~2024_2~3월 기온_서울.csv', encoding='utf-8')
data = data.drop('Unnamed: 0',axis=1)
data['년월일'] = pd.to_datetime(data['년월일'])
data['년월일'] = data['년월일'].dt.date
data_1 = data.copy()
data_1['년월일'] = pd.to_datetime(data_1['년월일'])

# 스트림릿
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Line
from pyecharts.charts import Bar

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

if Country:
    data_1 = data_1[data_1["지역명"].isin(Country)]

if Year:
    data_1 = data_1[pd.to_datetime(data_1['년월일']).dt.year.between(Year[0], Year[1])]

# if Month:
#     data_1 = data_1[pd.to_datetime(data_1['년월일']).dt.month.isin(Month)]

# if Day:
#     data_1 = data_1[pd.to_datetime(data_1['년월일']).dt.day.between(Year[0], Year[1])]


st.write(data_1)

c = Line()
for country in Country:
    country_data = data_1[data_1["지역명"] == country]
    country_data['일교차']=(country_data['최고기온(℃)']-country_data['최저기온(℃)']).round(1)
    c.add_xaxis(country_data['년월일'].dt.date.tolist())
    c.add_yaxis(country, country_data['일교차'].tolist())
# 그래프 옵션 설정
c.set_global_opts(title_opts=opts.TitleOpts(title="일교차"))
# Streamlit으로 그래프 출력
st_pyecharts(c)

c = Line()
for country in Country:
    country_data = data_1[data_1["지역명"] == country]
    c.add_xaxis(country_data['년월일'].dt.date.tolist())
    c.add_yaxis(country, country_data['최저기온(℃)'].tolist())
# 그래프 옵션 설정
c.set_global_opts(title_opts=opts.TitleOpts(title="최저 기온"))
# Streamlit으로 그래프 출력
st_pyecharts(c)

c = Line()
for country in Country:
    country_data = data_1[data_1["지역명"] == country]
    c.add_xaxis(country_data['년월일'].dt.date.tolist())
    c.add_yaxis(country, country_data['최고기온(℃)'].tolist())
# 그래프 옵션 설정
c.set_global_opts(title_opts=opts.TitleOpts(title="최고 기온"))
# Streamlit으로 그래프 출력
st_pyecharts(c)


b = Bar()
for country in Country:
    country_data = data_1[data_1["지역명"] == country]
    x_data = country_data['년월일'].dt.date.tolist()
    y_data = country_data['일강수량(mm)'].tolist()
    # 숫자 0인 값을 빈 문자열로 대체합니다.
    y_data = ["" if y == 0 else y for y in y_data]
    b.add_xaxis(x_data)
    b.add_yaxis(country, y_data)

# 그래프 옵션 설정
b.set_global_opts(
    title_opts=opts.TitleOpts(title="강수량", subtitle="mm"),
    toolbox_opts=opts.ToolboxOpts(),
)

# 그래프 출력
st_pyecharts(b)
