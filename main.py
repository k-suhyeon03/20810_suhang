
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="층간소음 원인별 비율 분석",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 연도별 층간소음 원인 비율 분석")

st.markdown("""
### 층간소음은 어떤 원인으로 발생할까?

층간소음은 공동주택에서 발생하는 생활 소리로 인해
이웃에게 불편을 주는 현상입니다. 대표적인 원인으로는
뛰거나 걷는 소리, 망치질, 가구를 끄는 소리 등이 있습니다.

이 웹사이트는 한국환경공단의 층간소음 원인별 분석 자료를 활용하여
2012년부터 2024년까지 각 원인이 차지하는 비율을 비교합니다.
이를 통해 층간소음의 주요 원인과 연도별 변화를 확인할 수 있습니다.
""")

st.divider()

# 원인별 실제 발생 횟수
data = {
    "연도": list(range(2012, 2025)),
    "뛰거나 걷는 소리": [
        1338, 2383, 3190, 3423, 4509, 6356, 6987,
        4958, 7453, 6303, 5518, 5097, 5206
    ],
    "망치질": [
        67, 170, 180, 171, 235, 314, 497,
        383, 568, 661, 646, 728, 910
    ],
    "가구(끌거나 찍는 행위)": [
        44, 90, 170, 160, 208, 302, 365,
        327, 561, 450, 405, 320, 326
    ],
    "문 개폐": [
        24, 50, 93, 101, 127, 166, 225,
        130, 270, 230, 201, 165, 190
    ],
    "가전제품(TV·청소기·세탁기)": [
        36, 80, 140, 152, 239, 312, 406,
        225, 109, 222, 241, 260, 211
    ],
    "악기(피아노 등)": [
        39, 66, 82, 88, 126, 148, 146,
        96, 129, 94, 63, 55, 63
    ],
    "기타": [
        281, 432, 610, 617, 862, 1628, 1516,
        1852, 3049, 1251, 697, 439, 127
    ]
}

df = pd.DataFrame(data)

# 원인별 비율 계산
cause_cols = df.columns[1:]
df["합계"] = df[cause_cols].sum(axis=1)

ratio_df = df.copy()

for col in cause_cols:
    ratio_df[col] = (
        ratio_df[col] / ratio_df["합계"] * 100
    )

# 그래프에 사용할 데이터 형태로 변환
plot_df = ratio_df.melt(
    id_vars="연도",
    value_vars=cause_cols,
    var_name="소음 원인",
    value_name="비율"
)

st.subheader("📊 연도별 층간소음 원인 비율")

st.write(
    "각 연도의 전체 층간소음 발생 횟수를 100%로 설정하고, "
    "원인별 비율을 누적 막대그래프로 나타냈습니다."
)

fig = px.bar(
    plot_df,
    x="연도",
    y="비율",
    color="소음 원인",
    barmode="stack",
    labels={
        "연도": "연도",
        "비율": "발생 비율(%)",
        "소음 원인": "소음 원인"
    },
    hover_data={
        "연도": True,
        "소음 원인": True,
        "비율": ":.1f"
    }
)

fig.update_layout(
    xaxis=dict(
        tickmode="linear",
        dtick=1,
        title="연도"
    ),
    yaxis=dict(
        title="발생 비율(%)",
        range=[0, 100]
    ),
    legend_title="소음 원인",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📌 그래프 살펴보기")

st.markdown("""
- **주요 원인:** 모든 연도에서 '뛰거나 걷는 소리'가 가장 높은 비율을 차지합니다.
- **망치질:** 2020년 이후 비율이 점차 증가하여 2024년에는 약 12.9%를 차지합니다.
- **기타:** 2020년에는 약 25.1%였지만 2024년에는 약 1.9%로 감소했습니다.

그래프를 통해 층간소음의 전체 발생 횟수뿐만 아니라
원인별 비중도 연도에 따라 달라진다는 점을 확인할 수 있습니다.
""")

st.divider()

st.subheader("📚 자료 출처")

st.markdown("""
- 자료명: 한국환경공단 층간소음 원인별 분석
- 분석 기간: 2012년 ~ 2024년
- 자료 제공: 한국환경공단
- [공공데이터포털 자료 확인](https://www.data.go.kr/data/15093156/fileData.do)
""")

st.caption(
    "각 원인의 비율은 해당 연도의 전체 발생 횟수를 기준으로 계산했습니다."
)
