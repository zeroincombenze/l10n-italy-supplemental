Questo modulo aggiunge lo stato di consegna negli ordini clienti.

Lo stato di consegna è dipende dal campo ``qty_delivered`` nelle rige ordini.

Può essere utile per altri moduli che dipendono dallo stato di consegna.

Lo stato di consegna può essere forzato a consegnato nel caso che qualche quantità
o qualche riga in ordine sia successivamente annullata dal cliente finale e non si
debba più consegnare altri prodotti.

Questo modulo migliora la visibilità dello stato ordine completando l'informazione
dello stato di fatturazione con lo stato di consegna.

Questo modulo tiene conto anche le righe di spese di trasporto, qualora venga installato
il modulo *delivery* per il calcolo e l'addebito delle spese di trasporto che non
rientrno nel calcolo dello stato consegnato.

Questo modulo è un backport da Odoo 12.0
