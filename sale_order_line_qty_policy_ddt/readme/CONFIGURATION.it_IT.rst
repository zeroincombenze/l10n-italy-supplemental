Non è necessaria alcuna configurazione: il modulo mette in comunicazione due
moduli già configurati.

Le politiche dichiarate sul prodotto da `sale_order_line_qty_policy` sono le
medesime usate qui:

* **Dichiara automaticamente fatturato**: ogni riga di DdT di questo prodotto
  è considerata fatturata, esattamente come lo è ogni riga d'ordine.

La **Soglia di consegna (%)** non è valutata sul DdT: la soglia confronta la
quantità ordinata con quella consegnata e il DdT *è* la consegna, quindi
riporta la sola quantità consegnata. La soglia continua ad essere valutata
sulla riga d'ordine di vendita.
