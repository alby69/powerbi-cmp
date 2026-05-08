# Data Dictionary — DB_MAGAZZINO

> Standardized Semantic Model — Phase 3 Complete

---

## Dimension Tables

### DIM_Articoli (Products)
| Column | Type | Description |
|--------|------|-------------|
| CodiceArticolo | string | Primary key — product code |
| Nome | string | Product name |
| CostoUnitario | decimal | Unit cost |
| UltimoCostoDiretto | decimal | Last direct cost |
| GruppoRegistrazioneProdotto | string | General product posting group |
| NumeroAccisa | string | Excise number |
| DensitàTA | decimal | Density T/A |
| Densità15C | decimal | Density at 15°C |
| GruppoProdotto | string | Calculated — Product group (MIX, PROPANO, etc.) |
| GruppoCategoria | string | Source category group |

### DIM_Clienti (Customers)
| Column | Type | Description |
|--------|------|-------------|
| CodiceCliente | string | Primary key |
| Nome | string | Customer name |
| Indirizzo | string | Address |
| Indirizzo2 | string | Address line 2 |
| Città | string | City |
| Provincia | string | Province |
| CAP | string | Postal code |
| Gruppo | string | Customer group |
| Regione | string | Flattened from GEOGRAFIA |
| AreaGeografica | string | Flattened from GEOGRAFIA |
| Longitudine | double | Geo-coordinates |
| Latitudine | double | Geo-coordinates |

### DIM_Fornitori (Suppliers)
| Column | Type | Description |
|--------|------|-------------|
| CodiceFornitore | string | Primary key |
| Nome | string | Supplier name |
| Città | string | City |
| Provincia | string | Province |

### DIM_Calendario (Calendar)
| Column | Type | Description |
|--------|------|-------------|
| Date | date | Primary key — full date |
| Year | string | Year |
| MonthName | string | Month name (Italian) |
| MonthInCalendar | string | Month label (YYYY-MM) |
| DayOfWeekName | string | Day name (Italian) |

### DIM_Deposito (Warehouse Locations)
| Column | Type | Description |
|--------|------|-------------|
| CodiceDeposito | string | Primary key |
| NomeDeposito | string | Location name |

---

## Fact Tables

### FACT_Magazzino (Warehouse)
| Column | Type | Description |
|--------|------|-------------|
| CodiceArticolo | string | FK → DIM_Articoli |
| CodiceSoggetto | string | FK → DIM_Fornitori / DIM_Clienti |
| CodiceDeposito | string | FK → DIM_Deposito |
| Date | date | FK → DIM_Calendario |
| Quantity | decimal | Movement quantity |
| TipoMovimento | string | Movement type |
| UnitàMisura | string | Unit of measure |
| CodiceCategoria | string | FK → DIM_GruppiVendita |
| DataDocumento | date | Original document date |

### FACT_Ordini (Orders)
| Column | Type | Description |
|--------|------|-------------|
| CodiceOrdine | string | Primary key (ODA*) |
| CodiceArticolo | string | FK → DIM_Articoli |
| CodiceClienteFatturazione | string | FK → DIM_Clienti |
| CodiceSpedizioniere | string | FK → DIM_Spedizionieri |
| CodiceDeposito | string | FK → DIM_Deposito |
| DataSpedizione | date | FK → DIM_Calendario |
| Quantity | decimal | Ordered quantity |
| NetWeight | decimal | Net weight in Tons |

### FACT_Vendite (Sales Aggregated)
| Column | Type | Description |
|--------|------|-------------|
| CodiceArticolo | string | FK → DIM_Articoli |
| CodiceSoggetto | string | FK → DIM_Clienti |
| CodiceDeposito | string | FK → DIM_Deposito |
| Date | date | FK → DIM_Calendario |
| Quantity | decimal | Sold quantity |

---

## KPI / Measure Tables

### KPI_Vendite (Executive Sales KPIs)
| Measure | Description |
|---------|-------------|
| Importo Vendite (Doc) | Revenue from sales documents |
| Margine Cliente | Total Sales - Cost of Goods Sold |
| % Margine Cliente | Margin as percentage of revenue |
| # Nuovi Clienti | Count of customers with first purchase in period |
| # Clienti Persi | Count of customers inactive for > 365 days |

### KPI_Mix (Product Mix Analysis)
| Measure | Description |
|---------|-------------|
| Prezzo Euro | Price in EUR (handled currency conversion) |
| Qta BIL | Billed quantity in tons |
| Costo Unitario | Total Cost / Billed Quantity |
| Tasso Medio Mese | Average monthly exchange rate |

### KPI_CMP (Weighted Average Cost)
| Measure | Description |
|---------|-------------|
| CMP | Weighted Average Cost |
| COGS | Cost of Goods Sold based on CMP |
| Giacenza Qta CMP | Inventory quantity for CMP calculations |
