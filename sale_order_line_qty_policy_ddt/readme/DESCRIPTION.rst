`l10n_it_ddt` creates invoices from delivery notes (DdT) instead of from sale
orders, and it evaluates a delivery note from its lines only: the document is
declared invoiced when every one of its lines was turned into an invoice line
during one single run of the invoicing procedure.

`sale_order_line_qty_policy` makes it possible to declare a sale order line
invoiced without any invoice line at all, either by hand or by a policy
declared on the product, i.e. the environmental contribution (CONAI) whose
amount is evaluated again at invoice level.

Without this bridge module the two behaviours contradict each other: a
delivery note carrying a line the quantity policy declares invoiced can never
be closed. The invoicing procedure skips that line, so the invoice reference
of the delivery note is never written; the document keeps showing up as to be
invoiced and every further attempt to invoice it ends with *There is no
invoicable line*, which in the mass invoicing wizard takes down the invoicing
of every other delivery note of the period.

This module introduces on the delivery note line the same concepts the
quantity policy introduces on the sale order line, and it adds to the
delivery note the invoice status Odoo gives to a sale order.
