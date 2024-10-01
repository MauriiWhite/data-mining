import pandas as pd

from pandas.core.frame import DataFrame
from utils.decorators.time_it import time_it


def group_metrics(df: DataFrame, group_col: str) -> dict:
    """
    Calcula las siguientes métricas:
    - Cantidad de ventas por grupo
    - Precio medio por grupo
    - Cantidad de elementos por grupo
    - Valor maximo y minimo de ventas por grupo

    Args:
        df (DataFrame): Pandas DataFrame
        group_col (str): Columna por la que agrupar
    """

    group = df.groupby(group_col)

    sells_by_group = round(group["sells"].sum(), 1).to_dict()
    media_price_by_group = round(group["price"].mean(), 1).to_dict()
    amount_by_group = round(group[group_col].count(), 1).to_dict()
    group_max_sells = group["sells"].sum().idxmax()
    group_min_sells = group["sells"].sum().idxmin()

    return {
        f"sells_{group_col}": sells_by_group,
        f"media_price_{group_col}": media_price_by_group,
        f"amount_{group_col}": amount_by_group,
        f"{group_col}_max_sells": group_max_sells,
        f"{group_col}_min_sells": group_min_sells,
    }


@time_it
def metrics(df: DataFrame) -> dict:
    """
    Calcula las siguientes métricas:
    - Cantidad de ventas
    - Cantidad de transacciones
    - Cantidad de elementos unicos (peliculas)
    - Cantidad de distintos metodos de pago
    - Rango de tiempo (dias)

    Args:
        df (DataFrame): Pandas DataFrame
    """

    sells = df["sells"].sum()
    transactions = len(df)
    movies = df["film"].nunique()
    payments = len(df["payment"].unique())
    date_range = (df["date"].max() - df["date"].min()).days

    return {
        "sells": sells,
        "transactions": transactions,
        "average_sells": round(sells / transactions, 2),
        "max_sells": df["sells"].max(),
        "min_sells": df["sells"].min(),
        "movies": movies,
        "date_range": date_range,
        "payments": payments,
        "start_date": df["date"].min().date(),
        "end_date": df["date"].max().date(),
    }


@time_it
def film_metrics(df: DataFrame) -> dict:
    """
    Calcula las siguientes métricas:
    - Cantidad de ventas por película
    - Precio medio por película
    - Cantidad de elementos por película
    - Valor maximo y minimo de ventas por película

    Args:
        df (DataFrame): Pandas DataFrame
    """

    return group_metrics(df, "film")


@time_it
def gender_metrics(df: DataFrame) -> dict:
    """
    Calcula las siguientes métricas:
    - Cantidad de ventas por geño
    - Cantidad de elementos por geño
    - Valor maximo y minimo de ventas por geño

    Args:
        df (DataFrame): Pandas DataFrame

    Returns:
        dict: Diccionario con las siguientes llaves:
        - f"sells_gender": Cantidad de ventas por geño
        - f"amount_gender": Cantidad de elementos por geño
    """

    return group_metrics(df, "gender")


@time_it
def payment_metrics(df: DataFrame) -> dict:
    """
    Calcula las siguientes métricas:
    - Cantidad de ventas por metodo de pago
    - Cantidad de elementos por_MD de pago
    - Valor maximo y minimo de ventas por metodo de pago

    Args:
        df (DataFrame): Pandas DataFrame
    """

    metrics = group_metrics(df, "payment")

    number_of_errors = df[df["sells"].isna()].shape[0]
    proportion_of_errors = (
        round(number_of_errors / len(df) * 100, 1) if number_of_errors > 0 else 0
    )

    metrics.update(
        {
            "number_of_errors": number_of_errors,
            "proportion_of_errors": proportion_of_errors,
        }
    )

    return metrics


@time_it
def time_metrics(df: DataFrame) -> dict:
    """
    Calcula las siguientes métricas:
    - Cantidad de ventas por mes
    - Cantidad de elementos por mes
    - Valor maximo y minimo de ventas por mes

    Args:
        df (DataFrame): Pandas DataFrame
    """

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.date
    return group_metrics(df, "month")
