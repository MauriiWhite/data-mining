import pandas as pd

FILE = "data/films.csv"

def main():
    df = pd.read_csv(FILE)
    df = df.dropna()
    print(df)

if __name__ == "__main__":
    main()
