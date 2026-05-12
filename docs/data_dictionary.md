# Data Dictionary — DB_MAGAZZINO

> Standardized Semantic Model — Version 2.0 (Phase 4 Complete)

---

## Dimension Tables

### DIM_Articoli (Products)
| Column | Type | Description |
|--------|------|-------------|
| CodiceArticolo | string | Primary key — product code |
| Nome | string | Product name |
| CostoUnitario | decimal | Unit cost |
| GruppoProdotto | string | Calculated — Product group (MIX, PROPANO, etc.) |
| GruppoCategoria | string | Source category group |

### DIM_Clienti (Customers)
| Column | Type | Description |
|--------|------|-------------|
| CodiceCliente | string | Primary key |
| Nome | string | Customer name |
| Città | string | City |
| Regione | string | Flattened from GEOGRAFIA |
| AreaGeografica | string | Flattened from GEOGRAFIA |

### DIM_Calendario (Calendar)
| Column | Type | Description |
|--------|------|-------------|
| Date | date | Primary key — full date |
| Year | string | Year |
| MonthName | string | Month name (Italian) |

---

## Fact Tables

### FACT_Magazzino (Warehouse)
| Column | Type | Description |
|--------|------|-------------|
| CodiceArticolo | string | FK → DIM_Articoli |
| CodiceSoggetto | string | FK → DIM_Fornitori / DIM_Clienti |
| Date | date | FK → DIM_Calendario |
| Quantity | decimal | Movement quantity (Kg -> Ton in measures) |
| TipoMovimento | string | Movement type |

### FACT_MovimentiCG (General Ledger)
| Column | Type | Description |
|--------|------|-------------|
| DataRegistrazione | date | FK → DIM_Calendario |
| CodiceConto | string | FK → DIM_PianoConti |
| Importo | decimal | Amount |

---

## KPI / Measure Tables

### KPI_Vendite (Executive Sales KPIs)
| Measure | Description |
|---------|-------------|
| Importo Vendite (Doc) | Revenue from sales documents |
| Margine Cliente | Total Sales - Cost of Goods Sold |
| % Margine Cliente | Margin as percentage of revenue |

### KPI_Mix (Product Mix Analysis)
| Measure | Description |
|---------|-------------|
| Prezzo Euro | Price in EUR (handled currency conversion) |
| Qta BIL | Billed quantity in tons |

### KPI_CMP (Inventory Valuation)
| Measure | Description |
|---------|-------------|
| CMP | Weighted Average Cost |
| COGS | Cost of Goods Sold based on CMP |
