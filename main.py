import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    hamming_loss
)

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="층간소음 데이터 분석",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 층간소음 데이터 분석 및 해결 방안")

st.write("""
아파트와 같은 공동주택에서는 걷거나 뛰는 소리, 가구를 끄는 소리,
가전제품 작동 소리 등 다양한 층간소음이 발생한다.

이 웹앱에서는 한국환경공단의 층간소음 원인별 분석 데이터를 활용하여
2012년부터 2024년까지의 층간소음 발생 추이와 원인별 비율을 살펴보고,
건축적인 해결 방안도 함께 알아본다.
""")

st.markdown("---")


# --------------------------------------------------
# 데이터 입력
# --------------------------------------------------

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

causes = [
    "뛰거나 걷는 소리",
    "망치질",
    "가구(끌거나 찍는 행위)",
    "문 개폐",
    "가전제품(TV·청소기·세탁기)",
    "악기(피아노 등)",
    "기타"
]

df["전체 발생 건수"] = df[causes].sum(axis=1)


# --------------------------------------------------
# 그래프 1. 연도별 전체 발생 건수
# --------------------------------------------------

st.header("1. 연도별 층간소음 발생 추이")

fig1 = px.line(
    df,
    x="연도",
    y="전체 발생 건수",
    markers=True,
    title="2012~2024년 층간소음 전체 발생 건수",
    labels={"연도": "연도", "전체 발생 건수": "발생 건수"}
)

fig1.update_layout(
    xaxis=dict(tickmode="linear", dtick=1),
    hovermode="x unified"
)

st.plotly_chart(fig1, use_container_width=True)

st.write(
    "연도별 층간소음 발생 건수를 통해 전체적인 발생 추이와 "
    "증감 변화를 확인할 수 있다."
)


# --------------------------------------------------
# 그래프 2. 연도별 원인 비율
# --------------------------------------------------

st.markdown("---")
st.header("2. 연도별 층간소음 원인 비율")

percent_df = df[causes].div(df[causes].sum(axis=1), axis=0) * 100
percent_df["연도"] = df["연도"]

fig2 = px.bar(
    percent_df,
    x="연도",
    y=causes,
    title="연도별 층간소음 원인 비율 (100%)",
    labels={
        "연도": "연도",
        "value": "발생 비율 (%)",
        "variable": "소음 원인"
    },
    barmode="stack"
)

fig2.update_layout(
    xaxis=dict(tickmode="linear", dtick=1),
    yaxis_title="발생 비율 (%)",
    yaxis=dict(range=[0, 100]),
    legend_title="소음 원인",
    hovermode="x unified"
)

st.plotly_chart(fig2, use_container_width=True)

st.write(
    "각 연도에 발생한 층간소음 중 원인별 비율을 비교하여 "
    "어떤 소음이 주요 원인인지 살펴볼 수 있다."
)


# --------------------------------------------------
# 그래프 3. 전체 기간 원인별 발생 건수
# --------------------------------------------------

st.markdown("---")
st.header("3. 원인별 전체 층간소음 발생 건수")

cause_total = (
    df[causes]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

cause_total.columns = ["소음 원인", "전체 발생 건수"]

fig3 = px.bar(
    cause_total,
    x="소음 원인",
    y="전체 발생 건수",
    title="2012~2024년 원인별 층간소음 발생 건수",
    labels={
        "소음 원인": "소음 원인",
        "전체 발생 건수": "전체 발생 건수"
    },
    text="전체 발생 건수"
)

fig3.update_traces(textposition="outside")
fig3.update_layout(
    xaxis_title="소음 원인",
    yaxis_title="전체 발생 건수",
    xaxis_tickangle=-20
)

st.plotly_chart(fig3, use_container_width=True)

st.write(
    "2012년부터 2024년까지의 데이터를 합산하여 "
    "어떤 원인으로 인한 층간소음이 가장 많이 발생했는지 비교한다."
)


# --------------------------------------------------
# 건축적 층간소음 해결 방안
# --------------------------------------------------

st.markdown("---")
st.header("🏢 건축적 층간소음 해결 방안")

st.write("""
건축물의 구조와 건축 자재를 개선하면 층간소음이 다른 공간으로
전달되는 것을 줄일 수 있다. 다음은 건축 분야에서 활용할 수 있는
대표적인 층간소음 저감 방법이다.
""")

solutions = [
    {
        "제목": "① 바닥 완충 구조",
        "내용": "바닥 슬래브 위에 완충재를 설치하고 바닥 마감층을 구성하여 걷거나 뛰는 행동으로 발생하는 충격음이 아래층으로 전달되는 것을 줄인다."
    },
    {
        "제목": "② 이중벽 및 차음 구조",
        "내용": "벽체 사이에 공기층과 차음재를 설치하는 이중벽 구조를 적용하여 벽을 통해 전달되는 소음을 줄인다."
    },
    {
        "제목": "③ 천장 방음 구조",
        "내용": "천장 내부에 흡음재와 차음 구조를 적용하여 소음이 실내로 전달되는 것을 줄인다."
    },
    {
        "제목": "④ 방진 설계",
        "내용": "기계와 설비의 하부에 방진재를 설치하여 작동 과정에서 발생하는 진동이 건물 구조체로 전달되는 것을 줄인다."
    },
    {
        "제목": "⑤ 흡음재 활용",
        "내용": "벽과 천장 등에 흡음재를 설치하여 실내에서 소리가 반사되어 울리는 현상을 줄인다."
    },
    {
        "제목": "⑥ 구조적 진동 전달 저감",
        "내용": "건물의 벽체와 바닥, 배관 및 접합부 등을 고려하여 진동과 소음이 다른 공간으로 전달되는 경로를 줄이도록 설계한다."
    },
    {
        "제목": "⑦ 문 충격 저감 구조",
        "내용": "문틀과 문이 맞닿는 부분에 완충 장치 등을 적용하여 문을 여닫을 때 발생하는 충격과 소음을 줄인다."
    },
    {
        "제목": "⑧ 설비 배치 개선",
        "내용": "소음과 진동이 발생하는 가전제품 및 설비의 위치를 주거 공간과 침실 등으로부터 적절히 분리하여 소음 전달의 영향을 줄인다."
    }
]

cols = st.columns(2)

for i, item in enumerate(solutions):
    with cols[i % 2]:
        with st.container(border=True):
            st.subheader(item["제목"])
            st.write(item["내용"])


# --------------------------------------------------
# 원인별 해결 방안 연결 기준
# --------------------------------------------------

st.markdown("---")
st.header("4. 층간소음 원인별 건축적 해결 방안")

st.write("""
아래 기준은 층간소음 원인에 따라 적용할 수 있다고 판단한 건축적 해결 방안을
직접 정리한 것이다. 이후 분류 모델은 이 기준을 학습하여 원인에 맞는
해결 방안을 예측한다.
""")

solution_labels = [
    "바닥 완충 구조",
    "이중벽 및 차음 구조",
    "천장 방음 구조",
    "문 충격 저감 구조",
    "방진 설계",
    "설비 배치 개선",
    "흡음재 활용",
    "구조적 진동 전달 저감"
]

mapping = {
    "뛰거나 걷는 소리": [
        "바닥 완충 구조",
        "구조적 진동 전달 저감"
    ],
    "망치질": [
        "이중벽 및 차음 구조",
        "천장 방음 구조"
    ],
    "가구(끌거나 찍는 행위)": [
        "바닥 완충 구조",
        "천장 방음 구조"
    ],
    "문 개폐": [
        "문 충격 저감 구조"
    ],
    "가전제품(TV·청소기·세탁기)": [
        "방진 설계",
        "설비 배치 개선"
    ],
    "악기(피아노 등)": [
        "이중벽 및 차음 구조",
        "흡음재 활용"
    ],
    "기타": [
        "이중벽 및 차음 구조"
    ]
}

mapping_df = pd.DataFrame(
    [
        {
            "층간소음 원인": cause,
            "건축적 해결 방안": ", ".join(mapping[cause])
        }
        for cause in causes
    ]
)

st.dataframe(mapping_df, use_container_width=True, hide_index=True)


# --------------------------------------------------
# 다중 출력 분류 모델 데이터 구성
# --------------------------------------------------

st.markdown("---")
st.header("5. 다중 출력 분류 모델")

st.write("""
층간소음 원인을 입력하면 그 원인에 해당하는 건축적 해결 방안을 분류하도록
의사결정나무와 랜덤 포레스트 모델을 구성하였다.

하나의 층간소음 원인에 여러 해결 방안이 연결될 수 있으므로,
여러 개의 정답을 동시에 예측하는 다중 출력 분류 방식을 사용한다.
""")

# 원인 7개를 원-핫 인코딩한 입력 데이터
X = pd.DataFrame(
    [
        [1 if cause == selected_cause else 0 for cause in causes]
        for selected_cause in causes
    ],
    columns=causes,
    index=causes
)

# 원인별 해결 방안을 0과 1로 표현한 정답 데이터
y = pd.DataFrame(
    [
        [1 if label in mapping[cause] else 0 for label in solution_labels]
        for cause in causes
    ],
    columns=solution_labels,
    index=causes
)

with st.expander("모델 학습에 사용하는 데이터 확인"):
    st.write("입력 데이터 (X): 원인을 원-핫 인코딩한 값")
    st.dataframe(X, use_container_width=True)
    st.write("정답 데이터 (y): 원인별 해결 방안 연결 기준")
    st.dataframe(y, use_container_width=True)


# --------------------------------------------------
# 모델 및 교차 검증
# --------------------------------------------------

models = {
    "의사결정나무": DecisionTreeClassifier(random_state=42),
    "랜덤 포레스트": RandomForestClassifier(
        n_estimators=300,
        random_state=42
    )
}

def evaluate_with_loo(model, X_data, y_data):
    """Leave-One-Out 교차 검증으로 각 모델의 예측값을 만든다."""
    loo = LeaveOneOut()
    predictions = pd.DataFrame(
        0,
        index=y_data.index,
        columns=y_data.columns,
        dtype=int
    )

    for train_index, test_index in loo.split(X_data):
        X_train = X_data.iloc[train_index]
        X_test = X_data.iloc[test_index]
        y_train = y_data.iloc[train_index]

        fold_model = model.__class__(**model.get_params())
        fold_model.fit(X_train, y_train)

        fold_prediction = fold_model.predict(X_test)
        predictions.iloc[test_index, :] = fold_prediction

    return predictions


def calculate_metrics(y_true, y_pred):
    """다중 출력 분류에 사용할 전체 평가 지표를 계산한다."""
    return {
        "Subset Accuracy": accuracy_score(y_true, y_pred),
        "Micro Precision": precision_score(
            y_true, y_pred, average="micro", zero_division=0
        ),
        "Micro Recall": recall_score(
            y_true, y_pred, average="micro", zero_division=0
        ),
        "Micro F1-score": f1_score(
            y_true, y_pred, average="micro", zero_division=0
        ),
        "Macro Precision": precision_score(
            y_true, y_pred, average="macro", zero_division=0
        ),
        "Macro Recall": recall_score(
            y_true, y_pred, average="macro", zero_division=0
        ),
        "Macro F1-score": f1_score(
            y_true, y_pred, average="macro", zero_division=0
        ),
        "Hamming Loss": hamming_loss(y_true, y_pred)
    }


with st.spinner("두 분류 모델의 교차 검증을 진행하고 있습니다..."):
    cv_predictions = {}
    metric_results = {}

    for model_name, model in models.items():
        cv_pred = evaluate_with_loo(model, X, y)
        cv_predictions[model_name] = cv_pred
        metric_results[model_name] = calculate_metrics(y, cv_pred)

metrics_df = pd.DataFrame(metric_results).T

st.subheader("모델별 전체 평가 지표")
st.dataframe(
    metrics_df.style.format("{:.3f}"),
    use_container_width=True
)

st.caption(
    "Subset Accuracy는 모든 해결 방안을 한꺼번에 정확히 맞힌 비율이며, "
    "Hamming Loss는 전체 예측 항목 중 틀린 항목의 비율이다."
)


# --------------------------------------------------
# 그래프 4. 전체 모델 성능 비교
# --------------------------------------------------

st.subheader("① 전체 모델 성능 비교")

overall_metric_names = [
    "Subset Accuracy",
    "Micro Precision",
    "Micro Recall",
    "Micro F1-score",
    "Macro Precision",
    "Macro Recall",
    "Macro F1-score"
]

overall_plot_df = (
    metrics_df[overall_metric_names]
    .reset_index(names="모델")
    .melt(
        id_vars="모델",
        var_name="평가 지표",
        value_name="점수"
    )
)

fig4 = px.bar(
    overall_plot_df,
    x="평가 지표",
    y="점수",
    color="모델",
    barmode="group",
    title="의사결정나무와 랜덤 포레스트의 전체 성능 비교",
    text_auto=".3f",
    labels={"점수": "평가 점수"}
)

fig4.update_layout(
    yaxis=dict(range=[0, 1.05]),
    xaxis_tickangle=-25,
    legend_title="모델"
)

st.plotly_chart(fig4, use_container_width=True)


# --------------------------------------------------
# 그래프 5. Hamming Loss 비교
# --------------------------------------------------

st.subheader("② Hamming Loss 비교")

hamming_df = (
    metrics_df[["Hamming Loss"]]
    .reset_index(names="모델")
)

fig5 = px.bar(
    hamming_df,
    x="모델",
    y="Hamming Loss",
    color="모델",
    text_auto=".3f",
    title="모델별 Hamming Loss",
    labels={"Hamming Loss": "오분류 비율"}
)

fig5.update_layout(
    yaxis=dict(range=[0, 1.05]),
    showlegend=False
)

st.plotly_chart(fig5, use_container_width=True)

st.caption("Hamming Loss는 낮을수록 예측 오류가 적다는 뜻이다.")


# --------------------------------------------------
# 그래프 6. 해결 방안별 F1-score 비교
# --------------------------------------------------

st.subheader("③ 해결 방안별 F1-score 비교")

per_label_rows = []

for model_name, prediction in cv_predictions.items():
    for label in solution_labels:
        score = f1_score(
            y[label],
            prediction[label],
            zero_division=0
        )
        per_label_rows.append({
            "모델": model_name,
            "해결 방안": label,
            "F1-score": score
        })

per_label_df = pd.DataFrame(per_label_rows)

fig6 = px.bar(
    per_label_df,
    x="해결 방안",
    y="F1-score",
    color="모델",
    barmode="group",
    title="해결 방안별 F1-score 비교",
    text_auto=".3f",
    labels={"F1-score": "F1-score"}
)

fig6.update_layout(
    yaxis=dict(range=[0, 1.05]),
    xaxis_tickangle=-35,
    legend_title="모델"
)

st.plotly_chart(fig6, use_container_width=True)

st.caption(
    "특정 해결 방안의 점수가 0이라면 교차 검증에서 해당 항목을 "
    "정확히 예측하지 못했다는 뜻이다. 이는 실제 해결 효과가 없다는 뜻이 아니다."
)


# --------------------------------------------------
# 그래프 7. 기준과 교차 검증 예측 비교
# --------------------------------------------------

st.subheader("④ 원인별 정답 기준과 교차 검증 예측 비교")

selected_model_for_heatmap = st.selectbox(
    "비교할 모델 선택",
    list(models.keys()),
    key="heatmap_model"
)

heatmap_pred = cv_predictions[selected_model_for_heatmap]

heatmap_df = pd.concat(
    [
        y.assign(구분="직접 설정한 기준"),
        heatmap_pred.assign(구분="교차 검증 예측")
    ]
)

heatmap_long = heatmap_df.reset_index(names="층간소음 원인").melt(
    id_vars=["층간소음 원인", "구분"],
    value_vars=solution_labels,
    var_name="건축적 해결 방안",
    value_name="값"
)

heatmap_long["행"] = (
    heatmap_long["구분"] + " - " + heatmap_long["층간소음 원인"]
)

fig7 = px.imshow(
    heatmap_long.pivot(
        index="행",
        columns="건축적 해결 방안",
        values="값"
    ),
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    zmin=0,
    zmax=1,
    title=f"{selected_model_for_heatmap}: 기준과 교차 검증 예측 비교"
)

fig7.update_layout(
    xaxis_title="건축적 해결 방안",
    yaxis_title="층간소음 원인 및 구분",
    coloraxis_colorbar_title="분류값"
)

st.plotly_chart(fig7, use_container_width=True)


# --------------------------------------------------
# 사용자가 원인을 선택하고 해결 방안 예측
# --------------------------------------------------

st.markdown("---")
st.header("6. 층간소음 원인 입력 및 해결 방안 예측")

st.write("""
층간소음 원인을 선택하면 전체 7개 원인으로 학습한 두 모델이
해당 원인에 적합하다고 예측하는 건축적 해결 방안을 보여준다.
""")

selected_cause = st.selectbox(
    "층간소음 원인을 선택하세요.",
    causes
)

# 전체 데이터로 최종 모델 학습
final_models = {}

for model_name, model in models.items():
    final_model = model.__class__(**model.get_params())
    final_model.fit(X, y)
    final_models[model_name] = final_model

input_data = pd.DataFrame(
    [[1 if cause == selected_cause else 0 for cause in causes]],
    columns=causes
)

col1, col2 = st.columns(2)

for column, model_name in zip(
    [col1, col2],
    ["의사결정나무", "랜덤 포레스트"]
):
    with column:
        st.subheader(model_name)

        prediction = final_models[model_name].predict(input_data)[0]
        predicted_solutions = [
            solution_labels[i]
            for i, value in enumerate(prediction)
            if value == 1
        ]

        if predicted_solutions:
            for solution in predicted_solutions:
                st.success(solution)
        else:
            st.warning("예측된 해결 방안이 없습니다.")

        st.write("해결 방안별 예측 확률")

        probability_list = final_models[model_name].predict_proba(
            input_data
        )

        probability_values = []

        for i, probabilities in enumerate(probability_list):
            classes = final_models[model_name].classes_[i]
            if 1 in classes:
                positive_index = list(classes).index(1)
                probability = probabilities[0][positive_index]
            else:
                probability = 0.0

            probability_values.append(probability)

        probability_df = pd.DataFrame({
            "건축적 해결 방안": solution_labels,
            "예측 확률": probability_values
        })

        probability_fig = px.bar(
            probability_df,
            x="예측 확률",
            y="건축적 해결 방안",
            orientation="h",
            range_x=[0, 1],
            text=probability_df["예측 확률"].map(
                lambda value: f"{value:.2f}"
            )
        )

        probability_fig.update_layout(
            xaxis_title="예측 확률",
            yaxis_title="",
            showlegend=False,
            height=350
        )

        st.plotly_chart(
            probability_fig,
            use_container_width=True
        )

st.subheader("직접 설정한 기준과 모델 예측 비교")

reference_solutions = mapping[selected_cause]

comparison_rows = []

for solution in solution_labels:
    comparison_rows.append({
        "건축적 해결 방안": solution,
        "직접 설정한 기준": (
            "적용" if solution in reference_solutions else "미적용"
        ),
        "의사결정나무 예측": (
            "적용"
            if final_models["의사결정나무"].predict(input_data)[0][
                solution_labels.index(solution)
            ] == 1
            else "미적용"
        ),
        "랜덤 포레스트 예측": (
            "적용"
            if final_models["랜덤 포레스트"].predict(input_data)[0][
                solution_labels.index(solution)
            ] == 1
            else "미적용"
        )
    })

st.dataframe(
    pd.DataFrame(comparison_rows),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# 모델의 한계 및 해석
# --------------------------------------------------

st.markdown("---")
st.header("7. 모델 해석 및 한계")

st.write("""
- 이 모델은 실제 건축물에서 해결 방안의 효과를 측정한 자료를 학습한 것이 아니다.
- 원인별 해결 방안은 직접 설정한 기준이며, 모델은 이 기준을 학습하고 재현한다.
- 학습 자료는 원인 7개이므로 데이터 수가 매우 적다.
- Leave-One-Out 교차 검증은 원인 하나씩을 제외하고 학습하는 방식이다. 따라서 학습 과정에서 보지 못한 원인을 예측하는 상황이 되어 점수가 낮게 나타날 수 있다.
- 그러므로 평가 점수는 실제 건축 현장에서의 해결 효과나 새로운 상황에 대한 일반화 성능을 증명하지 않는다.
""")

st.markdown("---")


# --------------------------------------------------
# 자료 출처
# --------------------------------------------------

st.subheader("📚 자료 출처")

st.markdown(
    "[한국환경공단 층간소음 원인별 분석 데이터](https://www.data.go.kr/data/15093156/fileData.do)"
)

st.caption(
    "※ 본 웹앱은 2012~2024년 층간소음 원인별 발생 데이터를 활용하였습니다. "
    "건축적 해결 방안 연결 기준은 탐구를 위해 직접 설정하였습니다."
)
