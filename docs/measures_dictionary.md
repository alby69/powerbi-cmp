# Measures Dictionary

This document lists all DAX measures defined in the model, organized by table.

## CALC_PreviousPeriod

### Value Previous
```dax
SUMX('CALC_PreviousPeriod','CALC_PreviousPeriod'[PreviousPeriod])
```

## FACT_Mix

### # Qta BIL MIX
```dax
SUM('FACT_Mix'[# Qta BIL])
```

### Qta BIL MIX
```dax
SUMX('FACT_Mix','FACT_Mix'[Qta BIL])
```

### Costo Mix
```dax
CALCULATE(
DIVIDE([Costo Totale],[Qta BIL],0),
FILTER(DIM_Clienti,DIM_Clienti[CodiceCliente] IN {"C01049","C00991"}
)
)
```

### Importo Costo Mix
```dax
CALCULATE(
[Costo Totale],
FILTER(DIM_Clienti,DIM_Clienti[CodiceCliente] IN {"C01049","C00991"}
))
```

### Costo Mix Resa
```dax
CALCULATE(
DIVIDE([Costo Totale],[Qta Resa],0),
FILTER(DIM_Clienti,DIM_Clienti[CodiceCliente] IN {"C01049","C00991"}))
```

### Qta RESA MIX
```dax
SUMX('FACT_Mix','FACT_Mix'[Qta Resa])
```

## FACT_Propano

### Costo Propano
```dax
DIVIDE([Total Costs NAVI],[Qta Magazzino Acquisto IPEM CD])
```

### Importo Costo Propano
```dax
[Total Costs NAVI]
```

## FACT_Vendite

### Qta Tab Vendite
**Description:** Somma quantità tabella vendite

```dax
// Somma totale delle quantità presenti nella tabella FACT_Vendite
SUMX('FACT_Vendite', 'FACT_Vendite'[Quantity])
```

### # Qta Vendite
**Description:** Conteggio record vendite

```dax
// Conteggio totale dei movimenti di vendita (basato sulla colonna CountQta)
SUM('FACT_Vendite'[CountQta])
```

## KPI_AcquistiDocumento

### Importo Acquisti (Doc)
**Description:** Importo totale acquisti basato su documenti

```dax
// Somma totale degli importi dai documenti di acquisto
SUMX ( 'FACT_DocumentoAcquisto', 'FACT_DocumentoAcquisto'[Importo] )
```

### Importo Materia Prima (Doc)
**Description:** Importo acquisti materia prima (Articolo 4020002)

```dax
// Importo acquisti filtrato per il codice articolo materia prima '4020002'
CALCULATE (
[Importo Acquisti (Doc)],
'FACT_DocumentoAcquisto'[CodiceArticolo] = "4020002"
)
```

### Qta Acquisti (Doc)
**Description:** Quantità totale acquisti basata su documenti

```dax
// Somma totale delle quantità dai documenti di acquisto
SUMX ( 'FACT_DocumentoAcquisto', 'FACT_DocumentoAcquisto'[Quantity] )
```

## KPI_CMP

### Qta CMP
**Description:** Quantità BIL per il calcolo del CMP

```dax
// Quantità bilanciata per il calcolo del Costo Medio Ponderato
SUM(FACT_MagazzinoCMP[Qta_BIL])
```

### Costo Medio Acquisto
**Description:** Costo medio di acquisto per il calcolo del CMP

```dax
// Rapporto tra importo acquisto CMP e quantità CMP
DIVIDE([Imp_Acquisto_CMP], [Qta CMP])
```

### Giacenza Quantità (CMP)
**Description:** Quantità in giacenza per il calcolo del CMP

```dax
// Restituisce la quantità progressiva di stock all'ultima data utile del periodo
CALCULATE(
MAX(FACT_Stock[QtaProgressiva]),
LASTDATE(DIM_Calendario[Date])
)
```

### Giacenza Valore (CMP)
**Description:** Valore in giacenza per il calcolo del CMP

```dax
// Restituisce il valore progressivo di stock all'ultima data utile del periodo
CALCULATE(
MAX(FACT_Stock[ValoreProgressivo]),
LASTDATE(DIM_Calendario[Date])
)
```

### CMP (Calcolato)
**Description:** Costo Medio Ponderato calcolato su stock progressivo

```dax
// Calcola il CMP come rapporto tra Valore Stock e Quantità Stock
VAR Valore = [Giacenza Valore (CMP)]
VAR Quantita = [Giacenza Quantità (CMP)]
RETURN
DIVIDE(Valore, Quantita)
```

### Costo Venduto (CMP)
**Description:** Costo del venduto basato su CMP calcolato

```dax
// Valorizzazione del venduto utilizzando il CMP calcolato
SUM(FACT_Stock[Quantità]) * [CMP (Calcolato)]
```

### Giacenza Quantità Periodo
**Description:** Somma quantità stock nel periodo

```dax
// Somma delle quantità progressive nel periodo selezionato
SUM(FACT_Stock[QtaProgressiva])
```

### Giacenza Valore Periodo
**Description:** Somma valore stock nel periodo

```dax
// Somma dei valori progressivi nel periodo selezionato
SUM(FACT_Stock[ValoreProgressivo])
```

### Importo CMP
**Description:** Importo totale movimenti CMP

```dax
// Somma totale degli importi in FACT_MagazzinoCMP
SUM(FACT_MagazzinoCMP[Importo])
```

## KPI_Magazzino

### Qta Magazzino
**Description:** Quantità in magazzino in tonnellate (da Kg)

```dax
// Calcola la quantità totale in magazzino convertendo Kg in Tonnellate
VAR QtaKg = SUMX ( FACT_Magazzino, FACT_Magazzino[Quantity] )
RETURN
DIVIDE ( QtaKg, 1000, 0 )
```

### Qta Magazzino Progressivo
**Description:** Saldo progressivo della quantità in magazzino

```dax
// Quantità in magazzino accumulata nel tempo (saldo ad oggi)
CALCULATE (
[Qta Magazzino],
FILTER (
ALL ( DIM_Calendario ),
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
)
```

### Qta Acquisti
**Description:** Quantità acquistata totale (Resa Mix + Quantity IPEM Propano)

```dax
// Somma le quantità acquistate in base al gruppo prodotto (MIX o PROPANO)
VAR Gruppo = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () )

VAR QtaMix = [Qta RESA MIX]
VAR QtaPropano = SUMX(FACT_Propano, FACT_Propano[QuantityIPEM] )

RETURN
SWITCH (
TRUE (),
Gruppo = "MIX", QtaMix,
Gruppo = "PROPANO", QtaPropano,
QtaMix + QtaPropano // Default: somma entrambi
)
```

### Importo Magazzino
**Description:** Importo totale movimenti di magazzino da CG

```dax
// Importo totale dei movimenti di magazzino registrati in CG
CALCULATE(
SUMX(FACT_MovimentiCG, FACT_MovimentiCG[Importo]),
REMOVEFILTERS(FACT_MovimentiCG[CodiceCategoria])
)
```

### Importo Fornitori
**Description:** Debiti verso fornitori (Conto CG 2030001)

```dax
// Importo dei movimenti CG filtrati per il conto fornitori '2030001'
CALCULATE (
[Importo Magazzino],
FACT_MovimentiCG[CodiceConto] = "2030001"
)
```

### Importo Acquisti (CG)
**Description:** Ricavi/Costi acquisti da CG (Conto 4020002)

```dax
// Importo degli acquisti registrati sul conto '4020002'
CALCULATE (
ABS ( [Importo Magazzino] ),
FACT_MovimentiCG[CodiceConto] = "4020002"
)
```

### Importo per Data Documento
**Description:** Importo movimenti CG basato sulla data documento

```dax
// Calcola l'importo CG utilizzando la relazione con la data del documento anziché la registrazione
CALCULATE (
SUMX ( FACT_MovimentiCG, FACT_MovimentiCG[Importo] ),
USERELATIONSHIP ( DIM_Calendario[Date], FACT_MovimentiCG[DataDocumento] )
)
```

### Importo Acquisti Altro
**Description:** Importo altri acquisti (Conto 3100001, Progetto PS01)

```dax
// Importo per acquisti vari su conto '3100001' e progetto 'PS01'
CALCULATE (
ABS ( [Importo Magazzino] ),
FACT_MovimentiCG[CodiceConto] = "3100001" &&
FACT_MovimentiCG[Progetto] = "PS01"
)
```

### Importo Accantonamenti
**Description:** Totale accantonamenti

```dax
// Somma totale degli accantonamenti registrati
SUMX ( FACT_Accantonamenti, FACT_Accantonamenti[Importo] )
```

### Importo Qta Ton Progressivo YTD
**Description:** Valorizzazione della giacenza progressiva annuale al costo di acquisto

```dax
// Valorizzazione della giacenza YTD al costo di acquisto unitario
[Qta Magazzino Progressivo YTD] * [Costo Acquisto Qta Ton]
```

### Importo Qta Ton
**Description:** Valorizzazione quantità magazzino al costo acquisto

```dax
// Valorizzazione della giacenza istantanea al costo di acquisto
[Qta Magazzino] * [Costo Acquisto Qta Ton]
```

### Importo Qta Ton Differenza CY-LY
**Description:** Differenza di valorizzazione giacenza YTD tra anno corrente e precedente

```dax
// Delta di valorizzazione tra l'anno corrente e l'anno precedente (stesso periodo)
VAR ValCY = [Importo Qta Ton Progressivo YTD]
VAR ValLY = CALCULATE([Importo Qta Ton Progressivo YTD], SAMEPERIODLASTYEAR(DIM_Calendario[Date]))
RETURN
ValCY - ValLY
```

### Importo Qta Ton Vendita
**Description:** Valorizzazione quantità venduta al costo acquisto

```dax
// Costo del venduto calcolato su quantità venduta e costo acquisto unitario
[Qta Vendite] * [Costo Acquisto Qta Ton]
```

### Importo Magazzino Progressivo
**Description:** Importo progressivo movimenti magazzino per deposito IPEM

```dax
// Importo progressivo dei movimenti di magazzino filtrato per deposito IPEM (dal 2021)
VAR Articolo = SELECTEDVALUE ( DIM_Articoli[CodiceArticolo] )
VAR AnnoInizio = 2021
VAR TabellaFiltrata =
FILTER (
ALL ( FACT_Magazzino ),
FACT_Magazzino[CodiceDeposito] = "IPEM" &&
FACT_Magazzino[CodiceArticolo] = Articolo &&
FACT_Magazzino[Date] >= DATE ( AnnoInizio, 1, 1 ) &&
FACT_Magazzino[Date] <= MAX ( DIM_Calendario[Date] )
)
RETURN
CALCULATE ( [Importo Magazzino], TabellaFiltrata )
```

### Importo Magazzino Progressivo (2)
**Description:** Valorizzazione progressiva acquisti (CMP x Qta)

```dax
// Valorizzazione progressiva: CMP Acquisto x Quantità Acquisto
[CMP Acquisto Mag Progr] * [Qta Acquisto Progr]
```

### Importo Qta Ton Previsto
**Description:** Importo magazzino previsto basato su giacenza iniziale 2021

```dax
// Calcola l'importo previsto di magazzino partendo da una giacenza iniziale al 01/01/2021
VAR Gruppo = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto] )
VAR DataCorrente = SELECTEDVALUE ( DIM_Calendario[Date] )

VAR ImportoIniziale =
SUMX (
FILTER (
FACT_Giacenza,
FACT_Giacenza[Date] = DATE ( 2021, 1, 1 ) &&
FACT_Giacenza[GruppoProdotto] = Gruppo
),
FACT_Giacenza[Importo]
)
VAR TabellaFiltroCalendario =
FILTER (
ALLSELECTED ( DIM_Calendario ),
DIM_Calendario[Date] < MAX ( DIM_Calendario[Date] )
)
RETURN
CALCULATE (
IF (
DataCorrente = DATE ( 2021, 1, 1 ) || ISBLANK ( [Qta Magazzino] ),
ImportoIniziale,
[Qta Magazzino]
),
TabellaFiltroCalendario
)
```

### Importo Vendite (CG)
**Description:** Ricavi vendite da CG (Conti 30*)

```dax
// Ricavi totali dalle vendite registrate sui conti CG 30*
CALCULATE (
ABS ( [Importo Magazzino] ),
FACT_MovimentiCG[CodiceConto] IN { "3000002", "3000003", "3000004", "3000005" }
)
```

### Importo Passaggi (CG)
**Description:** Ricavi passaggi da CG (Conti 31*)

```dax
// Ricavi totali dai passaggi registrati sui conti CG 31*
CALCULATE (
ABS ( [Importo Magazzino] ),
FACT_MovimentiCG[CodiceConto] IN { "3100001", "3100002", "3100003", "3100004", "3100005" }
)
```

### Importo Rimanenze Iniziali Propano (CG)
**Description:** Importo rimanenze iniziali Propano (Conto 4010002)

```dax
// Valore delle giacenze iniziali di Propano (Conto 4010002)
CALCULATE (
ABS ( [Importo Dare (CG)] ),
FACT_MovimentiCG[CodiceConto] = "4010002"
)
```

### Importo Rimanenze Finali Propano (CG)
**Description:** Importo rimanenze finali Propano (Conto 3300002)

```dax
// Valore delle giacenze finali di Propano (Conto 3300002)
CALCULATE (
ABS ( [Importo Dare (CG)] ),
FACT_MovimentiCG[CodiceConto] = "3300002"
)
```

### Importo CMP
**Description:** Importo totale per calcolo CMP (Iniziali + Acquisti)

```dax
// Base di calcolo per il Costo Medio Ponderato: Giacenza Iniziale + Acquisti
[Importo Rimanenze Iniziali Propano (CG)] + [Importo Acquisti (CG)]
```

### Importo Inventario
**Description:** Valorizzazione inventario (Acquisti + CD IPEM) x CMP

```dax
// Valore totale dell'inventario: (Qta Acquisti + Qta Giacenza IPEM) x CMP
([Qta Acquisti] + [Qta Magazzino CD Giacenza IPEM]) * [CMP Acquisto]
```

### Importo Rimanenze Finali Mix (CG)
**Description:** Importo rimanenze finali Mix (Conto 3300003)

```dax
// Valore delle giacenze finali di Mix (Conto 3300003)
CALCULATE (
ABS ( [Importo Dare (CG)] ),
FACT_MovimentiCG[CodiceConto] = "3300003"
)
```

### Importo Rimanenze Iniziali Mix (CG)
**Description:** Importo rimanenze iniziali Mix (Conto 4010003)

```dax
// Valore delle giacenze iniziali di Mix (Conto 4010003)
CALCULATE (
ABS ( [Importo Dare (CG)] ),
FACT_MovimentiCG[CodiceConto] = "4010003"
)
```

### Qta Magazzino Acquisto IPEM CD
**Description:** Quantità acquisti in Conto Deposito deposito IPEM

```dax
// Quantità acquistata per il deposito IPEM in regime di Conto Deposito
CALCULATE (
[Qta Magazzino CD],
FACT_ContoDeposito[TipoMovimento] = "Acquisto" &&
FACT_ContoDeposito[CodiceDeposito] = "IPEM"
)
```

### Qta Magazzino CD
**Description:** Quantità totale movimenti in Conto Deposito

```dax
// Somma delle quantità presenti in Conto Deposito
SUMX ( FACT_ContoDeposito, FACT_ContoDeposito[Quantity] )
```

### Qta Magazzino Acquisto IPEM CD Progressivo
**Description:** Somma progressiva acquisti CD per deposito IPEM

```dax
// Saldo progressivo degli acquisti in Conto Deposito per IPEM
CALCULATE (
[Qta Magazzino Acquisto IPEM CD],
FILTER (
ALL ( DIM_Calendario ),
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
)
```

### Qta Magazzino CD Progressivo
**Description:** Giacenza progressiva in Conto Deposito con gestione dei set-point 'Giacenza'

```dax
// Calcola la giacenza progressiva in Conto Deposito gestendo correttamente i movimenti di tipo 'Giacenza' (set point)
VAR InizioPeriodo =
CALCULATE(
MIN(FACT_ContoDeposito[DataMovimento]),
ALLSELECTED(FACT_ContoDeposito)
)
VAR DataCorrente = MAX(FACT_ContoDeposito[DataMovimento])
VAR OrdineCorrente = MAX(FACT_ContoDeposito[EntryNo])

VAR UltimaGiacenzaPrecedente =
MAXX(
FILTER(
ALL(FACT_ContoDeposito),
FACT_ContoDeposito[TipoMovimento] = "Giacenza" &&
FACT_ContoDeposito[DataMovimento] <= InizioPeriodo
),
FACT_ContoDeposito[DataMovimento]
)

VAR Tab_Filtro =
FILTER(
ALLSELECTED(FACT_ContoDeposito),
(
FACT_ContoDeposito[TipoMovimento] = "Giacenza" &&
FACT_ContoDeposito[DataMovimento] = UltimaGiacenzaPrecedente
)
||
(
FACT_ContoDeposito[TipoMovimento] <> "Giacenza" &&
FACT_ContoDeposito[DataMovimento] >= InizioPeriodo &&
(
FACT_ContoDeposito[DataMovimento] < DataCorrente ||
(
FACT_ContoDeposito[DataMovimento] = DataCorrente &&
FACT_ContoDeposito[EntryNo] <= OrdineCorrente
)
)
)
)

VAR Risultato = CALCULATE([Qta Magazzino CD], Tab_Filtro)

RETURN
IF(
HASONEVALUE(FACT_ContoDeposito[DataMovimento]),
Risultato,
BLANK()
)
```

### Qta Magazzino CD Giacenza IPEM
**Description:** Quantità di giacenza iniziale/set-point per deposito IPEM in CD

```dax
// Quantità registrata come set-point di giacenza per il deposito IPEM
CALCULATE (
[Qta Magazzino CD],
FACT_ContoDeposito[TipoMovimento] = "Giacenza" &&
FACT_ContoDeposito[CodiceDeposito] = "IPEM"
)
```

### Valore Magazzino
**Description:** Valorizzazione giacenza al CMP cumulato

```dax
// Valorizzazione della giacenza progressiva al CMP cumulato di acquisto
[Qta Magazzino Progressivo] * [CMP Acquisto CUM]
```

### Valore Magazzino (2)
**Description:** Valorizzazione giacenza al CMP cumulato prodotto

```dax
// Valorizzazione della giacenza progressiva al CMP cumulato di prodotto
[Qta Magazzino Progressivo] * [CMP Prodotto CUM]
```

### Rapporto Inventario
**Description:** Indice di rotazione: Rapporto tra vendite N giorni e valore inventario

```dax
// Indice di rotazione o copertura: Rapporto tra vendite ultimi N giorni e valore inventario attuale
DIVIDE([Importo Vendita N DAYS], [Importo Inventario], 0)
```

### Importo Dare (CG)
**Description:** Somma degli importi 'Dare' (positivi) in CG

```dax
// Somma degli importi positivi (Dare) nei movimenti di Contabilità Generale
CALCULATE(
SUMX ( FACT_MovimentiCG, FACT_MovimentiCG[Importo]),
FACT_MovimentiCG[Importo] > 0
)
```

### Unità Misura
**Description:** Unità di misura di magazzino

```dax
// Restituisce l'unità di misura utilizzata nei movimenti di magazzino
MINX(FACT_Magazzino, FACT_Magazzino[UnitàMisura])
```

### Qta Magazzino Progressivo YTD
**Description:** Saldo quantità progressivo dall'inizio dell'anno corrente

```dax
// Giacenza progressiva calcolata dall'inizio dell'anno (Year-To-Date)
CALCULATE (
[Qta Magazzino],
FILTER (
ALL ( DIM_Calendario ),
DIM_Calendario[Year] = MAX ( DIM_Calendario[Year] ) &&
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
)
```

### Qta Magazzino Giacenza
**Description:** Giacenza calcolata come Iniziale + Acquisti - Vendite

```dax
// Calcolo teorico giacenza: Iniziale + Acquisti - Vendite
[Qta Giacenza Iniziale] + [Qta Acquisti] - [Qta Vendite]
```

### Qta Magazzino Giacenza OLD
**Description:** Giacenza progressiva senza filtri gruppo vendita

```dax
// Quantità progressiva ignorando i filtri sui gruppi vendita
CALCULATE(
[Qta Magazzino Progressivo],
REMOVEFILTERS(DIM_GruppiVendita)
)
```

### Qta Magazzino Prevista
**Description:** Quantità magazzino prevista basata su giacenza 2021

```dax
// Stima della giacenza prevista partendo dalla giacenza iniziale del 2021
VAR Gruppo = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto] )
VAR DataCorrente = SELECTEDVALUE ( DIM_Calendario[Date] )

VAR QtaIniziale =
SUMX (
FILTER (
FACT_Giacenza,
FACT_Giacenza[Date] = DATE ( 2021, 1, 1 ) &&
FACT_Giacenza[GruppoProdotto] = Gruppo
),
FACT_Giacenza[Quantity]
)
VAR TabellaFiltroCalendario =
FILTER (
ALLSELECTED ( DIM_Calendario ),
DIM_Calendario[Date] < MAX ( DIM_Calendario[Date] )
)
RETURN
CALCULATE (
IF (
DataCorrente = DATE ( 2021, 1, 1 ) || ISBLANK ( [Qta Magazzino] ),
QtaIniziale,
[Qta Magazzino]
),
TabellaFiltroCalendario
)
```

### Qta Magazzino Giacenza LM
**Description:** Giacenza al mese precedente (Last Month)

```dax
// Giacenza calcolata allo stesso giorno del mese precedente
CALCULATE ( [Qta Magazzino Giacenza OLD], DATEADD ( DIM_Calendario[Date], -1, MONTH ) )
```

### Qta Magazzino Giacenza IPEM
**Description:** Giacenza calcolata per il deposito IPEM

```dax
// Giacenza filtrata per il solo deposito IPEM
CALCULATE(
[Qta Magazzino Giacenza OLD],
FACT_Magazzino[CodiceDeposito] = "IPEM"
)
```

### Qta Magazzino CD per Movimento
**Description:** Quantità CD dinamica in base al tipo movimento (Vendita vs Altri)

```dax
// Determina se mostrare la quantità vendita o la quantità CD in base al tipo movimento selezionato
VAR MovimentoCorrente = SELECTEDVALUE(FACT_ContoDeposito[TipoMovimento], 0)
RETURN
IF(MovimentoCorrente = "Vendita", [Qta Vendita Deposito], [Qta Magazzino CD])
```

### Qta Vendita Deposito
**Description:** Quantità venduta per deposito mappato su soggetti CD

```dax
// Calcola le quantità vendute dai depositi, mappando i depositi CD sui codici soggetti (C00*)
VAR Gruppo = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () )
VAR Deposito = SELECTEDVALUE ( FACT_ContoDepositoOLD[CodiceDeposito], BLANK () )
VAR SoggettoFiltro =
SWITCH (
TRUE (),
Deposito = "AUTOGASNORD", "C00525",
Deposito = "BUTANGAS", "C00229",
Deposito = "LIQUIGAS", "C00261",
Deposito = "VERSALIS", "C00794",
""
)

VAR QtaMix =
CALCULATE(
SUMX(FACT_Vendite, FACT_Vendite[Quantity]),
FACT_Vendite[CodiceArticolo] IN {"1","1T"} &&
IF( SoggettoFiltro <> "",
FACT_Vendite[CodiceSoggetto] = SoggettoFiltro,
FACT_Vendite[CodiceCategoria] <> "PASSAGGIO"
)
)

VAR QtaPropano =
CALCULATE(
SUMX(FACT_Vendite, FACT_Vendite[Quantity]),
FACT_Vendite[CodiceArticolo] IN {"2","2T"} &&
IF( SoggettoFiltro <> "",
FACT_Vendite[CodiceSoggetto] = SoggettoFiltro,
FACT_Vendite[CodiceCategoria] <> "PASSAGGIO"
)
)

RETURN
SWITCH (
TRUE (),
Gruppo = "MIX", QtaMix,
Gruppo = "PROPANO", QtaPropano,
QtaMix + QtaPropano
)
```

### Qta Magazzino Giacenza (2)
**Description:** Giacenza specifica 2024 con set-point iniziale al 01/01

```dax
// Calcolo giacenza 2024 basato su set-point iniziale e movimenti YTD
VAR Prodotto = SELECTEDVALUE(DIM_Articoli[GruppoProdotto])
VAR DataInizio2024 = DATE(2024,1,1)

VAR GiacenzaInizialePropano = 4901
VAR GiacenzaInizialeMix = 219.520
VAR GiacenzaIniziale = IF(Prodotto = "PROPANO", GiacenzaInizialePropano, GiacenzaInizialeMix)

VAR QtaAcquistoYTD = TOTALYTD ( [Qta Acquisti], DIM_Calendario[Date] )
VAR QtaVenditaYTD = TOTALYTD ( [Qta Vendita Prodotto], DIM_Calendario[Date] )

RETURN
IF(
MIN(DIM_Calendario[Date]) = DataInizio2024 && MAX(DIM_Calendario[Date]) = DATE(2024,1,31),
GiacenzaIniziale,
GiacenzaIniziale + QtaAcquistoYTD - QtaVenditaYTD
)
```

### Qta Magazzino Vendita (MAG)
**Description:** Quantità scaricata da FACT_Magazzino per vendite

```dax
// Quantità scaricata dal magazzino per movimenti di tipo 'Vendita'
CALCULATE(
[Qta Magazzino],
FACT_Magazzino[TipoMovimento] = "Vendita"
)
```

### Qta Acquisti Progressivo
**Description:** Quantità acquisti accumulata nel tempo (periodo corrente)

```dax
// Quantità totale acquistata accumulata nel periodo selezionato
IF (
ISBLANK ( [Qta Acquisti] ),
BLANK (),
CALCULATE (
[Qta Acquisti],
FILTER (
ALLSELECTED ( DIM_Calendario ),
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
)
)
```

### Qta Magazzino Acquisto
**Description:** Carichi di magazzino (Acquisti + Rettifiche Positive)

```dax
// Quantità caricata a magazzino per Acquisti o Rettifiche Positive
CALCULATE(
[Qta Magazzino],
FACT_Magazzino[TipoMovimento] IN {"Acquisto", "Rettifica Positiva"}
)
```

### Mostra Giacenza No Movimenti
**Description:** Flag per visualizzazione righe di giacenza senza movimenti nel periodo

```dax
// Flag tecnico per gestire la visualizzazione delle giacenze anche in assenza di movimenti nel periodo
VAR HaQuantita = NOT(ISBLANK([Qta Magazzino CD]))
VAR AnnoCorrente = YEAR(MAX(FACT_ContoDeposito[DataMovimento]))
VAR InizioAnno = DATE(AnnoCorrente, 1, 1)
VAR IsGiacenzaIniziale =
MAX(FACT_ContoDeposito[TipoMovimento]) = "Giacenza" &&
MAX(FACT_ContoDeposito[DataMovimento]) <= InizioAnno
VAR IsAltroMovimento = MAX(FACT_ContoDeposito[TipoMovimento]) <> "Giacenza"

RETURN
IF(
HaQuantita && (IsGiacenzaIniziale || IsAltroMovimento),
1,
BLANK()
)
```

### FiltroAttivo
**Description:** Stato dei filtri principali (Debug)

```dax
// Visualizza lo stato dei filtri attivi per Gruppo e Categoria (debug)
VAR IsGruppoFiltrato = ISFILTERED(DIM_GruppiVendita[Gruppo])
VAR IsCategoriaFiltrata = ISFILTERED(FACT_MovimentiCG[CodiceCategoria])
RETURN
"Gruppo: " & IF(IsGruppoFiltrato, "✅", "❌") &
" | Categoria: " & IF(IsCategoriaFiltrata, "✅", "❌")
```

### Qta Giacenza Iniziale
**Description:** Alias quantità giacenza iniziale IPEM

```dax
// Alias per la giacenza iniziale IPEM in Conto Deposito
[Qta Magazzino CD Giacenza IPEM]
```

## KPI_Mix

### # Tassi Mese
**Description:** Numero di tassi di cambio rilevati nel mese

```dax
// Conta il numero di rilevazioni di tassi di cambio nel periodo selezionato
COUNTROWS ( ALLSELECTED ( FACT_Cambi ) )
```

### Tasso Giorno
**Description:** Tasso di cambio giornaliero (USD/EUR) con logica di fallback

```dax
// Determina il tasso di cambio USD/EUR per la data di spedizione dell'ordine
// Se il tasso non è presente per il giorno esatto, prova a recuperare quello di 3 giorni dopo (fall-back)
VAR DataOrdine = SELECTEDVALUE ( FACT_Ordini[DataSpedizione] )
VAR TassoEsatto =
CALCULATE (
SELECTEDVALUE ( FACT_Cambi[Tasso] ),
FACT_Cambi[Data] = DataOrdine
)
VAR TassoFallback =
CALCULATE (
SELECTEDVALUE ( FACT_Cambi[Tasso] ),
FACT_Cambi[Data] = DataOrdine + 3
)
RETURN
IF ( TassoEsatto <> 0 && NOT(ISBLANK(TassoEsatto)), TassoEsatto, TassoFallback )
```

### Tasso Medio Mese
**Description:** Tasso di cambio medio mensile

```dax
// Calcola la media aritmetica semplice dei tassi di cambio del periodo
VAR NrGiorni = COUNTROWS ( FACT_Cambi )
VAR SommaTassi = CALCULATE ( SUMX ( FACT_Cambi, FACT_Cambi[Tasso] ), FACT_Cambi )
RETURN
DIVIDE ( SommaTassi, NrGiorni, 0 )
```

### Prezzo USD
**Description:** Prezzo unitario in USD dalla tabella prezzi Mix

```dax
// Recupera il prezzo in USD dalla tabella dei prezzi Mix filtrando per cliente e periodo
VAR ClienteCodice = SELECTEDVALUE ( DIM_Clienti[CodiceCliente] )
VAR Anno = SELECTEDVALUE ( DIM_Calendario[Year] )
VAR Mese = SELECTEDVALUE ( DIM_Calendario[MonthName] )

VAR TabellaFiltrata =
FILTER (
FACT_PrezziMix,
'FACT_PrezziMix'[Cliente] = ClienteCodice &&
(FORMAT(YEAR(FACT_PrezziMix[Data]), "String") = Anno || MONTH(FACT_PrezziMix[Data]) = Mese)
)
RETURN
SELECTCOLUMNS ( TabellaFiltrata, "Prezzo", FACT_PrezziMix[Prezzo USD] )
```

### # ATB Giorno
**Description:** Numero di ordini giornalieri

```dax
// Conta il numero di ordini effettuati nel giorno (ATB)
COUNT ( FACT_Ordini[CodiceOrdine] )
```

### Prezzo Euro
**Description:** Prezzo in Euro calcolato in base al cliente (MITSUI tasso giorno, TOTAL tasso mese)

```dax
// Converte il prezzo da USD a EUR in base alle regole specifiche del cliente:
// TOTAL: usa tasso medio mese
// MITSUI: usa tasso del giorno
VAR Cliente = SELECTEDVALUE ( FACT_Ordini[CodiceClienteFatturazione] )
VAR Deposito = SELECTEDVALUE ( FACT_Ordini[CodiceDeposito] )
VAR IsTotal = ( Cliente = "C00991" || Deposito = "TOTAL" )
VAR IsMitsui = ( Cliente = "C01049" || Deposito = "MITSUI" )
RETURN
IF (
IsTotal || IsMitsui,
SWITCH (
TRUE (),
IsTotal, DIVIDE ( [Prezzo USD], [Tasso Medio Mese], 0 ),
IsMitsui, DIVIDE ( [Prezzo USD], [Tasso Giorno], 0 )
),
BLANK ()
)
```

### Qta BIL
**Description:** Quantità BIL in tonnellate (da ordini ODA)

```dax
// Calcola la quantità fatturata (BIL) in tonnellate filtrando per ordini ODA
// Converte automaticamente da Kg a Ton se il valore è >= 1000
CALCULATE(
SUMX(
FILTER(
FACT_Ordini,
LEFT(FACT_Ordini[CodiceOrdine], 3) = "ODA"
),
IF(FACT_Ordini[Quantity] >= 1000,
DIVIDE(FACT_Ordini[Quantity], 1000, 0),
FACT_Ordini[Quantity]
)
)
)
```

### Qta Resa
**Description:** Quantità RESA in tonnellate (da ordini ODA)

```dax
// Calcola la quantità resa (NetWeight) in tonnellate filtrando per ordini ODA
VAR QuantitaResa =
SUMX(
FILTER(
FACT_Ordini,
LEFT(FACT_Ordini[CodiceOrdine], 3) = "ODA"
),
IF(FACT_Ordini[NetWeight] >= 1000,
DIVIDE(FACT_Ordini[NetWeight], 1000, 0),
FACT_Ordini[NetWeight]
)
)
RETURN
QuantitaResa
```

### Importo USD
**Description:** Importo totale in USD per il Mix

```dax
// Calcola il valore totale degli ordini in USD: Prezzo unitario x Qta BIL
SUMX ( VALUES ( DIM_Calendario[MonthName] ), [Prezzo USD MIX] * [Qta BIL] )
```

### Accisa Unitario
**Description:** Accisa unitaria per tonnellata

```dax
// Somma delle accise unitarie registrate sugli ordini
SUMX ( FACT_Ordini, FACT_Ordini[Accisa])
```

### Importo Accisa
**Description:** Importo totale accisa

```dax
// Importo totale dell'accisa: Accisa Unitaria x Qta BIL
SUMX ( VALUES ( DIM_Calendario[MonthName] ), [Accisa Unitario] * [Qta BIL] )
```

### Trasporto Unitario
**Description:** Costo di trasporto unitario per tonnellata in base alla logistica

```dax
// Determina il costo di trasporto unitario per tonnellata in base alla base logistica
VAR Deposito = SELECTEDVALUE ( FACT_Ordini[CodiceDeposito] )
RETURN
SWITCH (
TRUE (),
Deposito IN { "MITSUI", "TOTAL" }, 0,
Deposito = "IPEM", 23,
0
)
```

### Importo Trasporto
**Description:** Importo totale trasporto

```dax
// Valore totale del trasporto: Costo Unitario x Qta BIL
[Trasporto Unitario] * [Qta BIL]
```

### Costo Totale
**Description:** Costo totale (Importo Euro + Trasporto)

```dax
// Somma dell'importo merce in Euro e dei costi di trasporto
[Importo Euro] + [Importo Trasporto]
```

### Costo Unitario
**Description:** Costo unitario per tonnellata incl. trasporto

```dax
// Rapporto tra costo totale (merce + trasporto) e quantità BIL
DIVIDE ( [Costo Totale], [Qta BIL], 0 )
```

### Nome Spedizioniere
**Description:** Ragione sociale dello spedizioniere dell'ordine

```dax
// Recupera il nome dello spedizioniere associato all'ordine corrente
CALCULATE (
FIRSTNONBLANK ( DIM_Spedizionieri[Name], 1 ),
FILTER (
DIM_Spedizionieri,
DIM_Spedizionieri[CodiceSpedizioniere] = SELECTEDVALUE ( FACT_Ordini[CodiceSpedizioniere] )
)
)
```

### Tasso Giorno Medio
**Description:** Media dei tassi di cambio giornalieri nel periodo

```dax
// Media dei tassi di cambio giornalieri nel contesto temporale
AVERAGEX ( VALUES ( DIM_Calendario[Date] ), [Tasso Giorno] )
```

### Costo €/T NEW
**Description:** Costo per tonnellata (logica di aggregazione media)

```dax
// Calcola il costo per tonnellata gestendo il contesto di singola data o aggregato
IF (
HASONEVALUE ( FACT_Ordini[DataSpedizione] ),
[Costo €/T],
AVERAGEX ( VALUES ( FACT_Ordini[DataSpedizione] ), [Costo €/T] )
)
```

### Prezzo USD Mese
**Description:** Media mensile del prezzo in USD

```dax
// Media del prezzo USD nel periodo selezionato
AVERAGEX ( VALUES ( FACT_Ordini[DataSpedizione] ), [Prezzo USD MIX] )
```

### Costo €/T Medio
**Description:** Costo medio per tonnellata su base mensile

```dax
// Media del costo per tonnellata aggregata per mese in calendario
AVERAGEX ( VALUES ( DIM_Calendario[MonthInCalendar] ), [Costo €/T] )
```

### Importo Euro
**Description:** Importo totale in Euro per il Mix

```dax
// Valore totale degli ordini in Euro: Prezzo unitario medio mese x Qta BIL
[Prezzo € MIX Mese] * [Qta BIL]
```

### Costo MIX
**Description:** Costo di riferimento per il prodotto Mix

```dax
// Restituisce il valore della misura base [Costo Mix]
[Costo Mix]
```

### Prezzo USD MIX
**Description:** Prezzo medio USD dalla tabella prezzi Mix

```dax
// Media aritmetica dei prezzi USD presenti nella tabella FACT_PrezziMix
AVERAGEX ( FACT_PrezziMix, FACT_PrezziMix[Prezzo USD] )
```

### Costo MIX 2
**Description:** Costo unitario MIX filtrato per clienti strategici

```dax
// Costo per tonnellata filtrato per i clienti principali (TOTAL/MITSUI) e prodotti MIX (1, 1T)
CALCULATE (
[Costo €/T],
FILTER (
FACT_Ordini,
FACT_Ordini[CodiceClienteFatturazione] IN { "C00991", "C01049" } &&
FACT_Ordini[CodiceArticolo] IN { "1", "1T" }
)
)
```

### Prezzo € MIX
**Description:** Prezzo MIX convertito in Euro (tasso specifico cliente)

```dax
// Conversione del prezzo USD in Euro utilizzando il tasso specifico del cliente
DIVIDE ( [Prezzo USD MIX], [Tasso Giorno Cliente], 0 )
```

### Prezzo € MIX Mese
**Description:** Prezzo medio Euro MIX per cliente

```dax
// Media ponderata del prezzo Euro MIX aggregata per cliente
AVERAGEX (
VALUES(DIM_Clienti[Nome & Codice]),
[Prezzo € MIX]
)
```

### Costo Totale Mese
**Description:** Costo totale mensile aggregato per giorno

```dax
// Somma dei costi totali giornalieri per l'intero mese
SUMX ( VALUES ( FACT_Ordini[DataSpedizione] ), [Costo Totale] )
```

### Tasso Giorno Medio 2
**Description:** Tasso di cambio medio con logica di contesto (Mese vs Totale)

```dax
// Logica dinamica: se nel contesto c'è un solo mese usa la media giornaliera, altrimenti la media mensile
IF ( HASONEVALUE ( DIM_Calendario[MonthName] ), [Tasso Giorno Medio], [Tasso Medio Mese] )
```

### Tasso Mese 2
**Description:** Tasso medio mensile ricalcolato con filtri espliciti

```dax
// Calcolo manuale del tasso medio mensile filtrato per l'anno e mese selezionati
VAR AnnoCorrente = VALUE({ SELECTEDVALUE ( DIM_Calendario[Year] ) })
VAR MeseCorrente = VALUE({ SELECTEDVALUE ( DIM_Calendario[MonthnYear] ) })

VAR ConteggioGiorni =
CALCULATE (
COUNTROWS ( ALLSELECTED ( FACT_Cambi[Data] ) ),
YEAR(FACT_Cambi[Data]) = AnnoCorrente &&
MONTH( FACT_Cambi[Data] ) = MeseCorrente
)
VAR SommaTassi =
CALCULATE ( SUMX ( FACT_Cambi, FACT_Cambi[Tasso] ), ALLSELECTED ( FACT_Cambi ) )

RETURN
DIVIDE(SommaTassi, ConteggioGiorni, 0)
```

### Tasso Giorno Cliente
**Description:** Tasso applicabile al cliente (Mese per TOTAL, Giorno per MITSUI)

```dax
// Determina quale tasso applicare al cliente selezionato:
// TOTAL: Tasso Medio Mese
// MITSUI: Tasso Giorno Medio
VAR CodiceCliente = SELECTEDVALUE ( DIM_Clienti[CodiceCliente] )
VAR CodiceDeposito = SELECTEDVALUE ( DIM_Deposito[CodiceDeposito] )
VAR IsTotal = ( CodiceCliente = "C00991" || CodiceDeposito = "TOTAL" )
VAR IsMitsui = ( CodiceCliente = "C01049" || CodiceDeposito = "MITSUI" )

RETURN
IF (
IsTotal || IsMitsui,
SWITCH (
TRUE (),
IsTotal, [Tasso Medio Mese],
IsMitsui, [Tasso Giorno Medio]
),
BLANK ()
)
```

### # Qta_BIL
**Description:** Conteggio record ordini ODA

```dax
COUNT(FACT_Ordini[CodiceOrdine])
```

### Qta BIL (2)
**Description:** Quantità BIL totale per ordini ODA

```dax
// Somma grezza delle quantità per gli ordini di tipo ODA
CALCULATE(
SUMX(FACT_Ordini, FACT_Ordini[Quantity]),
LEFT(FACT_Ordini[CodiceOrdine], 3) = "ODA"
)
```

### Spedizionieri Attivi
**Description:** Spedizionieri con movimenti MIX nel periodo

```dax
// Restituisce il nome dello spedizioniere se ha effettuato almeno una consegna di prodotti MIX (1, 1T)
IF(
CALCULATE(
COUNTROWS(FACT_Ordini),
FACT_Ordini[CodiceArticolo] IN {"1", "1T"}
) > 0,
SELECTEDVALUE(DIM_Spedizionieri[Name])
)
```

### Ordini MIX
**Description:** Numero ordini MIX clienti TOTAL/MITSUI

```dax
// Conta gli ordini di prodotti MIX effettuati dai clienti strategici
CALCULATE(
COUNTROWS(FACT_Ordini),
FACT_Ordini[CodiceArticolo] IN {"1", "1T"} &&
FACT_Ordini[CodiceClienteVendita] IN {"C00991", "C01049"}
)
```

### Qta Acquisto MIX Tempa
**Description:** Quantità acquisto MIX (Tab Tempa)

```dax
// Somma delle quantità di acquisto MIX dalla tabella temporanea Tempa
SUMX(FACT_AcquistiMixTemp, FACT_AcquistiMixTemp[Qta])
```

### # Qta Acquisto MIX Tempa
**Description:** Numero carichi MIX (Tab Tempa)

```dax
// Conteggio dei record di acquisto MIX nella tabella temporanea Tempa
COUNTX(FACT_AcquistiMixTemp, FACT_AcquistiMixTemp[Qta])
```

## KPI_ObiettivoVendite

### Valore Obiettivo Vendite
**Description:** Valore obiettivo vendite (da parametro)

```dax
// Restituisce il valore dell'obiettivo di vendita selezionato dal parametro
SELECTEDVALUE('KPI_ObiettivoVendite'[Obiettivo Vendite])
```

## KPI_Prodotto

### Agenzia
**Description:** Spese di agenzia (CG 4030004 + Accantonamenti)

```dax
// Somma i costi di agenzia registrati in CG (conto 4030004) e gli accantonamenti associati
VAR ImportoCG =
CALCULATE (
[Importo],
FACT_MovimentiCG[CodiceConto] = "4030004" && FACT_MovimentiCG[CodiceSorgente] = "ACQUISTI"
)
VAR ImportoAccantonamenti =
CALCULATE (
[Importo Accantonamenti],
FACT_Accantonamenti[CodiceConto] = "4030004"
)
RETURN
ImportoCG + ImportoAccantonamenti
```

### Controstallie
**Description:** Oneri per controstallie (CG 4030008, Progetto ML04)

```dax
// Costi per controstallie registrati su conto 4030008 e progetto ML04
CALCULATE (
[Importo],
FACT_MovimentiCG[CodiceConto] = "4030008" && FACT_MovimentiCG[Progetto] = "ML04"
)
```

### Dogana
**Description:** Spese doganali (CG 4030002, Sorgente ACQUISTI)

```dax
// Oneri doganali registrati su conto 4030002 con sorgente ACQUISTI
CALCULATE (
[Importo],
FACT_MovimentiCG[CodiceConto] = "4030002" && FACT_MovimentiCG[CodiceSorgente] = "ACQUISTI"
)
```

### Perizia
**Description:** Spese per perizie (CG 4030007, Progetto ML04)

```dax
// Spese per perizie tecniche registrate su conto 4030007 e progetto ML04
CALCULATE (
[Importo],
FACT_MovimentiCG[CodiceConto] = "4030007" && FACT_MovimentiCG[Progetto] = "ML04"
)
```

### Recupero Controstallie
**Description:** Ricavi da recupero controstallie (CG 3400025)

```dax
// Ricavi da recupero controstallie registrati su conto 3400025
CALCULATE ( [Importo], FACT_MovimentiCG[CodiceConto] = "3400025" )
```

### Recupero Dazi Doganali
**Description:** Recupero dazi doganali da documenti di vendita

```dax
// Recupero dei dazi doganali basato su documenti di vendita (Articolo 3400026 o Progetto ML04)
VAR NaveSelezionata = SELECTEDVALUE ( DIM_MezziTrasporto[CodiceMezzo] )
VAR ImportoRecupero =
CALCULATE (
[Importo Doc Vendita],
'FACT_DocumentoVendita'[CodiceArticolo] = "3400026" ||
'FACT_DocumentoVendita'[Progetto] = "ML04" ||
'FACT_DocumentoVendita'[MezzoTrasporto] = NaveSelezionata
)
RETURN
ImportoRecupero
```

### Recupero Spese Terzi
**Description:** Ricavi recupero spese terzi (CG 3400023)

```dax
// Ricavi per recupero spese effettuate per conto terzi (Conto 3400023)
CALCULATE ( [Importo], FACT_MovimentiCG[CodiceConto] = "3400023" )
```

### Rimorchio
**Description:** Spese di rimorchio (CG 4030006, Progetto ML04)

```dax
// Costi per servizi di rimorchio (Conto 4030006, Progetto ML04)
CALCULATE (
[Importo],
FACT_MovimentiCG[CodiceConto] = "4030006" && FACT_MovimentiCG[Progetto] = "ML04"
)
```

### Trasporto Acquisti
**Description:** Costi trasporto acquisti (CG 4030003, Sorgente REGACQ)

```dax
// Costi di trasporto su acquisti registrati su conto 4030003
CALCULATE (
[Importo],
FACT_MovimentiCG[CodiceConto] = "4030003" && FACT_MovimentiCG[CodiceSorgente] = "REGACQ"
)
```

### COSTI_ACCESSORI_GPL
**Description:** Totale costi accessori acquisto GPL (Costi - Recuperi)

```dax
// Somma algebrica di tutti i costi accessori legati all'acquisto di GPL (Dogana, Agenzia, Rimorchio, etc.) al netto dei recuperi
VAR SommaCosti = [Dogana] + [Agenzia] + [Rimorchio] + [Perizia] + [Controstallie]
VAR SommaRecuperi = [Recupero Spese Terzi] + [Recupero Controstallie] + [Recupero Dazi Doganali]
RETURN
SommaCosti - SommaRecuperi
```

### €/Ton CostoGPL_Resa
**Description:** Costo totale nave per tonnellata resa

```dax
// Incidenza unitaria per tonnellata del costo totale nave sulla quantità resa IPEM
DIVIDE ( [Total Costs NAVI], [QuantityIPEM], 0 )
```

### COSTO GPL
**Description:** Costo base GPL (Materia Prima + Trasporto)

```dax
// Somma dei costi di materia prima e trasporto acquisti
[Materia Prima €] + [Trasporto Acquisti]
```

### Materia Prima € OLD
**Description:** Costo materia prima (legacy via accantonamenti)

```dax
// Misura legacy per il calcolo della materia prima basato su accantonamenti
VAR ImpMP =
CALCULATE (
[Importo Accantonamenti],
FACT_Accantonamenti[CodiceConto] = "4020002"
)
VAR ImpMP2 =
CALCULATE (
[Importo Accantonamenti],
FACT_Accantonamenti[CodiceConto] = "2030004"
)
RETURN
ImpMP + ImpMP2
```

### Total Costs NAVI
**Description:** Costo totale navi (GPL + Accessori)

```dax
// Costo complessivo associato alle navi: GPL + Accessori
[COSTO GPL] + [COSTI_ACCESSORI_GPL]
```

### Materia Prima €
**Description:** Valore materia prima da Contabilità Generale

```dax
// Calcola il valore della materia prima dai movimenti CG (Conti 4020002 e 2030004)
VAR ImportoMP1 =
CALCULATE (
[Importo],
FACT_MovimentiCG[CodiceConto] = "4020002" && FACT_MovimentiCG[CodiceSorgente] = "REGACQ"
)
VAR ImportoMP2 =
CALCULATE (
[Importo],
FACT_MovimentiCG[CodiceConto] = "2030004" &&
FACT_MovimentiCG[CodiceSorgente] IN { "REGACQ", "REGACQIC" } &&
FACT_MovimentiCG[Progetto] = ""
)
RETURN
ImportoMP1 + ImportoMP2
```

### Materia Prima € 2
**Description:** Materia prima filtrata per record con mezzo trasporto

```dax
// Altra versione del calcolo materia prima filtrata per mezzo di trasporto
CALCULATE (
[Importo],
FACT_MovimentiCG[CodiceConto] = "2030004"
&& FACT_MovimentiCG[TipoSorgente] = ""
&& FACT_MovimentiCG[MezzoTrasporto] <> ""
)
```

### Perizia 2
**Description:** Spese perizia (versione ACQ)

```dax
// Versione alternativa della misura Perizia utilizzando [Importo ACQ]
CALCULATE (
[Importo ACQ],
FACT_MovimentiCG[CodiceConto] = "4030007" && FACT_MovimentiCG[Progetto] = "ML04"
)
```

### Costo Acquisto Qta Ton
**Description:** Costo di acquisto unitario (CMP) nel contesto quantità

```dax
// Restituisce il CMP di acquisto solo se è presente una quantità nel contesto
IF ( ISBLANK ( [Quantity] ), BLANK (), [CMP Acquisto] )
```

### Recupero Spese Trasporto
**Description:** Recupero spese di trasporto (CG 3400024)

```dax
// Ricavi da recupero spese di trasporto (Conto 3400024)
CALCULATE ( ABS ( [Importo] ), FACT_MovimentiCG[CodiceConto] = "3400024" )
```

### CMP Acquisto CUM
**Description:** CMP Acquisto cumulato nel tempo

```dax
// Calcola il CMP di acquisto accumulato storicamente
CALCULATE (
[CMP Acquisto],
FILTER ( ALL ( DIM_Calendario ), DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] ) )
)
```

### CMP Prodotto
**Description:** CMP calcolato sulla quantità totale

```dax
// Rapporto tra i costi totali nave e la quantità totale prodotta/acquistata
DIVIDE ( [Total Costs NAVI], [Quantity] )
```

### CMP Acquisto CD
**Description:** CMP calcolato sulla quantità resa CD

```dax
// Rapporto tra i costi totali nave e la quantità resa in Conto Deposito
DIVIDE ( [Total Costs NAVI], [QuantityIPEM] )
```

### CMP Prodotto CUM
**Description:** CMP Prodotto cumulato nel tempo

```dax
// Calcola il CMP prodotto accumulato storicamente
CALCULATE (
[CMP Prodotto],
FILTER ( ALL ( DIM_Calendario ), DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] ) )
)
```

### CMP Acquisto
**Description:** CMP di acquisto dinamico per MIX, PROPANO o totale ponderato

```dax
// Calcola il CMP di acquisto differenziato per gruppo prodotto (MIX vs PROPANO)
// Se nessun gruppo è filtrato, esegue una media ponderata tra i due prodotti
VAR GruppoFiltrato = { SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () ) }

VAR CMP_Mix = [Costo Mix Resa]
VAR CMP_Propano = [Costo Propano]

VAR Qta_Mix = SUMX(FACT_Mix, FACT_Mix[Qta BIL] )
VAR Qta_Propano = SUMX(FACT_Propano, FACT_Propano[QuantityIPEM] )

VAR CMP_Ponderato = DIVIDE((CMP_Mix * Qta_Mix) + (CMP_Propano * Qta_Propano), Qta_Mix + Qta_Propano)

RETURN
SWITCH (
TRUE (),
GruppoFiltrato = "MIX", CMP_Mix,
GruppoFiltrato = "PROPANO", CMP_Propano,
GruppoFiltrato = BLANK (), CMP_Ponderato
)
```

### CMP Acquisto Prodotto
**Description:** Rapporto tra Importo Acquisto e Qta Acquisto

```dax
// Rapporto semplice tra importo totale acquisti e quantità acquistata
DIVIDE ( [Importo Acquisto], [Qta Acquisto], 0 )
```

### Importo Costo Acquisto
**Description:** Valore acquisto (QuantityIPEM x CMP)

```dax
// Valorizzazione della quantità resa CD al CMP di acquisto
[QuantityIPEM] * [CMP Acquisto]
```

### Importo Acquisto
**Description:** Importo totale acquisti per gruppo prodotto

```dax
// Somma gli importi di acquisto per MIX e PROPANO in base al contesto
VAR GruppoFiltrato = { SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () ) }
VAR Imp_Mix = [Importo Costo Mix]
VAR Imp_Propano = [Importo Costo Propano]

RETURN
SWITCH (
TRUE (),
GruppoFiltrato = "MIX", Imp_Mix,
GruppoFiltrato = "PROPANO", Imp_Propano,
GruppoFiltrato = BLANK (), Imp_Mix + Imp_Propano
)
```

### Margine Unitario
**Description:** Differenza unitaria tra Prezzo Medio e CMP

```dax
// Differenza tra prezzo medio di vendita e CMP di acquisto
VAR Prezzo = [Prezzo Medio Vendita]
VAR Costo = [CMP Acquisto]
RETURN
IF (Prezzo > 0, Prezzo - Costo, 0)
```

### % Profitto
**Description:** Percentuale di profitto sul fatturato

```dax
// Rapporto tra importo margine e importo vendita
DIVIDE ( [Importo Margine], [Importo Vendita], 0 )
```

### Trasporto Vendite
**Description:** Spese trasporto su vendite (CG 4110045)

```dax
// Costi di trasporto legati alle vendite (Conto 4110045)
CALCULATE ( [Importo], FACT_MovimentiCG[CodiceConto] = "4110045" )
```

### Filtro Anno
**Description:** Valore dell'anno selezionato

```dax
// Restituisce l'anno selezionato nel filtro calendario
SELECTEDVALUE ( DIM_Calendario[Year] )
```

### Filtro Mese
**Description:** Valore del mese selezionato

```dax
// Restituisce il nome del mese selezionato nel filtro calendario
SELECTEDVALUE ( DIM_Calendario[MonthName] )
```

### Costo Venduto
**Description:** Costo del venduto basato su CMP Giacenza

```dax
// Calcola il costo del venduto: Giacenza CMP x Quantità Venduta
[CMP Giacenza] * [Qta Vendita]
```

### Importo Giacenza Iniziale
**Description:** Importo rimanenze iniziali (CG 401*)

```dax
// Valore delle giacenze iniziali (Conti 4010002 per Propano, 4010003 per Mix)
VAR GruppoFiltrato = { SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () ) }

VAR Imp_Mix = CALCULATE ( [Importo], FACT_MovimentiCG[CodiceConto] = "4010003" )
VAR Imp_Propano = CALCULATE ( [Importo], FACT_MovimentiCG[CodiceConto] = "4010002" )

RETURN
SWITCH (
TRUE (),
GruppoFiltrato = "MIX", Imp_Mix,
GruppoFiltrato = "PROPANO", Imp_Propano,
GruppoFiltrato = BLANK (), Imp_Mix + Imp_Propano
)
```

### CMP Giacenza
**Description:** CMP calcolato sulla somma di acquisti e rimanenze iniziali

```dax
// Calcolo del CMP di giacenza come media ponderata tra (Acquisti + Iniziali)
VAR ValoreTotale = [Importo Acquisto] + [Importo Giacenza Iniziale]
VAR QuantitaTotale = [Qta Acquisto] + [Qta Giacenza Iniziale]
RETURN
DIVIDE(ValoreTotale, QuantitaTotale)
```

### CMP Acquisto AVG QTD
**Description:** Media trimestrale del CMP Acquisto

```dax
// Media del CMP di acquisto calcolata sui trimestri (Quarter-To-Date)
AVERAGEX (
VALUES(DIM_Calendario[MonthInCalendar]),
TOTALQTD([CMP Acquisto], DIM_Calendario[Date])
)
```

### CMP Acquisto AVG YTD
**Description:** Media annuale progressiva del CMP Acquisto

```dax
// Media del CMP di acquisto calcolata dall'inizio dell'anno (Year-To-Date)
AVERAGEX (
VALUES(DIM_Calendario[MonthInCalendar]),
TOTALYTD([CMP Acquisto], DIM_Calendario[Date])
)
```

### CMP Giacenza YTD
**Description:** Media mobile a 4 mesi del CMP YTD

```dax
// Calcola la media dei CMP YTD degli ultimi 4 mesi
VAR MediaYTD = [CMP Acquisto AVG YTD]
VAR CMP_LM1 = CALCULATE ( MediaYTD, DATEADD ( DIM_Calendario[Date], -1, MONTH ) )
VAR CMP_LM2 = CALCULATE ( MediaYTD, DATEADD ( DIM_Calendario[Date], -2, MONTH ) )
VAR CMP_LM3 = CALCULATE ( MediaYTD, DATEADD ( DIM_Calendario[Date], -3, MONTH ) )
VAR CMP_LM4 = CALCULATE ( MediaYTD, DATEADD ( DIM_Calendario[Date], -4, MONTH ) )

VAR SommaCMP = CMP_LM1 + CMP_LM2 + CMP_LM3 + CMP_LM4
RETURN
DIVIDE(SommaCMP, 4, 0)
```

### CMP Acquisto 2
**Description:** CMP Acquisto basato su medie tabelle FACT_Mix/Propano

```dax
// Media aritmetica semplice dei costi medi MIX e PROPANO
VAR GruppoFiltrato = { SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () ) }
VAR CMP_Mix = AVERAGEX(FACT_Mix, FACT_Mix[Costo] )
VAR CMP_Propano = AVERAGEX(FACT_Propano, FACT_Propano[Costo] )
RETURN
SWITCH (
TRUE (),
GruppoFiltrato = "MIX", CMP_Mix,
GruppoFiltrato = "PROPANO", CMP_Propano,
DIVIDE(CMP_Mix + CMP_Propano, 2, 0)
)
```

### Importo Margine
**Description:** Margine totale (Qta x Margine Unitario)

```dax
// Margine totale calcolato come Quantità Venduta x Margine Unitario
[Qta Vendita] * [Margine Unitario]
```

### # Mezzi
**Description:** Conteggio mezzi di trasporto (escluso ATB)

```dax
// Conta il numero di mezzi di trasporto diversi da 'ATB'
CALCULATE(
COUNTX(DIM_MezziTrasporto, [QuantityIPEM]),
DIM_MezziTrasporto[CodiceMezzo] <> "ATB"
)
```

### Costo Venduto 2
**Description:** Delta tra giacenza iniziale e acquisti

```dax
// Calcolo alternativo del costo venduto (Differenza tra Iniziali e Acquisti - logica specifica)
[Importo Giacenza Iniziale] - [Importo Acquisto]
```

### Costo Venduto 3
**Description:** Costo del venduto calcolato per differenza inventariale (Iniziale + Acquisti - Finale)

```dax
// Calcola il costo del venduto basato sulla formula: Giacenza Iniziale + Acquisti - Giacenza Finale
VAR Imp_Giacenza = [Importo Giacenza Iniziale]
VAR Imp_Giacenza_LM = CALCULATE ( Imp_Giacenza, DATEADD ( DIM_Calendario[Date], -1, MONTH ) )
VAR Imp_Giacenza_NM = CALCULATE ( Imp_Giacenza, DATEADD ( DIM_Calendario[Date], 1, MONTH ) )
VAR Imp_Acquisto_CM = [Importo Acquisto]

RETURN
Imp_Giacenza_LM + Imp_Acquisto_CM - Imp_Giacenza_NM
```

### CMP Acquisto MEDIAN YTD
**Description:** Mediana annuale progressiva del CMP Acquisto

```dax
// Mediana del CMP di acquisto calcolata dall'inizio dell'anno (YTD)
MEDIANX(
VALUES(DIM_Calendario[MonthInCalendar]),
TOTALYTD([CMP Acquisto], DIM_Calendario[Date])
)
```

### Importo Giacenza Finale
**Description:** Importo rimanenze finali (CG 330*)

```dax
// Valore delle giacenze finali (Conti 3300002 per Propano, 3300003 per Mix)
VAR GruppoFiltrato = { SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () ) }

VAR Imp_Mix = CALCULATE ( [Importo], FACT_MovimentiCG[CodiceConto] = "3300003" )
VAR Imp_Propano = CALCULATE ( [Importo], FACT_MovimentiCG[CodiceConto] = "3300002" )

RETURN
SWITCH (
TRUE (),
GruppoFiltrato = "MIX", Imp_Mix,
GruppoFiltrato = "PROPANO", Imp_Propano,
GruppoFiltrato = BLANK (), Imp_Mix + Imp_Propano
)
```

### Importo Movimento Mese
**Description:** Delta valore magazzino nel mese (Acquisti - Vendite valorizzate CMP)

```dax
// Calcola la variazione di valore del magazzino nel mese (Acquisti - Costo Venduto CMP)
[Importo Acquisto] - ([Qta Vendita] * [CMP Giacenza])
```

### Importo Giacenza
**Description:** Valore giacenza calcolato come progressivo dei movimenti YTD

```dax
// Calcola il valore della giacenza come: Iniziale + Somma dei delta mensili YTD
VAR GiacenzaCorrente =
[Importo Giacenza Iniziale] +
CALCULATE (
[Importo Movimento Mese],
DATESYTD ( DIM_Calendario[Date] )
)

RETURN
IF ( ABS ( GiacenzaCorrente ) > 100000000, BLANK (), GiacenzaCorrente )
```

## KPI_Vendite

### Importo Vendite (Doc)
**Description:** Importo vendite basato su documenti di vendita

```dax
// Restituisce l'importo totale delle vendite dai documenti
[Importo Vendita]
```

### Margine Cliente
**Description:** Margine calcolato come differenza tra vendite e costo venduto

```dax
// Calcola il margine assoluto per cliente
VAR Vendite = [Importo Vendite (Doc)]
VAR Costo = [Costo Venduto Cliente]
RETURN
Vendite - Costo
```

### Importo Acquisti
**Description:** Importo totale acquisti

```dax
// Importo totale degli acquisti
[Importo Acquisto]
```

### % Margine Cliente
**Description:** Percentuale di margine sul cliente

```dax
// Percentuale di marginalità sul fatturato
VAR Margine = [Margine Cliente]
VAR Vendite = [Importo Vendite (Doc)]
RETURN
DIVIDE ( Margine, Vendite, 0 )
```

### % Margine Cliente LY
**Description:** Percentuale di margine sul cliente dello scorso anno

```dax
// Marginalità percentuale dello stesso periodo dell'anno precedente
CALCULATE ( [% Margine Cliente], DATEADD ( DIM_Calendario[Date], -1, YEAR ) )
```

### % Crescita Margine
**Description:** Percentuale di crescita del margine rispetto allo scorso anno

```dax
// Variazione percentuale della marginalità rispetto all'anno precedente
VAR MargineAttuale = [% Margine Cliente]
VAR MarginePrecedente = [% Margine Cliente LY]
RETURN
DIVIDE (
MargineAttuale - MarginePrecedente,
MarginePrecedente,
0
)
```

### % Crescita YoY
**Description:** Percentuale di crescita delle vendite anno su anno

```dax
// Crescita percentuale del fatturato anno su anno
VAR VenditeAttuali = [Importo Vendite (Doc)]
VAR VenditePrecedenti = [Importo Vendite (Doc) LY]
RETURN
DIVIDE ( VenditeAttuali - VenditePrecedenti, VenditePrecedenti, 0 )
```

### Importo Vendite (Doc) LY
**Description:** Importo vendite dello scorso anno

```dax
// Fatturato dello stesso periodo dell'anno precedente
CALCULATE ( [Importo Vendite (Doc)], DATEADD ( DIM_Calendario[Date], -1, YEAR ) )
```

### Margine Cliente LY
**Description:** Margine cliente dello scorso anno

```dax
// Margine assoluto dello stesso periodo dell'anno precedente
CALCULATE ( [Margine Cliente], DATEADD ( DIM_Calendario[Date], -1, YEAR ) )
```

### Costo Venduto Cliente
**Description:** Costo del venduto calcolato su quantità venduta e CMP

```dax
// Valorizzazione del venduto: Quantità x Costo Medio Ponderato (CMP)
VAR Quantita = [Qta Vendita]
VAR CMP = [CMP Acquisto Prodotto]
RETURN
Quantita * CMP
```

### # Nuovi Clienti
**Description:** Numero di nuovi clienti che non acquistavano da N giorni

```dax
// Conta i clienti che hanno effettuato il primo acquisto nel periodo selezionato
// Un cliente è considerato "nuovo" se non ha acquistato nei precedenti N giorni (default 90)
VAR nr_giorni = SELECTEDVALUE(PARAM_NrGiorni[PARAM_NrGiorni], 90)
VAR Tab_Clienti_Attuali = VALUES ( 'FACT_DocumentoVendita'[CodiceClienteFatturazione] )

VAR Clienti_Storici =
CALCULATETABLE (
VALUES ( 'FACT_DocumentoVendita'[CodiceClienteFatturazione]  ),
FILTER (
ALL ( DIM_Calendario[Date] ),
DIM_Calendario[Date] > MIN ( DIM_Calendario[Date] ) - nr_giorni &&
DIM_Calendario[Date] < MIN ( DIM_Calendario[Date] )
)
)
RETURN
COUNTROWS (
EXCEPT ( Tab_Clienti_Attuali, Clienti_Storici )
)
```

### # Clienti Persi
**Description:** Numero di clienti persi (non acquistano da 365 giorni)

```dax
// Calcola i clienti "persi": quelli che hanno acquistato in passato (fino a 365 gg fa)
// ma non hanno effettuato acquisti negli ultimi N giorni (default 60)
VAR nr_giorni = 60
VAR Tab_Clienti_Attivi_Passato =
CALCULATETABLE (
VALUES ( 'FACT_DocumentoVendita'[CodiceClienteFatturazione]  ),
FILTER (
ALL ( DIM_Calendario[Date] ),
DIM_Calendario[Date] > MIN ( DIM_Calendario[Date] ) - 365 &&
DIM_Calendario[Date] <= MIN ( DIM_Calendario[Date] ) - nr_giorni
)
)
VAR Clienti_Recenti =
CALCULATETABLE (
VALUES ( 'FACT_DocumentoVendita'[CodiceClienteFatturazione]  ),
FILTER (
ALL ( DIM_Calendario[Date] ),
DIM_Calendario[Date] > MIN ( DIM_Calendario[Date] ) - nr_giorni &&
DIM_Calendario[Date] <= MIN ( DIM_Calendario[Date] )
)
)
RETURN
COUNTROWS ( EXCEPT ( Tab_Clienti_Attivi_Passato, Clienti_Recenti ) ) * -1
```

### Data Ultimo Acquisto Cliente
**Description:** Data dell'ultima spedizione per il cliente

```dax
// Restituisce la data dell'ultimo documento di vendita per il cliente nel contesto
LASTDATE('FACT_DocumentoVendita'[DataSpedizione])
```

### Data Ultimo Acquisto
**Description:** Data massima di spedizione assoluta a sistema

```dax
// Restituisce la data massima assoluta di vendita nel sistema (ignora i filtri temporali ma non quelli cliente)
MAXX(
ALL('FACT_DocumentoVendita'),
'FACT_DocumentoVendita'[DataSpedizione]
)
```

### # Giorni da ultimo Acquisto
**Description:** Giorni trascorsi dall'ultimo acquisto del cliente rispetto alla data massima di sistema

```dax
// Calcola la distanza in giorni tra l'ultima vendita assoluta e l'ultima vendita del cliente
VAR DataUltimaCliente = [Data Ultimo Acquisto Cliente]
VAR DataUltimaAssoluta = [Data Ultimo Acquisto]
RETURN
IF(
ISBLANK(DataUltimaCliente),
BLANK(),
VALUE(DataUltimaAssoluta - DataUltimaCliente)
)
```

### # Clienti Persi (2)
**Description:** Clienti senza acquisti nel range temporale selezionato

```dax
// Identifica i clienti che non hanno acquistato negli ultimi N giorni selezionati
VAR Lista_Tutti_Clienti = ALL('FACT_DocumentoVendita'[CodiceClienteFatturazione])
VAR nr_days = SELECTEDVALUE(PARAM_NrGiorni[PARAM_NrGiorni], 90)

VAR tab_periodo_controllo =
FILTER(
ALLSELECTED(DIM_Calendario),
DIM_Calendario[Date] > ( MIN(DIM_Calendario[Date]) - nr_days ) &&
DIM_Calendario[Date] < MIN(DIM_Calendario[Date])
)
VAR tab_clienti_senza_vendite =
FILTER(
Lista_Tutti_Clienti,
CALCULATE(
COUNTROWS('FACT_DocumentoVendita'),
tab_periodo_controllo
) = 0
)

RETURN
COUNTROWS(tab_clienti_senza_vendite)
```

### # Nuovi Clienti (2)
**Description:** Clienti al loro primo acquisto assoluto nel periodo

```dax
// Identifica i clienti che hanno acquistato ora ma non avevano MAI acquistato prima della data minima selezionata
VAR Clienti_Attuali = VALUES('FACT_DocumentoVendita'[CodiceClienteFatturazione])
VAR nr_days = SELECTEDVALUE(PARAM_NrGiorni[PARAM_NrGiorni], 90)

VAR tab_calendario_storico =
FILTER(
ALLSELECTED(DIM_Calendario),
DIM_Calendario[Date] < MIN(DIM_Calendario[Date])
)

VAR tab_nuovi =
FILTER(
Clienti_Attuali,
CALCULATE(
COUNTROWS('FACT_DocumentoVendita'),
tab_calendario_storico
) = 0
)

RETURN
CALCULATE(
COUNTROWS(VALUES('FACT_DocumentoVendita'[CodiceClienteFatturazione])),
tab_nuovi
)
```

### # Clienti Ritornati
**Description:** Clienti che tornano ad acquistare dopo un periodo di inattività

```dax
// Clienti che hanno acquistato nel periodo attuale e avevano acquistato in passato,
// ma non nel periodo immediatamente precedente (definito da nr_days)
VAR Clienti_Attuali = VALUES('FACT_DocumentoVendita'[CodiceClienteFatturazione])
VAR nr_days = SELECTEDVALUE(PARAM_NrGiorni[PARAM_NrGiorni], 90)

VAR tab_finestra_assenza =
FILTER(
ALLSELECTED(DIM_Calendario),
DIM_Calendario[Date] > ( MIN(DIM_Calendario[Date]) - nr_days ) &&
DIM_Calendario[Date] < MIN(DIM_Calendario[Date])
)

VAR tab_ritornati =
FILTER(
Clienti_Attuali,
CALCULATE(
COUNTROWS('FACT_DocumentoVendita'),
tab_finestra_assenza
) = 0
)

RETURN
COUNTROWS(tab_ritornati)
```

### Qta Vendite
**Description:** Quantità totale venduta in tonnellate

```dax
// Somma delle quantità in tonnellate filtrate per movimenti di tipo 'Vendita' in FACT_Magazzino
CALCULATE (
ABS ( [Qta Ton] ),
FACT_Magazzino[TipoMovimento] = "Vendita"
)
```

### Prezzo Medio Vendita
**Description:** Prezzo medio unitario di vendita per categorie NAZ, UE, NAZPERM

```dax
// Calcola il prezzo medio unitario per le categorie NAZ, UE e NAZPERM
CALCULATE(
AVERAGEX(
'FACT_DocumentoVendita',
'FACT_DocumentoVendita'[PrezzoUnitario]
),
'FACT_DocumentoVendita'[CodiceCategoria] IN {"NAZ", "UE", "NAZPERM"}
)
```

### Rank Cliente
**Description:** Classifica del cliente per importo vendita

```dax
// Classifica i clienti in base all'importo delle vendite
RANKX ( ALL ( DIM_Clienti ), [Importo Vendita], , DESC )
```

### Top 10 Clienti Vendite
**Description:** Importo vendite per i primi 10 clienti

```dax
// Restituisce l'importo vendite solo per i primi 10 clienti in classifica
VAR Classifica = [Rank Cliente]
RETURN
IF (
ISFILTERED ( DIM_Clienti[Nome] ),
IF ( Classifica <= 10, [Importo Vendite (CG)], BLANK () ),
CALCULATE (
[Importo Vendite (CG)],
TOPN ( 10, VALUES ( DIM_Clienti[Nome] ), [Importo Vendite (CG)] )
)
)
```

### Importo Vendite (CG)
**Description:** Importo vendite basato sui movimenti di contabilità generale (CG)

```dax
// Valore delle vendite derivante dalla Contabilità Generale (CG)
// Se presente l'importo clienti vendite usa quello, altrimenti usa i passaggi
VAR VenditeCG = [Importo Clienti Vendite]
VAR PassaggiCG = [Importo Clienti Passaggi]
RETURN
IF (
VenditeCG <> 0,
VenditeCG,
PassaggiCG
)
```

### Importo Clienti Passaggi
**Description:** Importo vendite per passaggi (conti CG 31*)

```dax
// Fatturato relativo ai conti di 'Passaggio' (Conti 31*)
CALCULATE (
ABS ( [Importo] ),
FACT_MovimentiCG[Conto] IN { "3100001", "3100002", "3100003", "3100004" }
)
```

### Importo Clienti Vendite
**Description:** Importo ricavi da Contabilità Generale filtrato per conti 30*

```dax
// Filtra i movimenti CG per i conti ricavi (30*) e per tipo Fattura/Nota Credito
VAR ContiRicavi = { "3000002", "3000003", "3000005" }
VAR ProdottoSelezionato = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto] )
VAR ProgettoCG =
SWITCH (
TRUE (),
ProdottoSelezionato = "PROPANO", "PROPAN",
ProdottoSelezionato = "MIX", "MIX",
BLANK ()
)

VAR TabellaFiltrata =
FILTER (
'FACT_MovimentiCG',
FACT_MovimentiCG[Conto] IN ContiRicavi &&
(ISBLANK(ProgettoCG) || FACT_MovimentiCG[Progetto] = ProgettoCG) &&
FACT_MovimentiCG[Tipo Documento] IN { "Fattura", "Nota Credito" }
)

RETURN
CALCULATE ( ABS ( [Importo] ), TabellaFiltrata )
```

### Prezzo Dirette
**Description:** Rapporto tra ricavi diretti CG e quantità venduta

```dax
// Prezzo medio per le vendite dirette (Ricavi CG / Qta Ton)
DIVIDE ( [Importo Clienti Vendite], [Qta Vendite], 0 )
```

### Prezzo Passaggio
**Description:** Rapporto tra ricavi passaggi CG e quantità venduta

```dax
// Prezzo medio per i passaggi (Passaggi CG / Qta Ton)
DIVIDE ( [Importo Clienti Passaggi], [Qta Vendite], 0 )
```

### Importo Acquisti Progressivo (NAVI)
**Description:** Costi totali navi accumulati nel tempo

```dax
// Somma progressiva dei costi legati alle Navi (Acquisti)
CALCULATE (
[Total Costs NAVI],
FILTER (
ALL ( DIM_Calendario ),
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
)
```

### # Clienti Vendita
**Description:** Numero di clienti unici con movimenti di vendita

```dax
// Conta i codici soggetti distinti che hanno effettuato una vendita in FACT_Magazzino
VAR Tab_Clienti_Vendita =
CALCULATETABLE (
VALUES ( FACT_Magazzino[Codice] ),
FACT_Magazzino[Tipo Movimento] = "Vendita"
)
RETURN
COUNTROWS ( Tab_Clienti_Vendita )
```

### Importo Vendite Gruppo Cliente
**Description:** Fatturato segmentato per cluster di importo cliente

```dax
// Calcola le vendite aggregate per gruppi definiti in base a soglie di importo
CALCULATE (
[Importo Vendite (CG)],
FILTER (
VALUES ( FACT_MovimentiCG[Importo] ),
COUNTROWS (
FILTER (
'Gruppo Vendite Clienti',
FACT_MovimentiCG[Importo] >= MIN ( 'Gruppo Vendite Clienti'[Min] )
&& FACT_MovimentiCG[Importo] < MAX ( 'Gruppo Vendite Clienti'[Max] )
)
) > 0
)
)
```

### Qta Vendite Progressivo
**Description:** Somma progressiva delle quantità vendute (dal 2015)

```dax
// Quantità venduta accumulata a partire dal 2015
VAR tab_periodo_storico =
FILTER (
ALL ( DIM_Calendario[Date] ),
DIM_Calendario[Date] >= DATE ( 2015, 1, 1 )
&& DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
RETURN
CALCULATE ( [Qta Vendite], tab_periodo_storico )
```

### Prezzo Medio Vendita Mix
**Description:** Prezzo medio vendita per i prodotti Mix

```dax
// Calcola il prezzo medio ponderato per i prodotti del gruppo MIX
VAR GruppoArticolo = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () )
VAR MeseCalendario = SELECTEDVALUE ( DIM_Calendario[MonthInCalendar] )

VAR ArticoliGruppo =
CALCULATETABLE (
SELECTCOLUMNS(DIM_Articoli, "@Codice", DIM_Articoli[CodiceArticolo]),
DIM_Articoli[GruppoProdotto] = GruppoArticolo
)

VAR TabellaMixFiltrata =
FILTER (
'FACT_Mix',
'FACT_Mix'[CodiceArticolo] IN ArticoliGruppo &&
'FACT_Mix'[MonthInCalendar] = MeseCalendario
)
RETURN
AVERAGEX (
TabellaMixFiltrata,
'FACT_Mix'[Prezzo Euro Mese]
)
```

### Prezzo Permute
**Description:** Prezzo di riferimento per le permute

```dax
// Il prezzo delle permute viene equiparato al Costo Medio Ponderato di acquisto
[CMP Acquisto]
```

### Importo Vendite
**Description:** Fatturato teorico calcolato come Qta x Prezzo Medio

```dax
// Calcolo teorico fatturato: Quantità Venduta x Prezzo Medio
[Qta Vendita] * [Prezzo Medio Vendita]
```

### Importo Vendite OLD2
**Description:** Misura legacy per calcolo vendite con switch logico

```dax
// Logica di switch per determinare la fonte del fatturato in base al gruppo prodotto
VAR Gruppo = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () )
VAR Categoria = SELECTEDVALUE ( DIM_GruppiVendita[CodiceCategoria], BLANK () )
RETURN
SWITCH (
TRUE (),
Gruppo = "MIX", [Importo Clienti Vendite],
Gruppo = "PROPANO",
SWITCH (
TRUE (),
Categoria = "DIRETTE", [Importo Clienti Vendite],
Categoria = "PASSAGGIO", [Importo Clienti Passaggi],
BLANK ()
),
BLANK ()
)
```

### Prezzo Medio Vendita (CG)
**Description:** Prezzo medio unitario derivato dai dati CG

```dax
// Calcola il prezzo medio unitario basandosi sui ricavi di Contabilità Generale
DIVIDE ( [Importo Vendite (CG)], [Qta Vendite], 0 )
```

### Qta Vendite LY
**Description:** Quantità venduta anno precedente

```dax
// Quantità venduta nello stesso periodo dell'anno precedente
CALCULATE ( [Qta Vendite], DATEADD ( DIM_Calendario[Date], -1, YEAR ) )
```

### Prezzo Medio Vendita QTD
**Description:** Prezzo medio vendita QTD

```dax
// Media del prezzo di vendita accumulata nel trimestre (Quarter-To-Date)
TOTALQTD ( [Prezzo Medio Vendita], DIM_Calendario[Date] )
```

### Costo Venduto (Doc)
**Description:** Costo del venduto basato su documenti e CMP

```dax
// Valorizzazione del venduto basata su documenti: Qta Doc x CMP
VAR QtaDoc = [Qta Doc Vendita Articolo]
VAR CMP = [CMP Acquisto]
RETURN
QtaDoc * CMP
```

### # Clienti
**Description:** Numero totale di clienti distinti

```dax
// Conteggio univoco dei clienti che hanno documenti di vendita
DISTINCTCOUNT('FACT_DocumentoVendita'[CodiceClienteFatturazione])
```

### Importo Nuovi Clienti
**Description:** Importo vendite generato dai nuovi clienti

```dax
// Calcola il fatturato generato esclusivamente dai nuovi clienti (definizione N giorni)
VAR nr_giorni = SELECTEDVALUE(PARAM_NrGiorni[PARAM_NrGiorni], 90)
VAR Tab_Clienti_Attuali = VALUES ( 'FACT_DocumentoVendita'[CodiceClienteFatturazione] )

VAR Clienti_Storici =
CALCULATETABLE (
VALUES ( 'FACT_DocumentoVendita'[CodiceClienteFatturazione]  ),
FILTER (
ALL ( DIM_Calendario[Date] ),
DIM_Calendario[Date] > MIN ( DIM_Calendario[Date] ) - nr_giorni &&
DIM_Calendario[Date] < MIN ( DIM_Calendario[Date] )
)
)
VAR Tab_Nuovi = EXCEPT ( Tab_Clienti_Attuali, Clienti_Storici )

RETURN
CALCULATE(
[Importo Vendita],
Tab_Nuovi
)
```

### % Importo Nuovi Clienti
**Description:** Percentuale di fatturato da nuovi clienti

```dax
// Incidenza percentuale del fatturato dei nuovi clienti sul totale
DIVIDE([Importo Nuovi Clienti], [Importo Vendita], 0)
```

### % Nuovi Clienti
**Description:** Percentuale di nuovi clienti sul totale

```dax
// Incidenza percentuale del numero di nuovi clienti sul totale clienti
DIVIDE([# Nuovi Clienti], [# Clienti], 0)
```

### Importo Vendite (CMP)
**Description:** Fatturato valorizzato al CMP di giacenza

```dax
// Valorizzazione delle vendite al costo di giacenza (CMP)
[Qta Vendita] * [CMP Giacenza]
```

## KPI_VenditeDocumento

### Importo Doc Vendita
**Description:** Importo lordo da documenti di vendita

```dax
// Somma totale degli importi lordi presenti nei documenti di vendita
SUMX ( 'FACT_DocumentoVendita', 'FACT_DocumentoVendita'[Importo] )
```

### Importo Articolo Doc Vendita
**Description:** Importo filtrato per righe di tipo Articolo

```dax
// Importo filtrato esclusivamente per le righe di tipo 'Articolo' (esclude spese, conti, etc.)
CALCULATE (
[Importo Doc Vendita],
'FACT_DocumentoVendita'[TipoRiga] = "Articolo"
)
```

### Importo FT Doc Vendita
**Description:** Importo totale fatture di vendita (FT VENDITA)

```dax
// Importo delle sole fatture di vendita (FT VENDITA) per righe articolo
CALCULATE (
[Importo Doc Vendita],
'FACT_DocumentoVendita'[TipoRiga] = "Articolo" &&
'FACT_DocumentoVendita'[TipoDocumento] = "FT VENDITA"
)
```

### Importo NC Doc Vendita
**Description:** Importo totale note di credito di vendita (NC VENDITA)

```dax
// Importo totale delle note di credito di vendita (NC VENDITA)
CALCULATE (
[Importo Doc Vendita],
'FACT_DocumentoVendita'[TipoDocumento] = "NC VENDITA"
)
```

### Importo Netto Doc Vendita
**Description:** Importo netto vendita (FT - Trasporto - NC)

```dax
// Fatturato netto calcolato come: Fatture - Trasporti - Note di Credito
[Importo FT Doc Vendita] - [Importo Trasporto Doc Vendita] - [Importo NC Doc Vendita]
```

### Importo Costo Prodotto Doc Vendita
**Description:** Importo del costo del prodotto basato sulla quantità e costo unitario

```dax
// Valorizzazione del costo prodotto: Costo unitario x Quantità documenti
[Costo Prodotto] * [Qta Doc Vendita Articolo]
```

### Importo Margine Doc Vendita
**Description:** Importo del margine calcolato su quantità e margine per tonnellata

```dax
// Margine totale calcolato come: Margine per Ton x Quantità documenti
[Margine Ton Doc Vendita] * [Qta Doc Vendita Articolo]
```

### Importo FT PASSAGGIO Doc Vendita
**Description:** Importo fatture per movimenti di passaggio

```dax
// Importo delle fatture di passaggio (TipoRiga = Conto) ignorando i filtri sugli articoli
CALCULATE (
[Importo Doc Vendita],
REMOVEFILTERS ( DIM_Articoli ),
'FACT_DocumentoVendita'[TipoRiga] = "Conto",
'FACT_DocumentoVendita'[TipoDocumento] = "FT VENDITA"
)
```

### Importo NC PASSAGGIO Doc Vendita
**Description:** Importo note di credito per movimenti di passaggio

```dax
// Importo delle note di credito per i movimenti di passaggio
CALCULATE (
[Importo Doc Vendita],
'FACT_DocumentoVendita'[TipoRiga] = "Conto" &&
'FACT_DocumentoVendita'[TipoDocumento] = "NC VENDITA"
)
```

### Importo Netto PASSAGGIO Doc Vendita
**Description:** Importo netto per movimenti di passaggio

```dax
// Fatturato netto dei passaggi: Fatture - Note di Credito
[Importo FT PASSAGGIO Doc Vendita] - [Importo NC PASSAGGIO Doc Vendita]
```

### Importo Netto FILTER Doc Vendita
**Description:** Importo netto filtrato dinamicamente tra Passaggi e Vendite Dirette

```dax
// Switch dinamico dell'importo netto in base al gruppo vendita selezionato (PASSAGGIO vs DIRETTI)
IF (
SELECTEDVALUE ( DIM_GruppiVendita[Gruppo] ) = "PASSAGGIO",
[Importo Netto PASSAGGIO Doc Vendita],
[Importo Netto Doc Vendita]
)
```

### Importo Controllo (Doc - CG)
**Description:** Differenza tra importo da documenti e importo da contabilità generale

```dax
// Delta di controllo tra il fatturato calcolato dai documenti e quello da Contabilità Generale
KPI_Vendite[Importo Vendite] - KPI_Vendite[Importo Vendite (CG)]
```

### Importo Trasporto Doc Vendita
**Description:** Importo totale dei costi di trasporto da documenti

```dax
// Somma dei costi di trasporto esplicitati nelle righe dei documenti di vendita
SUMX ( 'FACT_DocumentoVendita', 'FACT_DocumentoVendita'[CostoTrasporto] )
```

### Importo Doc Vendita - Trasporto
**Description:** Importo lordo documenti al netto del trasporto

```dax
// Importo lordo dei documenti depurato dai costi di trasporto
[Importo Doc Vendita] - [Importo Trasporto Doc Vendita]
```

### Importo Vendita
**Description:** Importo vendita principale (netto documenti)

```dax
// Alias per l'importo netto da documenti di vendita
[Importo Netto Doc Vendita]
```

### Importo Acquisto Cliente
**Description:** Importo stimato di acquisto per il cliente basato sul CMP

```dax
// Stima del costo di acquisto per il volume venduto al cliente (Qta x CMP)
[Qta Vendita] * [CMP Acquisto]
```

### Importo Vendita %
**Description:** Percentuale dell'importo vendita del cliente sul totale

```dax
// Incidenza percentuale delle vendite del cliente corrente sul totale vendite del periodo
VAR VenditeCliente = [Importo Vendita]
VAR TotaleVendite =
CALCULATE (
[Importo Vendita],
REMOVEFILTERS ( DIM_Clienti[Nome] )
)
RETURN
DIVIDE ( VenditeCliente, TotaleVendite, 0 )
```

### Importo Vendita N DAYS
**Description:** Importo vendita riferito agli ultimi N giorni (default 90)

```dax
// Calcola l'importo delle vendite riferito a una finestra temporale di N giorni (default 90)
VAR NrOfDays = 90
VAR Risultato =
CALCULATE(
[Importo Vendita],
DATEADD(DIM_Calendario[Date], -NrOfDays, DAY)
)
RETURN
Risultato
```

### Importo Vendita IPEM N DAYS
**Description:** Importo vendita deposito IPEM negli ultimi N giorni

```dax
// Calcola le vendite del deposito IPEM riferite a una finestra di N giorni
VAR NrOfDays = 90
VAR ImportoVenditaIPEM =
CALCULATE(
[Importo Vendita],
'FACT_DocumentoVendita'[CodiceDeposito] = "IPEM"
)

VAR Risultato =
CALCULATE(
ImportoVenditaIPEM,
DATEADD(DIM_Calendario[Date], -NrOfDays, DAY)
)
RETURN
Risultato
```

### Qta Doc Vendita Articolo
**Description:** Quantità venduta per righe di tipo Articolo

```dax
// Quantità totale per le sole righe di tipo 'Articolo'
CALCULATE (
[Qta Doc Vendita],
'FACT_DocumentoVendita'[TipoRiga] = "Articolo"
)
```

### Qta Doc Vendita Cliente
**Description:** Quantità venduta filtrata per il cliente selezionato

```dax
// Quantità venduta specifica per il cliente nel contesto corrente
CALCULATE (
[Qta Doc Vendita Articolo],
DIM_Clienti[CodiceCliente] = SELECTEDVALUE ( DIM_Clienti[CodiceCliente] )
)
```

### Qta Doc Vendita
**Description:** Quantità totale da documenti di vendita

```dax
// Somma totale delle quantità presenti nei documenti di vendita
SUMX ( 'FACT_DocumentoVendita', 'FACT_DocumentoVendita'[Quantity] )
```

### Qta Doc Vendita IPEM
**Description:** Quantità venduta da deposito IPEM

```dax
// Quantità venduta dal deposito IPEM per le righe articolo
CALCULATE (
[Qta Doc Vendita Articolo],
'FACT_DocumentoVendita'[CodiceDeposito] = "IPEM"
)
```

### Qta Doc Vendita FT
**Description:** Quantità totale fatture di vendita

```dax
// Quantità totale caricata nelle fatture di vendita
CALCULATE (
[Qta Doc Vendita Articolo],
'FACT_DocumentoVendita'[TipoDocumento] = "FT VENDITA"
)
```

### Qta Doc Vendita NC
**Description:** Quantità totale note di credito di vendita

```dax
// Quantità totale stornata nelle note di credito di vendita
CALCULATE (
[Qta Doc Vendita],
'FACT_DocumentoVendita'[TipoDocumento] = "NC VENDITA"
)
```

### Qta Doc Vendita Netta
**Description:** Quantità netta venduta (FT - NC)

```dax
// Differenza tra quantità fatturata e quantità stornata (FT - NC)
[Qta Doc Vendita FT] - [Qta Doc Vendita NC]
```

### Qta Doc Vendita Gruppo Articolo
**Description:** Quantità venduta per gruppo registrazione prodotto

```dax
// Quantità venduta filtrata per gruppo registrazione prodotto (MIX/PROPANO)
VAR Gruppo = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto] )
RETURN
IF(Gruppo <> BLANK(),
CALCULATE (
[Qta Doc Vendita],
'FACT_DocumentoVendita'[GruppoRegistrazioneProdotto] = Gruppo
),
0
)
```

### Qta Vendita
**Description:** Misura principale per la quantità venduta

```dax
// Misura principale per la quantità venduta (netta FT - NC)
[Qta Doc Vendita Netta]
```

### Qta Vendita ALL
**Description:** Quantità totale venduta (senza filtri)

```dax
// Quantità totale venduta ignorando tutti i filtri contestuali sulla tabella documenti
SUMX ( ALL ( 'FACT_DocumentoVendita' ), [Qta Vendita] )
```

### Qta Doc Vendita 3000002
**Description:** Quantità venduta per l'articolo specifico 3000002

```dax
// Quantità venduta specificamente per l'articolo 3000002 in fattura
CALCULATE (
[Qta Doc Vendita],
'FACT_DocumentoVendita'[CodiceArticolo] = "3000002" &&
'FACT_DocumentoVendita'[TipoDocumento] = "FT VENDITA"
)
```

### Qta Vendita AVG YTD Monthly
**Description:** Media mensile della quantità venduta YTD

```dax
// Media della quantità venduta giornaliera calcolata sul periodo YTD
CALCULATE(
[Qta Vendita AVG Day],
ALL(DIM_Calendario),
DIM_Calendario[MonthInCalendar] <= MAX(DIM_Calendario[MonthInCalendar]) &&
DIM_Calendario[Year] = MAX(DIM_Calendario[Year])
)
```

### Qta Vendita IPEM
**Description:** Quantità venduta da deposito IPEM (misura base)

```dax
// Quantità venduta netta dal deposito IPEM
CALCULATE(
[Qta Vendita],
'FACT_DocumentoVendita'[CodiceDeposito] = "IPEM"
)
```

### Qta Vendita Media Pesata
**Description:** Quantità media pesata sulle vendite mensili

```dax
// Calcola la quantità media pesando i mesi in base al loro volume rispetto all'anno
VAR QtaAnno =
CALCULATE(
[Qta Vendita],
ALL(DIM_Calendario[MonthName], DIM_Calendario[MonthOfYear])
)
VAR TabellaMesi =
ADDCOLUMNS(
SUMMARIZE(
'FACT_DocumentoVendita',
DIM_Calendario[Year],
DIM_Calendario[MonthName]
),
"Qta_Mese", [Qta Vendita],
"Peso", DIVIDE([Qta Vendita], QtaAnno, 0)
)
RETURN
SUMX(
TabellaMesi,
[Peso] * [Qta_Mese]
)
```

### Qta Vendita Cliente CUM
**Description:** Quantità cumulata per classifica clienti

```dax
// Calcola il totale cumulato della quantità venduta seguendo il ranking dei clienti
VAR ClienteRank =
RANKX(
ALL(DIM_Clienti[Nome & Codice]),
[Qta Vendita],,
DESC,
Dense
)
VAR TotaleCumulato =
CALCULATE(
[Qta Vendita],
FILTER(
ALL(DIM_Clienti[Nome & Codice]),
ClienteRank >= RANKX(
ALL(DIM_Clienti[Nome & Codice]),
[Qta Vendita],,
DESC,
Dense
)
)
)
RETURN
IF( [Qta Vendita] <> BLANK(), TotaleCumulato )
```

### Importo Netto Doc Vendita LM CUM
**Description:** Importo netto mese precedente cumulato

```dax
// Importo netto del mese precedente (LM) accumulato nel tempo
CALCULATE (
[Importo Netto Doc Vendita LM],
FILTER (
ALLSELECTED ( DIM_Calendario ),
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
)
```

### Importo Netto Doc Vendita -2M CUM
**Description:** Importo netto 2 mesi fa cumulato

```dax
// Importo netto di due mesi fa accumulato nel tempo
CALCULATE (
[Importo Netto Doc Vendita -2M],
FILTER (
ALLSELECTED ( DIM_Calendario ),
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
)
```

### Importo Vendite CY-LY
**Description:** Differenza importo vendite tra anno corrente e precedente

```dax
// Variazione assoluta del fatturato netto tra l'anno corrente e l'anno precedente
[Importo Netto FILTER Doc Vendita] - CALCULATE([Importo Netto FILTER Doc Vendita], SAMEPERIODLASTYEAR(DIM_Calendario[Date]))
```

### Qta Vendita Forecast CUM
**Description:** Quantità forecast cumulata

```dax
// Somma progressiva della quantità di forecast
SUMX(
FILTER (
ALLSELECTED ( DIM_Calendario[Date] ),
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
),
[Qta Vendita Forecast]
)
```

### Qta Vendita Forecast MA 30D
**Description:** Media mobile 30 giorni per il forecast quantità

```dax
// Media mobile a 30 giorni per il forecast, calcolata solo sui giorni lavorativi (esclude weekend)
VAR GiornoSettimana = SELECTEDVALUE ( DIM_Calendario[DayOfWeekName] )
VAR IsWeekend = GiornoSettimana IN { "sabato", "domenica" }
RETURN
IF( ISBLANK([Qta Vendita]) && NOT(IsWeekend),
AVERAGEX (
DATESINPERIOD ( DIM_Calendario[Date], LASTDATE ( DIM_Calendario[Date] ), -30, DAY ),
[Qta Vendita]
),
BLANK ()
)
```

### Qta Vendita Forecast TOT
**Description:** Forecast totale quantità combinato

```dax
// Forecast totale che combina la media mobile 30gg applicata allo stesso periodo dell'anno precedente
IF (
ISBLANK ( [Qta Vendita] ),
CALCULATE (
[Qta Vendita Forecast MA 30D],
SAMEPERIODLASTYEAR ( DIM_Calendario[Date] )
),
BLANK ()
)
```

### Qta Vendita Forecast Remain
**Description:** Forecast rimanente dalla data dell'ultima vendita

```dax
// Calcola il forecast per il periodo residuo, partendo dall'ultima data di vendita registrata
VAR DataUltimaVendita = CALCULATE ( MAX ( 'FACT_DocumentoVendita'[DataSpedizione] ), REMOVEFILTERS () )
VAR ForecastResiduo =
CALCULATE (
[Qta Vendita Forecast],
KEEPFILTERS ( DIM_Calendario[Date] >= DataUltimaVendita )
)
RETURN
ForecastResiduo
```

### Qta Vendita & Forecast
**Description:** Combinazione di quantità venduta reale e forecast rimanente

```dax
// Totale quantità reale (consuntivo) + quantità forecast per il periodo residuo
[Qta Vendita] + [Qta Vendita Forecast Remain]
```

### Qta Vendita CUM vs Forecast CUM
**Description:** Differenza tra quantità cumulata reale e cumulata forecast

```dax
// Delta tra il totale cumulato reale e il totale cumulato previsto (forecast)
IF (
ISBLANK ( [Qta Vendita CUM] ),
BLANK (),
[Qta Vendita CUM] - [Qta Vendita Forecast CUM]
)
```

### Qta Vendita Forecast Remain CUM
**Description:** Forecast rimanente cumulato

```dax
// Somma progressiva del forecast rimanente
CALCULATE (
[Qta Vendita Forecast Remain],
FILTER (
ALLSELECTED ( DIM_Calendario[Date] ),
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
)
```

### Qta Vendita Forecast Remain Mediana
**Description:** Mediana del forecast rimanente

```dax
// Mediana del forecast rimanente nel contesto calendario
MEDIANX ( DIM_Calendario, [Qta Vendita Forecast Remain] )
```

### Regression Line
**Description:** Retta di regressione lineare sulle vendite cumulate

```dax
// Calcola i punti della retta di regressione lineare (Y = a + bX) per la quantità cumulata
VAR TabellaDati =
FILTER (
SELECTCOLUMNS (
ALLSELECTED ( DIM_Calendario ),
"x_val", DIM_Calendario[Date],
"y_val", [Qta Vendita CUM]
),
NOT ( ISBLANK ( [x_val] ) ) && NOT ( ISBLANK ( [y_val] ) )
)
VAR SumY = SUMX ( TabellaDati, [y_val] )
VAR SumX = SUMX ( TabellaDati, [x_val] )
VAR SumX2 = SUMX ( TabellaDati, [x_val] ^ 2 )
VAR SumXY = SUMX ( TabellaDati, [x_val] * [y_val] )
VAR N = COUNTROWS ( TabellaDati )

VAR Intercetta = DIVIDE ( ( SumY * SumX2 - SumX * SumXY ), ( N * SumX2 - ( SumX ) ^ 2 ), 0 )
VAR Pendenza = DIVIDE ( ( N * SumXY - SumX * SumY ), ( N * SumX2 - ( SumX ) ^ 2 ), 0 )

RETURN
SUMX ( DIM_Calendario, Pendenza * DIM_Calendario[Date] + Intercetta )
```

### Regression Slope
**Description:** Pendenza della retta di regressione (velocità di vendita)

```dax
// Calcola solo la pendenza (coefficiente angolare) della retta di regressione lineare
VAR TabellaDati =
FILTER (
SELECTCOLUMNS (
ALLSELECTED ( DIM_Calendario ),
"x_val", DIM_Calendario[Date],
"y_val", [Qta Vendita CUM]
),
NOT ( ISBLANK ( [x_val] ) ) && NOT ( ISBLANK ( [y_val] ) )
)
VAR SumY = SUMX ( TabellaDati, [y_val] )
VAR SumX = SUMX ( TabellaDati, [x_val] )
VAR SumX2 = SUMX ( TabellaDati, [x_val] ^ 2 )
VAR SumXY = SUMX ( TabellaDati, [x_val] * [y_val] )
VAR N = COUNTROWS ( TabellaDati )

VAR Pendenza = DIVIDE ( ( N * SumXY - SumX * SumY ), ( N * SumX2 - ( SumX ) ^ 2 ), 0 )
RETURN
Pendenza
```

### Qta Vendita ToDo
**Description:** Quantità ancora da vendere per raggiungere l'obiettivo

```dax
// Calcola la quantità mancante per raggiungere l'obiettivo di vendita fissato
VAR Differenza = [Valore Obiettivo Vendite] - [Qta Vendita ALL]
RETURN
IF(Differenza >= 0, Differenza, 0)
```

### Giorni Vendita x Obiettivo
**Description:** Stima dei giorni necessari per raggiungere l'obiettivo

```dax
// Stima il numero di giorni necessari a raggiungere l'obiettivo dividendo il ToDo per la pendenza di regressione
VAR GiorniStimati = DIVIDE ( [Qta Vendita ToDo], [Regression Slope], 0 )
RETURN
IF( GiorniStimati >= 0, GiorniStimati, 0 )
```

### Data Obiettivo Vendita
**Description:** Data prevista per il raggiungimento dell'obiettivo di vendita

```dax
// Proiezione della data di raggiungimento obiettivo aggiungendo i giorni stimati ad oggi
TODAY() + [Giorni Vendita x Obiettivo]
```

### Importo Vendita AVG N Days LQ
**Description:** Media importo vendita N giorni, riferita al trimestre precedente

```dax
// Media dell'importo vendita negli ultimi N giorni, riferita al trimestre precedente (Last Quarter)
CALCULATE (
[Importo Vendita AVG N Days],
DATEADD ( 'FACT_DocumentoVendita'[DataRegistrazione], -1, QUARTER )
)
```

### Qta Vendita Forecast
**Description:** Forecast quantità basato su medie storiche annuali

```dax
// Forecast quantità basato sulla media storica mensile degli anni passati (fino ad oggi)
VAR PrimoAnno = VALUE(MIN(DIM_Calendario[YEAR]))
VAR TabellaStorica =
FILTER(
SUMMARIZE(
DIM_Calendario,
DIM_Calendario[Year],
DIM_Calendario[MonthName],
"Qta_Vendite", [Qta Vendita]
),
VALUE(DIM_Calendario[Year]) >= PrimoAnno && VALUE(DIM_Calendario[Year]) <= YEAR(TODAY())
)

RETURN
AVERAGEX(TabellaStorica, [Qta_Vendite])
```

### Qta Vendita Forecast Mediana
**Description:** Forecast quantità basato su mediana storica

```dax
// Forecast quantità basato sulla mediana storica mensile degli anni passati (escludendo i mesi a zero)
VAR PrimoAnno = VALUE(MIN(DIM_Calendario[YEAR]))
VAR TabellaStorica =
FILTER(
SUMMARIZE(
DIM_Calendario,
DIM_Calendario[Year],
DIM_Calendario[MonthName],
"Qta_Vendite", [Qta Vendita]
),
VALUE(DIM_Calendario[Year]) >= PrimoAnno &&
VALUE(DIM_Calendario[Year]) <= YEAR(TODAY()) &&
[Qta Vendita] > 0
)

RETURN
MEDIANX(TabellaStorica, [Qta_Vendite])
```

### Prezzo Netto Doc Vendita OLD
**Description:** Prezzo netto da documenti (versione precedente)

```dax
// Calcolo legacy del prezzo netto unitario: Importo Netto / Quantità Articolo
DIVIDE ( [Importo Netto FILTER Doc Vendita], [Qta Doc Vendita Articolo], 0 )
```

### Costo Prodotto
**Description:** Calcolo del costo prodotto per cliente e anno

```dax
// Calcola il costo prodotto aggregato per cliente e anno confrontando vendite documenti e costi CG
VAR CodiceCliente = SELECTEDVALUE ( DIM_Clienti[CodiceCliente] )
VAR AnnoFiltro = SELECTEDVALUE ( DIM_Calendario[Year] )
VAR QtaCliente =
CALCULATE (
[Qta Doc Vendita Articolo],
'FACT_DocumentoVendita'[CodiceClienteFatturazione] = CodiceCliente &&
YEAR ( 'FACT_DocumentoVendita'[DataSpedizione] ) = VALUE ( AnnoFiltro )
)
VAR CostoTotaleGPL =
CALCULATE (
[COSTO GPL],
YEAR ( FACT_MovimentiCG[DataRegistrazione] ) = VALUE ( AnnoFiltro )
)
RETURN
QtaCliente & "_" & CostoTotaleGPL
```

### Costo Prodotto 2
**Description:** Costo prodotto specifico per cliente C00033

```dax
// Costo prodotto filtrato specificamente per il cliente C00033
CALCULATE ( [Costo Prodotto], DIM_Clienti[CodiceCliente] = "C00033" )
```

### % Importo Margine Doc Vendita
**Description:** Percentuale del margine sull'importo netto da documenti

```dax
// Incidenza percentuale del margine sull'importo netto dei documenti
DIVIDE ( [Importo Margine Doc Vendita], [Importo Netto Doc Vendita], 0 )
```

### Margine Ton Doc Vendita
**Description:** Margine per tonnellata da documenti (Prezzo - CMP)

```dax
// Margine unitario per tonnellata: Prezzo Netto - CMP Acquisto
[Prezzo Netto Doc Vendita OLD] - [CMP Acquisto]
```

### Prezzo Netto Doc Vendita
**Description:** Prezzo netto unitario da documenti

```dax
// Prezzo netto unitario: Importo Netto / Quantità Fatturata
DIVIDE ( [Importo Netto FILTER Doc Vendita], [Qta Doc Vendita FT], 0 )
```

### Prezzo Trasporto Doc Vendita
**Description:** Prezzo medio di trasporto da documenti

```dax
// Media dei costi di trasporto unitari registrati nelle righe articolo dei documenti
CALCULATE (
AVERAGEX ( 'FACT_DocumentoVendita', 'FACT_DocumentoVendita'[CostoTrasporto] ),
'FACT_DocumentoVendita'[TipoRiga] = "Articolo"
)
```

### Prezzo Doc Vendita - Trasporto
**Description:** Prezzo al netto del trasporto

```dax
// Prezzo unitario al netto del trasporto: (Importo - Trasporto) / Qta Gruppo Articolo
DIVIDE (
[Importo Doc Vendita - Trasporto],
[Qta Doc Vendita Gruppo Articolo],
0
)
```

### Prezzo Vendita
**Description:** Prezzo vendita medio per categorie principali

```dax
// Calcola il prezzo medio di vendita filtrando per le categorie principali di ricavo
CALCULATE(
DIVIDE([Importo Vendita], [Qta Vendita], 0),
'FACT_DocumentoVendita'[CodiceCategoria] IN {"NAZ", "UE", "NAZPERM"}
)
```

### Qta Vendita Forecast Media 2
**Description:** Media del forecast quantità sull'intero calendario

```dax
// Media complessiva del forecast quantità
AVERAGEX(DIM_Calendario, [Qta Vendita Forecast])
```

### Qta Vendita Forecast NEW
**Description:** Forecast quantità basato su CAGR (Compound Annual Growth Rate)

```dax
// Forecast quantità basato sulla proiezione CAGR (Compound Annual Growth Rate) storica
VAR AnnoCorrente = SELECTEDVALUE(DIM_Calendario[Year])
VAR PrimoAnno = MIN(DIM_Calendario[Year])
VAR UltimoAnno = MAX(DIM_Calendario[Year])
VAR NrAnniProiezione = AnnoCorrente - UltimoAnno

VAR QtaUltimoAnno = CALCULATE([Qta Vendita], DIM_Calendario[Year] = UltimoAnno)
VAR QtaPrimoAnno = CALCULATE([Qta Vendita], DIM_Calendario[Year] = PrimoAnno)

VAR CAGR = POWER(
DIVIDE(QtaUltimoAnno, QtaPrimoAnno),
DIVIDE(1, UltimoAnno - PrimoAnno)
) - 1

VAR ForecastCAGR = QtaUltimoAnno * POWER((1 + CAGR), NrAnniProiezione)

RETURN
IF( AnnoCorrente > UltimoAnno, ForecastCAGR )
```

### Qta Vendita Data Reg
**Description:** Quantità venduta riferita alla Data Registrazione (relazione inattiva)

```dax
// Forza il calcolo delle quantità utilizzando la relazione inattiva con DataRegistrazione
CALCULATE(
[Qta Vendita],
USERELATIONSHIP(DIM_Calendario[Date], 'FACT_DocumentoVendita'[DataRegistrazione])
)
```

### Qta Vendita Forecast 3Y
**Description:** Forecast quantità basato sulla media degli ultimi 3 anni

```dax
// Forecast semplificato basato sulla media delle quantità degli ultimi 3 anni (LY, 2LY, 3LY)
DIVIDE([Qta Vendita LY] + [Qta Vendita 2LY] + [Qta Vendita 3LY], 3, 0)
```

### Qta Vendita Forecast 3Y CUM
**Description:** Forecast 3 anni cumulato

```dax
// Somma progressiva del forecast 3 anni
CALCULATE (
[Qta Vendita Forecast 3Y],
FILTER (
ALLSELECTED ( DIM_Calendario[Date] ),
DIM_Calendario[Date] <= MAX ( DIM_Calendario[Date] )
)
)
```

### Qta Vendita NEW
**Description:** Nuova misura quantità per test star schema

```dax
// Nuova misura di quantità per test architettura Star Schema (mappa articoli su MIX e PROPANO)
VAR GruppoProdotto = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () )

VAR QtaMix = CALCULATE(
SUMX('FACT_Vendite', 'FACT_Vendite'[Quantity]),
'FACT_Vendite'[CodiceArticolo] IN {"1", "1T"}
)

VAR QtaPropano = CALCULATE(
SUMX('FACT_Vendite', 'FACT_Vendite'[Quantity]),
'FACT_Vendite'[CodiceArticolo] IN {"2", "2T"}
)

RETURN
SWITCH (
TRUE (),
GruppoProdotto = "MIX", QtaMix,
GruppoProdotto = "PROPANO", QtaPropano,
QtaMix + QtaPropano
)
```

### Bar
**Description:** Base per grafico Target vs Actual

```dax
// Restituisce il valore minimo tra il reale e il forecast (utilizzata per visualizzazione grafici target)
MIN([Importo Vendita], [Importo Vendita Forecast])
```

### Importo Vendita Forecast
**Description:** Forecast importo vendita basato su medie storiche

```dax
// Forecast del fatturato basato sulla media storica mensile degli anni passati
VAR PrimoAnno = VALUE(MIN(DIM_Calendario[YEAR]))
VAR TabellaStorica =
FILTER(
SUMMARIZE(
DIM_Calendario,
DIM_Calendario[Year],
DIM_Calendario[MonthName],
"Importo_Vendite", [Importo Vendita]
),
VALUE(DIM_Calendario[Year]) >= PrimoAnno && VALUE(DIM_Calendario[Year]) <= YEAR(TODAY())
)

VAR MediaStorica = AVERAGEX(TabellaStorica, [Importo_Vendite])
RETURN
IF( MediaStorica <> BLANK(), MediaStorica, 0 )
```

### Unmet Bar
**Description:** Quota mancante per raggiungere il target (grafico)

```dax
// Calcola la quota di target non ancora raggiunta per la visualizzazione a barre
VAR Sales = [Importo Vendita]
VAR Target = [Importo Vendita Forecast]
VAR Marker = [Marker Value]
VAR Base = [Bar]
RETURN
IF( Target > Sales, Marker - Base )
```

### Met Bar
**Description:** Quota raggiunta del target (grafico)

```dax
// Calcola la quota di target superata per la visualizzazione a barre
VAR Sales = [Importo Vendita]
VAR Target = [Importo Vendita Forecast]
VAR Marker = [Marker Value]
VAR Base = [Bar]
RETURN
IF( Sales >= Target, Marker - Base )
```

### Marker Value
**Description:** Valore massimo tra vendita e target (per marker grafico)

```dax
// Valore massimo tra il consuntivo e il target per definire il limite del marker nel grafico
MAX([Importo Vendita], [Importo Vendita Forecast])
```

### Qta Vendita PREV
**Description:** Quantità prevista tramite LINEST

```dax
// Proiezione della quantità venduta utilizzando i coefficienti Slope e Intercept calcolati via LINEST
SUM(LinestResult[Intercept]) + SUM(LinestResult[Slope1]) * SUM('FACT_Vendite'[Date])
```

### Qta Vendita CONTINUA
**Description:** Quantità venduta continua (riempie i vuoti con la media)

```dax
// Quantità venduta che riempie i valori nulli (gap) con la media mensile (utile per analisi di trend)
IF(ISBLANK([Qta Vendita]), [Qta Vendita AVG Month], [Qta Vendita])
```

### Qta Vendita AVG Month
**Description:** Media mensile della quantità venduta

```dax
// Media semplice delle quantità vendute aggregate per mese e anno
AVERAGEX ( VALUES(DIM_Calendario[MonthnYear]), [Qta Vendita] )
```

### Diff Actual/Previous
**Description:** Differenza tra valore attuale e periodo precedente

```dax
// Calcola la variazione tra il valore della misura selezionata e lo stesso valore nel periodo precedente
[Value Previous] - SELECTEDMEASURE()
```

### Qta Vendita Prodotto
**Description:** Quantità venduta per prodotto con logica di switch

```dax
// Calcola la quantità venduta totale applicando uno switch logico tra i prodotti (PROPANO/MIX)
VAR GruppoProdotto = SELECTEDVALUE ( DIM_Articoli[GruppoProdotto], BLANK () )

VAR QtaPropano = [Qta Vendita]
VAR QtaMix = [Qta Doc Vendita IPEM]
VAR QtaTotale = QtaPropano + QtaMix

RETURN
SWITCH (
TRUE (),
GruppoProdotto = "PROPANO", QtaPropano,
GruppoProdotto = "MIX", QtaMix,
QtaTotale
)
```

## PARAM_NrGiorni

### Valore PARAM_NrGiorni
```dax
SELECTEDVALUE('PARAM_NrGiorni'[PARAM_NrGiorni], 90)
```

## PARAM_TimeRange

### PARAM_ValoreTimeRange
```dax
SELECTEDVALUE('PARAM_TimeRange'[PARAM_TimeRange], 3)
```
