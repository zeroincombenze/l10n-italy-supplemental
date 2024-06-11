This module replaces the standard Odoo function ``get_taxes_values()``
of the module *account*. The function, revaluate precisely the tax amound depending on
base amount. This behavior is due to avoid refusing invocie from Italian Tax Authority
which check tax amount MUST be: base amount * tax rate +/- 1 cent
For this reason, this module depends on specific 10.0.1.1.2 version of *account*
