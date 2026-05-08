# Target Star Schema — DB_MAGAZZINO

> Target state design for the DB_MAGAZZINO semantic model after refactoring

---

## Current Architecture Issues

```
Current State (Snowflake + Mixed):
CLIENTI → COMUNI → AREA          ← 3-level snowflake
DOCUMENTO VENDITA has 9 FK rels   ← central hub, not star
17 LocalDateTable islands          ← ghost tables
Multiple AutoDetected relations    ← ambiguous
```

---

## Target Schema

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DIM_Calendario                             │
│  Date (PK) │ Year │ MonthName │ MonthInCalendar │ ...              │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
       ┌───────────────────┼───────────────────────┐
       │                   │                       │
       ▼                   ▼                       ▼
┌──────────────┐   ┌──────────────┐       ┌──────────────┐
│ FACT_Vendite │   │FACT_Ordini   │       │FACT_Magazzino│
│ (data)       │   │(data)        │       │(data)        │
└──────┬───────┘   └──────┬───────┘       └──────┬───────┘
       │                  │                      │
       ▼                  ▼                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          DIM_Articoli                               │
│  CodiceArticolo (PK) │ Nome │ GruppoArticolo │ ...                 │
└─────────────────────────────────────────────────────────────────────┘
       ▲                  ▲                      ▲
       │                  │                      │
┌──────┴───────┐   ┌──────┴───────┐       ┌──────┴───────┐
│ FACT_Vendite │   │FACT_Ordini   │       │FACT_Magazzino│
│ (articolo)   │   │(articolo)    │       │(articolo)    │
└──────────────┘   └──────────────┘       └──────────────┘
```

---

## Fact Tables (Target)

### FACT_Vendite (renamed from DOCUMENTO VENDITA + Tab VENDITE)
| Column | FK to | Type |
|--------|-------|------|
| CodiceDocumento | (PK) | string |
| CodiceCliente | DIM_Clienti | string |
| CodiceArticolo | DIM_Articoli | string |
| CodiceDeposito | DIM_Deposito | string |
| CodiceProgetto | DIM_Progetto | string |
| CodiceReparto | DIM_Reparto | string |
| CodiceCategoria | DIM_GruppiVendita | string |
| CodiceMezzoTrasporto | DIM_MezziTrasporto | string |
| DataSpedizione | DIM_Calendario | date |
| DataRegistrazione | DIM_Calendario | date (inactive) |
| TipoRiga | (attribute) | string |
| TipoDocumento | (attribute) | string |
| Importo | (measure) | decimal |
| Quantità | (measure) | decimal |
| CostoTrasporto | (measure) | decimal |

### FACT_Magazzino (renamed from MAGAZZINO)
| Column | FK to | Type |
|--------|-------|------|
| IDMovimento | (PK) | int64 |
| CodiceArticolo | DIM_Articoli | string |
| CodiceFornitore | DIM_Fornitori | string |
| CodiceDeposito | DIM_Deposito | string |
| CodiceCategoria | DIM_GruppiVendita | string |
| Data | DIM_Calendario | date |
| Quantità | (measure) | decimal |
| Importo | (measure) | decimal |
| CostoUnitario | (measure) | decimal |

### FACT_Ordini (renamed from ORDINI)
| Column | FK to | Type |
|--------|-------|------|
| IDOrdine | (PK) | int64 |
| CodiceArticolo | DIM_Articoli | string |
| CodiceSpedizioniere | DIM_Spedizionieri | string |
| CodiceCliente | DIM_Clienti | string |
| CodiceCategoria | DIM_GruppiVendite | string |
| CodiceDeposito | DIM_Deposito | string |
| DataSpedizione | DIM_Calendario | date |
| Quantità | (measure) | decimal |

### FACT_MovimentiCG (renamed from MOVCG)
| Column | FK to | Type |
|--------|-------|------|
| IDMovimento | (PK) | int64 |
| CodiceConto | DIM_PianoConti | string |
| CodiceMezzoTrasporto | DIM_MezziTrasporto | string |
| CodiceProgetto | DIM_Progetto | string |
| CodiceReparto | DIM_Reparto | string |
| CodiceCategoria | DIM_GruppiVendita | string |
| DataRegistrazione | DIM_Calendario | date |
| Quantità | (measure) | decimal |
| Importo | (measure) | decimal |

### FACT_Accantonamenti (renamed from ACCANTONAMENTI)
| Column | FK to | Type |
|--------|-------|------|
| IDAccantonamento | (PK) | int64 |
| CodiceConto | DIM_PianoConti | string |
| CodiceMezzoTrasporto | DIM_MezziTrasporto | string |
| DataAccantonamento | DIM_Calendario | date |
| Importo | (measure) | decimal |

---

## Dimension Tables (Target)

### DIM_Articoli (renamed from ARTICOLI)
| Column | Description |
|--------|-------------|
| CodiceArticolo (PK) | Product code |
| Nome | Product name |
| GruppoArticolo | Product group (PROPANO, MIX, etc.) |
| CostoUnitario | Unit cost |
| UltimoCostoDiretto | Last direct cost |
| DensitàTA | Density T/A |
| Densità15C | Density at 15°C |

### DIM_Clienti (renamed from CLIENTI)
| Column | Description |
|--------|-------------|
| CodiceCliente (PK) | Customer code |
| Nome | Customer name |
| Indirizzo | Address |
| Città | City |
| Provincia | Province |
| CAP | Postal code |
| Gruppo | Customer group |

**Flatten COMUNI + AREA into DIM_Clienti:**
Add `NomeComune` (string), `SiglaProvincia` (string), `AreaGeografica` (string)
→ Eliminates CLIENTI → COMUNI → AREA snowflake chain

### DIM_Fornitori (renamed from FORNITORI)
| Column | Description |
|--------|-------------|
| CodiceFornitore (PK) | Supplier code |
| Nome | Supplier name |
| Città | City |
| Provincia | Province |

### DIM_Calendario (renamed from CALENDARIO)
| Column | Description |
|--------|-------------|
| Date (PK) | Full date |
| Year | Year |
| MonthName | Month name (Italian) |
| MonthInCalendar | Month label |
| QuarterInCalendar | Quarter label |
| MonthnYear | Month-year integer |
| WeekEnding | Week ending date |
| DayOfWeekName | Day name |

**Mark as Date Table:**
```tmdl
table DIM_Calendario
    annotation PBI_CalendarTable = true
```

### DIM_Deposito (renamed from UBICAZIONE)
| Column | Description |
|--------|-------------|
| CodiceDeposito (PK) | Location code |
| NomeDeposito | Location name |

### DIM_GruppiVendita (renamed from GRUPPI_VENDITE)
| Column | Description |
|--------|-------------|
| CodiceCategoria (PK) | Category code |
| NomeCategoria | Category name |
| GruppoVendita | Sales group (PASSAGGIO, DIRETTE) |

---

## KPI Tables (Target)

### KPI_Vendite (merged from ANALISI_VENDITE)
Measures: Total Sales, Profit Margins Customer, Margin Growth %, # Clienti, etc.

### KPI_VenditeDocumento (renamed from ANALISI_DOC_VENDITA)
Measures: Importo Vendite, Qta Vendite, Forecast variants — consolidated

### KPI_Magazzino (renamed from ANALISI_MAGAZZINO)
Measures: Qta Ton, Importo, Giacenza, CMP

### KPI_Prodotto (renamed from ANALISI_PRODOTTO)
Measures: Costo Acquisto, CMP, Margine Unitario, Costo Venduto

### KPI_Mix (renamed from ANALISI_MIX)
Measures: Tassi, Prezzi, Costi MIX/PROPANO

### KPI_CMP (renamed from ANALISI_CMP)
Measures: CMP, COGS, Giacenza

---

## Calculation Groups (Target — unchanged, just renamed)

| Current | Target | Items |
|---------|--------|-------|
| CALC_Previous Period | CALC_PreviousPeriod | Value, Last DAY/MONTH/QUARTER/YEAR |
| CALC_ToDate | CALC_ToDate | Value, MTD, QTD, YTD |
| CALC_Rolling AVG | CALC_RollingAvg | Value, Rolling AVG DAY/MONTH/QUARTER/YEAR |

---

## Bridge Tables (Target)

### BRIDGE_Competenza (renamed from TAB_COMPETENZA)
| Column | FK to | Type |
|--------|-------|------|
| CodiceMezzo | DIM_MezziTrasporto | string |
| DataCompetenza | DIM_Calendario | date |
| Valore | (measure) | decimal |

---

## Relationship Summary (Target)

| From | To | Cardinality | Cross Filter |
|------|----|-------------|-------------|
| FACT_Vendite | DIM_Calendario | *:1 | Single |
| FACT_Vendite | DIM_Clienti | *:1 | Single |
| FACT_Vendite | DIM_Articoli | *:1 | Single |
| FACT_Vendite | DIM_Deposito | *:1 | Single |
| FACT_Vendite | DIM_GruppiVendita | *:1 | Single |
| FACT_Vendite | DIM_Progetto | *:1 | Single |
| FACT_Vendite | DIM_Reparto | *:1 | Single |
| FACT_Vendite | DIM_MezziTrasporto | *:1 | Single |
| FACT_Magazzino | DIM_Calendario | *:1 | Single |
| FACT_Magazzino | DIM_Articoli | *:1 | Single |
| FACT_Magazzino | DIM_Fornitori | *:1 | Single |
| FACT_Magazzino | DIM_Deposito | *:1 | Single |
| FACT_Magazzino | DIM_GruppiVendita | *:1 | Single |
| FACT_Ordini | DIM_Calendario | *:1 | Single |
| FACT_Ordini | DIM_Articoli | *:1 | Single |
| FACT_Ordini | DIM_Clienti | *:1 | Single |
| FACT_Ordini | DIM_Deposito | *:1 | Single |
| FACT_Ordini | DIM_GruppiVendita | *:1 | Single |
| FACT_Ordini | DIM_Spedizionieri | *:1 | Single |
| FACT_MovimentiCG | DIM_Calendario | *:1 | Single |
| FACT_MovimentiCG | DIM_PianoConti | *:1 | Single |
| FACT_Accantonamenti | DIM_Calendario | *:1 | Single |
| FACT_Accantonamenti | DIM_PianoConti | *:1 | Single |

**Target relationship count: ~23** (vs 71 current)

---

## Tables to Remove

| Table | Reason |
|-------|--------|
| 17 × LocalDateTable_* | Auto Date/Time disabled |
| DateTableTemplate_* | Auto Date/Time disabled |
| COMUNI | Flattened into DIM_Clienti |
| AREA | Flattened into DIM_Clienti |
| QUERY_BASE_DF | Merged into UTIL_DataflowQuery |
| QUERY_BASE_WEB | Merged into UTIL_WebQuery |

**Tables removed: 21**
**Tables merged/flattened: 4**
**Target total tables: ~50** (vs 75 current)

---

## Visual Migration Notes

| Page | Impact of Star Schema |
|------|----------------------|
| MAGAZZINO | Replace ANALISI_MAGAZZINO refs → KPI_Magazzino |
| GIACENZA_CMP | Replace ANALISI_CMP refs → KPI_CMP |
| ACQUISTO | Replace FACT references to new names |
| Pagina 2 | Update measures to use KPI tables |
| CONTO DEPOSITO | Update table references |
| CHURN | Update ANALISI_VENDITE refs → KPI_Vendite |
| REGRESSIONE | Update ANALISI_DOC_VENDITA refs → KPI_VenditeDocumento |
| FORECAST | Same as above |
| NUOVI_CLIENTI | Update ANALISI_VENDITE refs → KPI_Vendite |
| TAB_MIX_PROPANO | Update Tab MIX → FACT_Mix, Tab PROPANO → FACT_Propano |
