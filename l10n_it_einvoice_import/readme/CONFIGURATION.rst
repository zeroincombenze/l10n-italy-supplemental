A sale journal must exist for the company, and the customer must have a
receivable account: both are read when the invoice is created.

|menu| Accounting > Configuration > Settings

 - *Customer Payment Term*: whether the payment term of the imported invoice
   comes from the XML file or from the one assigned in the customer record
   (the default)
 - *Customer product search*: how to look the product up — by internal code,
   by exact name, or by similar name
 - *Rounding Tax on sale*: zero rate sale tax carrying the rounding line, when
   the totals of the XML file do not match the ones computed by Odoo. When not
   set, the purchase rounding tax of ``l10n_it_einvoice_in`` is used

The same two settings can be overridden per customer, in the partner form.

To see the forced number on the invoice form, the user must belong to the
*Allow to force invoice number* group of ``account_invoice_force_number``:
the number is written by the import in any case, the group only makes the
field visible.

Beware that an invoice carrying a forced number cannot be deleted, not even
while still in draft: this is standard Odoo behaviour for any invoice that has
been given a number. Cancel it instead.
