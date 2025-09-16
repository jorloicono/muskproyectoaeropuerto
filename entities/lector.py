import os
import json
import pandas as pd


class Lector:
    def __init__(self, path: str):
        self.path = path

    def _comprueba_extension(self, extension):
        _, ext = os.path.splitext(self.path)
        if ext.lower() != f".{extension.lower()}":
            raise ValueError(f"Extensión esperada .{extension} para el archivo {self.path}")

    def lee_archivo(self):
        raise NotImplementedError

    @staticmethod
    def convierte_dict_a_csv(data: dict):
        return pd.DataFrame(data)


class LectorCSV(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self, datetime_columns=[]):
        self._comprueba_extension('csv')
        df = pd.read_csv(self.path)
        for col in datetime_columns or []:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        return df


class LectorJSON(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self):
        self._comprueba_extension('json')
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)


class LectorTXT(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self):
        self._comprueba_extension('txt')
        rows = []
        with open(self.path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        # Saltar cabecera
        for line in lines[1:]:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) != 5:
                continue
            _id, fecha_llegada, retraso, tipo_vuelo, destino = parts
            rows.append({
                'id': _id,
                'fecha_llegada': fecha_llegada,
                'retraso': retraso,
                'tipo_vuelo': tipo_vuelo,
                'destino': destino.replace(' ', '')
            })
        return rows






