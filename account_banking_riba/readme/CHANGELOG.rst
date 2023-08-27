12.0.6.5.34 (2023-07-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Payment move date on wallet bank / Data accettazione per conto portafoglio
* [QUA] Test coverage 66% (460: 155+305) [117 TestPoint]

12.0.6.5.33 (2023-05-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring: migrated from 10.0
* [QUA] Test coverage 65% (442: 154+288) [113 TestPoint]

12.0.6.5.32 (2023-05-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Payment confirmed / Errato conferma incasso effettuato

12.0.6.5.31 (2023-02-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Error "Accredito" with refunc / Errore "Accredito" se NC

12.0.6.5.30 (2023-01-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Confirm payment of refund / Conferma incasso note credito
* [FIX] Sometimes, after upload, payment order ha not button "Accredito" / Bottone "Accredito" a volte non appare dopo upload
* [TEST] Primo grupo di test automatico (coverage 37% 295/197)


12.0.6.5.29 (2023-01-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Commentata parte di codice che modificava il link tra payment_order_line e move_line durante la registrazione dell'incasso delle RiBa

12.0.5.5.29 (2023-01-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto nome chiave dizionario errato nella funziona di registrazione pagamento RiBa

12.0.3.5.26 (2022-12-05)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Gestione RIBA modo II (Giolo) - Versione identificabile

12.0.3.5.25 (2022-11-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Gestione RIBA modo II (Giolo)

12.0.3.5.24 (2022-10-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato flag incasso effettuato se il conto non è di portafoglio e il file viene generato

12.0.3.5.23 (2022-07-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretta dipendenza

12.0.3.5.22 (2022-03-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito bug importo  da riga scadenza in conferma pagamento

12.0.3.5.21 (2022-03-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito bug importo accredito da riga scadenza

12.0.3.5.20 (2022-03-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Gestito pagamento riba fornitori

12.0.3.5.19 (2022-02-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Gestito pregresso scadenze company bank non di portafoglio

12.0.3.5.18 (2022-02-24)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato accredito con metodo di selezione registro per spese bancarie

12.0.3.5.17 (2022-02-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring conferma pagamento

12.0.3.5.16 (2022-01-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring impostazione conti trasferiti nel registro

12.0.3.5.15 (2021-12-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestione viste conti

12.0.3.5.14 (2021-12-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestione conto di portafoglio in riba

12.0.3.5.13 (2021-07-20)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiunto partner su righe movimento contabili (account.move.line) che lo richiedono per consentire conferma registrazione

12.0.3.5.13 (2021-04-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato nella tab [Transfer journal entries] il riferimento a alla registrazione di accredito
* [FIX] Calcolo portafolgio

12.0.3.5.12 (2021-04-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato calcoli conti degli effetti

12.0.3.5.11 (2021-04-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato castelletto

12.0.3.4.10 (2021-02-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] No riferimento a data bilancio

12.0.3.4.9 (2021-02-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Nuova implementazione registrazione contabile di incasso effettivo Ri.Ba.

12.0.2.3.9 (2021-02-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring

12.0.2.3.8 (2021-02-01)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fix bug accredito

12.0.2.3.7 (2021-01-25)
~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring

12.0.2.3.5 (2021-01-07)
~~~~~~~~~~~~~~~~~~~~~~~

12.0.2.3.6 (2021-01-08)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] impostato metodo di accredito

12.0.2.3.5 (2021-01-07)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] modificata regola validazione codice SIA

12.0.2.2.5 (2021-01-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added dependency account_duedates module

12.0.0.2.1 (2020-12-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] CAB and ABI taken directly from IBAN code, sia code '00000' accepted

12.0.0.0.1 (2020-12-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] First release of the module: CBI files generation and SIA code settings are available
