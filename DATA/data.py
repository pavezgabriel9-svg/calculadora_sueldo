# DATA/data.py

# Variable de estado para la UI
ESTADO_CONEXION = "OFFLINE" # Por defecto asumimos offline hasta que el loader diga lo contrario
MENSAJE_ESTADO = "Usando valores por defecto (Sin conexión)"

# --- VALORES POR DEFECTO (Hardcoded) ---
VALOR_UF_ACTUAL = 39597.67
SUELDO_MINIMO = 539000

# Topes Imponibles (En UF)
TOPE_IMPONIBLE_AFP_SALUD = 89.9  
TOPE_IMPONIBLE_CESANTIA = 135.1   

DEFAULT_PLAN_ISAPRE_UF = 2.822

# Tasas Previsionales (Diccionario)
TASAS_AFP = {
    "Capital": 0.1144,
    "Cuprum": 0.1144,
    "Habitat": 0.1127,
    "Modelo": 0.1066,
    "PlanVital": 0.1116,
    "Provida": 0.1145,
    "Uno": 0.1049  
}

# Parametros generales
parametros_default = {
    "ingreso_minimo": SUELDO_MINIMO,
    "valor_uf": VALOR_UF_ACTUAL,
    "tope_imponible_uf": TOPE_IMPONIBLE_AFP_SALUD, 
    "tope_cesantia_uf": TOPE_IMPONIBLE_CESANTIA,
    "tasa_afp": 0.1049,
    "tasa_salud": 0.07,         
    "tasa_cesant": 0.006,
    # --- GRATIFICACIÓN ---
    "factor_gratificacion": 4.75,
    "porcentaje_gratificacion": 0.25,
    # --- COSTOS PATRONALES (Aportes Empleador) ---
    "tasa_cesant_empleador": 0.024,
    "tasa_mutual": 0.0093,
    "tasa_sis": 0.0154,
}

# Tramos de Impuesto
tramos_default = [
    {"desde": 0,            "hasta": 938_817.00,   "tasa": 0.00,  "rebaja":       0.0},
    {"desde": 938_817.01,   "hasta": 2_086_260.00, "tasa": 0.04,  "rebaja":   37_552.68},
    {"desde": 2_086_260.01, "hasta": 3_477_100.00, "tasa": 0.08,  "rebaja":  121_003.08},
    {"desde": 3_477_100.01, "hasta": 4_867_940.00, "tasa": 0.135, "rebaja":  312_243.58},
    {"desde": 4_867_940.01, "hasta": 6_258_780.00, "tasa": 0.23,  "rebaja":  774_697.88},
    {"desde": 6_258_780.01, "hasta": 8_345_040.00, "tasa": 0.304, "rebaja": 1_237_847.60},
    {"desde": 8_345_040.01, "hasta": 21_558_020.00,"tasa": 0.35,  "rebaja": 1_621_719.44},
    {"desde": 21_558_020.01,"hasta": float('inf'), "tasa": 0.40,  "rebaja": 2_699_620.44},
]