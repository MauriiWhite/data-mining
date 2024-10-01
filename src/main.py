import pandas as pd

from metrics.statistics import time_metrics
from pprint import pprint

FILE = "data/films.csv"


def main() -> None:
    df = pd.read_csv(FILE).dropna()

    df["fecha"] = pd.to_datetime(df["fecha"])
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df["sells"] = df["precio"] * df["cantidad"]

    pprint(time_metrics(df), sort_dicts=False)


if __name__ == "__main__":
    main()
