import pandas as pd
from datetime import timedelta
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
        if row['tipo_vuelo'] == 'NAT':
            fecha_despegue = row['fecha_llegada'] + timedelta(hours=self.tiempo_embarque_nat)
        else:
            fecha_despegue = row['fecha_llegada'] + timedelta(hours=self.tiempo_embarque_internat)
        return fecha_despegue

    def encuentra_slot(self, fecha_vuelo) -> int:
        """
        Encuentra un slot disponible para una fecha de vuelo específica.
        Retorna el ID del slot disponible o 0 si no hay slots disponibles.
        """
        for slot_id, slot in self.slots.items():
            if slot.slot_esta_libre_fecha_determinada(fecha_vuelo):
                return slot_id
        return 0  # No hay slots disponibles

    def asigna_slot(self, vuelo) -> pd.Series:
        """
        Asigna un slot a un vuelo específico.
        Calcula la fecha de despegue y encuentra un slot disponible.
        """
        # Calcular fecha de despegue
        fecha_despegue = self.calcula_fecha_despegue(vuelo)
        
        # Encontrar slot disponible
        slot_id = self.encuentra_slot(fecha_despegue)
        
        if slot_id > 0:
            # Asignar el vuelo al slot
            self.slots[slot_id].asigna_vuelo(
                vuelo['id'], 
                vuelo['fecha_llegada'], 
                fecha_despegue
            )
            
            # Actualizar el DataFrame
            vuelo['fecha_despegue'] = fecha_despegue
            vuelo['slot'] = slot_id
            
            return vuelo
        else:
            # No hay slots disponibles, marcar como no asignado
            vuelo['fecha_despegue'] = pd.NaT
            vuelo['slot'] = 0
            return vuelo

    def asigna_slots(self):
        """
        Asigna slots a todos los vuelos del DataFrame.
        Procesa los vuelos en orden de llegada.
        """
        # Ordenar vuelos por fecha de llegada
        self.df_vuelos = self.df_vuelos.sort_values('fecha_llegada')
        
        # Aplicar asignación de slots a cada vuelo
        for index, vuelo in self.df_vuelos.iterrows():
            vuelo_actualizado = self.asigna_slot(vuelo)
            self.df_vuelos.loc[index] = vuelo_actualizado
        
        return self.df_vuelos







