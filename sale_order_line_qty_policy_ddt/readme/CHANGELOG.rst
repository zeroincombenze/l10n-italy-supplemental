10.0.0.1.0 (2026-09-01)
~~~~~~~~~~~~~~~~~~~~~~~

* [NEW] Initial implementation: bridge module between
  sale_order_line_qty_policy and l10n_it_ddt
* [NEW] Delivery note line flag force_invoiced and technical field
  line_invoiced
* [NEW] Delivery note field invoice_status
* [FIX] The invoice reference of the delivery note is written whenever every
  line is invoiced, no more only when every line was invoiced by one single
  run of the invoicing procedure
* [FIX] A delivery note with nothing to invoice is skipped by the invoicing
  procedure, so it no more stops the invoicing of the other ones
* [FIX] Deleting an invoice, or one of its lines, gives the delivery note
  lines back to be invoiced: the reference is dropped by the database, so the
  stored invoicing state was left behind and the line stayed invoiced forever
* [NEW] Italian translation
