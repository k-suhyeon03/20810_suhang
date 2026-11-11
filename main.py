
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="층간소음 분석",
    page_icon="🏠",
    layout="wide"
)

# 제목 및 사이트 소개
st.title("🏠 층간소음 발생 추이 및 원인 분석")

st.markdown("""
### 층간소음, 얼마나 자주 발생하고 있을까?

층간소음은 공동주택에서 위층이나 주변 세대의 생활 소리로 인해
다른 세대가 불편을 겪는 현상입니다.

뛰거나 걷는 소리, 가구를 끄는 소리, 망치질 등 다양한 원인으로
층간소음이 발생하며, 이는 이웃 간 갈등으로 이어지기도 합니다.

이 웹사이트는 한국환경공단의 층간소음 원인별 분석 자료를 활용하여
2012년부터 2024년까지의 발생 횟수와 원인별 비율을 살펴봅니다.
""")

st.divider()

# 원본 자료의 연도별 원인 데이터
data = {
    "연도": list(range(2012, 2025)),

    "뛰거나 걷는 소리": [
        1338, 2383, 3190, 3423, 4509, 6359, 6984,
        4956, 7456, 6299, 5515, 5098, 5204
    ],

    "망치질": [
        67, 170, 180, 171, 235, 317, 494,
        385, 569, 659, 648, 729, 907
    ],

    "가구(끌거나 찍는 행위)": [
        44, 90, 170, 160, 208, 303, 368,
        326, 555, 450, 403, 318, 326
    ],

    "문 개폐": [
        24, 50, 93, 101, 127, 170, 221,
        127, 271, 229, 199, 160, 188
    ],

    "가전제품(TV·청소기·세탁기)": [
        36, 80, 140, 152, 239, 316, 404,
        223, 109, 220, 240, 260, 214
    ],

    "악기(피아노 등)": [
        39, 66, 82, 88, 126, 148, 147,
        99, 132, 92, 61, 58, 63
    ],

    "기타": [
        281, 432, 610, 617, 862, 1613, 1524,
        1855, 3047, 1262, 705, 441, 131
    ]
}

df = pd.DataFrame(data)

# 원인별 열 지정
cause_cols = df.columns[1:]

# 연도별 전체 발생 횟수 계산
df["발생 횟수"] = df[cause_cols].sum(axis=1)


# --------------------------------------------------
# 첫 번째 그래프: 연도별 전체 발생 횟수
# --------------------------------------------------

st.subheader("📈 연도별 층간소음 발생 횟수")

st.write(
    "2012년부터 2024년까지 자료에 집계된 "
    "층간소음의 전체 발생 횟수를 나타냅니다."
)

fig1 = px.line(
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

fig1.update_traces(
    line=dict(width=3),
    marker=dict(size=8),
    texttemplate="%{text:,}",
    textposition="top center"
)

fig1.update_layout(
    xaxis=dict(
        tickmode="linear",
        dtick=1,
        title="연도"
    ),
    yaxis=dict(
        title="층간소음 발생 횟수(회)",
        rangemode="tozero"
    ),
    hovermode="x unified"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
**그래프 살펴보기**

- 2012년부터 2018년까지 발생 횟수가 전반적으로 증가했습니다.
- 2020년에 12,139회로 가장 높은 수치를 기록했습니다.
- 2020년 이후에는 감소하여 2024년에는 7,033회가 집계되었습니다.
""")

st.divider()


# --------------------------------------------------
# 두 번째 그래프: 연도별 원인 비율
# --------------------------------------------------

st.subheader("📊 연도별 층간소음 원인 비율")

st.write(
    "각 연도의 전체 발생 횟수에서 원인별 발생 횟수가 "
    "차지하는 비율을 100% 누적 막대그래프로 나타냈습니다."
)

# 원인별 비율 계산
ratio_df = df[["연도"] + list(cause_cols)].copy()

for col in cause_cols:
    ratio_df[col] = (
        ratio_df[col] / df["발생 횟수"] * 100
    )

# 그래프에 적합한 형태로 변환
plot_df = ratio_df.melt(
    id_vars="연도",
    var_name="소음 원인",
    value_name="비율"
)

fig2 = px.bar(
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

fig2.update_layout(
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

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
**그래프 살펴보기**

- 뛰거나 걷는 소리가 대부분의 연도에서 가장 높은 비율을 차지합니다.
- 망치질의 비율은 시간이 지날수록 전반적으로 증가하는 모습을 보입니다.
- 기타 원인의 비율은 연도에 따라 차이가 나타납니다.

각 연도의 원인별 비율을 비교하면 층간소음의 발생 원인이
시간에 따라 어떻게 변화했는지 확인할 수 있습니다.
""")

st.divider()


# --------------------------------------------------
# 세 번째 그래프: 전체 기간 원인별 발생 횟수
# --------------------------------------------------

st.subheader("📊 전체 기간 층간소음 원인별 발생 횟수")

st.write(
    "2012년부터 2024년까지의 발생 횟수를 원인별로 합산하여 "
    "전체 기간 동안 어떤 원인으로 층간소음이 많이 발생했는지 비교합니다."
)

# 전체 기간의 원인별 발생 횟수 합산
total_cause_df = df[cause_cols].sum().reset_index()

total_cause_df.columns = [
    "소음 원인",
    "발생 횟수"
]

# 발생 횟수가 많은 순서로 정렬
total_cause_df = total_cause_df.sort_values(
    by="발생 횟수",
    ascending=False
)

fig3 = px.bar(
    total_cause_df,
    x="소음 원인",
    y="발생 횟수",
    text="발생 횟수",
    labels={
        "소음 원인": "소음 원인",
        "발생 횟수": "전체 발생 횟수(회)"
    }
)

fig3.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig3.update_layout(
    xaxis_title="소음 원인",
    yaxis_title="전체 발생 횟수(회)",
    yaxis=dict(rangemode="tozero"),
    showlegend=False
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
**그래프 살펴보기**

- 가장 많이 집계된 원인은 뛰거나 걷는 소리입니다.
- 기타와 망치질도 전체 발생 횟수에서 큰 비중을 차지합니다.
- 악기 소리와 문 개폐는 상대적으로 적은 횟수를 기록했습니다.

이를 통해 전체 기간 동안 층간소음의 주요 원인이 무엇인지
한눈에 비교할 수 있습니다.
""")

st.divider()


st.markdown("---")
st.header("🏢 건축적 층간소음 해결 방안")
st.write(
    "건축 설계와 자재 및 구조 개선을 통해 "
    "층간소음 전달을 줄일 수 있는 다양한 방법을 소개합니다."
)

solutions = [
    {
        "제목": "바닥 완충 구조",
        "내용": "바닥에 완충재를 적용해 걷거나 뛰는 행동으로 발생하는 충격음이 아래층으로 전달되는 것을 줄입니다."
    },
    {
        "제목": "이중벽 및 차음 구조",
        "내용": "벽체 사이에 공기층과 차음재를 설치해 벽을 통해 전달되는 소음을 줄입니다."
    },
    {
        "제목": "천장 방음 구조",
        "내용": "천장 내부에 흡음재와 차음 구조를 적용해 실내로 전달되는 소음을 줄입니다."
    },
    {
        "제목": "방진 설계",
        "내용": "건물 설비와 기계의 하부에 방진 구조를 적용해 진동이 건물 구조체로 전달되는 것을 줄입니다."
    },
    {
        "제목": "흡음재 활용",
        "내용": "벽과 천장에 흡음재를 적용해 실내에서 소리가 반사되어 울리는 현상을 줄입니다."
    },
    {
        "제목": "구조적 진동 전달 저감",
        "내용": "건물의 구조체 연결부와 접합부를 고려해 진동이 다른 공간으로 전달되는 것을 줄이도록 설계합니다."
    }
]

cols = st.columns(2)

for i, item in enumerate(solutions):
    with cols[i % 2]:
        with st.container(border=True):
            st.subheader(item["제목"])
            st.write(item["내용"])

# --------------------------------------------------
# 자료 출처
# --------------------------------------------------

st.subheader("📚 자료 출처")

st.markdown("""
- 자료명: 한국환경공단 층간소음 원인별 분석
- 분석 기간: 2012년 ~ 2024년
- 자료 제공: 한국환경공단
- [공공데이터포털 자료 확인](https://www.data.go.kr/data/15093156/fileData.do)
""")

st.caption(
    "본 웹사이트는 공공데이터를 활용하여 "
    "층간소음 발생 추이와 원인별 비율을 시각화한 자료 분석 사이트입니다."
)
