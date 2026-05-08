# DAX Optimization Guide — DB_MAGAZZINO

> Patterns, anti-patterns, and optimization strategies for the DB_MAGAZZINO semantic model

---

## 1. Leverage Existing Calculation Groups

The model already has 3 Calculation Groups. Use them to eliminate manual time intelligence measures.

### CALC_ToDate (precedence: 1)
Instead of:
```dax
Qta Vendita YTD = TOTALYTD([Qta Vendita], CALENDARIO[Date])
Importo Vendite MTD = TOTALMTD([Importo Vendite], CALENDARIO[Date])
```

Use: Apply `CALC_ToDate[YTD]` or `CALC_ToDate[MTD]` on the base measure via visual/calc group.

### CALC_Previous Period (precedence: 2)
Instead of:
```dax
Qta Vendita LY = CALCULATE([Qta Vendita], DATEADD(CALENDARIO[Date], -1, YEAR))
Importo Netto Doc Vendita LM = CALCULATE([Importo Netto Filter Doc Vendita], DATEADD(CALENDARIO[Date], -1, MONTH))
```

Use: Apply `CALC_Previous Period[Last YEAR]` or `CALC_Previous Period[Last MONTH]` via the calculation group.

### CALC_Rolling AVG (precedence: default)
Instead of:
```dax
Qta Vendita AVG N Days = 
    VAR NrOfDays = 90
    RETURN CALCULATE(
        AVERAGEX(VALUES(CALENDARIO[Date]), [Qta Vendita]),
        DATESINPERIOD(CALENDARIO[Date], LASTDATE(CALENDARIO[Date]), -NrOfDays, DAY)
    )
```

Use: Apply `CALC_Rolling AVG[Rolling AVG DAY]` and set `NumOfInterval` via the TimeRange slicer.

---

## 2. Eliminate Redundant Measures

### Redundant pattern: Manual YTD + LY + 2LY + 3LY
```dax
// REMOVE — all replaceable by Calculation Groups
Qta Vendita LY = CALCULATE([Qta Vendita], DATEADD(CALENDARIO[Date], -1, YEAR))
Qta Vendita 2LY = CALCULATE([Qta Vendita], DATEADD(CALENDARIO[Date], -2, YEAR))
Qta Vendita 3LY = CALCULATE([Qta Vendita], DATEADD(CALENDARIO[Date], -3, YEAR))
```

### Redundant pattern: Manual CUM (Cumulative)
```dax
// REMOVE — use visual-level "Running total" or CALC_Previous Period
Qta Vendita CUM = 
    IF(
        ISBLANK([Qta Vendita]), BLANK(),
        CALCULATE([Qta Vendita], FILTER(ALLSELECTED(CALENDARIO), Date <= MAX(Date)))
    )
```

### What to keep: Business-specific measures
```dax
// KEEP — unique business logic, NOT replaceable by CGs
Margine Unitario = [Prezzo Netto Doc Vendita] - [CMP Acquisto]
% Margine = DIVIDE([Importo Margine Doc Vendita], [Importo Netto Doc Vendita], 0)
```

---

## 3. Optimize Iterator Patterns (SUMX)

### ❌ Anti-pattern: SUMX on a table directly
```dax
Importo Doc Vendita = SUMX('DOCUMENTO VENDITA', 'DOCUMENTO VENDITA'[Importo])
```
✅ **Fix:** Use `SUM('DOCUMENTO VENDITA'[Importo])` — faster, uses Storage Engine.

### ❌ Anti-pattern: CALCULATE + FILTER over full table
```dax
Importo FT Doc Vendita = 
    CALCULATE(
        [Importo Doc Vendita],
        FILTER('DOCUMENTO VENDITA', 'DOCUMENTO VENDITA'[Tipo Riga] = "Articolo")
    )
```
✅ **Fix:** Use boolean filter (no FILTER iterator):
```dax
Importo FT Doc Vendita = 
    CALCULATE(
        [Importo Doc Vendita],
        'DOCUMENTO VENDITA'[Tipo Riga] = "Articolo"
    )
```

### ❌ Anti-pattern: Multiple FILTERs stacked
```dax
Importo FT Doc Vendita = 
    CALCULATE(
        [Importo Doc Vendita],
        FILTER('DOCUMENTO VENDITA', 'DOCUMENTO VENDITA'[Tipo Riga] = "Articolo"),
        FILTER('DOCUMENTO VENDITA', 'DOCUMENTO VENDITA'[Tipo Documento] = "FT VENDITA")
    )
```
✅ **Fix:** Single filter with AND:
```dax
Importo FT Doc Vendita = 
    CALCULATE(
        [Importo Doc Vendita],
        'DOCUMENTO VENDITA'[Tipo Riga] = "Articolo" &&
        'DOCUMENTO VENDITA'[Tipo Documento] = "FT VENDITA"
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

### ⚠️ RISK: Multiple context transitions in complex measures
```dax
Qta Vendita Media Pesata = 
    VAR MediaPesata = 
        ADDCOLUMNS(
            SUMMARIZE(CALENDARIO, Year, MonthName),
            "Qta Mese", [Qta Vendita],     // <-- context transition per row
            "Peso", DIVIDE([Qta Vendita], ...) // <-- another context transition
        )
    RETURN SUMX(MediaPesata, [Qta Mese] * [Peso])
```

✅ **Fix:** Pre-calculate the numerator and denominator separately:
```dax
Qta Vendita Media Pesata = 
    VAR TotaleVendite = [Qta Vendita]
    VAR MediaMensile = 
        AVERAGEX(
            VALUES(CALENDARIO[MonthnYear]),
            [Qta Vendita]    // single context transition
        )
    RETURN MediaMensile
```

---

## 5. Use Variables to Reduce Redundant Calculations

### ❌ Anti-pattern: Repeated measure calls
```dax
% Importo Margine Doc Vendita = 
    DIVIDE(
        [Importo Margine Doc Vendita],     // computed once
        [Importo Netto Doc Vendita],        // computed once
        0
    )
```

✅ **Fix:** This is actually correct — DAX engine handles measure reuse efficiently. But for complex VAR patterns:

```dax
Importo Vendita CY-LY = 
    VAR VenditaCY = [Importo Netto Filter Doc Vendita]
    VAR VenditaLY = CALCULATE(VenditaCY, DATEADD(CALENDARIO[Date], -1, YEAR))
    RETURN VenditaCY - VenditaLY
```

---

## 6. Optimize Time Intelligence

### ❌ Anti-pattern: Manual period calculations
```dax
Qta Vendita AVG N Days = 
    VAR NrOfDays = 90
    RETURN CALCULATE(
        AVERAGEX(VALUES(CALENDARIO[Date]), [Qta Vendita]),
        DATESINPERIOD('DOCUMENTO VENDITA'[Data Registrazione], LASTDATE('DOCUMENTO VENDITA'[Data Registrazione]), -NrOfDays, DAY)
    )
```
Problems:
- Uses fact table column (Data Registrazione) instead of CALENDARIO[Date]
- Mixes USERELATIONSHIP implicitly
- Hardcodes 90 days

✅ **Fix:**
```dax
Qta Vendita AVG N Days = 
    CALCULATE(
        AVERAGEX(VALUES(CALENDARIO[Date]), [Qta Vendita]),
        DATESINPERIOD(CALENDARIO[Date], LASTDATE(CALENDARIO[Date]), -90, DAY)
    )
```
Or better: use CALC_Rolling AVG with TimeRange parameter.

### ✅ Best Practice: Single reference date table
```dax
// Always use CALENDARIO[Date] for time intelligence
// Never use fact table date columns directly in time intelligence

✅ CALCULATE([Qta Vendita], DATESINPERIOD(CALENDARIO[Date], ...))
❌ CALCULATE([Qta Vendita], DATESINPERIOD('DOCUMENTO VENDITA'[Data Registrazione], ...))
```

---

## 7. Relationship Optimization

### Current issues in relationships.tmdl:
| Issue | Count | Action |
|-------|-------|--------|
| `joinOnDateBehavior: datePartOnly` | 17 | Remove (after disabling Auto Date/Time) |
| `crossFilteringBehavior: bothDirections` | 5+ | Convert to single direction |
| `isActive: false` | 3 | Verify need, or enable |
| `AutoDetected_*` | 3+ | Remove or make explicit |

---

## 8. Pattern: IF + HASONEVALUE vs BLANK

```dax
// Current pattern (correct but verbose)
Importo Netto Doc Vendita LY = 
    IF(
        HASONEVALUE(CALENDARIO[Date]),
        CALCULATE([Importo Netto Filter Doc Vendita], DATEADD(CALENDARIO[Date], -1, YEAR)),
        BLANK()
    )

// Simplified:
Importo Netto Doc Vendita LY = 
    CALCULATE([Importo Netto Filter Doc Vendita], DATEADD(CALENDARIO[Date], -1, YEAR))
```
(Only use IF HASONEVALUE if there's a specific visual-level reason to suppress totals.)

---

## 9. VAR/RETURN Best Practices

```dax
// ✅ Good pattern: Named variables, single RETURN
Qta Vendita Mediana =
    VAR VenditaGiornaliera = [Qta Vendita]
    RETURN MEDIANX(CALENDARIO, VenditaGiornaliera)

// ✅ Good pattern: Debug via VAR (temporarily)
Qta Vendita Debug =
    VAR Qta = [Qta Vendita]
    VAR Testo = FORMAT(Qta, "#,##0")
    RETURN Testo     // shows value in visual for debugging
```

---

## 10. Measures to Review (High Priority)

From ANALISI_DOC_VENDITA (96 measures — heaviest table):

| Measure | Issue | Recommendation |
|---------|-------|---------------|
| `Regression Line` | Complex linear regression in DAX | Move to SQL/Python if static; keep if dynamic |
| `Qta Vendita Forecast` | AVERAGEX over SUMMARIZE | Consider simpler moving average or CALC_Rolling AVG |
| `Qta Vendita PREV` | References LinestResult table | Verify model dependency |
| All CUM variants (11 measures) | Manual running total | Use visual-level running total or CALC_Previous Period |
| All YTD/LY/LM variants (15+ measures) | Manual time intelligence | Use CALC_ToDate + CALC_Previous Period |
| `Importo Vendita %`, `Importo Vendita % LQ` | Percentage of total | Keep (business-specific) |
| `Importo Controllo (Doc - CG)` | Reconciliation measure | Keep (specific business need) |

---

## 11. Expected DAX Reduction

| Action | Measures Removed |
|--------|-----------------|
| Replace YTD/MTD/QTD with CALC_ToDate | ~15 |
| Replace LY/LM/LQ with CALC_Previous Period | ~20 |
| Replace Rolling AVG with CALC_Rolling AVG | ~6 |
| Remove redundant CUM measures | ~11 |
| Remove duplicate measures between ANALISI tables | ~10 |
| Merge duplicate Forecast measures | ~5 |
| **Total estimated reduction** | **~60-70 measures removed** |
| **Target measure count** | **~230 (from 301+)** |

---

## 12. Performance Testing Checklist

After each batch of changes, verify:

- [ ] Measures return same values as before (sampled across periods, categories, customers)
- [ ] Visuals render within acceptable time
- [ ] No regressions in existing reports
- [ ] Calculation Groups interact correctly
- [ ] Slicer selections work as expected
- [ ] Cumulative totals match original
