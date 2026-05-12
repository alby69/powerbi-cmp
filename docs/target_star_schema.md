# Target Star Schema — DB_MAGAZZINO

> Target state design for the DB_MAGAZZINO semantic model after refactoring

---

## Architecture Overview

The model follows a Star Schema pattern to maximize performance and usability. Geographic hierarchies and snowflake chains have been flattened into main dimensions.

---

## Fact Tables

### FACT_Vendite
Aggregated sales data from warehouse movements.
- **FK**: `CodiceArticolo`, `CodiceSoggetto`, `CodiceDeposito`, `Date`.

### FACT_DocumentoVendita
Detailed sales data from ERP documents.
- **FK**: `CodiceClienteFatturazione`, `CodiceArticolo`, `CodiceDeposito`, `DataSpedizione`, `DataRegistrazione`.

### FACT_Magazzino
Detailed warehouse movements.
- **FK**: `CodiceArticolo`, `CodiceSoggetto`, `CodiceDeposito`, `Date`, `DataDocumento`.

### FACT_Ordini
Sales orders (ODA).
- **FK**: `CodiceArticolo`, `CodiceClienteFatturazione`, `CodiceSpedizioniere`, `CodiceDeposito`, `DataSpedizione`, `DataRegistrazione`.

---

## Dimension Tables

### DIM_Articoli
Product master data.
- **PK**: `CodiceArticolo`.
- **Attributes**: `Nome`, `CostoUnitario`, `GruppoProdotto`, `GruppoCategoria`.

### DIM_Clienti
Customer master data with flattened geography.
- **PK**: `CodiceCliente`.
- **Attributes**: `Nome`, `Città`, `Provincia`, `Regione`, `AreaGeografica`.

### DIM_Calendario
Date dimension for time intelligence.
- **PK**: `Date`.
- **Attributes**: `Year`, `MonthName`, `MonthInCalendar`, `DayOfWeekName`.

### DIM_Deposito
Warehouse locations.
- **PK**: `CodiceDeposito`.
- **Attributes**: `NomeDeposito`.

---

## Key Performance Indicators (KPIs)

- **KPI_Vendite**: Executive sales and margin KPIs.
- **KPI_Mix**: Product mix and currency conversion analysis.
- **KPI_CMP**: Inventory valuation based on Weighted Average Cost.
- **KPI_Prodotto**: Product cost and accessory costs analysis.
