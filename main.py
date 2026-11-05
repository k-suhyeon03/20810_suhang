
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------------------------
# 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="층간소음 분석실",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 층간소음 원인 분석실")
st.markdown(
    "2012년부터 2024년까지의 데이터를 바탕으로 "
    "층간소음 발생 횟수와 원인별 변화를 분석합니다."
)

st.divider()

# ---------------------------------
# 데이터 불러오기
# ---------------------------------
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "층간소음_원인별_분석.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "CSV 파일을 찾을 수 없습니다. "
            "앱 파일과 같은 폴더에 CSV 파일을 넣어 주세요."
        )

    data = pd.read_csv(file_path, encoding="utf-8-sig")

    data.columns = data.columns.str.strip()

    data["연도"] = pd.to_numeric(
        data["연도"], errors="coerce"
    )

    for col in data.columns[1:]:
        data[col] = pd.to_numeric(
            data[col], errors="coerce"
        ).fillna(0)

    data = data.dropna(subset=["연도"])
    data["연도"] = data["연도"].astype(int)

    data = data.sort_values("연도")

    # 전체 발생 횟수 계산
    cause_columns = data.columns[1:].tolist()
    data["전체 발생 횟수"] = data[cause_columns].sum(axis=1)

    return data, cause_columns


try:
    df, causes = load_data()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# ---------------------------------
# 주요 데이터 요약
# ---------------------------------
total_count = int(df["전체 발생 횟수"].sum())

max_year = int(
    df.loc[df["전체 발생 횟수"].idxmax(), "연도"]
)

max_count = int(df["전체 발생 횟수"].max())

main_cause = df[causes].sum().idxmax()
main_cause_count = int(df[main_cause].sum())

st.subheader("📊 데이터 주요 정보")

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
st.subheader("1. 연도별 층간소음 발생 횟수")

st.write(
    "2012년부터 2024년까지 전체 층간소음 발생 횟수가 "
    "어떻게 변화했는지 확인할 수 있습니다."
)

fig1 = px.line(
    df,
    x="연도",
    y="전체 발생 횟수",
    markers=True,
    text="전체 발생 횟수",
    labels={
        "연도": "연도",
        "전체 발생 횟수": "발생 횟수(회)"
    },
    title="연도별 전체 층간소음 발생 횟수"
)

fig1.update_traces(
    line=dict(width=3),
    texttemplate="%{text:,}",
    textposition="top center"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis=dict(
        tickmode="linear",
        dtick=1
    ),
    yaxis_title="발생 횟수(회)",
    xaxis_title="연도"
)

st.plotly_chart(fig1, use_container_width=True)

# 전체 발생 횟수 변화 설명
first_count = int(df.iloc[0]["전체 발생 횟수"])
last_count = int(df.iloc[-1]["전체 발생 횟수"])

change = last_count - first_count
change_rate = change / first_count * 100

if change > 0:
    st.info(
        f"2012년과 비교했을 때 2024년의 발생 횟수는 "
        f"{abs(change):,}회 증가했습니다. "
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
# 2. 원인별 발생 횟수 비교
# ---------------------------------
st.subheader("2. 원인별 층간소음 발생 횟수")

st.write(
    "각 연도에 어떤 원인으로 층간소음이 발생했는지 "
    "누적 막대그래프로 비교합니다."
)

fig2 = px.bar(
    df,
    x="연도",
    y=causes,
    labels={
        "연도": "연도",
        "value": "발생 횟수(회)",
        "variable": "소음 원인"
    },
    title="연도별 층간소음 원인 구성",
    barmode="stack"
)

fig2.update_layout(
    xaxis=dict(
        tickmode="linear",
        dtick=1
    ),
    yaxis_title="발생 횟수(회)",
    xaxis_title="연도",
    legend_title="소음 원인",
    hovermode="x unified"
)

st.plotly_chart(fig2, use_container_width=True)

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
    labels={
        "연도": "연도",
        selected_cause: "발생 횟수(회)"
    },
    title=f"{selected_cause} 발생 횟수 변화"
)

fig3.update_traces(
    line=dict(width=3),
    texttemplate="%{text:,}",
    textposition="top center"
)

fig3.update_layout(
    xaxis=dict(
        tickmode="linear",
        dtick=1
    ),
    yaxis_title="발생 횟수(회)",
    xaxis_title="연도",
    hovermode="x unified"
)

st.plotly_chart(fig3, use_container_width=True)

# 선택 원인의 전체 발생 횟수
cause_total = int(df[selected_cause].sum())

st.metric(
    f"{selected_cause} 누적 발생 횟수",
    f"{cause_total:,}회"
)

st.divider()


# ---------------------------------
# 4. 원인별 누적 발생 횟수 순위
# ---------------------------------
st.subheader("4. 층간소음 원인별 누적 발생 횟수")

cause_summary = (
    df[causes]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

cause_summary.columns = ["소음 원인", "발생 횟수"]

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

st.plotly_chart(fig4, use_container_width=True)

st.divider()


# ---------------------------------
# 5. 원본 데이터 확인
# ---------------------------------
st.subheader("5. 연도별 원본 데이터")

st.write("표에서 연도별 실제 발생 횟수를 확인할 수 있습니다.")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# CSV 다운로드
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

st.caption(
    "자료: 한국환경공단 층간소음 원인별 분석 데이터 | "
    "분석 기간: 2012~2024년"
)
