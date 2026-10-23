Sulla scheda prodotto, linguetta *Fatturazione*, sezione *Politiche di
quantità*:

* **Soglia di consegna (%)**: massimo scostamento ammesso, in percentuale
  sulla quantità ordinata, fra quantità ordinata e consegnata. Lo scostamento
  è valutato in valore assoluto, quindi sono coperte sia le consegne in difetto
  sia quelle in eccesso. Lasciare 0 per ereditare la soglia della categoria
  prodotto.

La stessa **Soglia di consegna (%)** è disponibile sulla scheda della categoria
prodotto, così da poterla dichiarare una sola volta per un'intera famiglia di
prodotti. Prevale la soglia del prodotto; quella della categoria è usata solo
quando il prodotto non dichiara la propria. Lasciare entrambe a 0 per
disabilitare la politica.

* **Dichiara automaticamente fatturato**: quando le righe di questo prodotto
  sono dichiarate fatturate in automatico:

  * *Mai* (predefinito): comportamento standard di Odoo;
  * *Solo se 0*: una riga senza prezzo eliminata da una fattura in bozza viene
    dichiarata fatturata anziché tornare da fatturare, ad esempio la spesa di
    spedizione di una consegna gratuita. Applicato da
    `sale_order_line_qty_policy_ddt` alle righe di DdT;
  * *Sempre*: ogni riga d'ordine di questo prodotto è dichiarata fatturata.

Entrambi i campi sono dichiarati sul modello prodotto, quindi la politica vale
per tutte le varianti del prodotto.
