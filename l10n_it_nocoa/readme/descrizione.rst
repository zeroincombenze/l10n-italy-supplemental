Piano dei conti vuoto
---------------------

Questo modulo carica un PdC e una tabella codici IVA vuoti
ma imposta i registri sezionali e i dati interni.

Usare questo modulo quando l'utente finale vuole caricare il Piando dei Conti da se.

Attenzione! A causa della struttura di Odoo sono inseriti i seguenti conti:

* Clienti, codice CLI
* Fornitori, codice FOR
* Costo generico, codice CST
* Ricavo generico, codice RCV
* Banca, codice BCA
* IVA, codice IVA
* Codice IVA 22%

Come usare il modulo
--------------------

Il modulo è una base per lo sviluppo di un Piano dei Conti personalizzato
del cliente.
Sostituire i codice dei conti e delle imposta con i valori corretti e aggiungere i dati mancanti.
Si consiglia di aggiungere anche le posizioni fiscali.

Significato dei codici:

* CLI000 -> il conto clienti; usato da Odoo come default in res.partner
* FOR000 -> il conto fornitori; usato da Odoo come default in res.partner
* RCV000 -> il conto di ricavo predefinito in fatturazione
* CST000 -> il conto di costo predefinito in fatturazione
* IVA000 -> Il conto IVA predefinito; potrebbero essere più di uno
* BCA000 -> La radice dei conti bancari

Ricordardi di modificare i dati in tutti i 5 file nella directory ./data
