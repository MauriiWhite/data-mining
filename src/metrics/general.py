import pandas as pd


def main():
    df = pd.read_csv("data/films.csv")
    df = df.dropna()
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['ventas'] = df['precio'] * df['cantidad']
    total_ventas = df['ventas'].sum()
    numero_transacciones = len(df)
    
if __name__ == "__main__":
    main()
