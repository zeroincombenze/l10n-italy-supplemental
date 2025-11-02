Per ciascun fornitore è possibile impostare il **Livello dettaglio e-fatture**:

* Livello minimo: la fattura fornitore viene creata senza righe, che dovranno essere create dall'utente in base a quanto indicato nella fattura elettronica
* Livello codice IVA: le righe sono cumulate per codice IVA
* Livello massimo: le righe della fattura fornitore verranno generate a partire da tutte quelle presenti nella fattura elettronica

Nella scheda fornitore è inoltre possibile impostare il **Prodotto predefinito per e-fattura**:
verrà usato, durante la generazione delle fatture fornitore,
quando non sono disponibili altri prodotti adeguati.
Il conto e l'imposta della riga fattura verranno impostati in base a quelli configurati
nel prodotto.

Tutti i codici prodotto usati dai fornitori possono essere impostati nella relativa scheda, in

☰ Magazzino > Controllo inventario > Prodotti

Se il fornitore specifica un codice noto nell'XML, questo verrà usato dal sistema per
recuperare il prodotto corretto da usare nella riga fattura, impostando il conto collegato.
