import os
import pandas as pd
from entities.lector import LectorCSV, LectorJSON, LectorTXT
from entities.aeropuerto import Aeropuerto


def preprocess_data(df_list):
    """
    Combines multiple DataFrames and cleans the data.
    Converts date columns and handles missing values.
    """
    if not df_list:
        return pd.DataFrame()
    
    # Combine all DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Convert fecha_llegada to datetime if it's not already
    if 'fecha_llegada' in combined_df.columns:
        combined_df['fecha_llegada'] = pd.to_datetime(combined_df['fecha_llegada'])
    
    # Sort by arrival time
    combined_df = combined_df.sort_values('fecha_llegada').reset_index(drop=True)
    
    # Add index as flight order
    combined_df['orden_llegada'] = range(1, len(combined_df) + 1)
    
    return combined_df


if __name__ == '__main__':
    # File paths
    path_1 = os.path.abspath('./data/vuelos_1.txt')
    path_2 = os.path.abspath('./data/vuelos_2.csv')
    path_3 = os.path.abspath('./data/vuelos_3.json')
    
    print("=== Sistema de Gestión de Aeropuerto ===")
    print("Leyendo archivos de vuelos...")
    
    # Read flight data from all sources
    lector_txt = LectorTXT(path_1)
    lector_csv = LectorCSV(path_2)
    lector_json = LectorJSON(path_3)
    
    # Get data from each source
    vuelos_txt = lector_txt.lee_archivo()
    vuelos_csv = lector_csv.lee_archivo(datetime_columns=['fecha_llegada'])
    vuelos_json = lector_json.lee_archivo()
    
    # Convert to DataFrames
    df_txt = lector_txt.convierte_dict_a_csv(vuelos_txt)
    df_json = lector_json.convierte_dict_a_csv(vuelos_json)
    
    # Convert fecha_llegada to datetime for txt and json data
    df_txt['fecha_llegada'] = pd.to_datetime(df_txt['fecha_llegada'])
    df_json['fecha_llegada'] = pd.to_datetime(df_json['fecha_llegada'])
    
    print(f"Vuelos desde TXT: {len(df_txt)}")
    print(f"Vuelos desde CSV: {len(vuelos_csv)}")
    print(f"Vuelos desde JSON: {len(df_json)}")
    
    # Preprocess and combine all data
    all_flights = preprocess_data([df_txt, vuelos_csv, df_json])
    print(f"Total de vuelos: {len(all_flights)}")
    
    # Initialize airport with 5 slots, 1 hour for national, 2 hours for international
    aeropuerto = Aeropuerto(
        vuelos=all_flights,
        slots=5,
        t_embarque_nat=1,  # 1 hour for national flights
        t_embarque_internat=2  # 2 hours for international flights
    )
    
    print("\n=== Asignando slots a los vuelos ===")
    
    # Assign slots to all flights
    resultado = aeropuerto.asigna_slots()
    
    # Display results
    print("\n=== Resultados de la asignación ===")
    print(f"{'ID':<10} {'Llegada':<20} {'Despegue':<20} {'Tipo':<10} {'Destino':<15} {'Slot':<5}")
    print("-" * 85)
    
    for _, vuelo in resultado.iterrows():
        llegada_str = vuelo['fecha_llegada'].strftime('%Y-%m-%d %H:%M')
        despegue_str = vuelo['fecha_despegue'].strftime('%Y-%m-%d %H:%M') if pd.notna(vuelo['fecha_despegue']) else 'NO ASIGNADO'
        slot_str = str(vuelo['slot']) if vuelo['slot'] > 0 else 'NO'
        
        print(f"{vuelo['id']:<10} {llegada_str:<20} {despegue_str:<20} {vuelo['tipo_vuelo']:<10} {vuelo['destino']:<15} {slot_str:<5}")
    
    # Summary statistics
    asignados = len(resultado[resultado['slot'] > 0])
    no_asignados = len(resultado[resultado['slot'] == 0])
    
    print(f"\n=== Resumen ===")
    print(f"Vuelos asignados: {asignados}")
    print(f"Vuelos no asignados: {no_asignados}")
    print(f"Tasa de asignación: {asignados/len(resultado)*100:.1f}%")
    
    # Show slot utilization
    print(f"\n=== Utilización de slots ===")
    for slot_id in range(1, aeropuerto.n_slots + 1):
        vuelos_en_slot = resultado[resultado['slot'] == slot_id]
        if len(vuelos_en_slot) > 0:
            print(f"Slot {slot_id}: {len(vuelos_en_slot)} vuelo(s)")
        else:
            print(f"Slot {slot_id}: Libre")








