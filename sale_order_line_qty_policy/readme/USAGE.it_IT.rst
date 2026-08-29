Su un ordine di vendita confermato, il responsabile può marcare ogni riga con:

* **Dichiarata consegnata**: la riga è considerata interamente consegnata
  qualunque sia la quantità consegnata. La quantità consegnata non viene
  alterata, quindi al cliente è fatturato quanto realmente consegnato.

* **Dichiarata fatturata**: la riga è considerata interamente fatturata e non
  viene più selezionata quando si crea una fattura dall'ordine.

Entrambi i flag sono disponibili nell'elenco delle righe d'ordine e nell'elenco
*Righe ordine di vendita*, dove sono aggiunti i filtri *Interamente consegnate*,
*Dichiarate consegnate* e *Dichiarate fatturate*.

Lo stesso risultato si ottiene da codice con i metodi
``action_declare_delivered()``, ``action_undeclare_delivered()``,
``action_declare_invoiced()`` e ``action_undeclare_invoiced()`` di
``sale.order.line``.

A livello di ordine, ``force_delivery_state`` è mantenuto allineato alle
righe: è impostato quando tutte le righe rilevanti sono consegnate ed è
azzerato quando non lo sono. Il campo è condiviso con
``sale_delivery_state_z0``, che mostra l'ordine come consegnato, e nessuno dei
due moduli dipende dall'altro. Appena un utente scrive il flag manualmente
viene impostato ``force_delivery_state_manual`` e la politica smette di
gestire quell'ordine.

Quando l'ordine è riportato in bozza, la quantità consegnata delle righe di
prodotti stoccabili è riscritta a partire dai movimenti di magazzino ancora
collegati. Odoo standard scollega in quel momento ogni approvvigionamento dalla
riga, quindi la quantità consegnata viene azzerata; senza questo intervento la
riga manterrebbe per sempre la quantità dell'ultima consegna, anche se la merce
è stata resa. I servizi mantengono la quantità inserita manualmente.

Il campo tecnico ``line_delivered`` è memorizzato e calcolato: è vero quando la
riga ha raggiunto la quantità ordinata, oppure lo scostamento rientra nella
soglia del prodotto, oppure la riga è stata dichiarata consegnata.
