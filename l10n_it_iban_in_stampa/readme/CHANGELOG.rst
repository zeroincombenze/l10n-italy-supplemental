12.0.1.1.33 (2022-03-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto bug su vista registrazioni contabili (campo mancante)

12.0.1.1.32 (2022-01-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato le viste per fatture e registrazioni

12.0.1.1.31 (2022-01-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Refactoring del mixin documenti e impostato mixin base in l10n-italy

12.0.1.1.30 (2022-01-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Esclusi conti di portafoglio nel campo conto aziendale

12.0.1.1.29 (2021-12-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Esposto campo IBAN azienda sempre modificabile

12.0.1.1.28 (2021-09-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] correzione vista account.move per nascondere selettivamente i campi IBAN azienda e IBAN controparte
* [FIX] corretto campo utilizzato per determinare tipo di account.move

12.0.1.1.27 (2021-09-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] gestione copia dei campi relativi all'IBAN quando viene duplicato un documento
* [FIX] corretto errore in "account_move_view.xml" in cui veniva utilizzato il campo move_type di move_type invece del campo type

12.0.1.1.26 (2021-09-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto errore di battitura in purchase_order.py

12.0.1.1.25 (2021-09-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] eliminata derivazione di ResPartnerBank da OrderMixin in quanto errata

12.0.1.1.24 (2021-09-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] eliminata "assertion False" se documento passato ai metodi di "engine" non è ne di tipo cliente (fattura cliente o sale order) ne di tipo fornitore (fattura fornitore o purchase order) perchè le account.move possono essere di tipo diverso

12.0.1.1.23 (2021-09-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] aggiunta possibilità di configurare quali banche faranno parte di quelle di default da stampare se "Tipo stampa IBAN" = "Azienda" e "Banca aziendale" non ha valore.
* [FIX] corretto errore in stampa Ordini di Vendita, spostato campo bank_2_print nel mixin base in modo che sia disponibile anche per gli ordini

12.0.1.1.22 (2021-09-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] stampa di tutti gli IBAN dei conti correnti aziendali se bank_2_print_selector assume il valore “company” e il campo company_bank_id non è valorizzato (fattura, ordine di vendita, ordine di acquisto)
* [FIX] aggiunti codici di pagamento mancanti nell'algoritmo di calcolo del tipo di IBAN da utilizzare
* [FIX] rimosso "ensure_one()" da metodi in cui non era necessario in favore di ciclo "for" sugli elementi di contenuti nel recordset "self"
* [IMP] aggiunta campo bank_4_xml in account.invoice e account.move per calcolo del campo da utilizzare nella generazione dell'XML della fattura

12.0.1.1.21 (2021-09-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto funzionamento metodo res.partner.bank_infos() per gestire chiamate su recordset vuoto
* [FIX] corretta funzione di restituzione dei filtri in sale.order e purchase.order in modo da gestire casi in cui il partner è un indirizzo di fatturazione invece del partner vero e prorpio
* [IMP] campo Tipo stampa IBAN: aggiunto valore "ni" a stato "Non indicato" per distinguere il caso di campo non impostato dall caso di campo impostato a "Non indicato"
* [FIX] calcolo automatica dei campi: Banca appoggio, Banca aziendale e Tipo banca nel caso in cui non siano impostati al momento della creazione della fattura. Questa modifica è utile per gestire la creazione di fatture da Sale Order che NON hanno i campi impostati.

12.0.1.1.20 (2021-09-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] introduzione campo calcolato "bank_2_print" in account.invoice e account.move che ritorna l'IBAN da stampare / usare per la generazione della fattura XML
* [FIX] aggiornamento campo "Conto bancario" (partner_bank_id) di account.move e account.invoice al variare dei campi "Banca appoggio" e "Banca aziendale"
* [FIX] visualizzazione errore e blocco procedura nel caso in cui si tenti di creare una fattura da sale.order con termini di pagamento diversi
* [FIX] rimossa obbligatorietà da selettore tipo iban (bank_2_print_selector) altrimenti non permette più salvataggio fattura
* [FIX] rimossa chiamata a metodo obsoleto
* [DOC] aggiornamento history e numero di versione

12.0.1.1.19 (2021-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] + [IMP] Correzione dati bancari e filtri "domain" per tener conto di partner che sono indirizzi di fatturazione dell'azienda principale

12.0.1.1.18 (2021-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] + [IMP] Correzione "domain" per campi "Banca aziendale" e Banca d'appoggio" in Ordine di Vendita (sale.order) e Movimento Contabile (account.move) - completata copia campi nuovi in creazione fattura da DDT

12.0.1.1.17 (2021-08-20)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-433 Inserito domain nei campi extra di tutti i modelli

12.0.1.1.16 (2021-08-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Aggiornato traduzioni

12.0.1.1.15 (2021-08-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Impostato gestione banca in ordini di vendita e di acquisto

12.0.1.1.14 (2021-08-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Override stampa fattura cliente con banca

12.0.1.1.13 (2021-08-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Impostazioni stampa fattura cliente

12.0.1.1.12 (2021-08-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Verifica e aggiornamento ordine acquisto

12.0.1.1.11 (2021-08-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] POW-433 Rinominato il modulo
* [IMP] POW-433 Verifica e aggiornamento ordine clienti

12.0.1.1.10 (2021-08-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Verifica e aggiornamento fattura clienti

12.0.1.1.9 (2021-08-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Impostato campi nelle viste
* [IMP] POW-433 Impostato on change sui campi

12.0.1.1.8 (2021-08-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Impostato funzioni di utilità

12.0.1.1.7 (2021-08-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Funzione adattatore documento in account.invoice
* [IMP] POW-433 Funzione adattatore documento in sale.order
* [IMP] POW-433 Funzione adattatore documento in purchase.order

12.0.1.1.6 (2021-08-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-433 Funzione adattatore documento in account.move

12.0.1.0.5 (2021-08-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-462 Impostato campi per registrazione contabile

12.0.1.0.4 (2021-08-05)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] POW-449 Impostato campi per ordine di acquisto

12.0.1.0.3 (2021-08-05)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] POW-448 Impostato campi per ordine di vendita

12.0.1.0.2 (2021-08-05)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] POW-447 Refactoring

12.0.1.0.1 (2021-08-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-445 Implementato metodo di rilevamento tipo soggetto passivo

12.0.1.0.0 (2021-08-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-443 Campi extra in fattura
