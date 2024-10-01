import pandas as pd

from pathlib import Path
from typing import Dict

from .statistics import (
    metrics,
    film_metrics,
    payment_metrics,
    gender_metrics,
)

DATA_FILE = Path("data/films.csv")


def load_data(file_path: Path = DATA_FILE) -> pd.DataFrame:
    """
    Carga y limpia el archivo CSV, eliminando valores faltantes y renombrando columnas.

    Args:
        file_path (Path): Ruta del archivo CSV.

    Returns:
        pd.DataFrame: DataFrame limpio con los datos transformados.
    """
    try:
        df = pd.read_csv(file_path).dropna()
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {file_path} no se encontró.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"El archivo {file_path} está vacío.")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo {file_path}: {e}")

    # Renombrar columnas
    df.rename(
        columns={
            "fecha": "date",
            "pelicula": "film",
            "genero": "gender",
            "precio": "price",
            "cantidad": "amount",
            "metodo_pago": "payment",
        },
        inplace=True,
    )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["sells"] = df["price"] * df["amount"]
    return df


def results() -> Dict[str, dict]:
    """
    Calcula diferentes métricas basadas en el DataFrame cargado desde el archivo CSV.

    Returns:
        dict: Diccionario con los resultados de las métricas generales, por película, método de pago, género y tiempo.
    """
    df = load_data(DATA_FILE)

    return {
        "general": metrics(df),
        "film": film_metrics(df),
        "payment": payment_metrics(df),
        "gender": gender_metrics(df),
    }
