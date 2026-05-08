# Data Dictionary — DB_MAGAZZINO

> Based on TMDL analysis of DB_MAGAZZINO_SRC (Power BI Project)
> Auto-generated from semantic model — May 2026

---

## Dimension Tables (Current)

### ARTICOLI (Products)
| Column | Type | Description |
|--------|------|-------------|
| Codice Articolo | string | Primary key — product code |
| Nome | string | Product name |
| Unit Cost | decimal | Unit cost |
| Last Direct Cost | decimal | Last direct cost |
| Gen_Prod_Posting_Group | string | General product posting group |
| Nr_ Accisa | string | Excise number |
| Densita T/A | decimal | Density T/A |
| Densita 15 C | decimal | Density at 15°C |
| Gruppo Articolo | string | Product group (e.g., PROPANO, MIX) |

### CLIENTI (Customers)
| Column | Type | Description |
|--------|------|-------------|
| Codice Cliente | string | Primary key |
| Nome | string | Customer name |
| Indirizzo | string | Address |
| Indirizzo 2 | string | Address line 2 |
| Città | string | City |
| Provincia | string | Province |
| CAP | string | Postal code |
| Gruppo | string | Customer group |

### FORNITORI (Suppliers)
| Column | Type | Description |
|--------|------|-------------|
| Codice Fornitore | string | Primary key |
| Nome | string | Supplier name |
| Nome 2 | string | Supplier name line 2 |
| Indirizzo | string | Address |
| Città | string | City |
| Provincia | string | Province |
| CAP | string | Postal code |

### CALENDARIO (Calendar)
| Column | Type | Description |
|--------|------|-------------|
| Date | date | Primary key — full date |
| Year | string | Year (e.g., "2024") |
| QuarterOfYear | int64 | Quarter number (1-4) |
| MonthOfYear | int64 | Month number (1-12) |
| DayOfMonth | int64 | Day number |
| DateInt | int64 | Date as integer (YYYYMMDD) |
| MonthName | string | Month name (Italian) |
| MonthInCalendar | string | Month label (e.g., "2024-01") |
| QuarterInCalendar | string | Quarter label |
| DayInWeek | int64 | Day of week (1=Monday) |
| DayOfWeekName | string | Day name (Italian) |
| WeekEnding | date | Week ending date |
| Week Number | int64 | Week number |
| MonthnYear | int64 | Month-year as integer |
| QuarternYear | int64 | Quarter-year as integer |
| ShortYear | string | 2-digit year |
| FY | string | Fiscal year |

### UBICAZIONE (Warehouse Locations)
| Column | Type | Description |
|--------|------|-------------|
| Codice Ubicazione | string | Primary key |
| Nome | string | Location name |

### MEZZI_TRASPORTO (Transport Means)
| Column | Type | Description |
|--------|------|-------------|
| Codice Mezzo | string | Primary key |
| Nome | string | Vehicle/truck name |

### GRUPPI_VENDITE (Sales Groups)
| Column | Type | Description |
|--------|------|-------------|
| Codice Categoria | string | Primary key |
| Nome | string | Category name |
| Gruppo | string | Group (PASSAGGIO/other) |
| Permuta | string | Exchange flag |
| Categoria Permute | string | Exchange category |

### SPEDIZIONIERI (Shippers)
| Column | Type | Description |
|--------|------|-------------|
| Codice Spedizioniere | string | Primary key |
| Name | string | Shipper name |
| Indirizzo | string | Address |
| Località | string | Location |
| Città | string | City |
| CAP | string | Postal code |
| Civico | string | Street number |

### PROGETTO (Projects)
| Column | Type | Description |
|--------|------|-------------|
| Codice Progetto | string | Primary key |
| Nome | string | Project name |

### REPARTO (Departments)
| Column | Type | Description |
|--------|------|-------------|
| Codice Reparto | string | Primary key |
| Nome | string | Department name |

### AREA (Geographic Areas)
| Column | Type | Description |
|--------|------|-------------|
| Sigla | string | Primary key (province code) |
| Nome | string | Area/region name |

### COMUNI (Municipalities)
| Column | Type | Description |
|--------|------|-------------|
| Nome | string | Primary key — municipality name |
| Provincia | string | Province code (FK → AREA) |

### PIANO_DEI_CONTI (Chart of Accounts)
| Column | Type | Description |
|--------|------|-------------|
| Codice Conto | string | Primary key — account code |
| Nome | string | Account name |

---

## Fact Tables (Current)

### MAGAZZINO (Warehouse)
| Column | Type | Description |
|--------|------|-------------|
| Articolo | string | FK → ARTICOLI |
| Soggetto | string | FK → FORNITORI / CLIENTI |
| Deposito | string | FK → UBICAZIONE |
| Data | date | FK → CALENDARIO |
| Data Documento | date | Document date (→ LocalDateTable) |
| Categoria | string | FK → GRUPPI_VENDITE |
| Quantità | decimal | Quantity |
| Importo | decimal | Amount |
| Costo Unitario | decimal | Unit cost |

### ORDINI (Orders)
| Column | Type | Description |
|--------|------|-------------|
| Articolo | string | FK → ARTICOLI |
| Spedizioniere | string | FK → SPEDIZIONIERI |
| Codice Cliente Fatturazione | string | FK → CLIENTI |
| Categoria | string | FK → GRUPPI_VENDITE |
| Ubicazione | string | FK → UBICAZIONE |
| Data Spedizione | date | FK → CALENDARIO |
| Data Registrazione | date | Registration date |
| Quantità | decimal | Quantity |

### DOCUMENTO VENDITA (Sales Documents)
| Column | Type | Description |
|--------|------|-------------|
| No_ | string | Document number / FK → ARTICOLI |
| Codice Cliente Fatturazione | string | FK → CLIENTI |
| Ubicazione | string | FK → UBICAZIONE |
| Progetto | string | FK → PROGETTO |
| Reparto | string | FK → REPARTO |
| Categoria | string | FK → GRUPPI_VENDITE |
| Mezzo Trasporto | string | FK → MEZZI_TRASPORTO |
| Data Spedizione | date | FK → CALENDARIO |
| Data Registrazione | date | Registration date |
| Tipo Riga | string | Line type (Articolo, Conto) |
| Tipo Documento | string | Document type (FT VENDITA, NC VENDITA) |
| Importo | decimal | Amount |
| Quantity | decimal | Quantity |
| Costo Trasporto | decimal | Transport cost |

### DOCUMENTO ACQUISTO (Purchase Documents)
| Column | Type | Description |
|--------|------|-------------|
| Codice Fornitore | string | FK → FORNITORI |
| Progetto | string | FK → PROGETTO |
| Reparto | string | FK → REPARTO |
| Posting Date | date | FK → CALENDARIO |
| Importo | decimal | Amount |

### MOVCG (General Ledger Entries)
| Column | Type | Description |
|--------|------|-------------|
| Data Registrazione | date | FK → CALENDARIO |
| Data Documento | date | Document date |
| Mezzo Trasporto | string | FK → MEZZI_TRASPORTO |
| Progetto | string | FK → PROGETTO |
| Reparto | string | FK → REPARTO |
| Categoria | string | FK → GRUPPI_VENDITE |
| Conto | string | FK → PIANO_DEI_CONTI |
| Quantità | decimal | Quantity |
| Importo | decimal | Amount |

### ACCANTONAMENTI (Accruals)
| Column | Type | Description |
|--------|------|-------------|
| Data Registrazione Coge | date | Registration date |
| Data Accantonamento | date | FK → CALENDARIO |
| Conto | string | FK → PIANO_DEI_CONTI |
| Mezzo Trasporto | string | FK → MEZZI_TRASPORTO |
| Importo | decimal | Amount |

### Tab VENDITE (Sales Table)
| Column | Type | Description |
|--------|------|-------------|
| Codice Articolo | string | FK → ARTICOLI |
| Soggetto | string | FK → CLIENTI |
| Categoria | string | FK → GRUPPI_VENDITE |
| Deposito | string | FK → UBICAZIONE |
| Date | date | FK → CALENDARIO |
| Qta | decimal | Quantity |

---

## KPI / Measure Tables (Current)

### ANALISI_DOC_VENDITA (96 measures)
| Display Folder | Measures |
|---------------|----------|
| IMPORTO | Importo Doc Vendita, Importo Articolo Doc Vendita, Importo FT Doc Vendita, Importo NC Doc Vendita, Importo Netto Doc Vendita, Importo Trasporto, Importo Costo Prodotto, Importo Margine |
| QTA | Qta Doc Vendita, Qta Doc Vendita Articolo, Qta Doc Vendita FT, Qta Doc Vendita NC, Qta Doc Vendita Netta, Qta Vendita |
| TIME | Qta Vendita YTD, Qta Vendita LY, Qta Vendita 2LY, Qta Vendita 3LY, Qta Vendita CUM, Qta Vendita AVG Day, Importo Netto Doc Vendita LM, Importo Netto Doc Vendita LY, Importo Vendita LY, Importo Vendita LQ |
| FORECAST | Qta Vendita Forecast, Qta Vendita Forecast MA 30D, Qta Vendita Forecast Remain, Regression Line, Regression Slope, Qta Vendita ToDo, Data Obiettivo Vendita |
| Target vs Actual CHART | Bar, Unmet Bar, Met Bar, Marker Value |

### ANALISI_VENDITE (55 measures)
| Display Folder | Measures |
|---------------|----------|
| Gestione MARGINI | Total Sales, Total Profits Customer, Total Costs, Profit Margins Customer, Margin Growth %, YoY Growth % |
| TIME | Importo Vendite LM, Importo Vendite LY, Importo Vendite MTD, Importo Vendite YTD, Importo Vendite LY YTD |
| CHURNING | Nuovi Clienti, Clienti Persi, Clienti Ritornati, # Clienti, % Nuovi Clienti |

### ANALISI_MAGAZZINO (55 measures)
| Display Folder | Measures |
|---------------|----------|
| QTA | Qta Ton, Qta Ton YTD, Qta Ton LY, Qta Acquisto, Qta Ton Giacenza, Qta Ton CD |
| IMPORTO_MAG | Importo, Importo Fornitori, Importo Accantonamenti, Importo CMP, Importo Inventario, Valore Magazzino |
| QTA CONTO DEPOSITO | Qta Ton CD, Qta Ton CD CUM, Qta Ton CD Giacenza IPEM |

### ANALISI_PRODOTTO (50 measures)
| Display Folder | Measures |
|---------------|----------|
| COSTO_ACQUISTO | Costo Acquisto Qta Ton, Importo Costo Acquisto, Importo Acquisto |
| CMP | CMP Acquisto, CMP Prodotto, CMP Acquisto CUM, CMP Giacenza, CMP Acquisto AVG YTD |
| IMPORTO_PRODOTTO | Costo Venduto, Importo Giacenza Iniziale, Importo Giacenza Finale, Importo Margine |
| MARGINE | Margine Unitario, % Profitto |

### ANALISI_MIX (36 measures)
| Focus | Measures |
|-------|----------|
| Tassi | Tasso Giorno, Tasso Mese, Tasso Giorno Medio |
| Prezzi | Prezzo USD, Prezzo €, Prezzo USD Mese |
| Costi | Costo Totale, Costo €/T, Costo MIX, Costo MIX 2 |
| Quantità | Qta_BIL, Qta_RESA, Qta Acquisto MIX Tempa |

### ANALISI_CMP (9 measures)
| Measure | Description |
|---------|-------------|
| Qta_CMP | CMP quantity |
| Costo_Medio_Acquisto_CMP | Weighted average purchase cost |
| Giacenza_Qta_CMP | Inventory quantity at CMP |
| Giacenza_Valore_CMP | Inventory value at CMP |
| CMP | Weighted average cost |
| COGS | Cost of goods sold |
| Importo_CMP | CMP amount |

---

## Calculation Groups

### CALC_Previous Period (precedence: 2)
| Item | DAX |
|------|-----|
| Value | `SELECTEDMEASURE()` |
| Last DAY | `CALCULATE(SELECTEDMEASURE(), DATEADD(CALENDARIO[Date], -NumOfInterval, DAY))` |
| Last MONTH | `CALCULATE(SELECTEDMEASURE(), DATEADD(CALENDARIO[Date], -NumOfInterval, MONTH))` |
| Last QUARTER | `CALCULATE(SELECTEDMEASURE(), DATEADD(CALENDARIO[Date], -NumOfInterval, QUARTER))` |
| Last YEAR | `CALCULATE(SELECTEDMEASURE(), DATEADD(CALENDARIO[Date], -NumOfInterval, YEAR))` |

### CALC_ToDate (precedence: 1)
| Item | DAX |
|------|-----|
| Value | `SELECTEDMEASURE()` |
| MTD | `TOTALMTD(SELECTEDMEASURE(), CALENDARIO[Date])` |
| QTD | `TOTALQTD(SELECTEDMEASURE(), CALENDARIO[Date])` |
| YTD | `TOTALYTD(SELECTEDMEASURE(), CALENDARIO[Date])` |

### CALC_Rolling AVG (precedence: default)
| Item | DAX |
|------|-----|
| Value | `SELECTEDMEASURE()` |
| Rolling AVG DAY | `DATESINPERIOD(...)` + `AVERAGEX(VALUES(MonthInCalendar), SELECTEDMEASURE())` |
| Rolling AVG MONTH | Same pattern |
| Rolling AVG QUARTER | Same pattern |
| Rolling AVG YEAR | Same pattern |

---

## Tables to Remove (Phase 1)

### LocalDateTable (17 tables — Auto Date/Time)
Remove all after disabling Auto Date/Time:
- LocalDateTable_00278357
- LocalDateTable_0284d813
- LocalDateTable_5fdf6b65
- LocalDateTable_649f623b
- LocalDateTable_8a079956
- LocalDateTable_8a478964
- LocalDateTable_9ec9e902
- LocalDateTable_ae14ceb6
- LocalDateTable_b2dbc956
- LocalDateTable_b2fd2859
- LocalDateTable_c762b592
- LocalDateTable_cde1638f
- LocalDateTable_e266bb13
- LocalDateTable_e7ffeb37
- LocalDateTable_e88b2aef
- LocalDateTable_e9ebc3c5
- LocalDateTable_f457ce0f

### DateTableTemplate
- DateTableTemplate_508d27aa
