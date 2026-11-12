import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

st.set_page_config(page_title="층간소음 데이터 분석", page_icon="🏠", layout="wide")
st.title("🏠 층간소음 데이터 분석")
st.caption("연도별 층간소음 원인 통계를 활용한 분석 및 다중 클래스 분류")

# 사용자가 제공한 한국환경공단 CSV의 실제 값만 사용
data = {
    "연도": list(range(2012, 2025)),
    "뛰거나걷는소리": [1338, 2383, 3190, 3423, 4509, 6359, 6984, 4956, 7456, 6299, 5515, 5098, 5204],
    "망치질": [67, 170, 180, 171, 235, 317, 494, 385, 569, 659, 648, 729, 907],
    "가구(끌거나찍는행위)": [44, 90, 170, 160, 208, 303, 368, 326, 555, 450, 403, 318, 326],
    "문개폐": [24, 50, 93, 101, 127, 170, 221, 127, 271, 229, 199, 160, 188],
    "가전제품(TV청소기세탁기)": [36, 80, 140, 152, 239, 316, 404, 223, 109, 220, 240, 260, 214],
    "악기(피아노등)": [39, 66, 82, 88, 126, 148, 147, 99, 132, 92, 61, 58, 63],
    "기타": [281, 432, 610, 617, 862, 1613, 1524, 1855, 3047, 1262, 705, 441, 131],
}
df = pd.DataFrame(data)

cause_names = {
    "뛰거나걷는소리": "뛰거나 걷는 소리",
    "망치질": "망치질",
    "가구(끌거나찍는행위)": "가구 끌기 및 찍는 소리",
    "문개폐": "문 개폐 소리",
    "가전제품(TV청소기세탁기)": "가전제품 소리",
    "악기(피아노등)": "악기 소리",
    "기타": "기타",
}
cause_cols = list(cause_names)

# 1. 데이터 소개
st.header("1. 데이터 소개 및 요약")
st.write(
    "한국환경공단의 층간소음 원인별 연도별 발생 건수 자료입니다. "
    "2012년부터 2024년까지 13개 연도의 통계와 7가지 원인 항목을 사용합니다."
)
df["전체 발생 건수"] = df[cause_cols].sum(axis=1)
a, b, c = st.columns(3)
a.metric("분석 기간", "2012~2024년")
b.metric("연도별 기록", f"{len(df)}개")
c.metric("분류 대상 원인", f"{len(cause_cols)}개")
st.dataframe(df.rename(columns=cause_names), use_container_width=True, hide_index=True)

# 2. 현황 그래프
st.header("2. 층간소음 발생 현황")
st.subheader("연도별 전체 발생 건수")
fig = px.line(df, x="연도", y="전체 발생 건수", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("연도별 원인 비율")
ratio = df[["연도"] + cause_cols].copy()
totals = ratio[cause_cols].sum(axis=1)
for col in cause_cols:
    ratio[col] = ratio[col] / totals * 100
ratio_long = ratio.melt(id_vars="연도", var_name="원인", value_name="비율")
ratio_long["원인"] = ratio_long["원인"].map(cause_names)
fig = px.bar(ratio_long, x="연도", y="비율", color="원인", barmode="stack")
fig.update_yaxes(range=[0, 100], title="발생 비율(%)")
st.plotly_chart(fig, use_container_width=True)

st.subheader("전체 기간 원인별 발생 건수")
cause_total = df[cause_cols].sum().rename(index=cause_names).sort_values(ascending=False)
cause_total = cause_total.rename_axis("원인").reset_index(name="발생 건수")
fig = px.bar(cause_total, x="원인", y="발생 건수", color="원인")
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# 3. 건축적 해결 방안
st.header("3. 건축적 해결 방안")
solutions = [
    ("바닥 완충 구조", "바닥 완충재와 충격 저감 구조를 적용해 걷거나 뛰는 행동에서 발생하는 충격 전달을 줄입니다."),
    ("이중벽 및 차음 구조", "벽체 사이 공기층과 차음재를 활용하고 틈새를 막아 공기를 통해 전달되는 소음을 줄입니다."),
    ("천장 방음 구조", "천장 내부에 차음·흡음 구조를 적용합니다. 흡음재만으로 층간 전달음이 모두 차단되는 것은 아닙니다."),
    ("방진 설계", "기계와 설비 하부에 방진재를 설치해 진동이 구조체로 전달되는 정도를 줄입니다."),
    ("흡음재 활용", "실내 벽과 천장에 흡음재를 적용해 반사음과 울림을 줄입니다."),
    ("구조적 진동 전달 저감", "바닥·벽·기둥의 접합부와 진동 전달 경로를 고려해 설계합니다."),
]
for i in range(0, len(solutions), 2):
    cols = st.columns(2)
    for col, (title, desc) in zip(cols, solutions[i:i+2]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(desc)

# 4. Long format 변환 및 분류
st.header("4. 다중 클래스 분류 모델")
st.warning(
