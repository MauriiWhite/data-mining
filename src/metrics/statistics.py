import pandas as pd

from pandas.core.frame import DataFrame

def metrics(df: DataFrame) -> dict:
    sells = df['sells'].sum()
    transactions = len(df)
    movies = df['pelicula'].nunique()
    payments = len(df['metodo_pago'].unique())
    date_range = (df['fecha'].max() - df['fecha'].min()).days
    
    
    return {
        'sells': sells,
        'transactions': transactions,
        'average_sells': round(sells / transactions, 2),
        'max_sells': df['sells'].max(),
        'min_sells': df['sells'].min(),
        'movies': movies,
        'date_range': date_range,
        'payments': payments,
        'start_date': df['fecha'].min().date(),
        'end_date': df['fecha'].max().date(),
    }
    

def film_metrics(df: DataFrame) -> dict:
    films = df.groupby('pelicula')
    
    sells_by_film = round(films['sells'].sum(), 1).to_dict()
    media_price_by_film = round(films['precio'].mean(), 1).to_dict()
    amount_by_film = round(films['pelicula'].count(), 1).to_dict()
    film_max_sells = films['cantidad'].sum().idxmax()
    film_min_sells = films['sells'].sum().idxmin()
    
    return {
        'sells_by_film': sells_by_film,
        'media_price_by_film': media_price_by_film,
        'amount_by_film': amount_by_film,
        'film_max_sells': film_max_sells,
        'film_min_sells': film_min_sells
    }

def gender_metrics(df: DataFrame) -> dict:
    gender = df.groupby('genero')
    
    sells_by_gender = round(gender['sells'].sum(), 1).to_dict()
    media_price_by_gender = round(gender['precio'].mean(), 1).to_dict()
    amount_by_gender = round(gender['genero'].count(), 1).to_dict()
    gender_max_sells = gender['sells'].sum().idxmax()
    gender_min_sells = gender['sells'].sum().idxmin()
    
    return {
        'sells_by_gender': sells_by_gender,
        'media_price_by_gender': media_price_by_gender,
        'amount_by_gender': amount_by_gender,
        'gender_max_sells': gender_max_sells,
        'gender_min_sells': gender_min_sells
    }
    

def payment_metrics(df: DataFrame) -> dict:
    payment = df.groupby('metodo_pago')
    
    sells_by_payment = round(payment['sells'].sum(), 1).to_dict()
    media_price_by_payment = round(payment['precio'].mean(), 1).to_dict()
    amount_by_payment = round(payment['metodo_pago'].count(), 1).to_dict()
    payment_max_sells = payment['sells'].sum().idxmax()
    payment_min_sells = payment['sells'].sum().idxmin()
    
    # 15. Número de Transacciones con Error (asumiendo que los errores se marcan como NaN)
    number_of_errors = df[df['sells'].isna()].shape[0]
    
    proportion_of_errors = round(number_of_errors / len(df) * 100, 1) if number_of_errors > 0 else 0
    
    
    return {
        'sells_by_payment': sells_by_payment,
        'media_price_by_payment': media_price_by_payment,
        'amount_by_payment': amount_by_payment,
        'payment_max_sells': payment_max_sells,
        'payment_min_sells': payment_min_sells,
        'number_of_errors': number_of_errors,
        'proportion_of_errors': proportion_of_errors
    }
    
def time_metrics(df: DataFrame) -> dict:
    df['fecha'] = pd.to_datetime(df['fecha'])
    date = df.groupby(df['fecha'].dt.to_period('M'))
    
    sells_by_month = round(date['sells'].sum(), 1).to_dict()
    media_price_by_month = round(date['precio'].mean(), 1).to_dict()
    amount_by_month = round(date['fecha'].count(), 1).to_dict()
    month_max_sells = date['sells'].sum().idxmax()
    month_min_sells = date['sells'].sum().idxmin()
    
    return {
        'sells_by_month': sells_by_month,
        'media_price_by_month': media_price_by_month,
        'amount_by_month': amount_by_month,
        'month_max_sells': month_max_sells,
        'month_min_sells': month_min_sells
    }
