This module creates **customer invoices** out of electronic invoice XML files
(FatturaPA version 1.2.1), the same job ``l10n_it_einvoice_in`` does for
supplier bills.

It is meant for sale invoices issued outside Odoo — produced by another
program, or downloaded back from the Exchange System (SdI) or from an
intermediary — which have to be registered in the accounting.

In the XML file the company is the *CedentePrestatore* and the customer is the
*CessionarioCommittente*: it is the other way round of a received bill. A file
whose *CedentePrestatore* is not the current company is refused.

For every customer it is possible to set the 'E-bills Detail Level':

 - Minimum level: invoice is created with no lines; user will have to create
   them, according to what specified in the electronic invoice
 - VAT code level: lines are cumulated by VAT code
 - Maximum level: every line contained in the electronic invoice creates a
   line in the invoice

Products are looked up by internal code or by description, since a sale
e-invoice carries the codes of the company itself. When no product is found,
the 'E-bill Default Product' of the customer is used.

Self billing documents (*autofattura*, TipoDocumento TD16 to TD23) are
imported too, but the roles in their header are swapped: the resulting invoice
is reported as an inconsistency, so that it can be checked by hand.

A whole zip file of e-invoices can be loaded at once, the way
``l10n_it_einvoice_import_zip`` does for purchase files; that module is left
to the purchase side, so neither has to depend on the other.
