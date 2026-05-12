# DAX Optimization Guide — DB_MAGAZZINO

> Patterns, anti-patterns, and optimization strategies for the DB_MAGAZZINO semantic model

---

## 1. Leverage Existing Calculation Groups

The model already has 3 Calculation Groups. Use them to eliminate manual time intelligence measures.

### CALC_ToDate (precedence: 1)
Instead of:
```dax
Qta Vendita YTD = TOTALYTD([Qta Vendita], DIM_Calendario[Date])
Importo Vendite MTD = TOTALMTD([Importo Vendite], DIM_Calendario[Date])
```

Use: Apply `CALC_ToDate[YTD]` or `CALC_ToDate[MTD]` on the base measure via visual/calc group.

### CALC_PreviousPeriod (precedence: 2)
Instead of:
```dax
Qta Vendita LY = CALCULATE([Qta Vendita], DATEADD(DIM_Calendario[Date], -1, YEAR))
```

Use: Apply `CALC_PreviousPeriod[Last YEAR]` or `CALC_PreviousPeriod[Last MONTH]` via the calculation group.

---

## 2. Eliminate Redundant Measures

### Redundant pattern: Manual YTD + LY
```dax
// REMOVE — all replaceable by Calculation Groups
Qta Vendita LY = CALCULATE([Qta Vendita], DATEADD(DIM_Calendario[Date], -1, YEAR))
```

### What to keep: Business-specific measures
```dax
// KEEP — unique business logic, NOT replaceable by CGs
Margine Unitario = [Prezzo Medio Vendita] - [CMP Acquisto]
% Margine Cliente = DIVIDE([Margine Cliente], [Importo Vendite (Doc)], 0)
```

---

## 3. Optimize Iterator Patterns (SUMX)

### ❌ Anti-pattern: SUMX on a table directly
```dax
Importo Doc Vendita = SUMX('FACT_DocumentoVendita', 'FACT_DocumentoVendita'[Importo])
```
✅ **Fix:** Use `SUM('FACT_DocumentoVendita'[Importo])` — faster, uses Storage Engine.

### ❌ Anti-pattern: CALCULATE + FILTER over full table
```dax
Importo Articolo Doc Vendita =
    CALCULATE(
        [Importo Doc Vendita],
        FILTER('FACT_DocumentoVendita', 'FACT_DocumentoVendita'[TipoRiga] = "Articolo")
    )
```
✅ **Fix:** Use boolean filter (no FILTER iterator):
```dax
Importo Articolo Doc Vendita =
    CALCULATE(
        [Importo Doc Vendita],
        'FACT_DocumentoVendita'[TipoRiga] = "Articolo"
    )
```

---

## 4. Optimize Context Transition

### ❌ Anti-pattern: Unnecessary CALCULATE wrapping
```dax
Importo Netto Doc Vendita = 
    [Importo FT Doc Vendita] - [Importo Trasporto Doc Vendita] - [Importo NC Doc Vendita]
// No CALCULATE needed — measure references already have context transition
```

✅ **Keep as is** — this pattern is correct.

---

## 5. Best Practice: Single reference date table
```dax
// Always use DIM_Calendario[Date] for time intelligence
// Never use fact table date columns directly in time intelligence

✅ CALCULATE([Qta Vendita], DATESINPERIOD(DIM_Calendario[Date], ...))
❌ CALCULATE([Qta Vendita], DATESINPERIOD('FACT_DocumentoVendita'[DataRegistrazione], ...))
```

---

## 6. Relationship Optimization

- **Single Direction**: Preference for 1:* relationships with single filtering from Dimension to Fact.
- **Star Schema**: Flattened dimensions (like `DIM_Clienti` containing geographic data) reduce the need for snowflake joins.
