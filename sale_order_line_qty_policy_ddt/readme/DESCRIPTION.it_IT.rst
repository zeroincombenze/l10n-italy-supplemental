`l10n_it_ddt` crea le fatture dai documenti di trasporto (DdT) anziché dagli
ordini di vendita e valuta il DdT dalle sole righe: il documento è dichiarato
fatturato quando tutte le sue righe sono diventate righe di fattura in una
singola esecuzione della procedura di fatturazione.

`sale_order_line_qty_policy` permette di dichiarare fatturata una riga
d'ordine anche senza alcuna riga di fattura, manualmente oppure tramite una
politica dichiarata sul prodotto, come il contributo ambientale (CONAI) il cui
importo viene rivalutato a livello di fattura.

Senza questo modulo ponte i due comportamenti si contraddicono: un DdT che
contiene una riga dichiarata fatturata dalla politica di quantità non può mai
essere chiuso. La procedura di fatturazione salta quella riga, quindi il
riferimento alla fattura non viene mai scritto sul DdT; il documento continua
a risultare da fatturare e ogni ulteriore tentativo di fatturarlo termina con
*There is no invoicable line*, errore che nella procedura di fatturazione
massiva blocca la fatturazione di tutti gli altri DdT del periodo.

Questo modulo introduce sulla riga del DdT gli stessi concetti che la politica
di quantità introduce sulla riga d'ordine e aggiunge al DdT lo stato di
fatturazione che Odoo attribuisce all'ordine di vendita.
