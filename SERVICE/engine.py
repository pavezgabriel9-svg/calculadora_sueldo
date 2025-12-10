# calculos.py
# SERVICE/engine.py
from DATA import data
from typing import List, Dict
import math

def redondear_a_miles_arriba(valor: float) -> int:
    """
    Redondea un valor hacia arriba al siguiente múltiplo de 1000.
    Ejemplos:
        123.456 → 124.000
        523.001 → 524.000
        520.000 → 520.000 (ya es múltiplo, no cambia)
    """
    if valor <= 0:
        return 0
    return int(math.ceil(valor / 1000) * 1000)


def calcular_impuesto_unico(base_tributable: float) -> float:
    """Calcula el impuesto de segunda categoría según tramos de data.py"""
    if base_tributable <= 0:
        return 0.0
    
    for tramo in data.tramos_default:
        if tramo['desde'] <= base_tributable <= tramo['hasta']:
            return (base_tributable * tramo['tasa']) - tramo['rebaja']
            
    # Seguridad para tramos infinitos si no se capturó antes
    ultimo = data.tramos_default[-1]
    if base_tributable > ultimo['desde']:
        return (base_tributable * ultimo['tasa']) - ultimo['rebaja']
         
    return 0.0


def simular_liquido(sueldo_base: float, datos: dict) -> tuple:
    """
    Función de simulación forward: dado un sueldo base, calcula el líquido resultante.
    Retorna (liquido_calculado, diccionario_detalles)
    """
    # Desempaquetar datos
    lista_bonos: List[Dict] = datos.get('bonos', [])
    movilizacion = datos['movilizacion']
    
    # Sumas de bonos
    bonos_imponibles = sum(b['monto'] for b in lista_bonos if b['imponible'])
    bonos_no_imponibles = sum(b['monto'] for b in lista_bonos if not b['imponible'])
    
    # Parámetros económicos desde DATA
    uf = data.VALOR_UF_ACTUAL
    ingreso_minimo = data.SUELDO_MINIMO
    
    # Topes en Pesos
    tope_pesos_afp_salud = data.TOPE_IMPONIBLE_AFP_SALUD * uf
    tope_pesos_cesantia = data.TOPE_IMPONIBLE_CESANTIA * uf
    
    # Tasas
    tasa_afp = data.TASAS_AFP.get(datos['afp_nombre'], 0.1049)
    tasa_fonasa = data.parametros_default['tasa_salud']
    tasa_cesantia = data.parametros_default['tasa_cesant']
    
    # Configuración Salud
    usar_fonasa = (datos['salud_sistema'] == 'fonasa')
    costo_plan_isapre = 0
    if not usar_fonasa:
        costo_plan_isapre = datos['salud_uf'] * uf
    
    # A. Gratificación
    tope_grat = (4.75 * ingreso_minimo) / 12
    gratificacion = min(sueldo_base * 0.25, tope_grat)
    
    # B. Total Imponible (Base + Grat + Bonos)
    imponible = sueldo_base + gratificacion + bonos_imponibles
    
    # C. Aplicar Topes Legales Diferenciados 
    imp_afecto_afp_salud = min(imponible, tope_pesos_afp_salud)
    imp_afecto_cesantia = min(imponible, tope_pesos_cesantia)
    
    # D. Cálculos Previsionales
    val_afp = imp_afecto_afp_salud * tasa_afp
    val_cesantia = imp_afecto_cesantia * tasa_cesantia
    
    val_salud = 0
    if usar_fonasa:
        val_salud = imp_afecto_afp_salud * tasa_fonasa
    else:
        siete_porciento = imp_afecto_afp_salud * tasa_fonasa
        val_salud = max(siete_porciento, costo_plan_isapre)
        
    # E. Impuesto
    base_trib = imponible - val_afp - val_salud - val_cesantia
    val_impuesto = calcular_impuesto_unico(base_trib)
    
    # F. Líquido
    tot_haberes = imponible + movilizacion + bonos_no_imponibles
    tot_descuentos = val_afp + val_salud + val_cesantia + val_impuesto
    
    liquido = tot_haberes - tot_descuentos
    
    detalles = {
        "grat": gratificacion,
        "imp": imponible,
        "afp": val_afp,
        "salud": val_salud,
        "ces": val_cesantia,
        "tax": val_impuesto,
        "hab": tot_haberes,
        "desc": tot_descuentos,
        "base_trib": base_trib,
        "bonos_imp": bonos_imponibles,
        "bonos_no_imp": bonos_no_imponibles
    }
    
    return liquido, detalles


def resolver_sueldo_base(datos: dict) -> dict:
    """
    Algoritmo de búsqueda binaria con REDONDEO A MILES hacia arriba.
    
    El flujo es:
    1. Buscar el sueldo base exacto que da el líquido objetivo
    2. Redondear ese sueldo base a miles hacia arriba
    3. Recalcular con el sueldo redondeado para mostrar cifras reales
    """
    liquido_objetivo = datos['sueldo_liquido']
    movilizacion = datos['movilizacion']
    lista_bonos: List[Dict] = datos.get('bonos', [])
    
    bonos_imponibles = sum(b['monto'] for b in lista_bonos if b['imponible'])
    bonos_no_imponibles = sum(b['monto'] for b in lista_bonos if not b['imponible'])
    
    # --- Configuración del Algoritmo de Búsqueda ---
    precision = 1.0
    min_base = 0
    max_base = liquido_objetivo * 3.0
    iteraciones = 0
    
    # Expandir rango si es necesario
    while simular_liquido(max_base, datos)[0] < liquido_objetivo:
        max_base *= 2
        if max_base > 100_000_000:  # Límite de seguridad
            break

    # --- Búsqueda Binaria ---
    base_exacta = 0
    while (max_base - min_base) > precision and iteraciones < 100:
        base_exacta = (min_base + max_base) / 2
        liquido_calc, _ = simular_liquido(base_exacta, datos)
        
        if liquido_calc < liquido_objetivo:
            min_base = base_exacta
        else:
            max_base = base_exacta
        
        iteraciones += 1
    
    # --- REDONDEO A MILES HACIA ARRIBA ---
    sueldo_base_redondeado = redondear_a_miles_arriba(base_exacta)
    
    # --- Recalcular con el sueldo redondeado ---
    liquido_real, d = simular_liquido(sueldo_base_redondeado, datos)
    
    # Calcular diferencia (cuánto más recibirá el trabajador por el redondeo)
    diferencia = liquido_real - liquido_objetivo
    
    return {
        "sueldo_base": sueldo_base_redondeado,
        "sueldo_base_exacto": round(base_exacta),  # Para referencia
        "gratificacion": round(d['grat']),
        "bonos_imponibles": round(bonos_imponibles),
        "bonos_no_imponibles": round(bonos_no_imponibles),
        "movilizacion": round(movilizacion),
        "sueldo_liquido": round(liquido_real),
        "imponible": round(d['imp']),
        "total_haberes": round(d['hab']),
        "total_descuentos": round(d['desc']),
        "impuesto": round(d['tax']),
        "cesantia": round(d['ces']),
        "diferencia": round(diferencia),
        "cotizacion_salud": round(d['salud']),
        "cotizacion_previsional": round(d['afp']),
        "redondeo_aplicado": sueldo_base_redondeado - round(base_exacta)
    }