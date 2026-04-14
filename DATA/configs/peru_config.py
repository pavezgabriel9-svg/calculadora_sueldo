# DATA/configs/peru_config.py
"""
Configuración específica para PERÚ
BOSQUEJO - Completar con datos reales del sistema laboral peruano

Referencias:
- SUNAT: https://www.sunat.gob.pe/
- SBS (Superintendencia de Banca y Seguros): https://www.sbs.gob.pe/
- MTPE (Ministerio de Trabajo): https://www.gob.pe/mtpe
"""

# --- INFORMACIÓN DEL PAÍS ---
CODIGO_PAIS = "peru"
NOMBRE_PAIS = "Perú"
MONEDA = "PEN"  # Sol Peruano
SIMBOLO_MONEDA = "S/."

# --- UNIDAD DE VALOR ---
# TODO: Actualizar con valor UIT vigente 2025-2026
# UIT: Unidad Impositiva Tributaria (se actualiza anualmente)
VALOR_UIT_ACTUAL = 5150.0  # ⚠️ VERIFICAR: Valor UIT 2025 (ejemplo: S/. 5,150)
NOMBRE_UNIDAD_VALOR = "UIT"

# --- SALARIOS MÍNIMOS ---
# TODO: Actualizar con RMV (Remuneración Mínima Vital) vigente
SUELDO_MINIMO = 1025.0  # ⚠️ VERIFICAR: RMV 2025 (ejemplo: S/. 1,025)

# --- TOPES IMPONIBLES ---
# TODO: Investigar si existen topes para pensiones y salud en Perú
# En Perú generalmente NO hay topes para ONP/AFP, verificar
TOPE_IMPONIBLE_PENSION = None  # ⚠️ COMPLETAR: Generalmente sin tope
TOPE_IMPONIBLE_SALUD = None    # ⚠️ COMPLETAR: EsSalud sin tope

# --- SISTEMA PREVISIONAL ---
NOMBRE_SISTEMA_PENSION = "ONP/AFP"

# ONP: Sistema Público (similar a Fonasa Chile)
TASA_ONP = 0.13  # ⚠️ VERIFICAR: 13% para ONP

# AFP: Sistema Privado (múltiples administradoras)
# TODO: Actualizar con tasas vigentes de cada AFP peruana
# Fuente: https://www.sbs.gob.pe/app/stats/TasaPrevisional_33.asp
TASAS_AFP = {
    "Integra": 0.1025,    # ⚠️ VERIFICAR: Tasa aproximada (comisión + seguro)
    "Profuturo": 0.1067,  # ⚠️ VERIFICAR
    "Prima": 0.1070,      # ⚠️ VERIFICAR
    "Habitat": 0.1072,    # ⚠️ VERIFICAR
}

# --- SISTEMA DE SALUD ---
NOMBRE_SISTEMA_SALUD_PUBLICO = "EsSalud"
NOMBRE_SISTEMA_SALUD_PRIVADO = "EPS"  # Entidades Prestadoras de Salud

# EsSalud: 9% aportado por el EMPLEADOR (no descuenta al trabajador)
TASA_ESSALUD_TRABAJADOR = 0.00  # ⚠️ IMPORTANTE: El trabajador NO paga
TASA_ESSALUD_EMPLEADOR = 0.09   # ⚠️ VERIFICAR: 9% paga el empleador

# EPS: Seguro privado (descuento adicional al trabajador)
# TODO: Investigar cómo funciona el sistema EPS
TASA_EPS_MINIMA = 0.0  # ⚠️ COMPLETAR: Variable según plan

# --- SEGURO DE DESEMPLEO ---
# TODO: Investigar si Perú tiene seguro de desempleo obligatorio
# Nota: Perú NO tiene seguro de cesantía como Chile
TIENE_SEGURO_CESANTIA = False
TASA_CESANTIA_TRABAJADOR = 0.0
TASA_CESANTIA_EMPLEADOR = 0.0

# --- GRATIFICACIÓN ---
# Perú tiene 2 gratificaciones obligatorias al año (julio y diciembre)
# Equivalente a 2 sueldos anuales / 12 meses = ~16.67% mensual
# TODO: Validar cálculo de gratificación peruana
TIENE_GRATIFICACION = True
PORCENTAJE_GRATIFICACION = 0.1667  # ⚠️ VERIFICAR: 2 sueldos anuales / 12
FACTOR_GRATIFICACION = None         # ⚠️ COMPLETAR: ¿Hay tope?

# --- CTS (Compensación por Tiempo de Servicios) ---
# TODO: Investigar CTS - beneficio único de Perú
# CTS = 1 sueldo + 1 gratificación / 12 meses
TIENE_CTS = True
PORCENTAJE_CTS = 0.0972  # ⚠️ VERIFICAR: Aproximado (1 + 1/6) / 12

# --- COSTOS PATRONALES (Aportes del Empleador) ---
# TODO: Completar con tasas vigentes de SENATI, SCTR, etc.
TASA_ESSALUD = 0.09           # ⚠️ VERIFICAR: 9% EsSalud
TASA_SENATI = 0.0075          # ⚠️ VERIFICAR: 0.75% SENATI (solo manufactura)
TASA_SCTR_SALUD = 0.0         # ⚠️ COMPLETAR: Seguro Complementario de Trabajo de Riesgo
TASA_SCTR_PENSION = 0.0       # ⚠️ COMPLETAR: Variable según nivel de riesgo

# --- TRAMOS DE IMPUESTO A LA RENTA (5ta Categoría) ---
# TODO: Actualizar con tabla vigente 2025-2026
# Fuente: SUNAT - Tabla de Renta de 5ta Categoría
# Nota: En Perú se calcula ANUALMENTE, luego se prorratea mensual
TRAMOS_IMPUESTO = [
    # Base anual en UIT
    {"desde": 0,              "hasta": 5 * VALOR_UIT_ACTUAL,   "tasa": 0.08,  "rebaja": 0.0},
    {"desde": 5 * VALOR_UIT_ACTUAL,  "hasta": 20 * VALOR_UIT_ACTUAL,  "tasa": 0.14,  "rebaja": 0.0},  # ⚠️ COMPLETAR rebaja
    {"desde": 20 * VALOR_UIT_ACTUAL, "hasta": 35 * VALOR_UIT_ACTUAL,  "tasa": 0.17,  "rebaja": 0.0},  # ⚠️ COMPLETAR
    {"desde": 35 * VALOR_UIT_ACTUAL, "hasta": 45 * VALOR_UIT_ACTUAL,  "tasa": 0.20,  "rebaja": 0.0},  # ⚠️ COMPLETAR
    {"desde": 45 * VALOR_UIT_ACTUAL, "hasta": float('inf'),            "tasa": 0.30,  "rebaja": 0.0},  # ⚠️ COMPLETAR
]

# --- PARÁMETROS COMPLETOS ---
def obtener_parametros():
    """
    ⚠️ TODO: Adaptar este diccionario a la lógica de Perú
    Algunos campos pueden no aplicar o requerir nuevos campos
    """
    return {
        "ingreso_minimo": SUELDO_MINIMO,
        "valor_uit": VALOR_UIT_ACTUAL,  # Cambio: UF → UIT
        "tope_imponible_uit": TOPE_IMPONIBLE_PENSION,

        # Sistema previsional
        "tasa_onp": TASA_ONP,  # Nuevo campo
        "tasa_afp": TASAS_AFP.get("Integra", 0.1025),  # Default

        # Salud
        "tasa_essalud_trabajador": TASA_ESSALUD_TRABAJADOR,
        "tasa_essalud_empleador": TASA_ESSALUD_EMPLEADOR,

        # Gratificación y CTS
        "porcentaje_gratificacion": PORCENTAJE_GRATIFICACION,
        "porcentaje_cts": PORCENTAJE_CTS,  # Nuevo campo único de Perú

        # Costos patronales
        "tasa_senati": TASA_SENATI,
        "tasa_sctr_salud": TASA_SCTR_SALUD,
        "tasa_sctr_pension": TASA_SCTR_PENSION,
    }

# --- LABELS PARA LA UI ---
LABELS_UI = {
    "sistema_pension": "ONP/AFP",
    "sistema_salud_publico": "EsSalud",
    "sistema_salud_privado": "EPS",
    "unidad_valor": "UIT",
    "sueldo_base": "Remuneración Básica",
    "sueldo_liquido": "Remuneración Neta",
    "gratificacion": "Gratificación",
    "cts": "CTS (Compensación por Tiempo de Servicios)",
    "impuesto": "Impuesto a la Renta (5ta Categoría)",
}

# ═══════════════════════════════════════════════════════════════
#  ⚠️ TAREAS PENDIENTES PARA COMPLETAR ESTE ARCHIVO:
# ═══════════════════════════════════════════════════════════════
#
# 1. [ ] Verificar UIT vigente 2025-2026
# 2. [ ] Actualizar RMV (Remuneración Mínima Vital)
# 3. [ ] Confirmar tasas de AFP actualizadas (SBS)
# 4. [ ] Validar si existen topes para ONP/AFP
# 5. [ ] Completar tabla de Impuesto a la Renta con rebajas correctas
# 6. [ ] Investigar funcionamiento de EPS (seguros privados)
# 7. [ ] Calcular correctamente CTS mensual
# 8. [ ] Verificar tasa SENATI (aplica solo a ciertas industrias)
# 9. [ ] Investigar SCTR (Seguro Complementario de Trabajo de Riesgo)
# 10. [ ] Validar que gratificaciones se calculan correctamente
#
# Referencias útiles:
# - SUNAT Tablas: https://www.sunat.gob.pe/indicestasas/
# - SBS AFPs: https://www.sbs.gob.pe/app/stats/TasaPrevisional_33.asp
# - Código Tributario: Decreto Supremo N° 133-2013-EF
# ═══════════════════════════════════════════════════════════════
