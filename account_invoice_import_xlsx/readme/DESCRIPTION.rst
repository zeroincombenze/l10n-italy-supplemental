Import invoices from Excel
--------------------------

This module imports invoice data from an Excel (.xlsx) file in two ways:

* **Import lines into an invoice**: the button [Import xlsx] on a draft invoice or
  vendor bill adds one line per row of the file. Products are searched by code and
  name; price, account and taxes come from the product unless the file supplies them.
* **Create invoices**: the menu *Accounting › Configuration › Import Account Invoice*
  creates draft invoices. A row with customer data starts a new invoice; rows
  without customer data add lines to it.

Recognized column titles:

* ``Denominazione Cliente``: Partner name
* ``Partita Iva``: Partner VAT number (``IT`` is added to digits only)
* ``Codice Fiscale``: Partner fiscal code
* ``Codice``: Product code
* ``Nome``: Line description
* ``Quantita``: Quantity
* ``Imponibile``: Taxable amount (line with quantity 1)
* ``Iva``: Tax amount; nearest rate among 0, 4, 5, 10, 22% is used
* ``Numero``: Invoice number
* ``Data``: Invoice date (dd/mm/yyyy or Excel date)

Numbers can be written in Italian format (``2.049,18``).
You can find Excel examples in the example directory.
