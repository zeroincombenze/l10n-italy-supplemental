12.0.1.9.2 (2024-01-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Regression tests
* [IMP] Print down payment / Imporot acconto in stampa liquidazione
* [QUA] Test coverage 56% (685: 304+381) [14 TestPoints] - quality rating 37 (target 100)

12.0.1.9.1_2 (2021-12-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Inserito migrations per aggiornamento valori pregressi

12.0.1.9.1_1 (2021-12-24)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring campi per liquidazioine EU-OSS

12.0.1.9.1 (2021-10-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring campo date_apply_vat rimosso e spostato in modulo common

12.0.1.9.0 (2021-09-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Refactoring funzione di calcolo delle tasse (spostata in apposito modulo l10n_it_vat_common)

12.0.1.8.13 (2021-09-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimozione statement_credit_group_line da it.po perchè impediva caricamento della lingua IT

12.0.1.8.12 (2021-09-17)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato stampa liquidazione e fix bugs

12.0.1.8.11 (2021-09-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato filtro per i movimenti contabili dell'iva

12.0.1.8.10 (2021-09-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Inserito i totali nella visualizzazione e nella stampa

12.0.1.8.9 (2021-09-08)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto il comportamento con i codici iva di EU OSS

12.0.1.8.8 (2021-07-22)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato il model delle righe tasse di debito con campo deducibile

12.0.1.8.7 (2021-07-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato il model delle righe tasse di debito con campo deducibile

12.0.1.8.6 (2021-07-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato il template

12.0.1.8.5 (2021-07-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato il model delle righe tasse di debito con campo calcolato indeducibile

12.0.1.8.4 (2021-06-24)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato la stampa della liquidazione iva con gestione split payment

12.0.1.8.3 (2021-06-24)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato campo 'Apply for VAT date' con copy a false
* [IMP] Nell'elenco delle righe di debito iva sostituito il campo amount con amount deducibile calcolato

12.0.1.8.2 (2021-06-22)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto bug template stampa liquidazione

12.0.1.8.1 (2021-05-27)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto bug totali stampa liquidazione

12.0.1.6.7 (2021-05-18)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto bug registrazione della liquidazione

12.0.1.6.6 (2021-04-09)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto bug generazione stampa liquidazione

12.0.1.6.5 (2021-04-07)
~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Aggiornate dipendenze

12.0.1.6.4 (2021-03-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring gestione data competenza IVA


12.0.1.6.3 (2020-12-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-106 Data competenza IVA da data registrazione, se vuota


12.0.1.6.2 (2020-12-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-92 Corretto errore calcolo liquidazione IVA per data competenze


12.0.1.6.1 (2020-11-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Inserita la verifica sulla data fattura e la data di applicazione iva
