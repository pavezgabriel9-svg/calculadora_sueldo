"""
    Módulo de servicios para la calculadora de sueldos.
"""
from DATA import data  

def obtener_lista_afps() -> list:
    """Retorna la lista de nombres de AFPs ordenadas alfabéticamente"""
    return sorted(list(data.TASAS_AFP.keys()))

def obtener_tasa_afp(nombre_afp: str) -> float:
    """Retorna la tasa decimal asociada al nombre de la AFP"""
    return data.TASAS_AFP.get(nombre_afp, 0.0)


def formato_chile_sueldo(current_value: str) -> str:
    try:
        numeric_value = int("".join(filter(str.isdigit, current_value)))
        formatted_value = f"{numeric_value:,}".replace(",", ".")
        return formatted_value
    except (ValueError, TypeError):
        return ""
    
def obtener_defaults_salud():
    """Retorna una tupla con (Valor UF Global, Plan Isapre Default)"""
    return data.VALOR_UF_ACTUAL, data.DEFAULT_PLAN_ISAPRE_UF

def calcular_costo_isapre_pesos(plan_uf: str) -> str:
    """Convierte el plan UF a pesos y lo formatea"""
    try:
        # Reemplazar comas por puntos si el usuario usa decimales latinos
        valor_uf_float = float(plan_uf.replace(',', '.'))
        total_pesos = int(valor_uf_float * data.VALOR_UF_ACTUAL)
        return f"$ {total_pesos:,}".replace(",", ".")
    except ValueError:
        return "$ 0"