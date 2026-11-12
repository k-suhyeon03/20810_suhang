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
    "중요한 한계: 이 자료에는 실제 소리의 크기·주파수·진동 측정값이 없습니다. "
    "따라서 이 모델은 실제 소음을 듣고 원인을 진단하는 모델이 아니라, "
    "연도와 발생 건수의 조합을 기존 통계 패턴에 따라 원인 유형으로 분류하는 학습용 모델입니다."
)
long_df = df[["연도"] + cause_cols].melt(
    id_vars="연도", var_name="원인코드", value_name="발생 건수"
)
long_df["원인"] = long_df["원인코드"].map(cause_names)
long_df = long_df[["연도", "발생 건수", "원인"]].dropna()
long_df["연도"] = long_df["연도"].astype(int)
long_df["발생 건수"] = long_df["발생 건수"].astype(float)

st.write(f"가로형 데이터를 세로형으로 변환한 결과 **{len(long_df)}개 행**이 생성되었습니다.")
with st.expander("분류에 사용하는 데이터 확인"):
    st.dataframe(long_df, use_container_width=True, hide_index=True)

st.subheader("원인별 연도 발생 건수 분포")
fig = px.box(long_df, x="원인", y="발생 건수", color="원인", points="all")
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

X = long_df[["연도", "발생 건수"]]
y = long_df["원인"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=2, random_state=42)
forest = RandomForestClassifier(
    n_estimators=200, max_depth=5, min_samples_leaf=2,
    class_weight="balanced", random_state=42
)
models = {"의사결정트리": tree, "랜덤 포레스트": forest}
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    results[name] = {
        "train": accuracy_score(y_train, model.predict(X_train)),
        "test": accuracy_score(y_test, model.predict(X_test)),
        "pred": model.predict(X_test),
    }

# 5. 성능 비교
st.subheader("모델별 정확도 비교")
m1, m2, m3, m4 = st.columns(4)
m1.metric("트리 훈련 정확도", f"{results['의사결정트리']['train']:.1%}")
m2.metric("트리 테스트 정확도", f"{results['의사결정트리']['test']:.1%}")
m3.metric("랜덤 포레스트 훈련 정확도", f"{results['랜덤 포레스트']['train']:.1%}")
m4.metric("랜덤 포레스트 테스트 정확도", f"{results['랜덤 포레스트']['test']:.1%}")

acc_df = pd.DataFrame([
    {"모델": name, "훈련 정확도": res["train"], "테스트 정확도": res["test"]}
    for name, res in results.items()
]).melt(id_vars="모델", var_name="평가 구분", value_name="정확도")
fig = px.bar(acc_df, x="모델", y="정확도", color="평가 구분", barmode="group", text_auto=".1%")
fig.update_yaxes(range=[0, 1])
st.plotly_chart(fig, use_container_width=True)

st.info(
    "각 원인에는 연도별 관측값이 13개씩 있고 테스트 데이터는 전체 91개 중 약 30%입니다. "
    "표본 수가 작으므로 평가 지표는 불안정할 수 있으며 실제 현장의 원인 판별 성능을 나타내지 않습니다."
)

# 6. 클래스별 평가 및 혼동 행렬
st.subheader("원인별 정밀도·재현율·F1 점수")
chosen_eval = st.selectbox("평가할 모델", list(models.keys()), key="eval_model")
pred = results[chosen_eval]["pred"]
labels = sorted(y.unique())
rep = classification_report(y_test, pred, labels=labels, output_dict=True, zero_division=0)
metric_df = pd.DataFrame([
    {
        "원인": label,
        "정밀도": rep[label]["precision"],
        "재현율": rep[label]["recall"],
        "F1 점수": rep[label]["f1-score"],
        "테스트 표본 수": int(rep[label]["support"]),
    }
    for label in labels
])
st.dataframe(
    metric_df.style.format({"정밀도": "{:.3f}", "재현율": "{:.3f}", "F1 점수": "{:.3f}"}),
    use_container_width=True, hide_index=True
)

st.subheader("혼동 행렬")
cm = confusion_matrix(y_test, pred, labels=labels)
fig = px.imshow(
    cm, x=labels, y=labels, text_auto=True, aspect="auto",
    labels={"x": "예측한 원인", "y": "실제 원인", "color": "건수"},
    color_continuous_scale="Blues"
)
st.plotly_chart(fig, use_container_width=True)

# 7. 트리 시각화 및 예측 결과
st.subheader("의사결정트리 구조")
fig_tree, ax = plt.subplots(figsize=(18, 9))
plot_tree(
    tree, feature_names=["연도", "발생 건수"],
    class_names=list(tree.classes_), filled=True, rounded=True,
    impurity=False, fontsize=8, ax=ax
)
st.pyplot(fig_tree, use_container_width=True)
plt.close(fig_tree)

st.subheader("테스트 데이터의 실제 원인과 예측 결과")
test_result = X_test.copy()
test_result["실제 원인"] = y_test
test_result["예측 원인"] = results[chosen_eval]["pred"]
test_result["결과"] = (test_result["실제 원인"] == test_result["예측 원인"]).map(
    {True: "일치", False: "불일치"}
)
st.dataframe(test_result.reset_index(drop=True), use_container_width=True, hide_index=True)

# 8. 사용자 입력 예측 및 규칙 기반 해결 방안
st.header("5. 사용자 입력 및 원인 예측")
st.write("연도와 발생 건수를 입력하면 모델이 기존 통계 패턴을 기준으로 원인 유형을 예측합니다.")
chosen_model = st.selectbox("예측 모델 선택", list(models.keys()), key="predict_model")
col1, col2 = st.columns(2)
with col1:
    year_input = st.number_input("연도", min_value=2012, max_value=2024, value=2024, step=1)
with col2:
    count_input = st.number_input(
        "발생 건수", min_value=0, max_value=int(long_df["발생 건수"].max() * 2),
        value=int(long_df["발생 건수"].median()), step=1
    )

recommendations = {
    "뛰거나 걷는 소리": [
        "바닥 완충 구조: 바닥 완충재와 충격 저감 구조를 적용합니다.",
        "구조적 진동 전달 저감: 바닥과 구조체를 통한 충격 전달 경로를 검토합니다.",
    ],
    "망치질": [
        "차음 구조: 소리가 전달되는 벽·바닥의 차음 성능과 틈새를 검토합니다.",
        "구조적 진동 전달 저감: 충격 진동이 구조체를 따라 전달되는 경로를 확인합니다.",
    ],
    "가구 끌기 및 찍는 소리": [
        "바닥 완충 구조: 바닥 마감과 완충층을 검토해 충격 전달을 줄입니다.",
    ],
    "문 개폐 소리": [
        "문 충격 저감: 도어 클로저와 완충 장치를 적용해 닫힐 때의 충격을 줄입니다.",
        "문 틈새 차음: 문틀과 문 사이의 기밀 구조를 검토합니다.",
    ],
    "가전제품 소리": [
        "방진 설계: 기기 하부에 방진재를 설치해 진동 전달을 줄입니다.",
        "설비 배치 개선: 진동이 구조체로 전달되지 않도록 위치와 고정 방식을 검토합니다.",
    ],
    "악기 소리": [
        "이중벽 및 차음 구조: 벽체 사이 공기층과 차음재를 활용합니다.",
        "천장 방음 구조: 천장과 바닥의 차음 성능 및 틈새를 검토합니다.",
        "흡음재 활용: 실내 반사음과 울림을 줄입니다.",
    ],
    "기타": [
        "구조적 진동 전달 저감: 소음 전달 경로를 조사한 뒤 구조적 대책을 검토합니다.",
        "이중벽 및 차음 구조: 공기 전달음이 의심되면 벽체 차음 성능을 검토합니다.",
    ],
}

if st.button("🔍 원인 예측하기", type="primary", use_container_width=True):
    model = models[chosen_model]
    input_row = pd.DataFrame({"연도": [int(year_input)], "발생 건수": [float(count_input)]})
    predicted = model.predict(input_row)[0]
    probs = model.predict_proba(input_row)[0]
    prob_df = pd.DataFrame({"원인": model.classes_, "예측 확률": probs}).sort_values(
        "예측 확률", ascending=False
    )
    st.success(f"분류 결과: **{predicted}**")
    fig = px.bar(
        prob_df, x="원인", y="예측 확률", color="원인",
        text=prob_df["예측 확률"].map(lambda v: f"{v:.1%}")
    )
    fig.update_yaxes(range=[0, 1])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("#### 관련 건축적 해결 방안")
    st.caption("다음 추천은 모델이 학습한 결과가 아니라, 예측된 원인에 미리 연결한 규칙 기반 안내입니다.")
    for item in recommendations.get(predicted, []):
        st.markdown(f"- {item}")

st.divider()
st.caption(
    "자료: 사용자가 제공한 한국환경공단 「층간소음 원인별 분석」(2012~2024) 자료. "
    "본 웹앱은 교육·탐구 목적이며 실제 건물의 소음 원인을 진단하는 도구가 아닙니다."
)
