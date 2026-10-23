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
  * *Solo se 0*: una riga senza prezzo è dichiarata subito fatturata, ad
    esempio la spesa di spedizione di una consegna gratuita: non viene mai
    aggiunta in fattura. Applicato anche alle righe di DdT da
    `sale_order_line_qty_policy_ddt`;
  * *Sempre*: ogni riga d'ordine di questo prodotto è dichiarata fatturata.

Entrambi i campi sono dichiarati sul modello prodotto, quindi la politica vale
per tutte le varianti del prodotto.
