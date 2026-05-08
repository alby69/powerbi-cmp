# Naming Conventions — DB_MAGAZZINO

> Standard per il refactoring del semantic model Power BI

---

## 1. Table Prefixes

| Prefix | Category | Examples |
|--------|----------|---------|
| `DIM_` | Dimension tables (attributes, hierarchies) | `DIM_Articoli`, `DIM_Clienti`, `DIM_Calendario` |
| `FACT_` | Fact tables (transactional, measurable) | `FACT_Vendite`, `FACT_Magazzino`, `FACT_Ordini` |
| `KPI_` | Measure-only tables (business metrics) | `KPI_Vendite`, `KPI_Magazzino`, `KPI_Margine` |
| `CALC_` | Calculation Groups | `CALC_PreviousPeriod`, `CALC_ToDate`, `CALC_RollingAvg` |
| `BRIDGE_` | Bridge tables (many-to-many) | `BRIDGE_Competenza` |
| `PARAM_` | Parameter tables | `PARAM_TimeRange`, `PARAM_NrGiorni` |
| `UTIL_` | Utility tables (technical) | `UTIL_DataflowQuery`, `UTIL_SelectMeasureCG` |

### Current → Target Mapping

| Current Name | Target Name | Prefix Type |
|-------------|-------------|-------------|
| ARTICOLI | DIM_Articoli | DIM |
| CLIENTI | DIM_Clienti | DIM |
| FORNITORI | DIM_Fornitori | DIM |
| CALENDARIO | DIM_Calendario | DIM |
| UBICAZIONE | DIM_Deposito | DIM |
| MEZZI_TRASPORTO | DIM_MezziTrasporto | DIM |
| GRUPPI_VENDITE | DIM_GruppiVendita | DIM |
| SPEDIZIONIERI | DIM_Spedizionieri | DIM |
| PROGETTO | DIM_Progetto | DIM |
| REPARTO | DIM_Reparto | DIM |
| AREA | DIM_Area | DIM |
| COMUNI | DIM_Comuni | DIM |
| PIANO_DEI_CONTI | DIM_PianoConti | DIM |
| MAGAZZINO | FACT_Magazzino | FACT |
| ORDINI | FACT_Ordini | FACT |
| MOVCG | FACT_MovimentiCG | FACT |
| ACCANTONAMENTI | FACT_Accantonamenti | FACT |
| DOCUMENTO VENDITA | FACT_DocumentoVendita | FACT |
| DOCUMENTO ACQUISTO | FACT_DocumentoAcquisto | FACT |
| Tab VENDITE | FACT_Vendite | FACT |
| CAMBI | FACT_Cambi | FACT |
| CONTO_DEPOSITO | FACT_ContoDeposito | FACT |
| CONTO_DEPOSITO_OLD | FACT_ContoDepositoOLD | FACT |
| Tab MIX | FACT_Mix | FACT |
| Tab PROPANO | FACT_Propano | FACT |
| PREZZI_MIX | FACT_PrezziMix | FACT |
| QUANTITA_MIX | FACT_QuantitaMix | FACT |
| QUANTITA_PROPANO | FACT_QuantitaPropano | FACT |
| MIX_COSTI | FACT_MixCosti | FACT |
| PROPANO_COSTI | FACT_PropanoCosti | FACT |
| MAGAZZINO_CMP | FACT_MagazzinoCMP | FACT |
| Tab_Stock | FACT_Stock | FACT |
| TAB_GIACENZA | FACT_Giacenza | FACT |
| Tab_CMP_Progressivo | FACT_CMPProgressivo | FACT |
| ACQUISTI_MIX_TEMPA | FACT_AcquistiMixTemp | FACT |
| TAB_COMPETENZA | BRIDGE_Competenza | BRIDGE |
| ANALISI_DOC_VENDITA | KPI_VenditeDocumento | KPI |
| ANALISI_VENDITE | KPI_Vendite | KPI |
| ANALISI_MAGAZZINO | KPI_Magazzino | KPI |
| ANALISI_PRODOTTO | KPI_Prodotto | KPI |
| ANALISI_MIX | KPI_Mix | KPI |
| ANALISI_CMP | KPI_CMP | KPI |
| Obiettivo | KPI_Obiettivo | KPI |
| Obiettivo Vendite | KPI_ObiettivoVendite | KPI |
| Tab Clienti Persi | KPI_ClientiPersi | KPI |
| CALC_Previous Period | CALC_PreviousPeriod | CALC |
| CALC_Rolling AVG | CALC_RollingAvg | CALC |
| CALC_ToDate | CALC_ToDate | CALC |
| TimeRange | PARAM_TimeRange | PARAM |
| NrGiorni | PARAM_NrGiorni | PARAM |
| QUERY_BASE_DF | UTIL_DataflowQuery | UTIL |
| QUERY_BASE_WEB | UTIL_WebQuery | UTIL |
| LinestResult | UTIL_LinestResult | UTIL |
| Stat-Vendite | UTIL_StatVendite | UTIL |
| Select a Measure CG | UTIL_SelectMeasureCG | UTIL |
| Select Measure Value and % | UTIL_SelectMeasureValuePct | UTIL |

---

## 2. Column Naming

| Rule | Example |
|------|---------|
| Use Italian for business concepts | `Codice Articolo`, `Nome Cliente` |
| Use English for technical concepts | `Date`, `Quantity`, `Amount` |
| PascalCase for multi-word | `CodiceArticolo`, `DataRegistrazione` |
| No underscores (except PK/FK prefixes) | `CodiceCliente`, not `Codice_Cliente` |
| PK columns: same name as table key | `CodiceArticolo` in DIM_Articoli |
| FK columns: same name as referenced PK | `CodiceArticolo` in FACT_Vendite |

### Examples

```
✅ DIM_Articoli.CodiceArticolo
✅ DIM_Clienti.CodiceCliente
✅ FACT_Vendite.CodiceArticolo
✅ DIM_Calendario.Date
✅ DIM_Calendario.MonthInCalendar
❌ No_                      → CodiceArticolo
❌ Soggetto                  → CodiceCliente / CodiceFornitore
❌ Gen_Prod_Posting_Group    → GruppoRegistrazioneProdotto
```

---

## 3. Measure Naming

### Format
```
[Category] [Metric] [Modifier]
```

### Prefixes by Category
| Category | Prefix | Example |
|----------|--------|---------|
| Amount | `Importo` | `Importo Vendite` |
| Quantity | `Qta` | `Qta Vendite` |
| Count | `#` | `# Clienti` |
| Percentage | `%` | `% Margine` |
| Price/Rate | `Prezzo` | `Prezzo Medio` |
| Cost | `Costo` | `Costo Venduto` |
| Margin | `Margine` | `Margine Unitario` |

### Time Intelligence Modifiers (use sparingly — prefer Calculation Groups)
| Modifier | Meaning |
|----------|---------|
| YTD | Year to date |
| MTD | Month to date |
| LY | Last year |
| LM | Last month |
| CUM | Cumulative |
| AVG | Average |

### Examples

```
✅ Importo Vendite
✅ Qta Vendite YTD
✅ % Margine
✅ Costo Medio Acquisto
✅ # Clienti Attivi
✅ Prezzo Medio Vendita

❌ Total Sales                    → Importo Vendite
❌ Total Profits Customer         → Margine Cliente
❌ Profit Margins Customer LY     → use CALC_Previous Period
❌ Qta Vendita CUM                → Qta Vendite Progressivo (or visual running total)
❌ Regression Slope               → Pendenza Regressione
```

---

## 4. Display Folders

| Display Folder | Content |
|---------------|---------|
| KPI Vendite | Revenue-related measures |
| KPI Magazzino | Warehouse/stock measures |
| KPI Margine | Margin and profitability measures |
| KPI Mix | Mix/product measures |
| KPI Prodotto | Product cost measures |
| KPI Time Intelligence | Only if not using Calculation Groups |
| KPI Forecast | Forecast and regression measures |
| KPI Churn | Customer churn measures |
| Parametri | Parameters and what-if |

### Organization Rule
```
KPI <Area>          → Business KPIs
PARAM <Area>        → Parameters
CALC <Area>         → Calculation Groups
UTIL <Area>         → Utility
```

---

## 5. Calculation Groups Naming

| Object | Convention | Example |
|--------|-----------|---------|
| CG table | `CALC_<Name>` | `CALC_ToDate` |
| CG column | `<name>` (lowercase) | `dim`, `previousperiod` |
| CG item | Active voice | `Value`, `YTD`, `MTD`, `Last Year` |

---

## 6. File & Folder Structure (PBIP)

```
Model/
├── model.tmdl
├── database.tmdl
├── expressions.tmdl
├── relationships.tmdl
├── cultures/
│   └── it-IT.tmdl
└── tables/
    ├── DIM_Articoli.tmdl
    ├── DIM_Calendario.tmdl
    ├── DIM_Clienti.tmdl
    ├── FACT_Vendite.tmdl
    ├── KPI_Vendite.tmdl
    ├── CALC_ToDate.tmdl
    └── ...
```

---

## 7. SQL Object Naming (for `sql/schema/` and `sql/queries/`)

| Object | Convention | Example |
|--------|-----------|---------|
| Tables/Views | `v_<area>_<name>` | `v_magazzino_movimenti` |
| Stored Procedures | `sp_<area>_<action>` | `sp_magazzino_aggiorna_cmp` |
| Ad-hoc queries | descriptive filename | `analisi_vendite_ytd.sql` |
