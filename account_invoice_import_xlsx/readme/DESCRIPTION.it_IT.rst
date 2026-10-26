Importa fatture da Excel
------------------------

Questo modulo importa dati di fattura da un file Excel (.xlsx) in due modi:

* **Importa righe in una fattura**: il bottone [Import xlsx] su una fattura o fattura
  fornitore in bozza aggiunge una riga per ogni riga del file. I prodotti sono cercati
  per codice e nome; prezzo, conto e imposte derivano dal prodotto, se il file non li
  indica.
* **Crea fatture**: il menù *Contabilità › Configurazione › Import Account Invoice*
  crea fatture in bozza. Una riga con i dati del cliente apre una nuova fattura; le
  righe senza dati del cliente vi aggiungono righe.

Titoli di colonna riconosciuti:

* ``Denominazione Cliente``: Nome del soggetto
* ``Partita Iva``: Partita IVA (alle sole cifre viene anteposto ``IT``)
* ``Codice Fiscale``: Codice fiscale
* ``Codice``: Codice prodotto
* ``Nome``: Descrizione della riga
* ``Quantita``: Quantità
* ``Imponibile``: Imponibile (riga con quantità 1)
* ``Iva``: Importo IVA; aliquota più vicina tra 0, 4, 5, 10, 22%
* ``Numero``: Numero fattura
* ``Data``: Data fattura (gg/mm/aaaa o data Excel)

I numeri possono essere scritti in formato italiano (``2.049,18``).
Si possono vedere esempi nella cartella example.
