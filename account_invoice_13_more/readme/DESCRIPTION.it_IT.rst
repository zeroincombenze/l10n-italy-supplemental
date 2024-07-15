Questo modulo replica alcuni campi della fattura nella registrazione contabile.
Il modello account.move ha la stessa struttura di Odoo 13.0 e successive.
Il modulo semplifica il backport da Odoo 13.0+

Strutture comuni con Odoo 13.0+
-------------------------------

* account.move.invoice_date
* account.move.move_type
* account.move.move_type (sarà rimosso a breve)
* account.move.fiscal_position_id
* account.move.payment_term_id
* account.move.partner_bank_id

Differenze da Odoo 13.0+
------------------------

* Le fatture in bozza e cancellate non hanno registrazioni contabili
* La gestione degli eventi è sul modello account.invoice
* Il campo move_type è compatibile con Odoo 14+ non con Odoo 13.0
