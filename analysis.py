
import pandas as pd


def 정제(df):
    # 원본을 직접 바꾸지 않고 복사본을 만든다.
    df = df.copy()

    print("시작:", len(df))

    # 1. 점수가 비어 있는 행 제거
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거:", len(df))

    # 2. 완전히 동일한 중복 행 제거
    df = df.drop_duplicates()
    print("중복 제거:", len(df))

   # 3. 반과 과목의 앞뒤 공백 제거
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()

    # 4. 점수가 0~100 범위 밖인 행 제거
    df = df[df["점수"].between(0, 100)]
    print("범위 밖 제거:", len(df))
    
    # 반별 인원 수와 점수 평균
    반별통계 = df.groupby("반").agg(인원=("점수", "count"), 평균=("점수", "mean"))
    print(반별통계)

    # 과목과 반별 인원 수와 점수 평균
    과목반별통계 = df.groupby(["과목", "반"]).agg(인원=("점수", "count"), 평균=("점수", "mean"))
    print(과목반별통계)

    return df

# 반별평균 함수 정의
def 반별평균(df):
    표 = df.groupby("반")["점수"].agg(
        개수="count",
        평균="mean",
        중앙값="median",
        최댓값="max"
    ).round(2)

    print(표)
    return 표["평균"]


# CSV 파일 불러오기
원본 = pd.read_csv("scores_2026.csv")

# 데이터 정제 실행
df = 정제(원본)

# 정제된 df로 반별 통계 실행
반별평균(df)


# CSV 파일 불러오기
원본 = pd.read_csv("scores_2026.csv")

# 데이터 정제 실행
df = 정제(원본)

# 정제된 데이터 저장
df.to_csv("scores_2026_cleaned.csv",
          index=False, encoding="utf-8-sig")

# 정제 결과 확인
print("\n정제 완료!")
print("최종 행 수:", len(df))

print("반 종류:", sorted(df["반"].unique()))
print("과목 종류:", sorted(df["과목"].unique()))

print("\n정제된 데이터:")
print(df.to_string(index=False))

print(df.groupby("반")["점수"].sum().sum())   # 7484.0
print(df["점수"].sum())                        # 7484.0   
print(df.groupby("반")["점수"].count().sum())  # 100
print(len(df))                                 # 100   
print(df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"])


import pandas as pd
from analysis import 정제, 반별평균

본 = 정제(pd.read_csv("scores_2026.csv"))
미니 = 정제(pd.read_csv("mini.csv"))
def test_정제하면_100행이_남는다():           # ① 행 수 보존
    assert len(본) == 100

def test_반은_두_종류만_남는다():             # ① 행 수 보존
    assert sorted(본["반"].unique()) == ["1반", "2반"]

def test_그룹합이_전체합과_같다():             # ② 합계 일치
    assert 본.groupby("반")["점수"].sum().sum() == 본["점수"].sum()

def test_손계산과_일치한다():                 # ③ 손계산 대조
    assert 반별평균(미니)["1 반"] == 80.0

print(반별평균(미니))