# SERVICE/engine.py
from DATA import data
from typing import List, Dict
import math

def redondear_a_miles_arriba(valor: float) -> int:
    """
    Redondea un valor hacia arriba al siguiente múltiplo de 1000.
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
    MOTOR CORE: Calcula líquido dado un sueldo base.
    
    Args:
        sueldo_base: Sueldo base bruto
        datos: Diccionario con configuración (AFP, salud, bonos, etc)
    
    Returns:
        tuple: (liquido_calculado, diccionario_detalles_brutos)
    """
    # Desempaquetar datos
    lista_bonos: List[Dict] = datos.get('bonos', [])
    movilizacion = datos.get('movilizacion', 0)
    
    # Sumas de bonos
    bonos_imponibles = sum(b['monto'] for b in lista_bonos if b['imponible'])
    bonos_no_imponibles = sum(b['monto'] for b in lista_bonos if not b['imponible'])
    
    # Parámetros económicos
    uf = data.VALOR_UF_ACTUAL
    ingreso_minimo = data.SUELDO_MINIMO
    
    # Topes
    tope_pesos_afp_salud = data.TOPE_IMPONIBLE_AFP_SALUD * uf
    tope_pesos_cesantia = data.TOPE_IMPONIBLE_CESANTIA * uf
    
    # Tasas trabajador
    tasa_afp = data.TASAS_AFP.get(datos.get('afp_nombre', 'Uno'), 0.1049)
    tasa_fonasa = data.parametros_default['tasa_salud']
    tasa_cesantia = data.parametros_default['tasa_cesant']
    
    # Configuración Salud
    usar_fonasa = (datos.get('salud_sistema', 'fonasa') == 'fonasa')
    costo_plan_isapre = 0
    if not usar_fonasa:
        costo_plan_isapre = datos.get('salud_uf', 0) * uf
    
    # A. Gratificación
    tope_grat = (4.75 * ingreso_minimo) / 12
    gratificacion = min(sueldo_base * 0.25, tope_grat)
    
    # B. Total Imponible
    imponible = sueldo_base + gratificacion + bonos_imponibles
    
    # C. Aplicar Topes
    imp_afecto_afp_salud = min(imponible, tope_pesos_afp_salud)
    imp_afecto_cesantia = min(imponible, tope_pesos_cesantia)
    
    # D. Descuentos Trabajador
    val_afp = imp_afecto_afp_salud * tasa_afp
    val_cesantia_trab = imp_afecto_cesantia * tasa_cesantia
    
    val_salud = 0
    if usar_fonasa:
        val_salud = imp_afecto_afp_salud * tasa_fonasa
    else:
        siete_porciento = imp_afecto_afp_salud * tasa_fonasa
        val_salud = max(siete_porciento, costo_plan_isapre)
    
    # E. Impuesto
    base_trib = imponible - val_afp - val_salud - val_cesantia_trab
    val_impuesto = calcular_impuesto_unico(base_trib)
    
    # F. Costos Patronales
    tasa_ces_emp = data.parametros_default.get('tasa_cesant_empleador', 0.024)
    cesantia_empleador = imp_afecto_cesantia * tasa_ces_emp
    
    tasa_mutual = data.parametros_default.get('tasa_mutual', 0.0093)
    mutual = imp_afecto_afp_salud * tasa_mutual
    
    # Obtener tasa SIS según AFP (CORREGIDO)
    afp_nombre = datos.get('afp_nombre', 'Uno')
    tasa_sis = data.parametros_default.get('tasa_sis', 0.0154) 
    sis = imp_afecto_afp_salud * tasa_sis
    
    # G. Totales
    tot_haberes = imponible + movilizacion + bonos_no_imponibles
    tot_descuentos = val_afp + val_salud + val_cesantia_trab + val_impuesto
    total_patronal = cesantia_empleador + mutual + sis
    
    liquido = tot_haberes - tot_descuentos
    
    # Diccionario de detalles BRUTOS (sin formateo)
    detalles = {
        "grat": gratificacion,
        "imp": imponible,
        "afp": val_afp,
        "salud": val_salud,
        "ces_trab": val_cesantia_trab,
        "tax": val_impuesto,
        "hab": tot_haberes,
        "desc": tot_descuentos,
        "base_trib": base_trib,
        "bonos_imp": bonos_imponibles,
        "bonos_no_imp": bonos_no_imponibles,
        # Costos patronales
        "ces_emp": cesantia_empleador,
        "mutual": mutual,
        "sis": sis,
        "total_patronal": total_patronal,
        # Tasas para referencia
        "tasa_ces_empleador": tasa_ces_emp,
        "tasa_mutual": tasa_mutual,
        "tasa_sis": tasa_sis
    }
    
    return liquido, detalles


def calcular_liquido_desde_base(datos: dict) -> dict:
    """
    API PÚBLICA: Calcula sueldo líquido desde base.
    Función Forward: Base → Líquido
    
    Esta función:
    1. Valida entrada
    2. Llama al motor simular_liquido()
    3. Formatea salida para UI
    
    Args:
        datos: dict con 'sueldo_base' y configuración
    
    Returns:
        dict formateado con todos los valores redondeados
    """
    sueldo_base = datos.get('sueldo_base', 0)
    
    # Validación
    if sueldo_base <= 0:
        raise ValueError("El sueldo base debe ser mayor a 0")
    
    # Extraer datos auxiliares
    movilizacion = datos.get('movilizacion', 0)
    lista_bonos: List[Dict] = datos.get('bonos', [])
    
    bonos_imponibles = sum(b['monto'] for b in lista_bonos if b['imponible'])
    bonos_no_imponibles = sum(b['monto'] for b in lista_bonos if not b['imponible'])
    
    # Llamar al motor
    liquido, d = simular_liquido(sueldo_base, datos)
    
    # Formatear respuesta (aplicar round)
    return {
        "sueldo_base": round(sueldo_base),
        "gratificacion": round(d['grat']),
        "bonos_imponibles": round(bonos_imponibles),
        "bonos_no_imponibles": round(bonos_no_imponibles),
        "movilizacion": round(movilizacion),
        "imponible": round(d['imp']),
        "total_haberes": round(d['hab']),
        
        # Descuentos trabajador
        "cotizacion_previsional": round(d['afp']),
        "cotizacion_salud": round(d['salud']),
        "cesantia": round(d['ces_trab']),
        "impuesto": round(d['tax']),
        "total_descuentos": round(d['desc']),
        "base_tributable": round(d['base_trib']),
        
        # Resultado
        "sueldo_liquido": round(liquido),
        
        # Costos patronales
        "cesantia_empleador": round(d['ces_emp']),
        "mutual": round(d['mutual']),
        "sis": round(d['sis']),
        "total_patronal": round(d['total_patronal']),
        
        # Costo total empresa
        "costo_total_empresa": round(d['hab'] + d['total_patronal'])
    }


def resolver_sueldo_base(datos: dict) -> dict:
    """
    API PÚBLICA: Calcula sueldo base desde líquido deseado.
    Función Inverse: Líquido → Base (con búsqueda binaria)
    
    Algoritmo de búsqueda binaria con REDONDEO A MILES hacia arriba.
    """
    liquido_objetivo = datos['sueldo_liquido']
    movilizacion = datos.get('movilizacion', 0)
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
        "sueldo_base_exacto": round(base_exacta),
        "gratificacion": round(d['grat']),
        "bonos_imponibles": round(bonos_imponibles),
        "bonos_no_imponibles": round(bonos_no_imponibles),
        "movilizacion": round(movilizacion),
        "sueldo_liquido": round(liquido_real),
        "imponible": round(d['imp']),
        "total_haberes": round(d['hab']),
        "total_descuentos": round(d['desc']),
        "impuesto": round(d['tax']),
        "cesantia": round(d['ces_trab']),
        "diferencia": round(diferencia),
        "cotizacion_salud": round(d['salud']),
        "cotizacion_previsional": round(d['afp']),
        "redondeo_aplicado": sueldo_base_redondeado - round(base_exacta),
        # Costos patronales
        "cesantia_empleador": round(d['ces_emp']),
        "mutual": round(d['mutual']),
        "sis": round(d['sis']),
        "total_patronal": round(d['total_patronal']),
        # Costo total empresa
        "costo_total_empresa": round(d['hab'] + d['total_patronal'])
    }


def calcular_costos_patronales(imponible: float, afp_nombre: str, 
                                tipo_contrato: str = "indefinido",
                                nivel_riesgo: str = "bajo",
                                numero_cargas: int = 0) -> dict:
    """
    Calcula todos los costos patronales asociados a la contratación.
    
    Args:
        imponible: Total imponible del trabajador
        afp_nombre: Nombre de la AFP
        tipo_contrato: 'indefinido', 'plazo_fijo', 'casa_particular'
        nivel_riesgo: 'bajo', 'medio', 'alto'
        numero_cargas: Cantidad de hijos para asignación familiar
    
    Returns:
        dict con todos los costos patronales desglosados
    """
    uf = data.VALOR_UF_ACTUAL
    tope_pesos_afp_salud = data.TOPE_IMPONIBLE_AFP_SALUD * uf
    tope_pesos_cesantia = data.TOPE_IMPONIBLE_CESANTIA * uf
    
    # Aplicar topes
    imp_afecto_afp_salud = min(imponible, tope_pesos_afp_salud)
    imp_afecto_cesantia = min(imponible, tope_pesos_cesantia)
    
    # 1. Seguro Cesantía Empleador
    tasa_ces_emp = data.parametros_default.get('tasa_cesant_empleador', 0.024)
    cesantia_empleador = imp_afecto_cesantia * tasa_ces_emp
    
    # 2. Mutual (Accidentes del Trabajo)
    tasa_mutual = data.parametros_default.get('tasa_mutual', 0.0093)
    mutual = imp_afecto_afp_salud * tasa_mutual
    
    # 3. SIS (Seguro Invalidez y Sobrevivencia) - CORREGIDO
    tasa_sis = data.parametros_default.get('tasa_sis', 0.0154)  # ✅ CORRECCIÓN
    sis = imp_afecto_afp_salud * tasa_sis
    
    # TOTAL COSTO PATRONAL
    total_patronal = cesantia_empleador + mutual + sis 
    
    return {
        "cesantia_empleador": round(cesantia_empleador),
        "mutual": round(mutual),
        "sis": round(sis),
        "total_patronal": round(total_patronal),
        "tasa_ces_empleador": tasa_ces_emp,
        "tasa_mutual": tasa_mutual,
        "tasa_sis": tasa_sis
    }

    
def resolver_sueldo_base_completo(datos: dict) -> dict:
    """
    Versión extendida que incluye costos patronales
    """
    # Primero resolver el sueldo base como antes
    resultado_base = resolver_sueldo_base(datos)
    
    # Ahora calcular costos patronales
    costos_patronales = calcular_costos_patronales(
        imponible=resultado_base['imponible'],
        afp_nombre=datos['afp_nombre'],
        tipo_contrato=datos.get('tipo_contrato', 'indefinido'),
        nivel_riesgo=datos.get('nivel_riesgo', 'bajo'),
        numero_cargas=datos.get('numero_cargas', 0)
    )
    
    # Combinar resultados
    resultado_completo = {**resultado_base, **costos_patronales}
    
    # Calcular COSTO TOTAL EMPRESA
    resultado_completo['costo_total_empresa'] = (
        resultado_base['total_haberes'] + 
        costos_patronales['total_patronal']
    )
    
    return resultado_completo