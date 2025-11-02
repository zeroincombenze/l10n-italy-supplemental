EInvoice in
-----------

This module allows to import Electronic Bill XML files version 1.2.1

http://www.fatturapa.gov.it/export/fatturazione/en/normativa/f-2.htm

received through the Exchange System (SdI).

http://www.fatturapa.gov.it/export/fatturazione/en/sdi.htm

For every supplier, it is possible to set the 'E-bills Detail Level':

 - Minimum level: Bill is created with no lines; User will have to create them, according to what specified in the electronic bill
 - VAT code level: Line are cumulated by VAT code
 - Maximum level: Every line contained in electronic bill will create a line in bill

Moreover, in supplier form you can set the 'E-bill Default Product': this product will be used, during generation of bills, when no other possible product is found. Tax and account of bill line will be set according to what configured in the product.

Every product code used by suppliers can be set, in product form, in

Inventory →  Products

If supplier specifies a known code in XML, the system will use it to retrieve the correct product to be used in bill line, setting the related tax and account.

 * Go to Accounting →  Purchases →  Electronic Bill
 * Upload XML file
 * View bill content clicking on 'Show preview'
 * Run 'Import e-bill' wizard to create a draft bill or run 'Link to existing bill' to link the XML file to an already (automatically) created bill

In the incoming electronic bill files list you will see, by default, files to be registered. These are files not yet linked to one or more bills.
