Add to OCA *l10n_it_delivery_note* the choice of how delivery notes (DDT) are
grouped together to make invoices, as in the former Odoo 10.0 *l10n_it_ddt*.

The grouping method is set on the customer and copied to the sale order:

* One DDT - One Invoice: every delivery note has its own invoice
* Billing Partner: delivery notes with the same invoice partner share the invoice
* Shipping Partner: one invoice for each shipping address
* By Sale Order: one invoice for each sale order
* Code group: delivery notes shipped to partners with the same *code group* share
  the invoice
