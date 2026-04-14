# Configuraciones Multi-País

Este directorio contiene las configuraciones específicas para cada país soportado por la calculadora de sueldos.

## 📁 Estructura

```
DATA/configs/
├── __init__.py                # Inicialización del paquete
├── config_loader.py           # Cargador dinámico de configuraciones
├── chile_config.py            ✅ COMPLETO - Datos migrados desde data.py
├── peru_config.py             ⚠️ BOSQUEJO - Completar con datos reales
├── brasil_config.py           ⚠️ BOSQUEJO - Completar con datos reales
└── README.md                  # Este archivo
```

---

## ✅ Chile (`chile_config.py`)

**Estado**: ✅ **COMPLETO Y FUNCIONAL**

Datos migrados desde `DATA/data.py` (configuración original que funciona correctamente).

### Contenido:
- ✅ UF (Unidad de Fomento): $39,597.67
- ✅ Sueldo Mínimo: $539,000
- ✅ Topes Imponibles: 89.9 UF (AFP/Salud), 135.1 UF (Cesantía)
- ✅ Sistema AFP: 7 administradoras con tasas actualizadas
- ✅ Sistema Salud: Fonasa (7%) / Isapre (variable)
- ✅ Gratificación Legal: 25% tope 4.75 sueldos mínimos
- ✅ Costos Patronales: Mutual, SIS, AFP empleador, etc.
- ✅ Tramos de Impuesto Único: 8 tramos progresivos

**No requiere modificaciones** - Listo para producción.

---

## ⚠️ Perú (`peru_config.py`)

**Estado**: ⚠️ **BOSQUEJO - COMPLETAR**

### Diferencias Clave vs Chile:
- 📌 **UIT** (Unidad Impositiva Tributaria) en lugar de UF
- 📌 **ONP** (Sistema Público) o **AFP** (Sistema Privado)
- 📌 **EsSalud**: 9% pagado por EMPLEADOR (trabajador no paga)
- 📌 **Gratificación**: 2 al año (julio y diciembre) = ~16.67% mensual
- 📌 **CTS**: Compensación por Tiempo de Servicios (único de Perú)
- 📌 **Impuesto a la Renta (5ta Categoría)**: Cálculo anual prorrateado

### ✅ Tareas para Completar:

1. **Valores Básicos**
   - [ ] Verificar UIT vigente 2025-2026
   - [ ] Actualizar RMV (Remuneración Mínima Vital)

2. **Sistema Previsional**
   - [ ] Confirmar tasa ONP (actualmente 13%)
   - [ ] Actualizar tasas AFP desde [SBS](https://www.sbs.gob.pe/app/stats/TasaPrevisional_33.asp)
   - [ ] Validar si existen topes para pensiones

3. **Sistema de Salud**
   - [ ] Confirmar que EsSalud es 9% empleador, 0% trabajador
   - [ ] Investigar funcionamiento de EPS (seguros privados)

4. **Beneficios**
   - [ ] Validar cálculo de gratificaciones (2 sueldos/año)
   - [ ] Calcular correctamente CTS mensualizado

5. **Impuestos**
   - [ ] Completar tabla de Impuesto a la Renta con rebajas correctas
   - [ ] Obtener tramos actualizados desde [SUNAT](https://www.sunat.gob.pe/)

6. **Costos Patronales**
   - [ ] Verificar tasa SENATI (0.75%, solo manufactura)
   - [ ] Investigar SCTR (Seguro Complementario de Trabajo de Riesgo)

### 📚 Referencias:
- **SUNAT**: https://www.sunat.gob.pe/indicestasas/
- **SBS AFP**: https://www.sbs.gob.pe/app/stats/TasaPrevisional_33.asp
- **Ministerio de Trabajo**: https://www.gob.pe/mtpe

---

## ⚠️ Brasil (`brasil_config.py`)

**Estado**: ⚠️ **BOSQUEJO - COMPLETAR**

### Diferencias Clave vs Chile:
- 📌 **Real (BRL)**: No usa unidad indexada como UF
- 📌 **INSS**: Sistema progresivo por tramos (similar al impuesto)
- 📌 **SUS**: Sistema de salud gratuito, sin descuento al trabajador
- 📌 **13º Salário**: Gratificación obligatoria de fin de año
- 📌 **Férias + 1/3**: Vacaciones con pago adicional de 33%
- 📌 **FGTS**: Fondo de garantía (8% empleador)
- 📌 **IRRF**: Impuesto a la renta progresivo mensual

### ✅ Tareas para Completar:

1. **Valores Básicos**
   - [ ] Verificar Salário Mínimo vigente 2025-2026
   - [ ] Actualizar Teto INSS (tope máximo de contribución)

2. **Sistema Previsional (INSS)**
   - [ ] Confirmar tabla INSS progresiva vigente (4 tramos)
   - [ ] Implementar función `calcular_inss_progresivo()`
   - [ ] Validar tasa INSS patronal (generalmente 20%)

3. **Sistema de Salud**
   - [ ] Confirmar que SUS no tiene descuento directo
   - [ ] Investigar funcionamiento de Planos de Saúde privados

4. **Beneficios Obligatorios**
   - [ ] Validar cálculo de 13º Salário mensualizado (1/12)
   - [ ] Validar cálculo de Férias + 1/3 mensualizado
   - [ ] Confirmar FGTS (8% sobre salario bruto)

5. **Impuestos (IRRF)**
   - [ ] Actualizar tabla IRRF con valores vigentes
   - [ ] Validar deducciones (por dependiente, pensión, etc.)
   - [ ] Confirmar rebajas por tramo

6. **Costos Patronales**
   - [ ] Verificar todas las tasas del Sistema S (SESI, SENAI, SESC, SENAC)
   - [ ] Confirmar SAT (Seguro Acidente Trabalho) - varía por riesgo
   - [ ] Validar Salário Educação, SEBRAE, INCRA

### 📚 Referencias:
- **Receita Federal**: https://www.gov.br/receitafederal/
- **INSS**: https://www.gov.br/inss/
- **Ministério do Trabalho**: https://www.gov.br/trabalho-e-previdencia/
- **CLT**: Consolidação das Leis do Trabalho (Lei 5.452/1943)
- **Reforma da Previdência**: EC 103/2019

---

## 🔧 Cómo Usar el Config Loader

### Ejemplo básico:

```python
from DATA.configs.config_loader import obtener_parametros, obtener_labels_ui

# Obtener configuración según país seleccionado
pais = "chile"  # o "peru", "brasil"

# Cargar parámetros
params = obtener_parametros(pais)
print(params["ingreso_minimo"])  # 539000 (Chile)

# Obtener labels para UI
labels = obtener_labels_ui(pais)
print(labels["sistema_pension"])  # "AFP" (Chile), "ONP/AFP" (Perú), "INSS" (Brasil)
```

### Funciones disponibles:

| Función                          | Descripción                                    |
|----------------------------------|------------------------------------------------|
| `obtener_config(codigo_pais)`    | Obtiene el módulo completo de configuración   |
| `obtener_parametros(codigo_pais)`| Obtiene dict de parámetros para cálculos      |
| `obtener_tramos_impuesto(codigo)`| Obtiene tabla de impuestos                     |
| `obtener_tasas_pension(codigo)`  | Obtiene tasas AFP/ONP/INSS según país          |
| `obtener_labels_ui(codigo)`      | Obtiene labels traducidos para la UI          |
| `obtener_info_pais(codigo)`      | Obtiene info general (nombre, moneda, etc.)   |

---

## 🚀 Próximos Pasos (Fase 2)

### 1. Completar Configuraciones
- Investigar legislación laboral de Perú y Brasil
- Actualizar valores en `peru_config.py` y `brasil_config.py`
- Validar con casos reales de cada país

### 2. Integrar con UI
- Modificar `UI/ui.py` para usar `config_loader`
- Actualizar labels dinámicamente según país
- Cambiar opciones de AFP/ONP/INSS según país

### 3. Adaptar Engine
- Modificar `SERVICE/engine.py` para aceptar parámetros por país
- Implementar lógicas especiales (INSS progresivo, CTS, etc.)
- Crear calculadoras específicas si es necesario

### 4. Testing
- Crear casos de prueba por país
- Validar cálculos con stakeholders locales
- Comparar con calculadoras oficiales de cada país

---

## ⚠️ Importante

**Chile está listo para producción.**
**Perú y Brasil son BOSQUEJOS** - no usar en producción sin completar y validar los datos.

Todos los valores marcados con ⚠️ **VERIFICAR** o **COMPLETAR** deben ser actualizados con datos oficiales antes de usar la calculadora para esos países.

---

## 📞 Soporte

Para completar las configuraciones de Perú y Brasil, consultar:
- Sitios oficiales de gobierno (SUNAT, Receita Federal, etc.)
- Ministerios de Trabajo de cada país
- Asesores laborales locales
- Casos de prueba reales de empresas en cada país
