# DATA/configs/brasil_config.py
"""
Configuración específica para BRASIL
BOSQUEJO - Completar con datos reales del sistema laboral brasileño

Referencias:
- Receita Federal: https://www.gov.br/receitafederal/
- Ministério do Trabalho: https://www.gov.br/trabalho-e-previdencia/
- Previdência Social (INSS): https://www.gov.br/inss/
"""

# --- INFORMACIÓN DEL PAÍS ---
CODIGO_PAIS = "brasil"
NOMBRE_PAIS = "Brasil"
MONEDA = "BRL"  # Real Brasileño
SIMBOLO_MONEDA = "R$"

# --- UNIDAD DE VALOR ---
# Brasil no tiene una unidad indexada como UF o UIT
# Se usa directamente el Real (BRL)
VALOR_UNIDAD = 1.0  # No aplica
NOMBRE_UNIDAD_VALOR = "BRL"

# --- SALARIOS MÍNIMOS ---
# TODO: Actualizar con Salário Mínimo vigente 2025-2026
SUELDO_MINIMO = 1412.0  # ⚠️ VERIFICAR: Salário Mínimo 2025 (ejemplo: R$ 1,412)

# --- TOPES IMPONIBLES ---
# TODO: Verificar topes del INSS (Teto da Previdência)
TOPE_IMPONIBLE_INSS = 7786.02  # ⚠️ VERIFICAR: Teto INSS 2025 (ejemplo: R$ 7,786.02)

# --- SISTEMA PREVISIONAL (INSS) ---
# INSS: Instituto Nacional do Seguro Social (Sistema Público)
# Régimen progresivo desde 2020 (Reforma da Previdência)
NOMBRE_SISTEMA_PENSION = "INSS"

# Tasas progresivas INSS (Trabajador)
# TODO: Actualizar con tabla vigente
TRAMOS_INSS = [
    {"desde": 0,       "hasta": 1412.00,  "tasa": 0.075},  # ⚠️ VERIFICAR: 7.5% hasta 1 salario mínimo
    {"desde": 1412.01, "hasta": 2666.68,  "tasa": 0.09},   # ⚠️ VERIFICAR: 9%
    {"desde": 2666.69, "hasta": 4000.03,  "tasa": 0.12},   # ⚠️ VERIFICAR: 12%
    {"desde": 4000.04, "hasta": 7786.02,  "tasa": 0.14},   # ⚠️ VERIFICAR: 14% hasta el tope
]

# INSS Empleador
TASA_INSS_EMPLEADOR = 0.20  # ⚠️ VERIFICAR: 20% (puede variar según actividad)

# --- SISTEMA DE SALUD (SUS) ---
# SUS: Sistema Único de Saúde (Público y gratuito)
# Financiado por impuestos, NO descuenta del salario del trabajador
NOMBRE_SISTEMA_SALUD_PUBLICO = "SUS"
NOMBRE_SISTEMA_SALUD_PRIVADO = "Plano de Saúde"

TASA_SUS_TRABAJADOR = 0.0  # ⚠️ IMPORTANTE: SUS es gratuito, sin descuento
TASA_SUS_EMPLEADOR = 0.0   # Financiado por tributos generales

# Plano de Saúde (Seguro privado opcional)
# TODO: Investigar si hay descuentos típicos para planes privados
TASA_PLANO_SAUDE_MINIMA = 0.0  # ⚠️ COMPLETAR: Variable según plan

# --- FGTS (Fundo de Garantia por Tempo de Serviço) ---
# Similar al ahorro para indemnización por despido
# 8% mensual depositado por el empleador (NO descuenta al trabajador)
TIENE_FGTS = True
TASA_FGTS = 0.08  # ⚠️ VERIFICAR: 8% sobre salario bruto

# --- 13º SALÁRIO (Décimo Tercero) ---
# Gratificación obligatoria de fin de año (equivalente a 1 sueldo anual)
# Mensualizado: 1/12 = 8.33%
TIENE_DECIMO_TERCERO = True
PORCENTAJE_DECIMO_TERCERO = 0.0833  # ⚠️ VERIFICAR: 1 sueldo / 12 meses

# --- FÉRIAS (Vacaciones) ---
# 30 días de vacaciones con pago adicional de 1/3 del salario
# Mensualizado: (1 + 1/3) / 12 = 11.11%
TIENE_FERIAS = True
PORCENTAJE_FERIAS = 0.1111  # ⚠️ VERIFICAR: 1.333 sueldos / 12 meses

# --- SEGURO DE DESEMPLEO ---
# TODO: Investigar si hay contribución para Seguro-Desemprego
TIENE_SEGURO_DESEMPLEO = False
TASA_SEGURO_DESEMPLEO = 0.0

# --- COSTOS PATRONALES (Aportes del Empleador) ---
# TODO: Completar con todas las contribuciones patronales brasileñas
TASA_INSS_PATRONAL = 0.20          # ⚠️ VERIFICAR: 20% INSS
TASA_FGTS_PATRONAL = 0.08          # ⚠️ VERIFICAR: 8% FGTS
TASA_SAT = 0.03                    # ⚠️ VERIFICAR: 1-3% SAT (Seguro Accidente Trabajo)
TASA_SISTEMA_S = 0.058             # ⚠️ VERIFICAR: 5.8% Sistema S (SESI, SENAI, etc.)
TASA_SALARIO_EDUCACAO = 0.025      # ⚠️ VERIFICAR: 2.5% Salário Educação
TASA_SEBRAE = 0.006                # ⚠️ VERIFICAR: 0.6% SEBRAE
TASA_INCRA = 0.002                 # ⚠️ VERIFICAR: 0.2% INCRA

# --- TRAMOS DE IMPUESTO A LA RENTA (IRRF - Imposto de Renda Retido na Fonte) ---
# TODO: Actualizar con tabla vigente 2025-2026
# Fuente: Receita Federal - Tabela IRRF
# Nota: Se aplica sobre salario mensual después de deducciones
TRAMOS_IMPUESTO = [
    {"desde": 0,       "hasta": 2259.20,   "tasa": 0.00,  "rebaja": 0.0},      # ⚠️ VERIFICAR: Exento
    {"desde": 2259.21, "hasta": 2826.65,   "tasa": 0.075, "rebaja": 169.44},   # ⚠️ VERIFICAR: 7.5%
    {"desde": 2826.66, "hasta": 3751.05,   "tasa": 0.15,  "rebaja": 381.44},   # ⚠️ VERIFICAR: 15%
    {"desde": 3751.06, "hasta": 4664.68,   "tasa": 0.225, "rebaja": 662.77},   # ⚠️ VERIFICAR: 22.5%
    {"desde": 4664.69, "hasta": float('inf'), "tasa": 0.275, "rebaja": 896.00}, # ⚠️ VERIFICAR: 27.5%
]

# Deducciones IRRF
# TODO: Verificar valores de deducción por dependiente
DEDUCCION_POR_DEPENDIENTE = 189.59  # ⚠️ VERIFICAR: Por cada dependiente mensual

# --- PARÁMETROS COMPLETOS ---
def obtener_parametros():
    """
    ⚠️ TODO: Adaptar este diccionario a la lógica de Brasil
    El sistema brasileño es más complejo con múltiples contribuciones
    """
    return {
        "ingreso_minimo": SUELDO_MINIMO,
        "tope_inss": TOPE_IMPONIBLE_INSS,

        # Sistema previsional
        "tramos_inss": TRAMOS_INSS,  # Nuevo: tasas progresivas
        "tasa_inss_empleador": TASA_INSS_EMPLEADOR,

        # Beneficios obligatorios
        "porcentaje_decimo_tercero": PORCENTAJE_DECIMO_TERCERO,
        "porcentaje_ferias": PORCENTAJE_FERIAS,
        "tasa_fgts": TASA_FGTS,

        # Costos patronales
        "tasa_inss_patronal": TASA_INSS_PATRONAL,
        "tasa_fgts_patronal": TASA_FGTS_PATRONAL,
        "tasa_sat": TASA_SAT,
        "tasa_sistema_s": TASA_SISTEMA_S,
        "tasa_salario_educacao": TASA_SALARIO_EDUCACAO,
        "tasa_sebrae": TASA_SEBRAE,
        "tasa_incra": TASA_INCRA,

        # Deducciones
        "deduccion_dependiente": DEDUCCION_POR_DEPENDIENTE,
    }

# --- PARÁMETROS ESPECÍFICOS DE CÁLCULO ---
def calcular_inss_progresivo(salario_bruto: float) -> float:
    """
    ⚠️ TODO: Implementar cálculo de INSS con tasas progresivas
    Desde la reforma de 2020, INSS se calcula por tramos (como impuesto)

    Ejemplo:
    Si salario = R$ 3000:
    - Tramo 1: 1412 * 7.5% = 105.90
    - Tramo 2: (2666.68 - 1412) * 9% = 112.92
    - Tramo 3: (3000 - 2666.68) * 12% = 39.99
    Total INSS = 258.81
    """
    inss_total = 0.0
    for tramo in TRAMOS_INSS:
        if salario_bruto > tramo["desde"]:
            base = min(salario_bruto, tramo["hasta"]) - tramo["desde"]
            inss_total += base * tramo["tasa"]
    return inss_total

# --- LABELS PARA LA UI ---
LABELS_UI = {
    "sistema_pension": "INSS",
    "sistema_salud_publico": "SUS",
    "sistema_salud_privado": "Plano de Saúde",
    "unidad_valor": "BRL",
    "sueldo_base": "Salário Base",
    "sueldo_liquido": "Salário Líquido",
    "decimo_tercero": "13º Salário",
    "ferias": "Férias + 1/3",
    "fgts": "FGTS",
    "impuesto": "IRRF (Imposto de Renda)",
}

# ═══════════════════════════════════════════════════════════════
#  ⚠️ TAREAS PENDIENTES PARA COMPLETAR ESTE ARCHIVO:
# ═══════════════════════════════════════════════════════════════
#
# 1. [ ] Verificar Salário Mínimo vigente 2025-2026
# 2. [ ] Actualizar Teto INSS (tope máximo)
# 3. [ ] Confirmar tabla INSS progresiva vigente
# 4. [ ] Validar tabla IRRF (Imposto de Renda) con rebajas
# 5. [ ] Verificar tasa INSS patronal (20% es promedio)
# 6. [ ] Confirmar todas las tasas del Sistema S (SESI, SENAI, SESC, etc.)
# 7. [ ] Investigar SAT (Seguro Acidente Trabalho) - varía por riesgo
# 8. [ ] Validar cálculo de 13º Salário mensualizado
# 9. [ ] Validar cálculo de Férias + 1/3 mensualizado
# 10. [ ] Implementar función calcular_inss_progresivo() correctamente
# 11. [ ] Investigar deducciones IRRF (dependientes, pensión alimenticia, etc.)
# 12. [ ] Validar si hay otros tributos municipales o estatales
#
# Referencias útiles:
# - Receita Federal Tabelas: https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/tributos/irpf-imposto-de-renda-pessoa-fisica
# - INSS Teto: https://www.gov.br/inss/pt-br/noticias/confira-as-aliquotas-de-contribuicao-ao-inss
# - CLT (Consolidação das Leis do Trabalho): Lei 5.452/1943
# - Reforma da Previdência: Emenda Constitucional 103/2019
# ═══════════════════════════════════════════════════════════════
