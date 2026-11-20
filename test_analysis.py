import pandas as pd
from analysis import 정제, 반별평균


본 = 정제(pd.read_csv("scores_2026.csv"))
미니 = 정제(pd.read_csv("mini.csv"))


def test_scores_2026을_정제하면_100행이_남는다():
    assert len(본) == 100


def test_정제후_반은_1반과_2반만_남는다():
    assert set(본["반"].unique()) == {"1반", "2반"}


def test_반별_점수합의_합은_전체_점수합과_같다():
    반별_점수합 = 본.groupby("반")["점수"].sum().sum()
    전체_점수합 = 본["점수"].sum()
    assert 반별_점수합 == 전체_점수합


def test_mini_정제후_1반_평균은_80이다():
    assert 반별평균(미니)["1반"] == 80.0