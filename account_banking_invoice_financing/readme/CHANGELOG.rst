12.0.8.9.19 (2023-01-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Changed name of field "payment_order_lines" to "payment_line_ids" to reflect the change made in the "account_duedates" module from which this module has a dependency.

12.0.7.9.19 (2022-01-18)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring impostazione conti trasferiti nel registro

12.0.7.9.18 (2022-01-14)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito impostazioni conti

12.0.7.9.17 (2021-12-02)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato conto corretto nella registrazione delle spese

12.0.7.9.16 (2021-12-01)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Reimpostato ricalcolo massimale

12.0.7.9.15 (2021-11-30)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato conto necessario a false nel file data

12.0.7.9.14 (2021-10-21)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito filtro sui conti padri

12.0.7.9.13 (2021-08-19)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Gestita relazione conti bancari figli

12.0.7.9.12 (2021-06-25)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiunto nome ordine in apertura e chiusura anticipo

12.0.7.9.11 (2021-05-18)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto calcolo su effetti allo sconto

12.0.7.9.10 (2021-04-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Inserito riferimento alla registrazione 'Apertura anticipo'
* [FIX] Calcolo portafoglio

12.0.7.9.9 (2021-04-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto calcolo sui conti degli effetti

12.0.7.9.8 (2021-04-14)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato castelletto nel registro e nel conto bancario

12.0.7.9.7_fix (2021-04-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Nascosto il campo 'Importo anticipato' nell'elenco delle Scadenze

12.0.7.9.7 (2021-03-31)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Compute massimale if invoice financing payment method only

12.0.6.8.6 (2021-02-19)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] account_payment_order.py", line 584

12.0.6.8.5 (2021-02-19)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Migliorato controlli su impostazioni conto corrente

12.0.6.8.4 (2021-02-19)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Raggruppari campi date e massimale/importo anticipato nell'ordine di debito di anticipo fatture

12.0.6.8.3 (2021-02-17)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Importo anticipato e date previsto incasso non modificabili dopo che la conferma dell'ordine

12.0.5.7.2 (2021-02-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] No riferimento a data bilancio

12.0.5.7.1 (2021-02-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato calcolo massimale

12.0.5.6.1 (2021-02-11)
~~~~~~~~~~~~~~~~~~~~~~~~

[IMP] Inserito campo massimale per anticipo fatture

12.0.5.5.23 (2021-02-10)
~~~~~~~~~~~~~~~~~~~~~~~~

[IMP] Modificata descrizione metodo di pagamento

12.0.5.5.22 (2021-02-04)
~~~~~~~~~~~~~~~~~~~~~~~~

[REF] Aggiornato registrazione di incasso

12.0.5.5.21 (2021-02-04)
~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Inserita dipendenza da account_invoice_13_more


12.0.5.5.20 (2021-02-02)
~~~~~~~~~~~~~~~~~~~~~~~~

[IMP] Possibilità di scegliere calcolo del massimale anticipo fatture su percentuale del totale o su percentuale imponibile


12.0.4.5.19 (2021-02-02)
~~~~~~~~~~~~~~~~~~~~~~~~

[IMP] Refactoring

12.0.4.5.18 (2021-02-01)
~~~~~~~~~~~~~~~~~~~~~~~~

[IMP] Impostato spese default

12.0.4.5.17 (2021-01-19)
~~~~~~~~~~~~~~~~~~~~~~~~

[REF] Refactoring e test

12.0.4.4.16 (2021-01-19)
~~~~~~~~~~~~~~~~~~~~~~~~

[REF] Refactoring

12.0.4.4.15 (2021-01-19)
~~~~~~~~~~~~~~~~~~~~~~~~

[REF] Refactoring configurazione nel metodo accredito pagamenti

12.0.4.4.14 (2021-01-08)
~~~~~~~~~~~~~~~~~~~~~~~~

[IMP] Implementato metodo accredito pagamenti

12.0.4.4.13 (2021-01-08)
~~~~~~~~~~~~~~~~~~~~~~~~

[MOD] Spostati campi "prorogation_ctr" e "unpaid_ctr" di account.move.line da modulo account_banking_invoice_financing a account_duedates

12.0.3.3.12 (2021-01-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato dipendenza al modulo account_duedates

12.0.2.1.7 (2020-12-21)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] aggiunti campi per gestione anticipi fatture in model e view di res.partner.bank
* [IMP] aggiunti controlli presenza e validazione sui campi di data previsto incasso e ammontare 
* [MOD] modificati nomi campi e viste per riflettere modifica nome modulo

12.0.2.0.6 (2020-12-21)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Implementato report distinta scadenze

12.0.1.0.5 (2020-12-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fix dependencies

12.0.1.0.4 (2020-12-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fix dependencies

12.0.1.0.3 (2020-12-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fix flake8

12.0.1.0.2 (2020-12-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostazione campi distinta

12.0.1.0.1 (2020-12-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostazione nuovi campi
