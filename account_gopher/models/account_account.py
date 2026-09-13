#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from odoo import _, models
from odoo.exceptions import UserError


class AccountAccount(models.Model):
    _inherit = "account.account"

    def gopher_reload_coa(self, html_txt=None):
        """Reload account records from the company's chart template.

        TODO: this used to browse ``account.account.template`` records
        (``company.chart_template_id`` -> template lines) and diff them
        against existing ``account.account`` records. Since Odoo 17.0 the
        whole chart-of-accounts-template mechanism was rewritten: there is
        no more browsable ``account.account.template`` model, no more
        ``company.chart_template_id`` many2one, and ``account.account``
        no longer has ``user_type_id``/``group_id`` as plain writable
        fields (``group_id`` is now computed; the account type lives in
        ``account_type``). Chart data is now produced on the fly by
        ``AccountChartTemplate._get_chart_template_data(company.chart_template)``
        as a dict of xmlid -> field-value dicts, not a queryable
        recordset, so the former diff-and-write logic cannot be ported
        mechanically. Left unimplemented on purpose rather than guessing
        a behavior; needs a deliberate redesign around the new chart
        template API before this option can be re-offered in the wizard.
        """
        raise UserError(
            _(
                "Reloading the Chart of Accounts from the chart template is "
                "not available in this version: Odoo removed the "
                "'account.account.template' model and 'chart_template_id' "
                "field this feature relied on. This needs to be redesigned "
                "around 'AccountChartTemplate._get_chart_template_data()'."
            )
        )
