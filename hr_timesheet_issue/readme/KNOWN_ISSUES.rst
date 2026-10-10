For historical reasons, `partner_id` in analytic line cannot be assigned to the customer
of the project or the customer of the task. This module use *analytic_partner* module
that use `other_partner_id` field for this purpose.

This module hasn't been tested with *account_analytic_distribution* module
installed, so maybe it's incompatible with it.
