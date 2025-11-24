# SERVICE/db_loader.py
#import pyodbc
import pyodbc
import os
from dotenv import load_dotenv
from DATA import data

load_dotenv(override=True)

def actualizar_configuracion_desde_db():
    """
    Intenta conectarse a la BD usando la configuración del .env para actualizar 
    los valores de DATA/data.py.
    """
    print("🔄 Intentando conectar a Base de Datos...")
    
    # Recuperar configuración del .env
    conn_str = os.getenv('DB_CONNECTION_STRING')
    query = os.getenv('DB_QUERY_CONFIG')

    if not conn_str or not query:
        print("⚠️ Error: No se encontraron las variables DB_CONNECTION_STRING o DB_QUERY_CONFIG en el archivo .env")
        data.ESTADO_CONEXION = "OFFLINE"
        data.MENSAJE_ESTADO = "Error Config .env"
        return

    try:
        # Timeout de 5 segundos para no congelar la app
        with pyodbc.connect(conn_str, timeout=5) as conn:
            cursor = conn.cursor()
            
            cursor.execute(query)
            
            # pyodbc retorna filas como objetos Row, permitiendo acceso por nombre
            rows = cursor.fetchall()
            
            # Convertir a diccionario para acceso rápido por ConfigKey
            raw_data = {row.ConfigKey: row for row in rows}

            # --- 1. ACTUALIZAR VARIABLES GLOBALES ---
            if 'VALOR_UF_ACTUAL' in raw_data:
                data.VALOR_UF_ACTUAL = float(raw_data['VALOR_UF_ACTUAL'].val_Main)
            if 'SUELDO_MINIMO' in raw_data:
                data.SUELDO_MINIMO = int(raw_data['SUELDO_MINIMO'].val_Main)
            if 'TOPE_IMPONIBLE_AFP_SALUD' in raw_data:
                data.TOPE_IMPONIBLE_AFP_SALUD = float(raw_data['TOPE_IMPONIBLE_AFP_SALUD'].val_Main)
            if 'TOPE_IMPONIBLE_CESANTIA' in raw_data:
                data.TOPE_IMPONIBLE_CESANTIA = float(raw_data['TOPE_IMPONIBLE_CESANTIA'].val_Main)
            if 'DEFAULT_PLAN_ISAPRE_UF' in raw_data:
                data.DEFAULT_PLAN_ISAPRE_UF = float(raw_data['DEFAULT_PLAN_ISAPRE_UF'].val_Main)

            # --- 2. ACTUALIZAR DICCIONARIO AFP ---
            data.TASAS_AFP.clear()
            for row in rows:
                if row.Category == 'AFP':
                    name = row.ConfigKey.replace('AFP_', '').capitalize()
                    if name == 'Planvital': name = 'PlanVital'
                    if name == 'Provida': name = 'Provida' 
                    data.TASAS_AFP[name] = float(row.val_Main)

            # --- 3. ACTUALIZAR TRAMOS ---
            data.tramos_default.clear()
            tramos_rows = sorted([r for r in rows if r.Category == 'IMPUESTO'], key=lambda x: x.ConfigKey)
            
            for t in tramos_rows:
                hasta = float(t.val_Aux1)
                # Manejo de infinito (si guardaste 999999999 en la BD)
                if hasta > 900_000_000: hasta = float('inf')
                
                data.tramos_default.append({
                    "desde": float(t.val_Main),
                    "hasta": hasta,
                    "tasa": float(t.val_Aux2),
                    "rebaja": float(t.val_Aux3)
                })

            # --- 4. ACTUALIZAR PARAMETROS DICT ---
            # Valores seguros por si faltan llaves en la BD
            tasa_afp_def = float(raw_data['DEFAULT_TASA_AFP'].val_Main) if 'DEFAULT_TASA_AFP' in raw_data else 0.1049
            tasa_salud_def = float(raw_data['DEFAULT_TASA_SALUD'].val_Main) if 'DEFAULT_TASA_SALUD' in raw_data else 0.07
            tasa_cesant_def = float(raw_data['DEFAULT_TASA_CESANT'].val_Main) if 'DEFAULT_TASA_CESANT' in raw_data else 0.006
            
            data.parametros_default.update({
                "ingreso_minimo": data.SUELDO_MINIMO,
                "valor_uf": data.VALOR_UF_ACTUAL,
                "tope_imponible_uf": data.TOPE_IMPONIBLE_AFP_SALUD,
                "tope_cesantia_uf": data.TOPE_IMPONIBLE_CESANTIA,
                "tasa_afp": tasa_afp_def,
                "tasa_salud": tasa_salud_def,
                "tasa_cesant": tasa_cesant_def,
            })
            
            data.ESTADO_CONEXION = "ONLINE"
            data.MENSAJE_ESTADO = "Conectado a IARRHH"
            print("✅ Datos actualizados desde SQL Server (IARRHH).")

    except Exception as e:
        data.ESTADO_CONEXION = "OFFLINE"
        data.MENSAJE_ESTADO = "Modo Offline"
        print(f"⚠️ Error de conexión BD: {e}. Usando valores locales.")