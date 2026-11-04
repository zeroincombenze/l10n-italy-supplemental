When a vendor bill or refund is validated, standard Odoo rejects it if another
bill/refund of the same supplier has the same vendor reference, whatever its date.

Italian suppliers restart their invoice numbering every year, so the same number
comes back each year. This module rejects a vendor reference as duplicated only
when it is found in the **same calendar year** as the invoice date.
If the invoice date is empty, the current year is used.
