# ETL_polimedicados.py

from faker import Faker           # Generación de datos sintéticos “realistas”
from db_config import get_engine  # Importamos la función get_engine() para conectarnos a PostgreSQL
import pandas as pd               # Librería para manipular y analizar datos en estructuras tipo DataFrame
import numpy as np                # Funciones y estructuras para cálculos numéricos (generadores aleatorios, etc)
import random                     # Librería para generar números y selecciones aleatorias
import psycopg2                   # Driver para PostgreSQL. SQLAlchemy ya lo importa internamente.
from sqlalchemy import create_engine  # En el flujo usamos get_engine(), que internamente llama a create_engine()
from ydata_profiling import ProfileReport  # Generación de informes de la calidad y distribución de los DataFrames
from datetime import datetime, timedelta   # Importa funciones generar o manipular fechas
                    

fake = Faker()       # Para llamar a métodos como fake.date_between() entre otros
np.random.seed(42)   # Establece la semilla aleatoria (“seed”) para NumPy y para el módulo random de Python
random.seed(42)      # garantizando que cada vez ejecutemos el script obtengamos los mismos valores aleatorios, 
                     # fundamental para reproducibilidad en pruebas                     


# --- Extracción ---
def generar_pacientes(n=100):
    data = []
    for _ in range(n):
        rango_edad = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
        genero = np.random.choice(['M', 'F', 'O'], p=[0.48, 0.51, 0.01])
        data.append({'rango_edad': rango_edad, 'genero': genero})
    return pd.DataFrame(data)

def generar_medicamentos():
    medicamentos = [
        {'codigo_atc': 'C10AA05', 'principio_activo': 'Atorvastatina'},
        {'codigo_atc': 'A10AB05', 'principio_activo': 'Insulina humana'},
        {'codigo_atc': 'N03AX12', 'principio_activo': 'Levetiracetam'},
        {'codigo_atc': 'R06AE07', 'principio_activo': 'Loratadina'},
        {'codigo_atc': 'J01MA02', 'principio_activo': 'Ciprofloxacino'},
        {'codigo_atc': 'J05AE01', 'principio_activo': 'Zidovudina'},
        {'codigo_atc': 'B03BA03', 'principio_activo': 'Cianocobalamina'},
        {'codigo_atc': 'H03AA01', 'principio_activo': 'Levotiroxina'},
        {'codigo_atc': 'N06AX11', 'principio_activo': 'Sertralina'},
        {'codigo_atc': 'A04AA01', 'principio_activo': 'Metoclopramida'},
        {'codigo_atc': 'C03CA01', 'principio_activo': 'Furosemida'},
        {'codigo_atc': 'C09AA05', 'principio_activo': 'Ramipril'},
        {'codigo_atc': 'C07AB02', 'principio_activo': 'Metoprolol'},
        {'codigo_atc': 'B01AA03', 'principio_activo': 'Warfarina'},
        {'codigo_atc': 'C08CA05', 'principio_activo': 'Amlodipino'},
        {'codigo_atc': 'N06AB03', 'principio_activo': 'Fluoxetina'},
        {'codigo_atc': 'N05BA06', 'principio_activo': 'Lorazepam'},
        {'codigo_atc': 'N02BE01', 'principio_activo': 'Paracetamol'},
        {'codigo_atc': 'N02AA01', 'principio_activo': 'Morfina'},
        {'codigo_atc': 'N06DA02', 'principio_activo': 'Donepezilo'},
        {'codigo_atc': 'A02BC02', 'principio_activo': 'Omeprazol'},
        {'codigo_atc': 'A06AD11', 'principio_activo': 'Lactulosa'},
        {'codigo_atc': 'A02BA02', 'principio_activo': 'Ranitidina'},
        {'codigo_atc': 'J01CR02', 'principio_activo': 'Amoxicilina/Ácido clavulánico'},
        {'codigo_atc': 'J01FA09', 'principio_activo': 'Claritromicina'},
        {'codigo_atc': 'J01XE01', 'principio_activo': 'Nitrofurantoína'},
        {'codigo_atc': 'H02AB06', 'principio_activo': 'Prednisona'},
        {'codigo_atc': 'M01AE01', 'principio_activo': 'Ibuprofeno'},
        {'codigo_atc': 'R03AC02', 'principio_activo': 'Salbutamol'},
        {'codigo_atc': 'A10BA02', 'principio_activo': 'Metformina'}
    ]
    return pd.DataFrame(medicamentos)

def generar_rams():
    rams = [
        {'codigo_cie': 'Y40.0', 'reaccion_adversa': 'Hemorragia digestiva'},
        {'codigo_cie': 'Y57.1', 'reaccion_adversa': 'Úlcera gástrica'},
        {'codigo_cie': 'Y45.1', 'reaccion_adversa': 'Diarrea medicamentosa'},
        {'codigo_cie': 'Y44.2', 'reaccion_adversa': 'Hipotensión'},
        {'codigo_cie': 'Y52.7', 'reaccion_adversa': 'Arritmia cardíaca'},
        {'codigo_cie': 'Y45.0', 'reaccion_adversa': 'Hemorragia intracraneal'},
        {'codigo_cie': 'Y49.0', 'reaccion_adversa': 'Somnolencia'},
        {'codigo_cie': 'Y49.3', 'reaccion_adversa': 'Convulsiones'},
        {'codigo_cie': 'Y46.5', 'reaccion_adversa': 'Delirio'},
        {'codigo_cie': 'Y54.5', 'reaccion_adversa': 'Insuficiencia renal aguda'},
        {'codigo_cie': 'Y54.6', 'reaccion_adversa': 'Alteraciones electrolíticas'},
        {'codigo_cie': 'Y44.9', 'reaccion_adversa': 'Hepatotoxicidad'},
        {'codigo_cie': 'Y45.5', 'reaccion_adversa': 'Ictericia'},
        {'codigo_cie': 'Y44.3', 'reaccion_adversa': 'Anemia'},
        {'codigo_cie': 'Y44.4', 'reaccion_adversa': 'Leucopenia'},
        {'codigo_cie': 'Y46.0', 'reaccion_adversa': 'Erupción cutánea'},
        {'codigo_cie': 'Y46.1', 'reaccion_adversa': 'Prurito'},
        {'codigo_cie': 'Y57.0', 'reaccion_adversa': 'Hipoglucemia'},
        {'codigo_cie': 'Y54.2', 'reaccion_adversa': 'Retención urinaria'},
        {'codigo_cie': 'Y55.0', 'reaccion_adversa': 'Tinnitus'},
        {'codigo_cie': 'Y44.5', 'reaccion_adversa': 'Mialgia'},
        {'codigo_cie': 'Y45.7', 'reaccion_adversa': 'Hiponatremia'},
        {'codigo_cie': 'Y42.0', 'reaccion_adversa': 'Hiperprolactinemia'},
        {'codigo_cie': 'Y52.8', 'reaccion_adversa': 'Prolongación del QT'},
        {'codigo_cie': 'Y43.0', 'reaccion_adversa': 'Fotosensibilidad'},
        {'codigo_cie': 'Y53.7', 'reaccion_adversa': 'Neuropatía periférica'},
        {'codigo_cie': 'Y51.9', 'reaccion_adversa': 'Rabdomiólisis'},
        {'codigo_cie': 'Y57.3', 'reaccion_adversa': 'Hipotiroidismo'},
        {'codigo_cie': 'Y40.8', 'reaccion_adversa': 'Acatisia'},
        {'codigo_cie': 'Y49.8', 'reaccion_adversa': 'Disfunción sexual'}
    ]
    return pd.DataFrame(rams)

def generar_ingresos(pacientes_df):
    ingresos = []
    for i, row in pacientes_df.iterrows():
        fecha_ingreso = fake.date_between_dates(date_start=datetime(2024, 1, 1), date_end=datetime(2025, 6, 1))
        # La fecha de alta se ajustará más adelante en función de la gravedad de las RAMs
        fecha_alta = fecha_ingreso + timedelta(days=1)  # Valor temporal
        ingresos.append({'id_paciente': i+1, 'fecha_ingreso': fecha_ingreso, 'fecha_alta': fecha_alta})
    return pd.DataFrame(ingresos)

def generar_tratamientos(ingresos_df, medicamentos_df):
    tratamientos = []
    for i, ingreso in ingresos_df.iterrows():
        n_meds = random.randint(5, 8)  # Entre 5 y 8 medicamentos
        # Usar el índice del DataFrame + 1 (para alinearse con IDs 1, 2, 3... en PostgreSQL)
        med_ids = random.sample(range(1, len(medicamentos_df) + 1), n_meds)  # IDs 1 a N
        for med_id in med_ids:
            dosis = random.choice(['Baja', 'Media', 'Alta'])
            fecha_inicio = ingreso['fecha_ingreso'] - timedelta(days=random.randint(0, 5))
            fecha_fin = ingreso['fecha_ingreso'] + timedelta(days=random.randint(1, (ingreso['fecha_alta'] - ingreso['fecha_ingreso']).days))
            
            tratamientos.append({
                'id_ingreso': i + 1,
                'id_medicamento': med_id,  # Usamos el ID generado automáticamente (índice + 1)
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'dosis': dosis
            })
    return pd.DataFrame(tratamientos)

def generar_rams_ingreso(ram_df, ingresos_df, tratamientos_df, medicamentos_df):
    ram_ingresos = []

    # Asegurarnos de tener identificadores
    if 'id_medicamento' not in medicamentos_df.columns:
        medicamentos_df['id_medicamento'] = medicamentos_df.index + 1
    if 'id_ram' not in ram_df.columns:
        ram_df['id_ram'] = ram_df.index + 1
    if 'id_ingreso' not in ingresos_df.columns:
        ingresos_df['id_ingreso'] = ingresos_df.index + 1

    # Mapas para acceso rápido
    med_map = medicamentos_df.set_index('id_medicamento')['principio_activo'].to_dict()
    ram_map = ram_df.set_index('reaccion_adversa')['id_ram'].to_dict()

    interacciones_conocidas = {
        ('Warfarina', 'Ibuprofeno'): ('Hemorragia digestiva', 'Grave'),
        ('Warfarina', 'Amoxicilina/Ácido clavulánico'): ('Hemorragia digestiva', 'Grave'),
        ('Metoprolol', 'Fluoxetina'): ('Arritmia cardíaca', 'Grave'),
        ('Ramipril', 'Ibuprofeno'): ('Insuficiencia renal aguda', 'Moderada'),
        ('Furosemida', 'Ibuprofeno'): ('Alteraciones electrolíticas', 'Moderada'),
        ('Furosemida', 'Prednisona'): ('Alteraciones electrolíticas', 'Moderada'),
        ('Metformina', 'Omeprazol'): ('Hipoglucemia', 'Moderada'),
        ('Paracetamol', 'Amoxicilina/Ácido clavulánico'): ('Hepatotoxicidad', 'Grave'),
        ('Amlodipino', 'Metoprolol'): ('Hipotensión', 'Moderada'),
        ('Donepezilo', 'Fluoxetina'): ('Convulsiones', 'Grave'),
        ('Lorazepam', 'Fluoxetina'): ('Somnolencia', 'Leve'),
        ('Paracetamol', 'Warfarina'): ('Hemorragia digestiva', 'Grave'),
        ('Ibuprofeno', 'Ramipril'): ('Insuficiencia renal aguda', 'Moderada'),
        ('Ranitidina', 'Ketoconazol'): ('Alteraciones electrolíticas', 'Moderada'),
        ('Atorvastatina', 'Ciprofloxacino'): ('Rabdomiólisis', 'Grave')
    }

    # Generar RAMs por ingreso
    for ingreso_id in ingresos_df['id_ingreso']:
        meds_ingreso = tratamientos_df[tratamientos_df['id_ingreso'] == ingreso_id]['id_medicamento'].tolist()
        principios = [med_map[med_id] for med_id in meds_ingreso]

        interacciones = set()
        for i in range(len(principios)):
            for j in range(i+1, len(principios)):
                par = (principios[i], principios[j])
                rev_par = (principios[j], principios[i])
                interaccion = interacciones_conocidas.get(par) or interacciones_conocidas.get(rev_par)
                if interaccion:
                    interacciones.add(interaccion)

        for ram_nombre, gravedad in interacciones:
            if ram_nombre in ram_map:
                ram_ingresos.append({
                    'id_ingreso': ingreso_id,
                    'id_ram': ram_map[ram_nombre],
                    'gravedad': gravedad
                })

        # RAM aleatoria si no hay interacciones
        if random.random() < 0.3 and not interacciones:
            ram_row = ram_df.sample(1).iloc[0]
            gravedad = random.choice(['Leve', 'Moderada', 'Grave'])
            ram_ingresos.append({
                'id_ingreso': ingreso_id,
                'id_ram': ram_row['id_ram'],
                'gravedad': gravedad
            })

    # --- Vectorizado: ajustar fecha_alta según gravedad ---
    ram_ingresos_df = pd.DataFrame(ram_ingresos)

    if ram_ingresos_df.empty:
        # Si no hay RAMs, devolver ingreso original
        return ram_ingresos_df, ingresos_df.copy()

    gravedad_peso = {'Leve': 1, 'Moderada': 2, 'Grave': 3}
    ram_ingresos_df['nivel'] = ram_ingresos_df['gravedad'].map(gravedad_peso)

    # Obtener RAM más grave por ingreso
    max_gravedad_df = ram_ingresos_df.sort_values('nivel', ascending=False).drop_duplicates('id_ingreso')

    # Asignar días extra
    def dias_extra(gravedad):
        if gravedad == 'Grave':
            return random.choice([7, 14, 21])
        elif gravedad == 'Moderada':
            return random.choice([3, 5, 7])
        else:
            return random.choice([1, 2])

    max_gravedad_df['dias_extra'] = max_gravedad_df['gravedad'].apply(dias_extra)

    # Crear copia de ingresos y unir días extra
    ingresos_actualizado = ingresos_df.copy()
    ingresos_actualizado = ingresos_actualizado.merge(
        max_gravedad_df[['id_ingreso', 'dias_extra']],
        on='id_ingreso',
        how='left'
    )

    ingresos_actualizado['dias_extra'] = ingresos_actualizado['dias_extra'].fillna(0).astype(int)

    ingresos_actualizado['fecha_alta'] = ingresos_actualizado.apply(
        lambda row: row['fecha_ingreso'] + timedelta(days=max(row['dias_extra'], 1)),
        axis=1
    )
    return ram_ingresos_df.drop(columns='nivel'), ingresos_actualizado


# --- Transformación ---
def anonimizar_ingresos(ingresos_df, max_dias_shift=60, seed=42):
    """
    Aplica un desplazamiento aleatorio a las fechas de ingreso y alta 
    preservando la duración real del ingreso, pero ocultando la fecha exacta.

    Parámetros:
    - ingresos_df: DataFrame con columnas 'fecha_ingreso' y 'fecha_alta'
    - max_dias_shift: máximo desplazamiento en días (+/-)
    - seed: para reproducibilidad del random

    Retorna:
    - DataFrame con fechas desplazadas pero estructura temporal conservada.
    """
    np.random.seed(seed)
    ingresos_actualizado = ingresos_df.copy()

    # Convertir columnas de fecha a datetime
    ingresos_actualizado['fecha_ingreso'] = pd.to_datetime(ingresos_actualizado['fecha_ingreso'])
    ingresos_actualizado['fecha_alta'] = pd.to_datetime(ingresos_actualizado['fecha_alta'])

    # Generar desplazamientos aleatorios en días
    shifts = np.random.randint(-max_dias_shift, max_dias_shift + 1, size=len(ingresos_actualizado))

    # Sumar desplazamientos como Timedelta, operación vectorizada
    ingresos_actualizado['fecha_ingreso'] += pd.to_timedelta(shifts, unit='D')
    ingresos_actualizado['fecha_alta'] += pd.to_timedelta(shifts, unit='D')

    return ingresos_actualizado


def validar_datos(df_dict):
    for name, df in df_dict.items():
        print(f"\n🔍 Perfilando: {name}")
        profile = ProfileReport(df, minimal=True)
        profile.to_file(f"{name}_profile.html")


# --- Carga ---
def cargar_a_postgres(engine, dfs):
    # Paso 1: insertar Pacientes primero, en su propia transacción
    with engine.begin() as conn:
        dfs['pacientes'].to_sql("Pacientes", conn, index=False, if_exists='append')

    # Paso 2: insertar el resto en una transacción separada
    with engine.begin() as conn:
        # Medicamentos
        medicamentos_df = dfs['medicamentos'].drop(columns=['id_medicamento'], errors='ignore')
        medicamentos_df.to_sql("Medicamentos", conn, index=False, if_exists='append')

        # Ingresos (eliminamos antes de insertar, las columnas id_ingreso y días_extra antes de insertar)
        ingresos_df = dfs['ingresos'].drop(columns=['id_ingreso', 'dias_extra'], errors='ignore')
        ingresos_df.to_sql("Ingresos", conn, index=False, if_exists='append')

        # Tratamientos
        dfs['tratamientos'].to_sql("Tratamientos", conn, index=False, if_exists='append')

        # RAM
        ram_df = dfs['ram'].drop(columns=['id_ram'], errors='ignore')
        ram_df.to_sql("Ram", conn, index=False, if_exists='append')

        # RAM-Ingreso
        dfs['ram_ingreso'].to_sql("Ram_Ingreso", conn, index=False, if_exists='append')


# --- Orquestación ---
def run_etl():
    pacientes = generar_pacientes()
    medicamentos = generar_medicamentos()
    ingresos = generar_ingresos(pacientes)
    tratamientos = generar_tratamientos(ingresos, medicamentos)
    ram = generar_rams()
    # CAMBIO: ahora obtenemos dos DataFrames
    ram_ingreso, ingresos_actualizado = generar_rams_ingreso(ram, ingresos, tratamientos, medicamentos)


    validar_datos({
        # Descomentar para depurar
        'pacientes': pacientes,
        'ingresos': ingresos_actualizado,
        'tratamientos': tratamientos,
        'ram': ram,
        'ram_ingreso': ram_ingreso
    })

    # Anonimizamos fechas de ingresos
    # ingresos_actualizado = anonimizar_ingresos(ingresos_actualizado, max_dias_shift=60, seed=42)
    
    # SQLAlchemy se encarga de insertar los datos de los DataFrames en la base de datos PostgreSQL
    # Variable engine para ejecutar consultas SQL, cargar Dataframes df.to_sql(...) o leer tablas pd.read_sql(...)
    engine = get_engine()

    # CAMBIO: usamos ingresos_actualizado, no ingresos
    cargar_a_postgres(engine, {
        'pacientes': pacientes,
        'medicamentos': medicamentos,
        'ingresos': ingresos_actualizado,
        'tratamientos': tratamientos,
        'ram': ram,
        'ram_ingreso': ram_ingreso        
    })
 
if __name__ == "__main__":
    run_etl()
