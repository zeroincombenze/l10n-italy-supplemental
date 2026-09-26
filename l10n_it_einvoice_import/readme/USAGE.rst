|menu| Accounting > Sales > E-invoice Export Files

 - Upload the XML file, or load a whole ZIP of them from
   |menu| Accounting > Sales > Electronic Invoice > Import eInvoice from ZIP,
   which is the sale counterpart of the same menu under Purchases
 - View the file content clicking on 'Preview'
 - Run the 'Import Sale Electronic Invoice' wizard to create the draft
   customer invoices

The list shows, for every file, how many invoices it contains and whether they
are already registered; the *Not registered* filter selects the files still to
be imported. A file the wizard has imported is flagged *Imported*, to tell it apart
from the ones this system generated out of its own invoices.

Whatever could not be matched — a tax code, a payment term, a product — is
written in the 'Import Inconsistencies' field of the created invoice, which is
left in draft state for review.

A file loaded here was already sent to the Exchange System by whoever produced
it, so it is marked as *Sent* as soon as it is uploaded, not only once it is
imported. Were it left in the *Ready to Send* state, the hourly send job of
``l10n_it_einvoice_send2sdi`` would send it to SdI a second time. Files this
system generates are untouched and stay *Ready to Send*.

To send such a file anyway, use the *Reset to ready* button on the file.

The number of the imported invoice is the one written in the xml file, forced
through the *Force Number* field of ``account_invoice_force_number``: the
document is already known to SdI and to the customer under that number, so the
sale journal sequence must not renumber it.
