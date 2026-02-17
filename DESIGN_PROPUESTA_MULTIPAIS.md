# Propuesta de Diseño: Calculadora Multi-País

## 🎯 Objetivo
Expandir la calculadora de sueldos para soportar cálculos en **Chile, Perú y Brasil**, manteniendo la arquitectura actual y siguiendo principios de diseño corporativo.

---

## 🎨 Diseño de Frontend

### 1. **Selector de País (Header Superior)**

#### Ubicación
- **Posición**: Parte superior de la ventana, justo debajo del título "Calculadora de Sueldos"
- **Integración**: Dentro del frame del header existente, antes del status de conexión

#### Componente Visual
```
┌─────────────────────────────────────────────────────────┐
│  Calculadora de Sueldos           [STATUS: ONLINE]      │
│                                                          │
│  🌎 País: [🇨🇱 Chile] [🇵🇪 Perú] [🇧🇷 Brasil]          │
└─────────────────────────────────────────────────────────┘
```

#### Especificaciones Técnicas
- **Componente**: `CTkSegmentedButton` (consistente con el selector de modo actual)
- **Valores**: Tres botones con banderas emoji + nombre del país
- **Estado por defecto**: Chile (país actual)
- **Altura**: 50px
- **Espaciado**: 15px padding superior e inferior
- **Comportamiento**: Al cambiar país → recarga configuración específica del país

---

### 2. **Estructura Visual Propuesta**

```
┌──────────────────────────────────────────────────────────────┐
│ ╔══════════════════════════════════════════════════════════╗ │
│ ║  Calculadora de Sueldos              🟢 ONLINE           ║ │
│ ╠══════════════════════════════════════════════════════════╣ │
│ ║  🌎 Seleccionar País:                                    ║ │
│ ║  ┌──────────┬──────────┬──────────┐                      ║ │
│ ║  │🇨🇱 Chile │ 🇵🇪 Perú │🇧🇷 Brasil│  ← CTkSegmentedButton║ │
│ ║  └──────────┴──────────┴──────────┘                      ║ │
│ ╚══════════════════════════════════════════════════════════╝ │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Modo de Cálculo                                          │ │
│ │ [Líquido → Base] [Base → Líquido]                        │ │
│ │ 💡 Ingresa el sueldo líquido deseado...                  │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Datos Principales                                        │ │
│ │ • Sueldo Líquido Deseado                                 │ │
│ │ • Sistema Previsional (AFP/ONP/INSS según país)          │ │
│ │ • Sistema de Salud (Fonasa/Isapre/EPS/SUS según país)    │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Arquitectura de Implementación

### Fase 1: Frontend (Diseño Visual)
**Objetivo**: Implementar la UI sin afectar la lógica existente

#### Cambios en `UI/ui.py`
1. ✅ Modificar `_crear_header()` para incluir selector de países
2. ✅ Agregar variable `self.pais_seleccionado_var = ctk.StringVar(value="chile")`
3. ✅ Crear método `_crear_selector_pais(parent)`
4. ✅ Crear callback `_on_pais_change(seleccion)` para manejar cambios
5. ✅ Agregar indicadores visuales del país activo (bandera + nombre)

#### Código Propuesto
```python
def _crear_selector_pais(self, parent):
    """Selector de país en el header"""
    frame_pais = ctk.CTkFrame(parent, fg_color="transparent")
    frame_pais.pack(pady=(10, 5), fill='x', padx=20)

    # Label
    ctk.CTkLabel(
        frame_pais,
        text="🌎 País:",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="white"
    ).pack(side='left', padx=(0, 10))

    # Segmented Button
    self.pais_segmented = ctk.CTkSegmentedButton(
        frame_pais,
        values=["🇨🇱 Chile", "🇵🇪 Perú", "🇧🇷 Brasil"],
        command=self._on_pais_change,
        font=ctk.CTkFont(size=13, weight="bold"),
        height=40,
        corner_radius=8,
        fg_color=("white", "#1f538d"),
        selected_color=("#FDD835", "#F9A825"),  # Color dorado corporativo
        selected_hover_color=("#FBC02D", "#F57F17")
    )
    self.pais_segmented.pack(side='left', fill='x', expand=True)
    self.pais_segmented.set("🇨🇱 Chile")  # Default

def _on_pais_change(self, seleccion: str):
    """Callback al cambiar de país"""
    # Extraer código del país
    pais_map = {
        "🇨🇱 Chile": "chile",
        "🇵🇪 Perú": "peru",
        "🇧🇷 Brasil": "brasil"
    }
    codigo_pais = pais_map.get(seleccion, "chile")
    self.pais_seleccionado_var.set(codigo_pais)

    # TODO: Cargar configuración del país
    # - Actualizar labels (AFP → ONP/INSS)
    # - Actualizar opciones de salud
    # - Actualizar valores por defecto

    print(f"🌎 País cambiado a: {codigo_pais}")
```

---

### Fase 2: Datos Multi-País
**Objetivo**: Crear estructura de configuración por país

#### Nueva Estructura en `DATA/`
```
DATA/
├── data.py                    # Archivo maestro actual
├── configs/
│   ├── chile_config.py        # Configuración Chile (actual)
│   ├── peru_config.py         # Configuración Perú (nueva)
│   └── brasil_config.py       # Configuración Brasil (nueva)
└── db_loader.py               # Mantener igual
```

#### Ejemplo `peru_config.py`
```python
# Configuración Perú
VALOR_UIT = 5150.0  # Unidad Impositiva Tributaria 2025
SALARIO_MINIMO = 1025.0  # RMV Perú

# Sistema de Pensiones
SISTEMAS_PENSION = {
    "ONP": 0.13,  # 13% para ONP
    "Integra": 0.1025,
    "Profuturo": 0.1067,
    "Prima": 0.1070,
    "Habitat": 0.1072
}

# Sistema de Salud (EsSalud)
TASA_ESSALUD_TRABAJADOR = 0.00  # No descuenta al trabajador
TASA_ESSALUD_EMPLEADOR = 0.09  # 9% empleador

# Tramos de Impuesto a la Renta (5ta categoría)
TRAMOS_IMPUESTO = [
    {"desde": 0, "hasta": 7 * VALOR_UIT, "tasa": 0.08, "deduccion": 0},
    {"desde": 7 * VALOR_UIT, "hasta": 20 * VALOR_UIT, "tasa": 0.14, "deduccion": ...},
    # ...
]
```

---

### Fase 3: Lógica de Negocio
**Objetivo**: Adaptar `SERVICE/engine.py` para multi-país

#### Strategy Pattern para Cálculos
```python
# SERVICE/calculators/
class CalculadoraPais(ABC):
    @abstractmethod
    def calcular_liquido(self, base, **kwargs): pass

    @abstractmethod
    def calcular_base(self, liquido, **kwargs): pass

class CalculadoraChile(CalculadoraPais):
    # Lógica actual

class CalculadoraPeru(CalculadoraPais):
    # Implementación peruana

class CalculadoraBrasil(CalculadoraPais):
    # Implementación brasileña
```

---

## 🎨 Paleta de Colores Corporativa

### Por País
| País   | Color Primario | Color Acento | Uso                          |
|--------|----------------|--------------|------------------------------|
| Chile  | `#0033A0`      | `#D52B1E`    | Botones, bordes activos      |
| Perú   | `#D91023`      | `#FFFFFF`    | Indicadores, badges          |
| Brasil | `#009739`      | `#FFDF00`    | Estado activo, highlights    |

### Componentes Actualizados
- **Botón Calcular**: Cambia color según país seleccionado
- **Header**: Aplica color corporativo del país
- **Indicadores**: Badges con colores nacionales

---

## 📱 UX/UI - Buenas Prácticas

### ✅ Principios Aplicados
1. **Consistencia Visual**: Usar `CTkSegmentedButton` para selectores (país + modo)
2. **Feedback Inmediato**: Mostrar país activo con color diferenciado
3. **Localización**: Términos específicos por país (AFP vs ONP vs INSS)
4. **Accesibilidad**: Banderas + texto para clarity
5. **Progressive Disclosure**: Mostrar solo campos relevantes al país

### 🔔 Notificaciones al Usuario
```
Al cambiar de país:
┌────────────────────────────────────────┐
│ ℹ️  Configuración actualizada          │
│                                        │
│ Ahora estás calculando salarios para:  │
│ 🇵🇪 Perú - Sistema ONP/EPS             │
│                                        │
│ [Entendido]                            │
└────────────────────────────────────────┘
```

---

## 🚀 Plan de Implementación

### Sprint 1: Frontend (Esta fase)
- [x] Revisar CLAUDE.md y código actual
- [ ] Implementar selector de país en header
- [ ] Adaptar labels dinámicos según país
- [ ] Crear sistema de callbacks para cambio de país
- [ ] Testing visual en Windows

### Sprint 2: Datos
- [ ] Investigar legislación laboral de Perú
- [ ] Investigar legislación laboral de Brasil
- [ ] Crear archivos de configuración por país
- [ ] Implementar loader dinámico de configuraciones

### Sprint 3: Lógica
- [ ] Refactorizar `engine.py` para Strategy Pattern
- [ ] Implementar `CalculadoraPeru`
- [ ] Implementar `CalculadoraBrasil`
- [ ] Validar cálculos con casos reales

### Sprint 4: Testing & Deploy
- [ ] Pruebas unitarias por país
- [ ] Validación con stakeholders de cada país
- [ ] Actualizar `build.py` para incluir nuevos assets
- [ ] Documentar en CLAUDE.md

---

## 📊 Métricas de Éxito

- ✅ UI responde en < 100ms al cambiar país
- ✅ 100% de campos se adaptan al país seleccionado
- ✅ Cálculos precisos (error < 1% vs casos reales)
- ✅ Ejecutable < 50MB con 3 países
- ✅ Zero breaking changes en funcionalidad Chile

---

## 🔒 Consideraciones de Seguridad

- Validar inputs según reglas de cada país
- Evitar inyección SQL en queries multi-país
- Encriptar configuraciones sensibles en `.env`
- Logs separados por país para auditoría

---

## 📚 Referencias por País

### Chile
- [Dirección del Trabajo](https://www.dt.gob.cl/)
- Código del Trabajo - Artículo 42 (Gratificación)

### Perú
- [SUNAT - 5ta Categoría](https://www.sunat.gob.pe/)
- [SBS - AFP](https://www.sbs.gob.pe/)

### Brasil
- [Ministério do Trabalho](https://www.gov.br/trabalho-e-previdencia/)
- CLT - Consolidação das Leis do Trabalho

---

**Próximo Paso**: ¿Apruebas este diseño para proceder con la implementación del frontend?
