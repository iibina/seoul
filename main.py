import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="서울 100년 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 100년 연평균 기온 변화")
st.write("1907년부터 최근까지 서울의 연평균 기온 변화를 그래프로 확인해 보세요.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

    # CP949 인코딩으로 읽기
    df = pd.read_csv(url, encoding="cp949")

    # 컬럼 이름 변경
    df.columns = ["날짜", "지점", "평균기온", "최저기온", "최고기온"]

    # 날짜 형식 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    # 평균기온 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 결측값 제거
    df = df.dropna(subset=["평균기온"])

    return df


df = load_data()

# -----------------------------
# 연평균 기온 계산
# -----------------------------
year_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

# -----------------------------
# 그래프 설정
# -----------------------------
plt.rcParams["font.family"] = "Malgun Gothic"   # Streamlit Cloud에서도 대부분 표시
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    year_temp["연도"],
    year_temp["평균기온"],
    color="tomato",
    linewidth=2.5
)

ax.fill_between(
    year_temp["연도"],
    year_temp["평균기온"],
    color="orange",
    alpha=0.2
)

ax.set_title("서울의 연평균 기온 변화 (1907~최근)", fontsize=18)
ax.set_xlabel("연도", fontsize=12)
ax.set_ylabel("연평균 기온 (℃)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

# -----------------------------
# 통계 정보
# -----------------------------
st.subheader("📊 간단한 통계")

col1, col2, col3 = st.columns(3)

col1.metric(
    "관측 시작 연도",
    f"{year_temp['연도'].min()}년"
)

col2.metric(
    "최근 연도",
    f"{year_temp['연도'].max()}년"
)

col3.metric(
    "전체 평균 기온",
    f"{year_temp['평균기온'].mean():.2f} ℃"
)

st.markdown("---")

st.subheader("📋 연도별 평균기온 데이터")
st.dataframe(year_temp, use_container_width=True)
