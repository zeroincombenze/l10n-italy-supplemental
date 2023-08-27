12.0.0.1.25 (2021-10-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Account nature matches with alt_nature too / Natura conto validata anche per natura alternativa
* [IMP] POW-484: parent_id of account removed / Rimosso conto padre in PdC
* [FIX] pow-485: wrong relationship between some account & type / Errata relazione conto e natura su alcuni conti

12.0.0.1.24 (2021-09-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Automatically set nature of group / Impostazione automatica della natura dei gruppi di conto
* [MIG] Migrate account hierarchy into account group / Migrazione gerarchia conti di gruppi conto

12.0.0.1.23 (2021-09-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-481: account.group integration / integrazione gruppi contabili
* [IMP] Conflicts in manifest
* [IMP] Account list in account type / Lista conti per tipo conto
* [IMP] Automatically set nature of account / Impostazione automatica della natura dei conti

12.0.0.1.22 (2021-09-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Alternate nature / natura alternativa

12.0.0.1.21 (2021-09-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Prepayments nature / natura risconti

12.0.0.1.20 (2021-08-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] No update in profile default / inserito il flag noupdate

12.0.0.1.19 (2021-02-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Singleton error in mass editing / Errore singleton in mass editing

12.0.0.1.18 (2020-12-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added context check / Inserito flag per importazione

12.0.0.1.17 (2020-10-20)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] flake8 elevated level / Aggiornato controllo sintattico

12.0.0.1.16 (2020-09-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Filtered prepayments / Applicato filtro su risconti attivi

12.0.0.1.15 (2020-08-31)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Disabled change of profile on zero code flag  / Rimossa la possibilità di modificare il flag 'Codici a zero' se alimentato il piano dei conti

12.0.0.1.14 (2020-08-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Remove create from change of profile  / Rimossa la possibilità di creare nuovi profili dalla selezione

12.0.0.1.13 (2020-07-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Prevent change of profile / Segnalazione in caso di cambio profilo

12.0.0.1.12 (2020-07-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Duplicate company warning / Segnalazione in caso di duplicazione profilo
* [IMP] Memorandum account type / Tipo conto d'ordine


12.0.0.1.2 (2020-04-01)
~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Checks refactored / Riprogettati i controlli
* [IMP] Flag account with zero / Possibile inserire conti con zero (personalizzabile)
* [FIX] Check work on existent CoA / I controlli funzionano anche con un PdC già installato
* [IMP] Nature in Coa list / Campo natura in lista PdC
