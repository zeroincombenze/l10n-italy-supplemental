Date di registrazione fatture

Questo modulo permette di registrare alcune date inerenti la registrazione fatture.

La lista delle date è la seguente:

* la data contabile, standard Odoo è chiamata di registrazione
* date_apply_vat è un nuovo campo che dichiara la data di competenza dell'IVA
* date_apply_balance è un nuovo cmapo che dichiara la data di competenza a bilancio

Note:

* Questo software è simile al modulo account_invoice_entry_date del gruppo italiano OCA
* Il modulo OCA italiano utiliza un nuovo campo chiamato registration_date (data di registrazione) menrte questo modulo rinomina il campo standard di Odoo
* Nel registro degli acquisti la data di registrazione è libera, senza controlli
* Nel registro delle vendite la data di registrazione è identica alla data fattura ed è in sola lettura
* La regola precedente può essere disabilita con una configurazione del registro
* I valori predefiniti delle date date_apply_vat e date_apply_balance sono quelli della data di registrazione; l'operatore ha facoltà di modifica
