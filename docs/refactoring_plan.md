# Refactoring Plan — DB_MAGAZZINO_SRC

## Project Overview

| Property | Value |
|----------|-------|
| Format | PBIP (Power BI Project) with TMDL |
| Tables | 75 (80 TMDL files) |
| Relationships | 71 |
| DAX Measures | 301+ (6 analysis tables) |
| Calculation Groups | 3 (14 calculation items) |
| Auto Date/Time Tables | 17 (LocalDateTable_*) |
| Report Pages | 11 pages, 81 visuals |
| Data Source | SQL Server (IPEMSERVER\bcdemo), Power Platform Dataflows |
| Target Database | IPEM |
| Company | Ipem Euro |

---

## Current Architecture Analysis

### Positives
- PBIP format → Git-friendly, CI/CD ready
- Calculation Groups already in use (Previous Period, ToDate, Rolling AVG)
- Parameters centralized (Server, Database, RangeStart, RangeEnd)
- Model organized by domain (Sales, Warehouse, Mix, Product)
- Display folders partially in use

### Critical Issues

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Auto Date/Time ON → 17 LocalDateTable | HIGH | 17 ghost tables in model |
| 2 | 301+ measures, many duplicate | HIGH | Same logic spread across tables |
| 3 | No naming convention | HIGH | ANALISI_*, Tab *, LocalDateTable_* mixed |
| 4 | 71 relationships → snowflake risk | MEDIUM | CLIENTI → COMUNI → AREA chain |
| 5 | DAX not optimized | MEDIUM | Nested FILTER, SUMX, manual YTD/LY patterns |
| 6 | No documentation | HIGH | No data dictionary, no lineage |

---

## Phase 1 — Quick Wins (Estimated: 2-3 hours)

### 1.1 Disable Auto Date/Time
**File:** `Model/model.tmdl`
- Set `discourageImplicitMeasures` (already present — good)
- In Power BI Desktop: File → Options → Auto Date/Time → OFF
- Or add annotation in TMDL
- **Impact:** Removes 17 LocalDateTable tables, reduces RAM, simplifies model

### 1.2 Delete LocalDateTable Files
- Delete all 17 `LocalDateTable_*.tmdl` files
- Remove their `ref table` lines from `model.tmdl`
- Remove all relationships referencing them from `relationships.tmdl`
- **Impact:** ~20% model size reduction

### 1.3 Consolidate Calendar as Single Date Table
- Ensure `CALENDARIO` is marked as Date Table
- Verify all date columns point to `CALENDARIO[Date]`
- Remove `joinOnDateBehavior: datePartOnly` (no longer needed)
- **Impact:** Clean time intelligence, one source of truth

### 1.4 Audit Bidirectional Relationships
**Current bidirectional:**
- `CAMBI.Data` ↔ `CALENDARIO.Date` (crossFiltering: bothDirections)
- `Tab Clienti Persi` ↔ `CLIENTI` (crossFiltering: bothDirections)
- `TAB_COMPETENZA` ↔ `MEZZI_TRASPORTO` (crossFiltering: bothDirections)
- `AutoDetected_f81cec85` (crossFiltering: bothDirections)
- 3 ambiguous AutoDetected relationships (IDs: `401dbfb2`, `c021ddd8`, `8be350c5`)

**Action:** Convert to single direction where possible. Only keep bidirectional if strictly needed.

### 1.5 Remove Unused Columns
- Scan each table TMDL for columns never used in measures or visuals
- Prioritize: high-cardinality text columns, duplicate ID columns

---

## Phase 2 — Standardization & Governance (Estimated: 4-6 hours)

### 2.1 Apply Naming Convention
See full convention in [`naming_conventions.md`](naming_conventions.md).

### 2.2 Rename Tables (TMDL rename)

| Current Name | Target Name | Type |
|-------------|-------------|------|
| ARTICOLI | DIM_Articoli | Dimension |
| CLIENTI | DIM_Clienti | Dimension |
| FORNITORI | DIM_Fornitori | Dimension |
| CALENDARIO | DIM_Calendario | Dimension |
| UBICAZIONE | DIM_Deposito | Dimension |
| MEZZI_TRASPORTO | DIM_MezziTrasporto | Dimension |
| GRUPPI_VENDITE | DIM_GruppiVendita | Dimension |
| SPEDIZIONIERI | DIM_Spedizionieri | Dimension |
| PROGETTO | DIM_Progetto | Dimension |
| REPARTO | DIM_Reparto | Dimension |
| AREA | DIM_Area | Dimension |
| COMUNI | DIM_Comuni | Dimension |
| PIANO_DEI_CONTI | DIM_PianoConti | Dimension |
| MAGAZZINO | FACT_Magazzino | Fact |
| ORDINI | FACT_Ordini | Fact |
| MOVCG | FACT_MovimentiCG | Fact |
| ACCANTONAMENTI | FACT_Accantonamenti | Fact |
| DOCUMENTO VENDITA | FACT_DocumentoVendita | Fact |
| DOCUMENTO ACQUISTO | FACT_DocumentoAcquisto | Fact |
| Tab VENDITE | FACT_Vendite | Fact |
| CAMBI | FACT_Cambi | Fact |
| CONTO_DEPOSITO | FACT_ContoDeposito | Fact |
| CONTO_DEPOSITO_OLD | FACT_ContoDepositoOLD | Fact |
| ANALISI_DOC_VENDITA | KPI_VenditeDocumento | KPI/Measure |
| ANALISI_VENDITE | KPI_Vendite | KPI/Measure |
| ANALISI_MAGAZZINO | KPI_Magazzino | KPI/Measure |
| ANALISI_PRODOTTO | KPI_Prodotto | KPI/Measure |
| ANALISI_MIX | KPI_Mix | KPI/Measure |
| ANALISI_CMP | KPI_CMP | KPI/Measure |
| CALC_Previous Period | CALC_PreviousPeriod | Calculation Group |
| CALC_Rolling AVG | CALC_RollingAvg | Calculation Group |
| CALC_ToDate | CALC_ToDate | Calculation Group |
| TimeRange | PARAM_TimeRange | Parameter |
| NrGiorni | PARAM_NrGiorni | Parameter |
| Tab MIX | FACT_Mix | Fact |
| Tab PROPANO | FACT_Propano | Fact |
| PREZZI_MIX | FACT_PrezziMix | Fact |
| QUANTITA_MIX | FACT_QuantitaMix | Fact |
| QUANTITA_PROPANO | FACT_QuantitaPropano | Fact |
| MIX_COSTI | FACT_MixCosti | Fact |
| PROPANO_COSTI | FACT_PropanoCosti | Fact |
| MAGAZZINO_CMP | FACT_MagazzinoCMP | Fact |
| Tab_Stock | FACT_Stock | Fact |
| TAB_GIACENZA | FACT_Giacenza | Fact |
| Tab_CMP_Progressivo | FACT_CMPProgressivo | Fact |
| ACQUISTI_MIX_TEMPA | FACT_AcquistiMixTemp | Fact |
| TAB_COMPETENZA | BRIDGE_Competenza | Bridge |
| Obiettivo | KPI_Obiettivo | KPI |
| Obiettivo Vendite | KPI_ObiettivoVendite | KPI |
| Tab Clienti Persi | KPI_ClientiPersi | KPI |
| QUERY_BASE_DF | UTIL_DataflowQuery | Utility |
| QUERY_BASE_WEB | UTIL_WebQuery | Utility |
| LinestResult | UTIL_LinestResult | Utility |
| Stat-Vendite | UTIL_StatVendite | Utility |
| Select a Measure CG | UTIL_SelectMeasureCG | Utility |
| Select Measure Value and % | UTIL_SelectMeasureValuePct | Utility |

### 2.3 Apply Display Folders (Measures)

| Display Folder | Example Measures |
|---------------|-----------------|
| KPI Vendite | Total Sales, Total Profits Customer |
| KPI Magazzino | Qta Ton, Importo |
| KPI Margine | Margin %, Profit Margins Customer |
| KPI Mix | Costo €/T, Prezzo USD |
| Time Intelligence | YTD, MTD, LY comparison variants |
| Forecast | Forecast, Regression Slope |
| Churn | Nuovi Clienti, Clienti Persi |

### 2.4 Document Each Measure
- Add `annotation PBI_Description = "..."` to each measure
- Describe calculation intent, not formula

---

## Phase 3 — DAX & Model Optimization (Estimated: 8-16 hours)

### 3.1 Eliminate Duplicate Measures

**Problem:** Same logic spread across ANALISI_DOC_VENDITA and ANALISI_VENDITE.

**Duplicates detected:**
- `Importo Vendita` / `Importo Vendite` (same logic)
- `Qta Vendita YTD` in ANALISI_DOC_VENDITA — should use CALC_ToDate[YTD] instead
- `Importo Vendita LY` in ANALISI_DOC_VENDITA — should use CALC_Previous Period[Last YEAR]
- `Qta Vendita AVG N Days` / `Importo Vendita AVG N Days` — should use CALC_Rolling AVG

**Action:** Leverage existing Calculation Groups to eliminate manual time intelligence measures.

### 3.2 Consolidate Calculation Groups
- `CALC_ToDate` (precedence: 1) — already covers MTD, QTD, YTD
- `CALC_Previous Period` (precedence: 2) — already covers DAY, MONTH, QUARTER, YEAR
- `CALC_Rolling AVG` (precedence: default 0) — already covers DAY, MONTH, QUARTER, YEAR

**Potential additions to CALC_Previous Period:**
- `SamePeriodLastYear` (SAMEPERIODLASTYEAR)
- `ParallelPeriod` (PREVIOUSMONTH, etc.)

### 3.3 Optimize DAX Patterns

| Current Pattern | Issue | Recommended |
|----------------|-------|-------------|
| `SUMX(table, table[col])` | Iterator overhead | Use `SUM(table[col])` if no row context needed |
| `CALCULATE(expr, FILTER(table, ...))` | Nested FILTER expensive | Replace with boolean filter: `CALCULATE(expr, table[col] = value)` |
| `DATESINPERIOD(...) → AVERAGEX(VALUES(...), SELECTEDMEASURE())` | Complex | Use CALC_Rolling AVG calculation group |
| `TOTALYTD(measure)` | Already handled by CALC_ToDate | Remove measure, use calculation group |
| `DATEADD(date, -N, YEAR)` | Already handled by CALC_Previous Period | Remove measure, use calculation group |

### 3.4 Eliminate Redundant Time Intelligence Measures

**Candidate measures for removal** (replace with Calculation Groups):
- `Qta Vendita YTD`, `Importo Vendite YTD`, `Importo Vendite MTD`, `Importo Vendite LY YTD`, `Importo Vendite -2Y YTD`
- `Qta Vendita LY`, `Qta Vendita 2LY`, `Qta Vendita 3LY`, `Importo Vendite LY`, `Importo Netto Doc Vendita LY`
- `Qta Vendita AVG N Days`, `Importo Vendita AVG N Days`
- All `CUM` variants (replaced by visual-level running total or CUM in Calculation Group)

**Potential reduction:** ~40-50 measures eliminated.

### 3.5 Convert to Star Schema

See [`target_star_schema.md`](target_star_schema.md) for detailed design.

**Key transformations:**
- `CLIENTI → COMUNI → AREA` → Flatten: add `Provincia`, `Regione` directly to `DIM_Clienti`
- `DOCUMENTO VENDITA` has 9 relationships → sign of central snowflake: split if needed
- Remove or deactivate ambiguous AutoDetected relationships

### 3.6 Optimize Data Types & Cardinality
- Convert high-cardinality text columns to integers where possible (codici)
- Remove redundant columns (e.g., both `Codice Articolo` and `No_`)
- Ensure date columns are all `Date` type, not `DateTime`

---

## Phase 4 — Enterprise Documentation (Estimated: 4-6 hours)

### 4.1 Documents to Create/Update
| Document | Status | Location |
|----------|--------|----------|
| Refactoring Plan | ✅ This file | `docs/refactoring_plan.md` |
| Data Dictionary | 📝 Created | `docs/data_dictionary.md` |
| Naming Conventions | 📝 Created | `docs/naming_conventions.md` |
| DAX Optimization Guide | 📝 Created | `docs/dax_optimization.md` |
| Target Star Schema | 📝 Created | `docs/target_star_schema.md` |

### 4.2 Measure Documentation Standard
```tmdl
measure 'MeasureName' = <DAX expression>
	annotation PBI_Description = "Description in Italian"
	formatString: "#,##0"
	displayFolder: "KPI Vendite"
```

### 4.3 SQL Schema Documentation
- Document views/stored procedures used in Power Query
- Map each source column to its TMDL column
- Create in `sql/schema/` folder

---

## Effort Summary

| Phase | Hours | Impact | Risk | Status |
|-------|-------|--------|------|--------|
| 1 — Quick Wins | 2-3h | 🔴 High (RAM, performance) | 🟢 Low | ✅ COMPLETED |
| 2 — Standardization | 4-6h | 🟡 Medium (maintainability) | 🟡 Medium (rename breaks refs) | 🔄 IN PROGRESS |
| 3 — DAX & Model | 8-16h | 🔴 High (performance, maintainability) | 🔴 High (regression risk) | ⏳ PENDING |
| 4 — Documentation | 4-6h | 🟢 Low (process) | 🟢 Low | ⏳ PENDING |
| **Total** | **18-31h** | | | |

---

## Execution Log

### Phase 1 — Quick Wins ✅

| # | Task | Status | Note |
|---|------|--------|------|
| 1.1 | Disable Auto Date/Time | ✅ Done | LocalDateTable auto-generated by Power BI removed |
| 1.2 | Delete LocalDateTable files | ✅ Done | 17 LocalDateTable_*.tmdl + 1 DateTableTemplate_*.tmdl eliminati |
| 1.3 | Consolidate CALENDARIO as Date Table | ✅ Done | Marked with `PBI_CalendarTable = true`, removed auto-hierarchy variations |
| 1.4 | Audit bidirectional relationships | ✅ Done | 4 reviewed, 1 removed (AutoDetected su quantità, già inattivo) |
| 1.5 | Remove unused columns | ✅ Done | 15 variation blocks in table TMDL referencing deleted LocalDateTable rimosse |

**Results after Phase 1:**
| Metric | Before | After |
|--------|--------|-------|
| Table files | 75 | 57 |
| LocalDateTable files | 17 | 0 |
| Relationships | 71 | 67 |
| LocalDateTable refs in relationships | 17 | 0 |

---

## Recommended Sequence

```
Week 1: Phase 1 (Quick Wins)                          ✅ COMPLETED
  ├── ✅ Disable Auto Date/Time, delete LocalDateTable
  └── ✅ Audit relationships, remove LocalDateTable refs

Week 2-3: Phase 2 (Standardization)                    🔄 IN PROGRESS
  ├── Rename tables, apply naming convention
  └── Add Display Folders, document measures

Week 3-5: Phase 3 (Optimization)
  ├── Eliminate duplicate measures, consolidate CGs
  └── Star schema refactoring, data type optimization

Week 5-6: Phase 4 (Documentation)
  ├── Finalize data dictionary
  └── Review & sign-off
```

---

## Rollback Strategy
- PBIP format enables Git rollback at any point
- Create a branch `refactor/piano-refactoring` before starting
- Commit after each Phase for safe rollback
- Test each Phase in a separate `.pbix` extracted from PBIP before merging

---

## Success Metrics

| Metric | Before | After (Target) | Actual (Phase 1) |
|--------|--------|---------------|-------------------|
| Tables | 75 | ~55 | **57** ✅ |
| Relationships | 71 | ~50 | **67** |
| Measures | 301+ | ~200 | 301+ (Phase 3) |
| LocalDateTable | 17 | 0 | **0** ✅ |
| Bidirectional relationships | 5+ | <2 | **3** (2 needed) |
| Data Dictionary | ❌ | ✅ | ✅ |
| Naming Convention | ❌ | ✅ | 🔄 In progress |
