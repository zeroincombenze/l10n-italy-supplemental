12.0.2.6.32 (2021-06-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato flag copy a false per il campo 'Esercizio contabile'

12.0.2.6.31 (2021-06-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato metodo write per validazione massiva

12.0.2.6.30 (2021-05-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto il calcolo per l'indeducibilità della tasse

12.0.2.6.29 (2021-03-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Spostato campo data competenza bilancio della registrazione contabile

12.0.2.6.28 (2021-03-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Spostato campo data competenza bilancio

12.0.2.6.27 (2021-03-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Tolto controllo sulla data fattura

12.0.2.6.26 (2021-02-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Data bilancio (mov. no fattura ) da data contabile
* [IMP] Data bilancio (mov. fattura ) da data bilancio fattura

12.0.2.6.25 (2021-02-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Tolto controllo sulla data bilancio

12.0.2.6.24 (2021-01-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Controllo sulla data fattura per fatture e NC fornitore

12.0.2.6.23 (2020-12-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Sostituito campo _13 e aggiornato dipendenze

12.0.2.6.22 (2020-11-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Campo date_apply_vat spostato in l10n_it_statement

12.0.2.6.21 (2020-11-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato default per data fattura

12.0.2.6.20 (2020-11-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Visualizzazione quota indetraibile dell'IVA

12.0.2.6.19 (2020-11-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto algoritmo di calcolo riassunto IVA in fattura nel caso di imposte indetraibili (parzialmente o completamente)

12.0.2.6.18 (2020-11-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] avoided SQL query error with empty accrual dates while generating account briefs

12.0.2.6.17 (2020-10-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] update view id

12.0.2.6.16 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] spostato campo "fiscal_year_id" da modulo "l10n_it_validations" a "account_invoice_entry_dates"

12.0.2.6.15 (2020-09-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] disabled contraint on due_amount > 0 / Disabilitato il controllo sull'importo della riga

12.0.2.5.15 (2020-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] disabled contraint on due_amount > 0 / Disabilitato il controllo sull'importo della riga

12.0.2.4.15 (2020-08-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] modificato modulo per utilizzare il nuovo campo "type" di account.move

12.0.2.3.15 (2020-08-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] attivato calcolo automatico, "Scadenze", "Prima nota" e "Riepilogo IVA" alla creazione, prima lo faceva solo al write


12.0.2.2.15 (2020-08-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] ricalcolo automatico, "Scadenze", "Prima nota" e "Riepilogo IVA" al salvataggio
* [FIX] corretto nome di variabile scritto in modo errato
* [FIX] Righe di "Prima Nota" e "Riepilogo IVA" non sono più direttamente modificabili dall'utente

12.0.1.2.14 (2020-08-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Riabilitata visualizzazione campo journal_id nella vista account.move

12.0.1.2.13 (2020-08-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] inseriti controlli in create, write e post per evitare che la generazione e i controlli di due_dates, account_brief e vat_brief su registrazioni "non IVA"

12.0.1.1.13 (2020-08-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Duplicate journal_id / Registro duplicato


