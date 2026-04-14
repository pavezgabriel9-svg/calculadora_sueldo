# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-country salary calculator desktop application that performs bidirectional salary calculations (base salary ↔ liquid salary) with support for country-specific pension systems, health insurance, bonuses, and employer costs.

**Supported Countries**: 🇨🇱 Chile (complete), 🇵🇪 Perú (in progress), 🇧🇷 Brasil (in progress)

**Tech Stack**: Python 3.13, CustomTkinter (GUI), PyODBC (database), PyInstaller (packaging)

## Architecture

3-layer architecture with clear separation of concerns:

- **DATA/**: Data layer containing configuration, database access, and caching
  - [data.py](DATA/data.py): Global defaults and connection state (maintained for backward compatibility)
  - [db_loader.py](DATA/db_loader.py): Database connection with JSON cache fallback mechanism
  - **[configs/](DATA/configs/)**: Multi-country configuration system
    - [chile_config.py](DATA/configs/chile_config.py): ✅ Complete Chilean configuration (UF, AFP, tax brackets)
    - [peru_config.py](DATA/configs/peru_config.py): ⚠️ Peruvian configuration skeleton (UIT, ONP/AFP, EsSalud)
    - [brasil_config.py](DATA/configs/brasil_config.py): ⚠️ Brazilian configuration skeleton (BRL, INSS, SUS)
    - [config_loader.py](DATA/configs/config_loader.py): Dynamic configuration loader by country

- **SERVICE/**: Business logic layer
  - [engine.py](SERVICE/engine.py): Core calculation algorithms (tax calculation, liquid simulation, binary search)
  - [services.py](SERVICE/services.py): Helper functions for formatting and data access

- **UI/**: User interface layer
  - [ui.py](UI/ui.py): Main window with CustomTkinter components
  - [components/](UI/components/): Reusable UI components (bonos, results_popup)

- [main.py](main.py): Application entry point that wires callbacks between layers

## Development Commands

### Running the Application
```bash
python main.py
```

### Building Executable (Windows)
```bash
python build.py
```

This creates a distributable Windows application in `dist/CalculadoraSueldos/` using PyInstaller. The build includes CustomTkinter assets and the application icon.

### Virtual Environment
```bash
# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix

# Install dependencies
pip install -r requirements.txt
```

## Key Calculation Algorithms

### Forward Calculation (Base → Liquid)
[engine.py:32-154](SERVICE/engine.py#L32-L154) `simular_liquido()` - Direct calculation from base salary to liquid salary. Steps:
1. Calculate gratification (capped at 4.75 * minimum wage / 12)
2. Sum taxable base (base + gratification + taxable bonuses)
3. Apply caps (AFP/health cap, unemployment cap)
4. Calculate worker deductions (AFP, health, unemployment)
5. Calculate tax on taxable base
6. Calculate employer costs (mutual, SIS, unemployment, life insurance, etc.)
7. Return liquid salary and detailed breakdown

### Reverse Calculation (Liquid → Base)
[engine.py:224-299](SERVICE/engine.py#L224-L299) `resolver_sueldo_base()` - Uses binary search to find base salary from target liquid salary. Critical detail: **rounds UP to nearest thousand** using [redondear_a_miles_arriba()](SERVICE/engine.py#L6-L12).

### Tax Calculation
[engine.py:15-29](SERVICE/engine.py#L15-L29) `calcular_impuesto_unico()` - Progressive tax brackets from DATA/data.py tramos_default. Returns: (base * rate) - rebate.

## Database & Configuration

### Connection Behavior
1. Attempts SQL Server connection using `.env` credentials
2. On success: updates in-memory values + saves to `cache_config.json`
3. On failure: loads from `cache_config.json` (if exists)
4. Final fallback: hardcoded defaults in [DATA/data.py](DATA/data.py)

### Environment Variables
Located in `.env` (NOT committed to git):
- `DB_CONNECTION_STRING`: SQL Server connection string
- `DB_QUERY_CONFIG`: Query to fetch configuration data

### Cache File
`cache_config.json` stores successful database fetches. JSON-safe handling of `float('inf')` by converting to `MAX_JSON_NUMBER = 999999999999.0`.

## Chilean Labor Law Context

This calculator implements Chilean labor regulations:

- **UF (Unidad de Fomento)**: Inflation-indexed unit of account
- **AFP**: Mandatory pension fund contributions (worker pays ~10-11%)
- **Fonasa vs Isapre**: Public vs private health insurance (7% minimum)
- **Gratificación**: Mandatory bonus (25% of base, capped at 4.75 minimum wages annually)
- **Topes Imponibles**: Caps on contributions (89.9 UF for AFP/health, 135.1 UF for unemployment)
- **Employer Costs**: Mutual (work accidents), SIS (disability insurance), unemployment insurance, life insurance, AFP employer contribution, supplementary health insurance

Tax brackets and rates are in [DATA/data.py](DATA/data.py#L50-L58).

## UI Modes

The application supports two calculation modes (toggled in UI):
- **liquido_a_base**: User enters desired liquid salary → calculates base (original mode)
- **base_a_liquido**: User enters base salary → calculates liquid (forward calculation)

Results displayed in popup via [UI/components/results_popup.py](UI/components/results_popup.py).

## Important Implementation Details

- **Rounding**: Base salary always rounded UP to nearest $1,000 in reverse calculation
- **Bonus Handling**: Bonuses can be marked as taxable (imponible) or non-taxable
- **Precision**: Binary search uses 1.0 peso precision, max 100 iterations
- **Number Formatting**: Chilean format uses dots for thousands (e.g., "1.234.567")
- **Icon**: Application icon at `assets/logo.ico` embedded in executable

## Code Conventions

- Function names in Spanish match domain language (gratificación, imponible, etc.)
- Type hints used for public APIs
- Comments in Spanish for domain-specific logic
- `simular_liquido()` returns tuple: (liquid_amount, details_dict)
- Public APIs (`calcular_liquido_desde_base`, `resolver_sueldo_base`) return formatted dicts with rounded values

## Multi-Country Support (NEW)

### Architecture
The application now supports multiple countries through a configuration-based system:

**Country Selector**: Located in UI header ([ui.py:102-156](UI/ui.py#L102-L156))
- CTkSegmentedButton with flags: 🇨🇱 Chile | 🇵🇪 Perú | 🇧🇷 Brasil
- State stored in `pais_seleccionado_var`
- Callback: `_on_pais_change()` triggers configuration reload

**Configuration Files**: [DATA/configs/](DATA/configs/)
- Each country has dedicated config file with country-specific parameters
- Dynamic loading via `config_loader.py`
- Chile configuration is complete and production-ready
- Peru and Brazil configs are skeletons requiring completion

### Configuration Structure
Each country config includes:
- **Currency & Units**: Valor UF (Chile), UIT (Peru), BRL (Brazil)
- **Minimum Wage**: Country-specific minimum salaries
- **Pension System**: AFP (Chile), ONP/AFP (Peru), INSS (Brazil)
- **Health System**: Fonasa/Isapre (Chile), EsSalud/EPS (Peru), SUS (Brazil)
- **Tax Brackets**: Progressive tax tables with country-specific rates
- **Employer Costs**: Mutual, SIS, FGTS, etc. (country-dependent)
- **UI Labels**: Localized terminology for each country

### Usage Example
```python
from DATA.configs.config_loader import obtener_parametros, obtener_labels_ui

# Get current country from UI
pais = app.obtener_pais_seleccionado()  # "chile", "peru", "brasil"

# Load country-specific parameters
params = obtener_parametros(pais)

# Get localized UI labels
labels = obtener_labels_ui(pais)
# Chile: {"sistema_pension": "AFP", ...}
# Peru:  {"sistema_pension": "ONP/AFP", ...}
# Brazil: {"sistema_pension": "INSS", ...}
```

### Implementation Status
- ✅ **Phase 1 Complete**: UI selector implemented and functional
- ✅ **Chile Config**: Complete with all parameters (migrated from data.py)
- ⚠️ **Peru Config**: Skeleton created, requires completion with real data
- ⚠️ **Brazil Config**: Skeleton created, requires completion with real data
- ⏳ **Phase 2 Pending**: Dynamic label updates based on country selection
- ⏳ **Phase 3 Pending**: Engine adaptation for country-specific calculations

### Important Notes
- Chile configuration is tested and production-ready
- Peru/Brazil configs marked with ⚠️ warnings - DO NOT use in production without validation
- Config loader provides type-safe access to all parameters
- See [DATA/configs/README.md](DATA/configs/README.md) for detailed completion tasks
