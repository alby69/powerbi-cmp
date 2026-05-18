# DB_MAGAZZINO — Power BI Project

Power BI semantic model per l'analisi di vendite, magazzino, acquisti, marginalità e KPI commerciali del gruppo IPEM.

## Panoramica

Progetto Power BI in formato **PBIP (Power BI Project)** con modello TMDL, connesso a SQL Server (`IPEMSERVER\bcdemo`, database `IPEM`) e a un dataset remoto Power BI. Il modello copre:

- Vendite e documenti di vendita
- Giacenza magazzino e CMP (Costo Medio Ponderato)
- Acquisti e ordini
- Mix prodotto e marginalità (PROPANO / MIX)
- KPI commerciali e obiettivi
- Churn clienti e forecast
- Time intelligence con Calculation Groups

## Struttura progetto

```
├── data/
│   ├── raw/                    # File originali (read-only)
│   └── processed/              # Dati puliti / trasformati
├── sql/
│   ├── queries/                # Query SQL analitiche
│   └── schema/                 # Script DDL tabelle / viste
├── powerbi/
│   ├── DB_MAGAZZINO_SRC/       # Sorgente PBIP (Power BI Project)
│   │   ├── Model/              # Modello TMDL (tabelle, misure, relazioni)
│   │   │   ├── tables/          # 75 definizioni tabella
│   │   │   ├── relationships.tmdl  # 71 relazioni
│   │   │   ├── expressions.tmdl    # Parametri (RangeStart, RangeEnd, etc.)
│   │   │   └── cultures/           # Traduzioni IT
│   │   ├── Report/             # Pagine report strutturate (VENDITE, ACQUISTI, MAGAZZINO, ANALISI)
│   │   │   └── sections/       # 17 sezioni organizzate per range (100, 200, 300, 400)
│   │   └── connections.json    # Connessione dataset remoto
│   ├── DB_MAGAZZINO.pbix       # Report .pbix (collegato a dataset)
│   └── datasets/               # Dataset esportati
├── docs/
│   ├── refactoring_plan.md     # Piano di refactoring in 4 fasi
│   ├── data_dictionary.md      # Dizionario dati completo
│   ├── naming_conventions.md   # Standard FACT_, DIM_, KPI_, CALC_
│   ├── dax_optimization.md     # Guida ottimizzazione DAX
│   ├── target_star_schema.md   # Schema star target
│   └── notes.md                # Note di lavoro
├── scripts/
│   └── etl/                    # Script ETL / pulizia dati
├── .gitignore
└── README.md
```

## Modello dati

| Area | Tabelle principali | Misure |
|------|-------------------|--------|
| Vendite | ANALISI_VENDITE, ANALISI_DOC_VENDITA, FACT_Vendite | ~150 |
| Magazzino | ANALISI_MAGAZZINO, FACT_Magazzino | ~55 |
| Prodotto / CMP | ANALISI_PRODOTTO, ANALISI_CMP | ~59 |
| Mix | ANALISI_MIX, Tab MIX, Tab PROPANO | ~36 |
| Time Intelligence | CALC_ToDate, CALC_Previous Period, CALC_Rolling AVG | 14 items |

**Totale:** ~301 misure DAX, 75 tabelle, 71 relazioni, 3 Calculation Groups.

## Regole

1. **Raw data read-only** — mai modificare i file in `data/raw/`
2. **Documentare sempre** — ogni trasformazione dev'essere tracciata in `docs/`
3. **Framework naming** — seguire le convenzioni in `docs/naming_conventions.md`
4. **Versioning .pbix** — usare suffissi (`dashboard_v1.pbix`, `dashboard_v2.pbix`)
5. **Refactoring** — seguire il piano in `docs/refactoring_plan.md` in ordine di fase

## Prerequisiti

- Power BI Desktop (build recente)
- Accesso a SQL Server `IPEMSERVER\bcdemo` (database IPEM)
- Git per versioning

## Stato refactoring

Vedi [`docs/refactoring_plan.md`](docs/refactoring_plan.md) per dettagli sul piano di ottimizzazione in 5 fasi:

- **Fase 1** — Quick Wins (Auto Date/Time off, LocalDateTable, relazioni)
- **Fase 2** — Standardizzazione naming
- **Fase 3** — Ottimizzazione DAX e star schema
- **Fase 4** — Documentazione enterprise
- **Fase 5** — Integrazione Report e Refactoring Visual
- **Fase 6** — Refactoring DAX e Dizionario Misure ([`docs/measures_dictionary.md`](docs/measures_dictionary.md))
