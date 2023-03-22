This module replicates some account.invoice fields on account.move.
The account.move model has the some structure of Odoo 13.0 and more.
This module simplify the backport from Odoo 13.0+.

Common structure with Odoo 13.0+
--------------------------------

* account.move.invoice_date
* account.move.move_type
* account.move.type (will be remove early)
* account.move.fiscal_position_id
* account.move.payment_term_id
* account.move.partner_bank_id

Difference from Odoo 13.0+
--------------------------

* Draft and cancelled invoice has no account.move records
* Events are still active on account.invoice model
* Field move_type is compatible with Odoo 14+ not with Odoo 13.0
