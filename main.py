
# 세 번째 그래프: 전체 기간 원인별 발생 횟수
st.divider()

st.subheader("📊 전체 기간 층간소음 원인별 발생 횟수")

st.write(
    "2012년부터 2024년까지의 발생 횟수를 원인별로 합산하여 "
    "전체 기간 동안 어떤 원인으로 층간소음이 많이 발생했는지 비교합니다."
)

# 전체 기간의 원인별 발생 횟수 합산
total_cause_df = df[cause_cols].sum().reset_index()
total_cause_df.columns = ["소음 원인", "발생 횟수"]

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
- 기타 원인과 망치질도 전체 발생 횟수에서 큰 비중을 차지합니다.
- 악기 소리와 문 개폐는 상대적으로 적은 횟수를 기록했습니다.

이를 통해 전체 기간 동안 층간소음의 주요 원인이 무엇인지
한눈에 비교할 수 있습니다.
""")
