12.0.0.3.72 (2022-07-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set correct parent id for accrual generation / Impostato il parent id corretto per ratei e risconti

12.0.0.3.71 (2022-04-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Print customers suppliers pdf / Stampa clienti fornitori pdf

12.0.0.3.70 (2022-04-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Print order report / Ordine di stampa

12.0.0.3.69 (2022-04-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fixed report pdf of opposite balance / Corretto layout di stampa del bilancio a conti contrapposti

12.0.0.3.68 (2022-02-25)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Sometimes record not found / Errore record non trovato in alcuni casi

12.0.0.3.67 (2021-11-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Line order print / Ordine di stampa
* [FIX] Print account w/o group too / Stampa anche conti senza gruppo
* [FIX] Date range selection / Selezione intervallo date
* [IMP] Print blank when code does not exist / Non stampa codici inesistenti
* [IMP] Print by competence or VAT date / Stampa per data competenza o data IVA

12.0.0.3.66 (2021-10-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto calcolo competenze flag

12.0.0.3.65 (2021-10-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-398: wrong earning balance / errato utile o perdita da esercizio precedente
* [IMP] POW-483: balance based on groups / bilancio basato su gruppi contabili

12.0.0.3.64 (2021-10-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto controllo per identificazione anno fiscale associato al bilancio

12.0.0.2.63 (2021-09-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] date_from = fy.date_from if no opening balance /data iniz. = data anno fiscale se saldi iniziali

12.0.0.2.62 (2021-05-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-158: calcolo ratei e risconti pluriennale
* [IMP] Importo consolidato (già calcolato in anni precedenti)
* [IMP] Riga ratei e risconti con totale fattura e importo consolidato

12.0.0.2.61 (2021-04-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] verifica esistenza della data competenza bilancio in creazione fattura

12.0.0.2.59 (2021-03-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] inserito campo data competenza bilancio nella registrazione contabile

12.0.0.2.58 (2021-03-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] inserito campo fattura data competenza bilancio

12.0.0.2.57 (2020-09-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] aggiornato typo nel nome del file di configurazione spreadsheet

12.0.0.2.56 (2020-09-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-153 - calcolo importi ratei/risconti
* [FIX] AXI-154 - crash

12.0.0.2.55 (2020-09-24)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-153 - calcolo importi ratei/risconti
* [FIX] AXI-154 - crash

12.0.0.2.54 (2020-09-24)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Refactor
* [FIX] AXI-136 - ordinamento righe bilancio a conti contrapposti
* [FIX] AXI-128 - inversione di segno caso 'sempre'
* [FIX] AXI-129 - inversione di segno caso 'se richiesto'

12.0.0.2.53 (2020-09-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Calcolo utile

12.0.0.2.52 (2020-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] travis - verifica

12.0.0.2.51 (2020-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-136 - ordinamento righe bilancio a conti contrapposti
* [FIX] AXI-128 - inversione di segno caso 'sempre'
* [FIX] AXI-129 - inversione di segno caso 'se richiesto'

12.0.0.2.50 (2020-08-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] AXI-109 - Aggiornato menu

12.0.0.2.49 (2020-08-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-108 - Rimosso vincolo su flag ecslusi conti iniziali

12.0.0.2.48 (2020-08-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-115 - Aggiornato ordinamento sul codice conto

12.0.0.2.47 (2020-08-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-55 / AXI-104 - Cambiato tipo di campo per inversione di segno

12.0.0.2.46 (2020-08-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-17 - Download immediato file xls per bilancio ordinario e di verifica

12.0.0.2.45 (2020-08-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-17 - Aggiornato larghezza colonne per bilancio a conti contrapposti

12.0.0.2.44 (2020-08-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-17 - Aggiornato formato numerico e allineamenti

12.0.0.2.43 (2020-07-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-90 - Indicato periodo e non anno nelle proiezioni ratei/risconti


12.0.0.2.42 (2020-07-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-89 - Alcuni conti sono spostati tra attivo e passivo
* [FIX] AXI-103 - Gestione warning profilo contabile
