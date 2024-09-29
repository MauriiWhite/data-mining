import pandas as pd

from pandas.core.frame import DataFrame

def metrics(df: DataFrame) -> None:
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['ventas'] = df['precio'] * df['cantidad']
    total_ventas = df['ventas'].sum()
    numero_transacciones = len(df)
    
    print(f"Total de ventas: {total_ventas}")
    print(f"Número de transacciones: {numero_transacciones}")
    print(f"Promedio de ventas por transacción: {total_ventas / numero_transacciones}")
    print(f"Máximo de ventas por transacción: {df['ventas'].max()}")
    print(f"Mínimo de ventas por transacción: {df['ventas'].min()}")

if __name__ == "__main__":
    metrics()