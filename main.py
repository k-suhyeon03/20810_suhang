import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    hamming_loss,
)

# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="층간소음 데이터 분석",
    page_icon="🏠",
    layout="wide",
)
st.title("🏠 층간소음 데이터 분석")
st.caption("연도별 층간소음 원인 통계 분석 및 건축적 해결 방안 다중 레이블 분류")

# ---------------------------------------------------------
# 1. 데이터 불러오기
# ---------------------------------------------------------
# 사용자가 제공한 한국환경공단 CSV의 실제 값
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
cause_cols = list(cause_names.keys())
cause_list = list(cause_names.values())

df["전체 발생 건수"] = df[cause_cols].sum(axis=1)

# ---------------------------------------------------------
# 2. 데이터 소개 및 요약
# ---------------------------------------------------------
st.header("1. 데이터 소개 및 요약")
st.write(
    "한국환경공단의 층간소음 원인별 연도별 발생 건수 자료입니다. "
    "2012년부터 2024년까지 13개 연도의 통계와 7가지 원인 항목을 사용합니다."
)

a, b, c = st.columns(3)
a.metric("분석 기간", "2012~2024년")
b.metric("연도별 기록", f"{len(df)}개")
c.metric("분류 대상 원인", f"{len(cause_cols)}개")
st.dataframe(
    df.rename(columns=cause_names),
    use_container_width=True,
    hide_index=True,
)

# ---------------------------------------------------------
# 3. 층간소음 발생 현황 그래프
# ---------------------------------------------------------
st.header("2. 층간소음 발생 현황")

st.subheader("연도별 전체 발생 건수")
fig = px.line(
    df,
    x="연도",
    y="전체 발생 건수",
    markers=True,
    title="연도별 층간소음 전체 발생 건수",
)
fig.update_layout(xaxis_title="연도", yaxis_title="발생 건수")
st.plotly_chart(fig, use_container_width=True)

st.subheader("연도별 원인 비율")
ratio = df[["연도"] + cause_cols].copy()
totals = ratio[cause_cols].sum(axis=1).replace(0, pd.NA)

for col in cause_cols:
    ratio[col] = ratio[col].div(totals).fillna(0) * 100

ratio_long = ratio.melt(
    id_vars="연도",
    var_name="원인코드",
    value_name="비율",
)
ratio_long["원인"] = ratio_long["원인코드"].map(cause_names)

fig = px.bar(
    ratio_long,
    x="연도",
    y="비율",
    color="원인",
    barmode="stack",
    title="연도별 층간소음 원인 비율",
)
fig.update_yaxes(range=[0, 100], title="발생 비율(%)")
st.plotly_chart(fig, use_container_width=True)

st.subheader("전체 기간 원인별 발생 건수")
cause_total = (
    df[cause_cols]
    .sum()
    .rename(index=cause_names)
    .sort_values(ascending=False)
    .rename_axis("원인")
    .reset_index(name="발생 건수")
)
fig = px.bar(
    cause_total,
    x="원인",
    y="발생 건수",
    color="원인",
    title="2012~2024년 원인별 누적 발생 건수",
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 4. 건축적 해결 방안 소개
# ---------------------------------------------------------
st.header("3. 건축적 해결 방안")

solutions = [
    (
        "바닥 완충 구조",
        "바닥 완충재와 충격 저감 구조를 적용해 걷거나 뛰는 행동에서 발생하는 충격 전달을 줄입니다.",
    ),
    (
        "이중벽 및 차음 구조",
        "벽체 사이 공기층과 차음재를 활용하고 틈새를 막아 공기를 통해 전달되는 소음을 줄입니다.",
    ),
    (
        "천장 방음 구조",
        "천장 내부에 차음·흡음 구조를 적용합니다. 흡음재만으로 층간 전달음이 모두 차단되는 것은 아닙니다.",
    ),
    (
        "방진 설계",
        "기계와 설비 하부에 방진재를 설치해 진동이 구조체로 전달되는 정도를 줄입니다.",
    ),
    (
        "흡음재 활용",
        "실내 벽과 천장에 흡음재를 적용해 반사음과 울림을 줄입니다.",
    ),
    (
        "구조적 진동 전달 저감",
        "바닥·벽·기둥의 접합부와 진동 전달 경로를 고려해 설계합니다.",
    ),
]

for i in range(0, len(solutions), 2):
    cols = st.columns(2)
    for col, (title, desc) in zip(cols, solutions[i:i + 2]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(desc)

# ---------------------------------------------------------
# 5. 사용자가 직접 설정한 원인별 해결 방안 기준
# ---------------------------------------------------------
st.header("4. 원인별 건축적 해결 방안 기준")

# 출력 레이블 8개. 아래 순서는 학습 데이터와 예측 결과에서 동일하게 사용합니다.
solution_labels = [
    "바닥 완충 구조",
    "이중벽 및 차음 구조",
    "천장 방음 구조",
    "문 충격 저감 구조",
    "방진 설계",
    "설비 배치 개선",
    "흡음재 활용",
    "구조적 진동 전달 저감",
]

# 사용자가 직접 정한 기준을 변경하지 않고 그대로 반영합니다.
cause_to_solutions = {
    "뛰거나 걷는 소리": [
        "바닥 완충 구조",
        "구조적 진동 전달 저감",
    ],
    "망치질": [
        "이중벽 및 차음 구조",
        "천장 방음 구조",
    ],
    "가구 끌기 및 찍는 소리": [
        "바닥 완충 구조",
        "천장 방음 구조",
    ],
    "문 개폐 소리": [
        "문 충격 저감 구조",
    ],
    "가전제품 소리": [
        "방진 설계",
        "설비 배치 개선",
    ],
    "악기 소리": [
        "이중벽 및 차음 구조",
        "흡음재 활용",
    ],
    "기타": [
        "이중벽 및 차음 구조",
    ],
}

# 원인별 정답 레이블을 0과 1로 변환합니다.
y = pd.DataFrame(
    [
        {
            solution: int(solution in cause_to_solutions[cause])
            for solution in solution_labels
        }
        for cause in cause_list
    ],
    index=cause_list,
)
y.index.name = "층간소음 원인"

st.write(
    "아래 표는 사용자가 직접 설정한 기준입니다. "
    "1은 해당 해결 방안을 적용한다는 뜻이고, 0은 적용하지 않는다는 뜻입니다."
)
st.dataframe(y, use_container_width=True)

fig = px.imshow(
    y,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    labels={
        "x": "건축적 해결 방안",
        "y": "층간소음 원인",
        "color": "적용 여부",
    },
    title="원인별 건축적 해결 방안 기준 히트맵",
)
fig.update_xaxes(tickangle=-35)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 6. 다중 레이블 분류용 데이터 구성
# ---------------------------------------------------------
st.header("5. 다중 레이블 분류 모델")

st.warning(
    "데이터의 한계: 기존 한국환경공단 자료에는 연도별 원인 발생 횟수만 있으며, "
    "건축적 해결 방안의 실제 효과를 나타내는 정답 데이터는 없습니다. "
    "따라서 이번 모델은 사용자가 직접 설정한 7가지 원인-해결 방안 관계를 학습해 "
    "그 기준을 재현하는 교육용 모델입니다. 실제 건축물에서 해결 효과를 검증하거나 "
    "새로운 소음 원인을 진단하는 모델은 아닙니다."
)

# 입력 X: 원인 7가지를 원-핫 인코딩합니다.
# 각 원인은 서로 다른 입력 특성으로 표현됩니다.
X = pd.DataFrame(
    [
        {
            f"원인_{i + 1}": int(cause == selected_cause)
            for i, selected_cause in enumerate(cause_list)
        }
        for cause in cause_list
    ],
    index=cause_list,
)
X.index.name = "층간소음 원인"

# 출력 y: 8가지 해결 방안 각각의 적용 여부(0/1)
training_df = X.copy()
training_df["원인"] = training_df.index
training_df = training_df[["원인"] + list(X.columns)].join(y)

st.write(
    f"원인별로 한 행씩 구성하여 총 **{len(X)}개 데이터**를 사용합니다. "
    "연도별 통계 행을 복제해 학습 표본 수를 부풀리지 않습니다."
)
with st.expander("모델 학습 데이터 확인"):
    st.dataframe(
        training_df.reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

# ---------------------------------------------------------
# 7. 모델 생성 및 교차 검증
# ---------------------------------------------------------
st.subheader("모델 학습 및 평가")

def make_tree():
    """8개 출력 레이블을 동시에 예측하는 다중 출력 의사결정나무."""
    return DecisionTreeClassifier(
        max_depth=None,
        min_samples_leaf=1,
        random_state=42,
    )


def make_forest():
    """8개 출력 레이블을 동시에 예측하는 다중 출력 랜덤 포레스트."""
    return RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=1,
        max_features=1.0,
        random_state=42,
        n_jobs=-1,
    )


model_factories = {
    "의사결정나무": make_tree,
    "랜덤 포레스트": make_forest,
}

# 원인 데이터가 7개뿐이므로 임의의 train/test 분할 대신 Leave-One-Out을 사용합니다.
# 매 반복에서 원인 하나를 제외하고 나머지 6개 원인으로 학습한 뒤 제외한 원인을 예측합니다.
# 단, 제외된 원인의 원-핫 특성은 학습 과정에서 한 번도 등장하지 않으므로
# 이는 새로운 원인에 대한 일반화가 어렵다는 점을 보여주는 제한적인 평가입니다.
loo = LeaveOneOut()
cv_predictions = {}

try:
    for model_name, factory in model_factories.items():
        fold_predictions = []

        for train_index, test_index in loo.split(X):
            X_train = X.iloc[train_index]
            X_test = X.iloc[test_index]
            y_train = y.iloc[train_index]

            fold_model = factory()
            fold_model.fit(X_train, y_train)
            fold_pred = fold_model.predict(X_test)
            fold_predictions.append(fold_pred[0])

        cv_predictions[model_name] = pd.DataFrame(
            fold_predictions,
            index=cause_list,
            columns=solution_labels,
        ).astype(int)

    # 실제 앱의 사용자 입력 예측에는 7개 원인 전체로 다시 학습한 모델을 사용합니다.
    final_models = {}
    for model_name, factory in model_factories.items():
        final_model = factory()
        final_model.fit(X, y)
        final_models[model_name] = final_model

except Exception as exc:
    st.error("모델을 학습하거나 평가하는 중 오류가 발생했습니다.")
    st.exception(exc)
    st.stop()

# ---------------------------------------------------------
# 8. 모델 성능 비교
# ---------------------------------------------------------
st.subheader("모델별 성능 비교")

st.info(
    "평가 방식: 원인 7개 중 하나씩 제외하는 Leave-One-Out 교차 검증을 적용했습니다. "
    "다만 제외된 원인은 학습 데이터에 없는 원-핫 입력이 되므로, 이 점수는 "
    "새로운 원인에 대한 성능을 안정적으로 증명하는 값이 아닙니다. "
    "현재 데이터로는 독립적인 실제 검증 데이터도 확보할 수 없습니다."
)

metric_rows = []
for model_name, pred_df in cv_predictions.items():
    y_true = y.to_numpy(dtype=int)
    y_pred = pred_df.to_numpy(dtype=int)

    metric_rows.append(
        {
            "모델": model_name,
            "정확도(Subset Accuracy)": accuracy_score(y_true, y_pred),
            "정밀도(Micro)": precision_score(
                y_true, y_pred, average="micro", zero_division=0
            ),
            "재현율(Micro)": recall_score(
                y_true, y_pred, average="micro", zero_division=0
            ),
            "F1-score(Micro)": f1_score(
                y_true, y_pred, average="micro", zero_division=0
            ),
            "Hamming Loss": hamming_loss(y_true, y_pred),
        }
    )

metrics_df = pd.DataFrame(metric_rows).set_index("모델")
st.dataframe(
    metrics_df.style.format("{:.3f}"),
    use_container_width=True,
)

metric_long = (
    metrics_df.reset_index()
    .melt(
        id_vars="모델",
        var_name="평가 지표",
        value_name="점수",
    )
)
fig = px.bar(
    metric_long,
    x="평가 지표",
    y="점수",
    color="모델",
    barmode="group",
    text_auto=".3f",
    title="의사결정나무와 랜덤 포레스트 성능 비교",
)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Subset Accuracy·정밀도·재현율·F1-score는 높을수록 좋고, "
    "Hamming Loss는 낮을수록 좋습니다. 모든 점수는 사용자가 정한 기준에 대한 "
    "Leave-One-Out 평가 결과이며 실제 건축적 효과를 뜻하지 않습니다."
)

# ---------------------------------------------------------
# 9. 해결 방안별 평가 결과
# ---------------------------------------------------------
st.subheader("해결 방안별 분류 평가")

per_label_rows = []
for model_name, pred_df in cv_predictions.items():
    y_true = y.to_numpy(dtype=int)
    y_pred = pred_df.to_numpy(dtype=int)

    for i, solution in enumerate(solution_labels):
        per_label_rows.append(
            {
                "모델": model_name,
                "해결 방안": solution,
                "정밀도": precision_score(
                    y_true[:, i], y_pred[:, i], zero_division=0
                ),
                "재현율": recall_score(
                    y_true[:, i], y_pred[:, i], zero_division=0
                ),
                "F1-score": f1_score(
                    y_true[:, i], y_pred[:, i], zero_division=0
                ),
            }
        )

per_label_df = pd.DataFrame(per_label_rows)
st.dataframe(
    per_label_df.style.format(
        {
            "정밀도": "{:.3f}",
            "재현율": "{:.3f}",
            "F1-score": "{:.3f}",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

per_label_long = per_label_df.melt(
    id_vars=["모델", "해결 방안"],
    value_vars=["정밀도", "재현율", "F1-score"],
    var_name="평가 지표",
    value_name="점수",
)
fig = px.bar(
    per_label_long,
    x="해결 방안",
    y="점수",
    color="모델",
    barmode="group",
    facet_row="평가 지표",
    title="해결 방안별 평가 지표 비교",
)
fig.update_yaxes(range=[0, 1])
fig.update_xaxes(tickangle=-30)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 10. 교차 검증 예측 결과 시각화
# ---------------------------------------------------------
st.subheader("원인별 기준과 교차 검증 예측 비교")

chosen_eval_model = st.selectbox(
    "비교할 모델 선택",
    list(final_models.keys()),
    key="evaluation_model",
)
selected_cv_pred = cv_predictions[chosen_eval_model]

comparison_heatmap = pd.concat(
    {
        "직접 설정한 기준": y,
        "교차 검증 예측": selected_cv_pred,
    },
    names=["구분"],
)
fig = px.imshow(
    comparison_heatmap,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    labels={
        "x": "건축적 해결 방안",
        "y": "구분 및 층간소음 원인",
        "color": "적용 여부",
    },
    title=f"{chosen_eval_model}: 기준과 교차 검증 예측 비교",
)
fig.update_xaxes(tickangle=-35)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 11. 의사결정나무 구조 시각화
# ---------------------------------------------------------
st.subheader("의사결정나무 구조")

st.write(
    "입력 특성은 원인별 원-핫 인코딩 값입니다. "
    "C1~C7은 아래 표에 표시된 원인 순서와 연결됩니다."
)
feature_map = pd.DataFrame(
    {
        "특성 이름": [f"C{i + 1}" for i in range(len(cause_list))],
        "층간소음 원인": cause_list,
    }
)
st.dataframe(feature_map, use_container_width=True, hide_index=True)

fig_tree, ax = plt.subplots(figsize=(18, 9))
plot_tree(
    final_models["의사결정나무"],
    feature_names=[f"C{i + 1}" for i in range(len(cause_list))],
    filled=True,
    rounded=True,
    impurity=False,
    fontsize=8,
    ax=ax,
)
ax.set_title("Decision Tree - Multi-output Classification")
st.pyplot(fig_tree, use_container_width=True)
plt.close(fig_tree)

# ---------------------------------------------------------
# 12. 사용자 입력 및 예측
# ---------------------------------------------------------
st.header("6. 사용자 입력 및 건축적 해결 방안 예측")
st.write(
    "층간소음 원인을 선택하면 의사결정나무와 랜덤 포레스트가 "
    "각각 예측한 해결 방안을 확인할 수 있습니다."
)

selected_cause = st.selectbox(
    "층간소음 원인 선택",
    options=cause_list,
    key="selected_noise_cause",
)

# 선택한 원인을 학습 때와 같은 원-핫 형식으로 변환합니다.
input_vector = pd.DataFrame(
    [
        [int(selected_cause == cause) for cause in cause_list]
    ],
    columns=X.columns,
)

def extract_positive_probabilities(model, input_data, output_names):
    """
    다중 출력 분류기의 predict_proba 결과에서 각 레이블의
    '적용(1)' 확률을 추출합니다. 해당 클래스가 없을 때도 오류가 나지 않게 처리합니다.
    """
    probability_list = model.predict_proba(input_data)
    positive_probabilities = []

    for i, probabilities in enumerate(probability_list):
        classes = model.classes_[i]
        if 1 in classes:
            positive_index = list(classes).index(1)
            positive_probabilities.append(float(probabilities[0][positive_index]))
        else:
            positive_probabilities.append(0.0)

    return pd.Series(positive_probabilities, index=output_names)


def get_selected_solutions(prediction):
    return [
        solution_labels[i]
        for i, value in enumerate(prediction)
        if int(value) == 1
    ]


tree_model = final_models["의사결정나무"]
forest_model = final_models["랜덤 포레스트"]

tree_prediction = tree_model.predict(input_vector)[0].astype(int)
forest_prediction = forest_model.predict(input_vector)[0].astype(int)
reference_prediction = y.loc[selected_cause].to_numpy(dtype=int)

tree_probabilities = extract_positive_probabilities(
    tree_model, input_vector, solution_labels
)
forest_probabilities = extract_positive_probabilities(
    forest_model, input_vector, solution_labels
)

tree_solutions = get_selected_solutions(tree_prediction)
forest_solutions = get_selected_solutions(forest_prediction)
reference_solutions = get_selected_solutions(reference_prediction)

col_tree, col_forest = st.columns(2)

with col_tree:
    st.markdown("#### 의사결정나무 예측")
    if tree_solutions:
        for solution in tree_solutions:
            st.success(f"✓ {solution}")
    else:
        st.warning("예측된 해결 방안이 없습니다.")

with col_forest:
    st.markdown("#### 랜덤 포레스트 예측")
    if forest_solutions:
        for solution in forest_solutions:
            st.success(f"✓ {solution}")
    else:
        st.warning("예측된 해결 방안이 없습니다.")

st.subheader("해결 방안별 예측 확률")
probability_df = pd.DataFrame(
    {
        "해결 방안": solution_labels,
        "의사결정나무": tree_probabilities.values,
        "랜덤 포레스트": forest_probabilities.values,
    }
).melt(
    id_vars="해결 방안",
    var_name="모델",
    value_name="적용 예측 확률",
)
fig = px.bar(
    probability_df,
    x="해결 방안",
    y="적용 예측 확률",
    color="모델",
    barmode="group",
    text=probability_df["적용 예측 확률"].map(lambda value: f"{value:.0%}"),
    title="해결 방안별 적용 예측 확률",
)
fig.update_yaxes(range=[0, 1], tickformat=".0%")
fig.update_xaxes(tickangle=-30)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 13. 직접 설정한 기준과 모델 예측 비교
# ---------------------------------------------------------
st.subheader("직접 설정한 기준과 모델 예측 비교")

comparison_rows = []
for i, solution in enumerate(solution_labels):
    comparison_rows.append(
        {
            "건축적 해결 방안": solution,
            "직접 설정한 기준": "적용" if reference_prediction[i] == 1 else "미적용",
            "의사결정나무": "적용" if tree_prediction[i] == 1 else "미적용",
            "랜덤 포레스트": "적용" if forest_prediction[i] == 1 else "미적용",
            "의사결정나무 일치 여부": (
                "일치"
                if tree_prediction[i] == reference_prediction[i]
                else "불일치"
            ),
            "랜덤 포레스트 일치 여부": (
                "일치"
                if forest_prediction[i] == reference_prediction[i]
                else "불일치"
            ),
        }
    )

comparison_df = pd.DataFrame(comparison_rows)
st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True,
)

st.subheader("사용자가 설정한 기준에 따른 건축적 해결 방안")
st.write(f"선택한 원인: **{selected_cause}**")
for solution in reference_solutions:
    st.markdown(f"- **{solution}**")

if (
    tree_solutions == reference_solutions
    and forest_solutions == reference_solutions
):
    st.success("두 모델의 예측이 사용자가 설정한 기준과 모두 일치합니다.")
else:
    st.warning(
        "일부 모델의 예측이 직접 설정한 기준과 다릅니다. "
        "위 비교표에서 차이가 발생한 해결 방안을 확인할 수 있습니다."
    )

st.divider()
st.caption(
    "자료: 사용자가 제공한 한국환경공단 「층간소음 원인별 분석」(2012~2024) 자료. "
    "건축적 해결 방안의 기준은 사용자가 직접 설정했습니다. "
    "본 웹앱은 교육·탐구 목적이며 실제 건물의 소음 원인을 진단하거나 "
    "해결 방안의 효과를 실증적으로 검증하는 도구가 아닙니다."
)
