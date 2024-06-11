Questo modulo calcola l'IVA della fattura in modo da aderire alle leggi fiscali
italiane ed evitare il rifiuto dallo SdI.

Odoo calcola l'IVA riga per riga e al termine somma tutti i totali imponibili e IVA
delle singole righe. Questo comportamento produce una picola differenza tra il totale
dell'IVA ed il valore dell'IVA partendo dal totale imponibile.

Questo è un esempio:

.. $include example.csv

Odoo restituisce il totale imponibile 27,96 (come somma di tutti gli imponibili delle
righe) e il totale IVA 6,14 (come somma dei totali IVA) ma il totale IVA calcolato da
27,96 è 6,15

Il parametro di configurazione "Arrotondare globalmente" è attivo solo in creazione ma
in modifica non funziona.
