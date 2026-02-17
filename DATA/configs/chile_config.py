# DATA/configs/chile_config.py
"""
Configuración específica para CHILE
Datos migrados desde DATA/data.py (configuración original que funciona correctamente)
"""

# --- INFORMACIÓN DEL PAÍS ---
CODIGO_PAIS = "chile"
NOMBRE_PAIS = "Chile"
MONEDA = "CLP"  # Peso Chileno
SIMBOLO_MONEDA = "$"

# --- UNIDAD DE VALOR ---
# UF: Unidad de Fomento (índice de inflación)
VALOR_UF_ACTUAL = 39597.67
NOMBRE_UNIDAD_VALOR = "UF"

# --- SALARIOS MÍNIMOS ---
SUELDO_MINIMO = 539000

# --- TOPES IMPONIBLES (En UF) ---
TOPE_IMPONIBLE_AFP_SALUD = 89.9   # Tope para AFP y Salud
TOPE_IMPONIBLE_CESANTIA = 135.1   # Tope para Seguro de Cesantía

# --- SISTEMA PREVISIONAL (AFP - Administradoras de Fondos de Pensiones) ---
NOMBRE_SISTEMA_PENSION = "AFP"
TASAS_PENSION = {
    "Capital": 0.1144,
    "Cuprum": 0.1144,
    "Habitat": 0.1127,
    "Modelo": 0.1066,
    "PlanVital": 0.1116,
    "Provida": 0.1145,
    "Uno": 0.1049  # AFP por defecto
}

# --- SISTEMA DE SALUD ---
NOMBRE_SISTEMA_SALUD_PUBLICO = "Fonasa"
NOMBRE_SISTEMA_SALUD_PRIVADO = "Isapre"
TASA_SALUD_MINIMA = 0.07  # 7% mínimo obligatorio
DEFAULT_PLAN_ISAPRE_UF = 2.822

# --- SEGURO DE CESANTÍA (Desempleo) ---
TASA_CESANTIA_TRABAJADOR = 0.006    # 0.6% (contrato indefinido)
TASA_CESANTIA_EMPLEADOR = 0.024     # 2.4% (contrato indefinido)

# --- GRATIFICACIÓN ---
# Chile tiene gratificación legal del 25% del sueldo, tope 4.75 sueldos mínimos anuales
TIENE_GRATIFICACION = True
PORCENTAJE_GRATIFICACION = 0.25
FACTOR_GRATIFICACION = 4.75  # Tope: 4.75 * sueldo_mínimo / 12 mensual

# --- COSTOS PATRONALES (Aportes del Empleador) ---
TASA_MUTUAL = 0.0093              # 0.93% Mutualidad (accidentes laborales)
TASA_SIS = 0.0154                 # 1.54% Seguro de Invalidez y Sobrevivencia
COTIZACION_EX_VIDA = 0.009        # 0.9% Cotización Ex Caja de Previsión
AFP_EMPLEADOR = 0.001             # 0.1% Aporte empleador AFP
SEGURO_COMPLEMENTARIO = 0.4822    # Porcentaje fijo seguro complementario

# --- TRAMOS DE IMPUESTO ÚNICO (Impuesto a la Renta de Segunda Categoría) ---
# Fuente: SII Chile - Tramos vigentes
TRAMOS_IMPUESTO = [
    {"desde": 0,            "hasta": 938_817.00,    "tasa": 0.00,  "rebaja": 0.0},
    {"desde": 938_817.01,   "hasta": 2_086_260.00,  "tasa": 0.04,  "rebaja": 37_552.68},
    {"desde": 2_086_260.01, "hasta": 3_477_100.00,  "tasa": 0.08,  "rebaja": 121_003.08},
    {"desde": 3_477_100.01, "hasta": 4_867_940.00,  "tasa": 0.135, "rebaja": 312_243.58},
    {"desde": 4_867_940.01, "hasta": 6_258_780.00,  "tasa": 0.23,  "rebaja": 774_697.88},
    {"desde": 6_258_780.01, "hasta": 8_345_040.00,  "tasa": 0.304, "rebaja": 1_237_847.60},
    {"desde": 8_345_040.01, "hasta": 21_558_020.00, "tasa": 0.35,  "rebaja": 1_621_719.44},
    {"desde": 21_558_020.01,"hasta": float('inf'),  "tasa": 0.40,  "rebaja": 2_699_620.44},
]

# --- PARÁMETROS COMPLETOS (Para compatibilidad con engine.py) ---
def obtener_parametros():
    """Retorna diccionario de parámetros en formato compatible con engine.py"""
    return {
        "ingreso_minimo": SUELDO_MINIMO,
        "valor_uf": VALOR_UF_ACTUAL,
        "tope_imponible_uf": TOPE_IMPONIBLE_AFP_SALUD,
        "tope_cesantia_uf": TOPE_IMPONIBLE_CESANTIA,
        "tasa_afp": TASAS_PENSION["Uno"],  # Default
        "tasa_salud": TASA_SALUD_MINIMA,
        "tasa_cesant": TASA_CESANTIA_TRABAJADOR,
        "factor_gratificacion": FACTOR_GRATIFICACION,
        "porcentaje_gratificacion": PORCENTAJE_GRATIFICACION,
        "tasa_cesant_empleador": TASA_CESANTIA_EMPLEADOR,
        "tasa_mutual": TASA_MUTUAL,
        "tasa_sis": TASA_SIS,
        "cot_exp_vida": COTIZACION_EX_VIDA,
        "afp_empleador": AFP_EMPLEADOR,
        "seguro_complementario": SEGURO_COMPLEMENTARIO
    }

# --- LABELS PARA LA UI ---
LABELS_UI = {
    "sistema_pension": "AFP",
    "sistema_salud_publico": "Fonasa",
    "sistema_salud_privado": "Isapre",
    "unidad_valor": "UF",
    "sueldo_base": "Sueldo Base",
    "sueldo_liquido": "Sueldo Líquido",
    "gratificacion": "Gratificación Legal",
    "impuesto": "Impuesto Único",
}
