On a delivery note, the manager can flag every line with:

* **Declared invoiced**: the line is considered fully invoiced and it is no
  more selected when an invoice is created from the delivery note. Use it when
  the goods of that line must not be billed, i.e. a free replacement.

The same result can be obtained from code with the methods
``action_declare_invoiced()`` and ``action_undeclare_invoiced()`` of
``stock.picking.package.preparation.line``.

The technical field ``line_invoiced`` is stored and computed: it is true when
an invoice line was created from the delivery note line, or the line was
declared invoiced, or the product carries the *Auto declare invoiced* policy,
or the **sale order line was declared invoiced**. That last case is the point
of the bridge: a decision taken on the order is never contradicted by the
delivery note, which would otherwise bill the customer for what the order
declares already invoiced.

The declaration travels from the order to the delivery note and never the
other way round: a delivery note line is one of the several deliveries of an
order line, so it cannot decide for it. When the order has to be closed as
well, declare its own line invoiced: `sale_order_line_qty_policy` handles it.

At delivery note level, **Invoice status** carries the same three values Odoo
uses for a sale order:

* *Nothing to invoice*: the delivery note is not invoiceable yet, or its
  reason for transportation declares it is not to be invoiced;
* *To invoice*: at least one line has still to be invoiced;
* *Fully invoiced*: every line is invoiced or declared invoiced. A delivery
  note can be fully invoiced without carrying any invoice, when the policy
  declares every one of its lines invoiced.

The *To Be Invoiced* and *Invoiced* filters of the delivery note list, and the
*To invoice* filter of the delivery note line list, are restated in terms of
these fields, so a document closed by the policy is no more offered for
invoicing.

Deleting an invoice, or one of its lines, gives the delivery note lines it
was holding back to be invoiced. Those references are dropped by the database
itself, so nothing would otherwise tell the delivery note to evaluate its
lines again: a line would stay invoiced forever, it could no more be billed,
and its delivery note would keep showing as fully invoiced while carrying no
invoice at all.

The invoice reference of the delivery note is written whenever every line is
invoiced, whatever the run which invoiced it: the standard module writes it
only when one single run invoices every line, so a line invoiced separately -
or declared invoiced - used to leave the document open forever.

A delivery note which has nothing left to invoice is skipped by the invoicing
procedure instead of stopping it. Note that the mass invoicing wizard still
selects it - its domain belongs to `l10n_it_ddt` - but the delivery note is
now skipped instead of taking down the whole run. An error is raised only when
none of the selected delivery notes has anything to invoice.
