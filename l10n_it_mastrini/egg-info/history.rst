12.0.10.12.34 (2022-06-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Currency statement / E/C in valuta
* [IMP] Residual amounts (experimental) / Importo partite aperte (sperimentale)

12.0.10.12.33 (2022-02-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added option order date filter / Selezione filtro su ordine data

12.0.10.12.32 (2021-11-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added journal selection / Selezione su registro

12.0.10.12.31 (2021-10-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-539: KeyError: 'accrual_start_date' when installed first / KeyError: 'accrual_start_date' durante installazione l10n_it_mastrini

12.0.10.12.30 (2021-10-22)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-525: corretto compoprtamento funzione di calcolo dei saldi

12.0.10.11.30 (2021-07-23)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-385, POW-417: correzzione calcolo totali e riabilitati alcuni campi nella vista che erano stati disabilitati per prove durante lo sviluppo

12.0.9.10.29 (2021-07-13)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-385, POW-417: visualizzazione di tutti i conti di un partner con filtro per natura e tipo di conto

12.0.8.7.22 (2021-04-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW - 121: fix popup bloccante

12.0.8.7.21 (2020-12-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW - 220: aggiornato campo type

12.0.8.7.20 (2020-08-31)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI - 138: gestito l'esercizio fiscale

12.0.8.6.20 (2020-08-31)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-6/AXI-31: corretta gestione del riepilogo IVA per le note di credito

12.0.8.5.20 (2020-08-31)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto XML ID del parent menu della voce Mastrini


12.0.8.5.19 (2020-08-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-6/AXI-28: Migliorata visualizzazione contropartite e controvalori


12.0.7.4.18 (2020-08-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] AXI-109: Refactoring menu



12.0.7.4.17 (2020-08-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-6/AXI-28: Aggiunta visualizzazione contropartite e controvalori



12.0.6.3.16 (2020-08-20)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-117: Visualizzazione nome breve del registro invece del nome completo



12.0.5.3.15 (2020-08-20)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-126: Aggiunta visualizzazione stato delle registrazioni e relativo filtro



12.0.4.2.15 (2020-08-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-121: nascosti i pulsanti salva / abbandona



12.0.4.2.14 (2020-08-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-125: aggiunta colonna con tipo registrazione nella visualizzazione mastrini



12.0.3.2.13 (2020-08-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] aggiornamento della documentazione / history



12.0.3.2.12 (2020-08-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] aggiunta gestione segni in riepilogo IVA
* [IMP] AXI-6/AXI-31: Riepilogo IVA, prima implementazione funzionante



12.0.2.1.11 (2020-07-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-6/AXI-29: Colonne con date competenze ratei e risconti e controllo per visualizzarle e nasconderle



12.0.1.1.10 (2020-07-24)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-6/AXI-81: Etichette in Italiano e righe totali in grassetto
* [IMP] AXI-6/AXI-81: Righe totali in grassetto



12.0.0.2.9 (2020-07-24)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-6/AXI-81: inseriti nomi dei campi in Italiano
* [MOD] rimosso file superfluo
* [MOD] aggiornato numero versione



12.0.0.1.9 (2020-07-24)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] name overlapping



12.0.0.0.8 (2020-07-23)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-6/AXI-77: selezione date tramite intervalli (date_range)
* [MOD] AXI-6/AXI-78 + AXI-6/AXI-79: rimossi campi superflui dai wrapper, rimossa
eliminazione righe vecchie (fa Odoo da solo), rimossa associazione righe con wizard (non è necessaria)



12.0.0.0.7 (2020-07-22)
~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] AXI-6/AXI-78 + AXI-6/AXI-79: completata implementazione totali in tabella
* [MOD] AXI-6/AXI-78 + AXI-6/AXI-79: prima implementazione totali in tabella



12.0.0.0.6 (2020-07-21)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto errore nella funzione di ricerca anni fiscali all'interno del wizard dei mastrini



12.0.0.0.5 (2020-07-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-6/AXI-81 Cambiare colonne visualizzate - Completato
* [IMP] AXI-6/AXI-82 Scelta partner per conti di debito o credito



12.0.0.0.3 (2020-07-17)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] AXI-6/AXI-78 Saldi iniziali: miglioramento parte grafica - AXI-6/AXI-79 Saldi finali: miglioramento parte grafica - AXI-6/AXI-75 Proporre automaticamente esercizio contabile attuale
* [IMP] AXI-6/AXI-78 Saldi iniziali - AXI-6/AXI-79 Saldi finali - Implementato algoritmo di calcolo e bozza parte grafica
* [IMP] aggiornato numero di versione - aggiunta history, autori, ecc.
* [IMP] AXI-6/AXI-74 filtro per esercizio contabile - AXI-6/AXI-80 filtri su unica riga


12.0.0.0.2 (2020-07-09)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto posizionamento saldo girnaliero
* [MOD] rimosso pulsante inutile dalla visualizzazione mastrini
* [FIX] eliminato problema del saldo giornaliero che scompariva quando le account.move.line venivano ricaricate


12.0.0.0.1 (2020-07-08)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] inseriti pulsanti apertura form di modifica, inseriti totali giornalieri totali per righe visualizzate, nascosti gli zero


12.0.0.0.0 (2020-07-07)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] prima implementazionezione funzionante
