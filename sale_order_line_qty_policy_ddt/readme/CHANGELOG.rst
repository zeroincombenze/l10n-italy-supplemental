10.0.0.1.2 (2026-09-04)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] The invoicing state of the delivery notes already in the database is
  recomputed when the module is installed and when it is upgraded: Odoo
  computes a stored field on existing records only when it creates its
  column, so the whole history was left with the 'To be Invoiced' flag
  raised and went on being offered for invoicing
* [FIX] Installing the module on a database which still carries its columns,
  after it had been uninstalled, left every delivery note written meanwhile
  without any invoicing state at all: the policy was simply not applied to
  the documents which predate the installation
* [NEW] The quantity of a delivery note line declared invoiced is taken off
  what is left to invoice on the sale order line it delivered, so the order
  can no more be invoiced for goods a delivery note already settled; a
  quantity is carried over and not a flag, so a partly declared order line
  keeps the rest of it to invoice

10.0.0.1.1 (2026-09-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] The 'To be Invoiced' flag of the delivery note is reset as soon as the
  delivery note is fully invoiced, so the mass invoicing wizard and the
  standard list filter no more offer for invoicing a document closed by the
  quantity policy; the flag is raised again when a line goes back to be
  invoiced
* [IMP] The invoice status of the delivery note reads the reason for
  transportation instead of the 'To be Invoiced' flag it mirrors, so that
  resetting the flag does not alter the status

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
