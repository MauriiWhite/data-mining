import pandas as pd

from metrics.statistics import metrics

FILE = "data/films.csv"

def main():
    df = pd.read_csv(FILE)
    df = df.dropna()
    metrics(df)
    
    
if __name__ == "__main__":
    main()
