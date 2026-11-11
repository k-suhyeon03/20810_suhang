
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="연도별 층간소음 발생 추이",
    page_icon="🏠",
    layout="wide"
)

st.title("연도별 층간소음 발생 추이")
st.write("2012년부터 2024년까지 층간소음 발생 횟수의 변화")

# 연도별 전체 발생 횟수
data = {
    "연도": [
        2012, 2013, 2014, 2015, 2016, 2017, 2018,
        2019, 2020, 2021, 2022, 2023, 2024
    ],
    "발생 횟수": [
        1829, 3271, 4465, 4712, 6306, 9226, 10142,
        7971, 12139, 9211, 7771, 7064, 7033
    ]
}

df = pd.DataFrame(data)

# 꺾은선 그래프
fig = px.line(
    df,
    x="연도",
    y="발생 횟수",
    markers=True,
    text="발생 횟수",
    labels={
        "연도": "연도",
        "발생 횟수": "층간소음 발생 횟수(회)"
    }
)

fig.update_traces(
    line=dict(width=3),
    texttemplate="%{text:,}",
    textposition="top center"
)

fig.update_layout(
    xaxis=dict(
        tickmode="linear",
        dtick=1
    ),
    yaxis=dict(
        title="층간소음 발생 횟수(회)",
        rangemode="tozero"
    ),
    xaxis_title="연도",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
