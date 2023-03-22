12.0.1.9.29 (2023-02-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Validation error on self invoice in prior year / Errata segnalazione di errore per auto-fatture anno preceente

12.0.1.9.28 (2022-09-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Module dependency
* [FIX] Crash rc_self_invoice_id

12.0.1.9.27 (2022-09-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Avoid validation on date when reverse charge invoice self / Gestita validazione della data contabile se ha autofattura

12.0.1.9.27 (2022-07-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Avoid validation on date when reverse charge self from SDI / Gestita validazione della data contabile se autofattura dallo SDI

12.0.1.9.26 (2022-04-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] No set date=date_invoice if rev_charge / Non imposta date=date_invoice in RC

12.0.1.9.24 (2021-10-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimosso controllo data documento se non è fattura o nota di credito

12.0.1.9.24 (2021-06-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Verifica write con anno fiscale assente in validazione

12.0.1.8.23 (2021-03-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Verifica anno fiscale assente in validazione

12.0.1.8.21 (2021-03-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Gestione anno fiscale in write e create

12.0.1.8.20 (2021-03-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato controllo data di registrazione su tipo vendite

12.0.1.8.19 (2021-03-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato controllo data di registrazione su tipo vendite

12.0.1.8.18 (2021-03-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato controllo data fattura fornitore

12.0.1.8.17 (2021-02-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] No check data bilancio

12.0.1.8.16 (2021-02-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Update validation

12.0.1.8.15 (2020-12-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Sostituito campo con _13 e aggiornato dipendenze

12.0.1.8.14 (2020-11-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Campo date_apply_vat spostato in l10n_it_statement

12.0.1.8.13 (2020-11-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Removed checks in date invoice

12.0.1.8.12 (2020-10-27)
~~~~~~~~~~~~~~~~~~~~~~~~
* [FIX] Removed checks in account move

12.0.1.8.11 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~
* [MOD] spostato campo "fiscal_year_id" da modulo "l10n_it_validations" a "account_invoice_entry_dates"
* [FIX] No constraints se stato bozza o annullata

12.0.1.8.10 (2020-10-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] No constraints se stato bozza o annullata

12.0.1.8.9 (2020-09-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimosse definizioni dei campi e commentato controllo su termini di pagamento

12.0.1.8.8 (2020-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* Patch per validazione fatture: ATTENZIONE Da approfondire

12.0.1.8.8 (2020-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* Patch per validazione fatture: ATTENZIONE Da approfondire


12.0.1.8.7 (2020-09-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] AXI - 133 Account move lines mandatory / Avviso bloccante per registrazione senza linee


12.0.1.7.7 (2020-09-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI - 133 Account move lines mandatory / Avviso bloccante per registrazione senza linee


12.0.1.6.7 (2020-09-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Invoice date mandatory in view / Data fattura per clenti e fornitori viene resa obbligatoria sulla vista


12.0.1.6.6 (2020-09-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] modificate etichette dei campi data


12.0.0.6.5 (2020-08-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Invoice date mandatory for invoices and credit notes / Data fattura obbligatoria per fatture e note di credito

12.0.0.6.4 (2020-08-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] filter on journal / Filtro del registro sul tipo di movimento

12.0.0.6.3 (2020-08-25)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] check partner enabled / Verifica sul conto e messaggio di errore se manca il partner

12.0.0.5.3 (2020-08-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] type readonly if account.move has lines / Il campo type è reso readonly se ha almeno una registrazione

12.0.0.4.2 (2020-08-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-113 Gestito i default e il cambio del tipo

12.0.0.3.2 (2020-08-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Reso obbligatorio il campo "tipo" per account.move / Set field "type" as required for account.move

12.0.0.2.2 (2020-08-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Journal changed by type / Registro aggiornato da tipo documento


12.0.0.2.1 (2020-08-03)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added type file in account move / Aggiunto campo tipo in registrazione contabile
* [IMP] Date invoice naming 13.0
