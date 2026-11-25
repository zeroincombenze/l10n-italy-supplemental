Aggiunge a *l10n_it_delivery_note* OCA la scelta di come raggruppare i DDT per
fatturarli insieme, come nel vecchio *l10n_it_ddt* di Odoo 10.0.

Il metodo di raggruppamento si imposta sul cliente e viene copiato nell'ordine:

* Un DDT - Una fattura: ogni DDT ha la sua fattura
* Cliente fatturazione: i DDT con lo stesso intestatario fattura condividono la fattura
* Destinazione: una fattura per ogni destinazione merci
* Per ordine di vendita: una fattura per ogni ordine di vendita
* Gruppo codice: i DDT con destinazione dello stesso *codice gruppo* condividono la
  fattura
