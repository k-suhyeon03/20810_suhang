
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="층간소음 원인 분석",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 층간소음 원인 분석")
st.markdown(
    "2012년부터 2024년까지의 데이터를 활용하여 "
    "층간소음 발생 횟수와 원인별 변화를 분석합니다."
)

st.divider()

# ---------------------------------
# 데이터 직접 입력
# CSV 파일 없이 실행 가능
# ---------------------------------
data = {
    "연도": [
        2012, 2013, 2014, 2015, 2016, 2017, 2018,
        2019, 2020, 2021, 2022, 2023, 2024
    ],

    "뛰거나걷는소리": [
        1338, 2383, 3190, 3423, 4509, 6359, 6984,
        4956, 7456, 6299, 5515, 5098, 5204
    ],

    "망치질": [
        67, 170, 180, 171, 235, 317, 494,
        385, 569, 659, 648, 729, 907
    ],

    "가구(끌거나찍는행위)": [
        44, 90, 170, 160, 208, 303, 368,
        326, 555, 450, 403, 318, 326
    ],

    "문개폐": [
        24, 50, 93, 101, 127, 170, 221,
        127, 271, 229, 199, 160, 188
    ],

    "가전제품(TV청소기세탁기)": [
        36, 80, 140, 152, 239, 316, 404,
        223, 109, 220, 240, 260, 214
    ],

    "악기(피아노등)": [
        39, 66, 82, 88, 126, 148, 147,
        99, 132, 92, 61, 58, 63
    ],

    "기타": [
        281, 432, 610, 617, 862, 1613, 1524,
        1855, 3047, 1262, 705, 441, 131
    ]
}

df = pd.DataFrame(data)

causes = list(data.keys())[1:]

# 전체 발생 횟수 계산
df["전체 발생 횟수"] = df[causes].sum(axis=1)

# ---------------------------------
# 주요 정보
# ---------------------------------
st.subheader("📊 데이터 주요 정보")

total_count = int(df["전체 발생 횟수"].sum())

max_year = int(
    df.loc[df["전체 발생 횟수"].idxmax(), "연도"]
)

max_count = int(df["전체 발생 횟수"].max())

main_cause = df[causes].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "전체 발생 횟수",
    f"{total_count:,}회"
)

col2.metric(
    "가장 많이 발생한 연도",
    f"{max_year}년"
)

col3.metric(
    "최대 연간 발생 횟수",
    f"{max_count:,}회"
)

col4.metric(
    "가장 큰 소음 원인",
    main_cause
)

st.divider()

# ---------------------------------
# 1. 연도별 전체 발생 횟수
# ---------------------------------
st.subheader("1. 연도별 전체 층간소음 발생 횟수")

st.write(
    "2012년부터 2024년까지 층간소음 발생 횟수의 "
    "변화를 확인할 수 있습니다."
)

fig1 = px.line(
    df,
    x="연도",
    y="전체 발생 횟수",
    markers=True,
    text="전체 발생 횟수",
    title="연도별 전체 층간소음 발생 횟수",
    labels={
        "연도": "연도",
        "전체 발생 횟수": "발생 횟수(회)"
    }
)

fig1.update_traces(
    line=dict(width=3),
    texttemplate="%{text:,}",
    textposition="top center"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis=dict(dtick=1),
    xaxis_title="연도",
    yaxis_title="발생 횟수(회)"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# 2012년과 2024년 비교
first_count = int(df.iloc[0]["전체 발생 횟수"])
last_count = int(df.iloc[-1]["전체 발생 횟수"])

change = last_count - first_count
change_rate = change / first_count * 100

if change > 0:
    st.info(
        f"2012년과 비교했을 때 2024년의 발생 횟수는 "
        f"{change:,}회 증가했습니다. "
        f"증가율은 {change_rate:.1f}%입니다."
    )
elif change < 0:
    st.info(
        f"2012년과 비교했을 때 2024년의 발생 횟수는 "
        f"{abs(change):,}회 감소했습니다. "
        f"감소율은 {abs(change_rate):.1f}%입니다."
    )
else:
    st.info("2012년과 2024년의 발생 횟수가 같습니다.")

st.divider()

# ---------------------------------
# 2. 원인별 발생 횟수
# ---------------------------------
st.subheader("2. 연도별 원인별 발생 횟수")

st.write(
    "누적 막대그래프를 통해 각 연도에 어떤 원인으로 "
    "층간소음이 발생했는지 비교할 수 있습니다."
)

fig2 = px.bar(
    df,
    x="연도",
    y=causes,
    barmode="stack",
    title="연도별 층간소음 원인 구성",
    labels={
        "연도": "연도",
        "value": "발생 횟수(회)",
        "variable": "소음 원인"
    }
)

fig2.update_layout(
    xaxis=dict(dtick=1),
    xaxis_title="연도",
    yaxis_title="발생 횟수(회)",
    legend_title="소음 원인",
    hovermode="x unified"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# ---------------------------------
# 3. 원인별 변화 추이
# ---------------------------------
st.subheader("3. 소음 원인별 변화 추이")

selected_cause = st.selectbox(
    "분석할 소음 원인을 선택하세요.",
    causes
)

fig3 = px.line(
    df,
    x="연도",
    y=selected_cause,
    markers=True,
    text=selected_cause,
    title=f"{selected_cause} 발생 횟수 변화",
    labels={
        "연도": "연도",
        selected_cause: "발생 횟수(회)"
    }
)

fig3.update_traces(
    line=dict(width=3),
    texttemplate="%{text:,}",
    textposition="top center"
)

fig3.update_layout(
    xaxis=dict(dtick=1),
    xaxis_title="연도",
    yaxis_title="발생 횟수(회)",
    hovermode="x unified"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.metric(
    f"{selected_cause} 누적 발생 횟수",
    f"{int(df[selected_cause].sum()):,}회"
)

st.divider()

# ---------------------------------
# 4. 원인별 누적 발생 횟수 비교
# ---------------------------------
st.subheader("4. 원인별 누적 발생 횟수 비교")

cause_summary = (
    df[causes]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

cause_summary.columns = [
    "소음 원인",
    "발생 횟수"
]

fig4 = px.bar(
    cause_summary,
    x="발생 횟수",
    y="소음 원인",
    orientation="h",
    text="발생 횟수",
    title="2012~2024년 원인별 누적 발생 횟수",
    labels={
        "발생 횟수": "발생 횟수(회)",
        "소음 원인": "소음 원인"
    }
)

fig4.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig4.update_layout(
    xaxis_title="누적 발생 횟수(회)",
    yaxis_title="소음 원인"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.divider()

# ---------------------------------
# 5. 원본 데이터 확인
# ---------------------------------
st.subheader("5. 연도별 원본 데이터")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# 데이터 다운로드
csv_data = df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 분석 데이터 다운로드",
    data=csv_data,
    file_name="층간소음_분석결과.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "자료: 한국환경공단 층간소음 원인별 분석 데이터 | "
    "분석 기간: 2012~2024년"
)
