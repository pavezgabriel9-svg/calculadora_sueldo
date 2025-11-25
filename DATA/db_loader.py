# SERVICE/db_loader.py
import pyodbc
import os
import json
#import math
from dotenv import load_dotenv
from DATA import data

load_dotenv(override=True)

CACHE_FILE = "cache_config.json"
MAX_JSON_NUMBER = 999999999999.0 

def guardar_cache_local(datos_dict):
    """
    Guarda la configuración exitosa en un archivo JSON local.
    Convierte 'inf' a un número finito para cumplir el estándar JSON.
    """
    try:
        # Hacemos una copia profunda para no modificar los datos en memoria
        datos_seguros = json.loads(json.dumps(datos_dict, default=lambda x: MAX_JSON_NUMBER if x == float('inf') else x))
        
        # Segunda pasada manual por seguridad si json.dumps no capturó todo (por ej en listas anidadas)
        # Especialmente para tramos
        if 'tramos_default' in datos_seguros:
            for tramo in datos_seguros['tramos_default']:
                if tramo['hasta'] == float('inf') or tramo['hasta'] >= MAX_JSON_NUMBER:
                    tramo['hasta'] = MAX_JSON_NUMBER

        with open(CACHE_FILE, 'w') as f:
            json.dump(datos_seguros, f, indent=4)
        print("💾 Configuración guardada en caché local (JSON Seguro).")
    except Exception as e:
        print(f"⚠️ No se pudo escribir caché local: {e}")

def cargar_desde_cache():
    """Intenta cargar la configuración desde el archivo JSON local"""
    if not os.path.exists(CACHE_FILE):
        return False
        
    print("📂 Cargando desde caché local...")
    try:
        with open(CACHE_FILE, 'r') as f:
            raw_data = json.load(f)
            aplicar_datos_a_memoria(raw_data)
            data.ESTADO_CONEXION = "OFFLINE (Caché)"
            data.MENSAJE_ESTADO = "Modo Offline (Datos Guardados)"
            return True
    except Exception as e:
        print(f"❌ Error leyendo caché: {e}")
        return False

def aplicar_datos_a_memoria(raw_data):
    """Lógica común para inyectar datos al módulo data"""
    
    # --- 1. ACTUALIZAR VARIABLES GLOBALES ---
    data.VALOR_UF_ACTUAL = float(raw_data.get('VALOR_UF_ACTUAL', data.VALOR_UF_ACTUAL))
    data.SUELDO_MINIMO = int(raw_data.get('SUELDO_MINIMO', data.SUELDO_MINIMO))
    data.TOPE_IMPONIBLE_AFP_SALUD = float(raw_data.get('TOPE_IMPONIBLE_AFP_SALUD', data.TOPE_IMPONIBLE_AFP_SALUD))
    data.TOPE_IMPONIBLE_CESANTIA = float(raw_data.get('TOPE_IMPONIBLE_CESANTIA', data.TOPE_IMPONIBLE_CESANTIA))
    data.DEFAULT_PLAN_ISAPRE_UF = float(raw_data.get('DEFAULT_PLAN_ISAPRE_UF', data.DEFAULT_PLAN_ISAPRE_UF))

    # --- 2. ACTUALIZAR DICCIONARIO AFP ---
    if 'TASAS_AFP' in raw_data:
        data.TASAS_AFP = raw_data['TASAS_AFP']

    # --- 3. ACTUALIZAR TRAMOS (Con restauración de infinito) ---
    if 'tramos_default' in raw_data:
        tramos_limpios = []
        for t in raw_data['tramos_default']:
            hasta = float(t['hasta'])
            # Restaurar infinito si es el número gigante
            if hasta >= MAX_JSON_NUMBER:
                hasta = float('inf')
            
            tramos_limpios.append({
                "desde": float(t['desde']),
                "hasta": hasta,
                "tasa": float(t['tasa']),
                "rebaja": float(t['rebaja'])
            })
        data.tramos_default = tramos_limpios

    # --- 4. ACTUALIZAR PARAMETROS DICT ---
    data.parametros_default.update({
        "ingreso_minimo": data.SUELDO_MINIMO,
        "valor_uf": data.VALOR_UF_ACTUAL,
        "tope_imponible_uf": data.TOPE_IMPONIBLE_AFP_SALUD,
        "tope_cesantia_uf": data.TOPE_IMPONIBLE_CESANTIA,
        "tasa_afp": data.TASAS_AFP.get('Uno', 0.1049),
        "tasa_salud": data.parametros_default['tasa_salud'],
        "tasa_cesant": data.parametros_default['tasa_cesant']
    })

def actualizar_configuracion_desde_db():
    print("🔄 Intentando conectar a Base de Datos...")
    conn_str = os.getenv('DB_CONNECTION_STRING')
    query = os.getenv('DB_QUERY_CONFIG')

    if not conn_str:
        print("⚠️ Sin conexión configurada. Intentando caché...")
        if not cargar_desde_cache():
            data.ESTADO_CONEXION = "OFFLINE (Default)"
            data.MENSAJE_ESTADO = "Usando valores de fábrica"
        return

    try:
        with pyodbc.connect(conn_str, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            datos_para_cache = {}

            raw_map = {row.ConfigKey: row for row in rows}
            datos_para_cache['VALOR_UF_ACTUAL'] = float(raw_map['VALOR_UF_ACTUAL'].val_Main)
            datos_para_cache['SUELDO_MINIMO'] = int(raw_map['SUELDO_MINIMO'].val_Main)
            datos_para_cache['TOPE_IMPONIBLE_AFP_SALUD'] = float(raw_map['TOPE_IMPONIBLE_AFP_SALUD'].val_Main)
            datos_para_cache['TOPE_IMPONIBLE_CESANTIA'] = float(raw_map['TOPE_IMPONIBLE_CESANTIA'].val_Main)
            datos_para_cache['DEFAULT_PLAN_ISAPRE_UF'] = float(raw_map['DEFAULT_PLAN_ISAPRE_UF'].val_Main)
            
            # AFPs
            afps = {}
            for row in rows:
                if row.Category == 'AFP':
                    name = row.ConfigKey.replace('AFP_', '').capitalize()
                    if name == 'Planvital': name = 'PlanVital'
                    if name == 'Provida': name = 'Provida' 
                    afps[name] = float(row.val_Main)
            datos_para_cache['TASAS_AFP'] = afps

            # Tramos
            tramos = []
            tramos_rows = sorted([r for r in rows if r.Category == 'IMPUESTO'], key=lambda x: x.ConfigKey)
            for t in tramos_rows:
                hasta = float(t.val_Aux1)
                # MANTENEMOS INFINITO EN MEMORIA
                if hasta > 900_000_000: hasta = float('inf')
                
                tramos.append({
                    "desde": float(t.val_Main),
                    "hasta": hasta,
                    "tasa": float(t.val_Aux2),
                    "rebaja": float(t.val_Aux3)
                })
            datos_para_cache['tramos_default'] = tramos

            # APLICAR Y GUARDAR
            aplicar_datos_a_memoria(datos_para_cache)
            
            # 2. Guardamos en disco, la función se encargará de cambiar 'inf' por el número gigante
            guardar_cache_local(datos_para_cache)
            
            data.ESTADO_CONEXION = "ONLINE"
            data.MENSAJE_ESTADO = "Conectado a IARRHH"
            print("✅ Datos actualizados y cacheados.")

    except Exception as e:
        print(f"⚠️ Error conexión BD: {e}")
        print("🔄 Intentando usar caché local...")
        if not cargar_desde_cache():
            data.ESTADO_CONEXION = "OFFLINE (Default)"
            data.MENSAJE_ESTADO = "Usando valores de fábrica"