# calculos.py
# SERVICE/engine.py
from DATA import data
from typing import List, Dict

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

def resolver_sueldo_base(datos: dict) -> dict:
    """
    Algoritmo de búsqueda binaria robusto (While Loop + Precisión).
    """
    # --- 1. Desempaquetar y preparar datos ---
    liquido_objetivo = datos['sueldo_liquido']
    movilizacion = datos['movilizacion']
    lista_bonos: List[Dict] = datos.get('bonos', [])
    
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
    if not usar_fonasa:
        # Si es Isapre, el valor viene en UF desde la UI
        costo_plan_isapre = datos['salud_uf'] * uf
    
    # --- 2. Configuración del Algoritmo de Búsqueda ---
    precision = 1.0  # Queremos exactitud de $1 peso
    min_base = 0
    max_base = liquido_objetivo * 3.0 # Rango amplio inicial
    
    # Variables de resultado
    base_final = 0
    iteraciones = 0
    
    # Función interna de estimación (Simulación Forward)
    def estimar_liquido(sueldo_base_test):
        # A. Gratificación
        tope_grat = (4.75 * ingreso_minimo) / 12
        gratificacion = min(sueldo_base_test * 0.25, tope_grat)
        
        #tope_gratificacion_mensual = 4.75 * ingreso_minimo / 12
        #gratificacion = min(0.25 * sueldo_base, tope_gratificacion_mensual)
    
        
        # B. Total Imponible (Base + Grat + Bonos)
        imponible = sueldo_base_test + gratificacion + bonos_imponibles
        
        # C. Aplicar Topes Legales Diferenciados 
        imp_afecto_afp_salud = min(imponible, tope_pesos_afp_salud)
        imp_afecto_cesantia = min(imponible, tope_pesos_cesantia)
        
        # D. Cálculos Previsionales
        val_afp = imp_afecto_afp_salud * tasa_afp
        val_cesantia = imp_afecto_cesantia * tasa_cesantia
        
        val_salud = 0
        if usar_fonasa:
            # Fonasa: 7% del imponible topeado
            val_salud = imp_afecto_afp_salud * tasa_fonasa
        else:
            # Isapre: Mayor valor entre el 7% legal y el plan pactado
            siete_porciento = imp_afecto_afp_salud * tasa_fonasa
            val_salud = max(siete_porciento, costo_plan_isapre)
            
        # E. Impuesto
        base_trib = imponible - val_afp - val_salud - val_cesantia
        val_impuesto = calcular_impuesto_unico(base_trib)
        
        # F. Líquido
        tot_haberes = imponible + movilizacion + bonos_no_imponibles
        tot_descuentos = val_afp + val_salud + val_cesantia + val_impuesto
        
        return tot_haberes - tot_descuentos, {
            "grat": gratificacion, "imp": imponible, "afp": val_afp, 
            "salud": val_salud, "ces": val_cesantia, "tax": val_impuesto,
            "hab": tot_haberes, "desc": tot_descuentos, "base_trib": base_trib,
        }

    # --- 3. Ejecución del Bucle (While Loop) ---
    detalles_finales = {}
    liquido_calc = 0
    
    # Expandir rango si es necesario (Safety check)
    while estimar_liquido(max_base)[0] < liquido_objetivo:
        max_base *= 2

    while (max_base - min_base) > precision and iteraciones < 100:
        base_final = (min_base + max_base) / 2
        liquido_calc, detalles = estimar_liquido(base_final)
        
        if liquido_calc < liquido_objetivo:
            min_base = base_final
        else:
            max_base = base_final
        
        detalles_finales = detalles
        iteraciones += 1
        
    # Redondear resultado final
    sueldo_base_final = round(base_final)
    
    # Recalcular una última vez con el entero redondeado para exactitud de visualización
    liquido_real, d = estimar_liquido(sueldo_base_final)
    
    return {
        "sueldo_base": sueldo_base_final,
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
        "diferencia": round(liquido_real - liquido_objetivo),
        "cotizacion_salud": round(d['salud']),
        "cotizacion_previsional": round(d['afp'])
    }