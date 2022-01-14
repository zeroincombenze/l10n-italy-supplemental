Account Opening Import
----------_-----------

Import account opening from Excel file.

Excel file must have following structure:

.. $include example_excel.rst

Notes:

* Please, import just xlsx files
* The labels of the header must be exactly as you see above
* Please set 1 in one of "Cliente" or "Fornitore" for partner lines
* Please set only one value in one of "Dare" "Avere"
* Partners search try to find by vat code and name
* In partner lines, account code is set by partner record if not in line
* Ref field i snot required; use it if you want load amount by invoices

You can find Excel example in example directory.