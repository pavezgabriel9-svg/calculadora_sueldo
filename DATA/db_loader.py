# SERVICE/db_loader.py
#import pyodbc
from DATA import data
import pymysql

# Configuración (Idealmente variables de entorno, pero hardcoded para este ejemplo)
# DB_CONFIG = {
#     'Driver': '{ODBC Driver 17 for SQL Server}',
#     'Server': 'LOCALHOST',     # Cambia esto por tu servidor real
#     'Database': 'RRHH_DB',     # Cambia esto por tu BD real
#     'Trusted_Connection': 'yes'
# }

# Configuración BD - mac

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "prueba"
DB_NAME = "prueba"

def actualizar_configuracion_desde_db():
    """
    Intenta conectarse a la BD para actualizar los valores de DATA/data.py.
    Si falla, deja los valores por defecto (Fail-Safe).
    """
    print("🔄 Intentando conectar a Base de Datos...")
    
    try:
        conexion = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset='utf8mb4'
            )
        cursor = conexion.cursor()
        
        #conn_str = f"DRIVER={DB_CONFIG['Driver']};SERVER={DB_CONFIG['Server']};DATABASE={DB_CONFIG['Database']};Trusted_Connection={DB_CONFIG['Trusted_Connection']}"
        
        
        # Timeout corto (3 segundos) para no congelar la app si no hay internet
        # with pyodbc.connect(conn_str, timeout=3) as conn:
        with cursor as conn:
            
            # Asumiendo que ya creaste la tabla AppConfig que diseñamos antes
            cursor.execute("SELECT ConfigKey, Category, val_Main, val_Aux1, val_Aux2, val_Aux3 FROM AppConfig")
            rows = cursor.fetchall()
            
            raw_data = {row.ConfigKey: row for row in rows}

            # --- 1. ACTUALIZAR VARIABLES GLOBALES EN DATA.PY ---
            # Sobrescribimos las variables del módulo importado
            data.VALOR_UF_ACTUAL = float(raw_data['VALOR_UF_ACTUAL'].val_Main)
            data.SUELDO_MINIMO = int(raw_data['SUELDO_MINIMO'].val_Main)
            data.TOPE_IMPONIBLE_AFP_SALUD = float(raw_data['TOPE_IMPONIBLE_AFP_SALUD'].val_Main)
            data.TOPE_IMPONIBLE_CESANTIA = float(raw_data['TOPE_IMPONIBLE_CESANTIA'].val_Main)
            data.DEFAULT_PLAN_ISAPRE_UF = float(raw_data['DEFAULT_PLAN_ISAPRE_UF'].val_Main)

            # --- 2. ACTUALIZAR DICCIONARIO AFP ---
            # Limpiamos y rellenamos
            data.TASAS_AFP.clear()
            for row in rows:
                if row.Category == 'AFP':
                    name = row.ConfigKey.replace('AFP_', '').capitalize()
                    # Correcciones de nombre manuales si es necesario
                    if name == 'Planvital': name = 'PlanVital'
                    if name == 'Provida': name = 'Provida' 
                    data.TASAS_AFP[name] = float(row.val_Main)

            # --- 3. ACTUALIZAR TRAMOS ---
            data.tramos_default.clear()
            tramos_rows = sorted([r for r in rows if r.Category == 'IMPUESTO'], key=lambda x: x.ConfigKey)
            
            for t in tramos_rows:
                hasta = float(t.val_Aux1)
                if hasta > 900000000: hasta = float('inf')
                
                data.tramos_default.append({
                    "desde": float(t.val_Main),
                    "hasta": hasta,
                    "tasa": float(t.val_Aux2),
                    "rebaja": float(t.val_Aux3)
                })

            # --- 4. ACTUALIZAR PARAMETROS DICT ---
            data.parametros_default.update({
                "ingreso_minimo": data.SUELDO_MINIMO,
                "valor_uf": data.VALOR_UF_ACTUAL,
                "tope_imponible_uf": data.TOPE_IMPONIBLE_AFP_SALUD,
                "tope_cesantia_uf": data.TOPE_IMPONIBLE_CESANTIA,
                "tasa_afp": float(raw_data['DEFAULT_TASA_AFP'].val_Main),
                "tasa_salud": float(raw_data['DEFAULT_TASA_SALUD'].val_Main),
                "tasa_cesant": float(raw_data['DEFAULT_TASA_CESANT'].val_Main),
            })
            
            # SI LLEGAMOS AQUÍ, TODO SALIÓ BIEN
            data.ESTADO_CONEXION = "ONLINE"
            data.MENSAJE_ESTADO = "🟢 Conectado a Base de Datos"
            print("✅ Datos actualizados desde SQL Server.")

    except Exception as e:
        # SI FALLA, NO HACEMOS NADA (Se quedan los defaults de data.py)
        data.ESTADO_CONEXION = "OFFLINE"
        data.MENSAJE_ESTADO = "🟠 Modo Offline"
        print(f"⚠️ No se pudo conectar a la BD ({e}). Usando valores locales.")