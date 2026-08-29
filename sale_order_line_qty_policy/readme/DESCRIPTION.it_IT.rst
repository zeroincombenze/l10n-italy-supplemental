Odoo valuta lo stato di una riga d'ordine solo in base alle quantità: una riga
è fatturata quando la quantità fatturata raggiunge quella ordinata (o quella
consegnata, in base alla politica di fatturazione del prodotto). Esistono però
casi ricorrenti in cui questa regola lascia l'ordine aperto all'infinito.

Questo modulo permette di dichiarare una riga d'ordine consegnata o fatturata,
manualmente oppure tramite una politica dichiarata sul prodotto.

Sul prodotto sono disponibili due politiche:

* **Dichiara automaticamente fatturato**: ogni riga di questo prodotto è
  considerata interamente fatturata alla conferma dell'ordine. Questa funzione
  è richiesta dai moduli che gestiscono prodotti di tipo imposta, come il
  contributo ambientale (CONAI), il cui importo viene rivalutato a livello di
  fattura: la quantità fatturata non coinciderà mai con quella ordinata e
  l'ordine resterebbe in uno stato incompleto o errato.

* **Soglia di consegna**: per alcuni prodotti non è possibile consegnare
  l'esatta quantità ordinata. Quando lo scostamento fra quantità ordinata e
  consegnata rientra nella percentuale dichiarata, la riga è considerata
  interamente consegnata e l'ordine si chiude non appena la quantità
  consegnata è stata fatturata. La soglia può essere dichiarata sul prodotto
  oppure, una sola volta per un'intera famiglia di prodotti, sulla categoria
  prodotto.

La quantità consegnata non viene mai alterata dal modulo: al cliente è sempre
fatturata la quantità realmente consegnata.
