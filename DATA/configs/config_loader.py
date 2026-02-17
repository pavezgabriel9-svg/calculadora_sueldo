# DATA/configs/config_loader.py
"""
Cargador dinámico de configuraciones por país
Permite obtener la configuración correcta según el país seleccionado en la UI
"""

from typing import Dict, Any, List
from . import chile_config, peru_config, brasil_config

# Mapeo de códigos de país a módulos de configuración
CONFIGS = {
    "chile": chile_config,
    "peru": peru_config,
    "brasil": brasil_config,
}

def obtener_config(codigo_pais: str):
    """
    Obtiene el módulo de configuración para un país específico

    Args:
        codigo_pais: Código del país ("chile", "peru", "brasil")

    Returns:
        Módulo de configuración del país

    Raises:
        ValueError: Si el país no está soportado
    """
    config = CONFIGS.get(codigo_pais)
    if config is None:
        raise ValueError(f"País '{codigo_pais}' no soportado. Países disponibles: {list(CONFIGS.keys())}")
    return config


def obtener_parametros(codigo_pais: str) -> Dict[str, Any]:
    """
    Obtiene el diccionario de parámetros para un país

    Args:
        codigo_pais: Código del país

    Returns:
        Dict con parámetros del país
    """
    config = obtener_config(codigo_pais)
    return config.obtener_parametros()


def obtener_tramos_impuesto(codigo_pais: str) -> List[Dict]:
    """
    Obtiene los tramos de impuesto para un país

    Args:
        codigo_pais: Código del país

    Returns:
        Lista de tramos de impuesto
    """
    config = obtener_config(codigo_pais)
    return config.TRAMOS_IMPUESTO


def obtener_tasas_pension(codigo_pais: str) -> Dict[str, float]:
    """
    Obtiene las tasas del sistema previsional para un país

    Args:
        codigo_pais: Código del país

    Returns:
        Dict con nombres y tasas de AFP/ONP/INSS según país
    """
    config = obtener_config(codigo_pais)

    if codigo_pais == "chile":
        return config.TASAS_PENSION
    elif codigo_pais == "peru":
        return config.TASAS_AFP  # Perú tiene AFP + ONP
    elif codigo_pais == "brasil":
        # Brasil tiene INSS progresivo, retornar estructura especial
        return {"INSS": config.TRAMOS_INSS}

    return {}


def obtener_labels_ui(codigo_pais: str) -> Dict[str, str]:
    """
    Obtiene los labels de UI específicos del país

    Args:
        codigo_pais: Código del país

    Returns:
        Dict con labels traducidos/adaptados al país
    """
    config = obtener_config(codigo_pais)
    return config.LABELS_UI


def obtener_info_pais(codigo_pais: str) -> Dict[str, str]:
    """
    Obtiene información general del país

    Args:
        codigo_pais: Código del país

    Returns:
        Dict con info del país (nombre, moneda, símbolo)
    """
    config = obtener_config(codigo_pais)
    return {
        "codigo": config.CODIGO_PAIS,
        "nombre": config.NOMBRE_PAIS,
        "moneda": config.MONEDA,
        "simbolo_moneda": config.SIMBOLO_MONEDA,
    }


# ═══════════════════════════════════════════════════════════════
#  EJEMPLO DE USO (Para implementar en main.py - Fase 2)
# ═══════════════════════════════════════════════════════════════
#
# from DATA.configs.config_loader import obtener_parametros, obtener_labels_ui
#
# # En el callback de cambio de país:
# pais_actual = app.obtener_pais_seleccionado()  # "chile", "peru", "brasil"
#
# # Cargar parámetros del país
# parametros = obtener_parametros(pais_actual)
#
# # Actualizar labels en la UI
# labels = obtener_labels_ui(pais_actual)
# app.actualizar_label_pension(labels["sistema_pension"])  # "AFP", "ONP/AFP", "INSS"
#
# # Pasar parámetros a engine.py para cálculos
# resultado = engine.calcular_liquido_desde_base(datos, parametros=parametros)
# ═══════════════════════════════════════════════════════════════
