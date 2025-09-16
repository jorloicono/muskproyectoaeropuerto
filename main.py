import os


def preprocess_data(df_list):
    """Ejemplo de preprocesamiento: combina varias tablas en una sola."""
    if not df_list:
        return None

    # Por simplicidad, asumimos que los dataframes tienen las mismas columnas y los concatenamos
    import pandas as pd

    df_combinado = pd.concat(df_list, ignore_index=True)
    return df_combinado


if __name__ == '__main__':
    path_1 = os.path.abspath('./data/vuelos_1.txt')
    path_2 = os.path.abspath('./data/vuelos_2.csv')
    path_3 = os.path.abspath('./data/vuelos_3.json')








