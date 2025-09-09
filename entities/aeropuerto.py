import pandas as pd

from slot import Slot


class Aeropuerto:
    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = {}
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(1, self.n_slots + 1):
            self.slots[i] = Slot()

        self.df_vuelos['fecha_despegue'] = pd.NaT
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row) -> pd.Series:
        pass

    def encuentra_slot(self, fecha_vuelo) -> int:
        pass

    def asigna_slot(self, vuelo) -> pd.Series:
        pass

    def asigna_slots(self):
        pass







