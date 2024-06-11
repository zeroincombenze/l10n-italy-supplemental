This module evaluate invoices taxes to comply italian laws and avoid refuse from
Italian Tax Authority.

Odoo standard evaluate tax line by line and at the end sum all values. This behavior
produces a little difference between tax evaluated from total base and the sum of
taxes.

Look at the following example:

.. $include example.csv

Odoo return the total base  27.96 (as sum of subtotal rounded)and total tax 6.14 (as
sum of taxes) but the total tax revaluate on 27.96 is 6.15

Odoo configuration "Round globally" solve when invoice is created but after update it
does not work.
