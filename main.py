
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

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
# CSV 파일 자동 검색
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent


def find_csv_file():
    # 프로젝트 폴더와 하위 폴더에서 CSV 검색
    csv_files = [
        p for p in BASE_DIR.rglob("*")
        if p.is_file()
        and p.suffix.lower() == ".csv"
        and not any(part.startswith(".") for part in p.parts)
    ]

    # 층간소음 관련 파일을 우선 검색
    matched_files = [
        p for p in csv_files
        if "층간소음" in p.name
        and "원인" in p.name
    ]

    if len(matched_files) == 1:
        return matched_files[0]

    if len(matched_files) > 1:
        raise ValueError(
            "층간소음 관련 CSV 파일이 여러 개 발견되었습니다: "
            + ", ".join(p.name for p in matched_files)
        )

    # 관련 이름이 없고 CSV가 하나뿐이면 해당 파일 사용
    if len(csv_files) == 1:
        return csv_files[0]

    if len(csv_files) == 0:
        raise FileNotFoundError(
            "프로젝트 폴더에서 CSV 파일을 찾을 수 없습니다. "
            "GitHub 저장소에 CSV 파일을 업로드했는지 확인해 주세요."
        )

    raise ValueError(
        "CSV 파일이 여러 개 발견되었습니다. "
        "파일 이름에 '층간소음'과 '원인'을 포함해 주세요. "
        "발견된 파일: "
        + ", ".join(p.name for p in csv_files)
    )


# ---------------------------------
# 데이터 불러오기
# ---------------------------------
@st.cache_data
def load_data(file_path):

    # 한글 파일 인코딩 대응
    encodings = ["utf-8-sig", "cp949", "euc-kr"]

    data = None

    for encoding in encodings:
        try:
            data = pd.read_csv(
                file_path,
                encoding=encoding
            )
            break
        except UnicodeDecodeError:
            continue

    if data is None:
        raise ValueError(
            "CSV 파일의 인코딩을 확인할 수 없습니다."
        )

    data.columns = data.columns.str.strip()

    required_columns = [
        "연도",
        "뛰거나걷는소리",
        "망치질",
        "가구(끌거나찍는행위)",
        "문개폐",
        "가전제품(TV청소기세탁기)",
        "악기(피아노등)",
        "기타"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"CSV에 필요한 열이 없습니다: {missing_columns}"
        )

    data = data[required_columns].copy()

    data["연도"] = pd.to_numeric(
        data["연도"],
        errors="coerce"
    )

    for col in required_columns[1:]:
        data[col] = pd.to_numeric(
            data[col],
            errors="coerce"
        ).fillna(0)

    data = data.dropna(subset=["연도"])

    data["연도"] = data["연도"].astype(int)

    data = data.sort_values("연도").reset_index(drop=True)

    causes = required_columns[1:]

    data["전체 발생 횟수"] = data[causes].sum(axis=1)

    return data, causes


# ---------------------------------
# 데이터 로딩 실행
# ---------------------------------
try:
    csv_path = find_csv_file()
    df, causes = load_data(str(csv_path))

    st.success(f"데이터 불러오기 성공: {csv_path.name}")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


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
    "2012년부터 2024년까지 전체 층간소음 발생 횟수의 "
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

first_count = int(df.iloc[0]["전체 발생 횟수"])
last_count = int(df.iloc[-1]["전체 발생 횟수"])

change = last_count - first_count
change_rate = change / first_count * 100

if change > 0:
    st.info(
        f"2012년보다 2024년의 발생 횟수가 "
        f"{change:,}회 증가했습니다. "
        f"증가율은 {change_rate:.1f}%입니다."
    )
elif change < 0:
    st.info(
        f"2012년보다 2024년의 발생 횟수가 "
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
# 4. 원인별 누적 발생 횟수
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
# 5. 원본 데이터
# ---------------------------------
st.subheader("5. 연도별 원본 데이터")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

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
