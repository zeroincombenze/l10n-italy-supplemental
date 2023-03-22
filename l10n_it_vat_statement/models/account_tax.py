# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class AccountTax(models.Model):
    _inherit = 'account.tax'

    vat_statement_account_id = fields.Many2one(
        'account.account',
        "Account used for VAT statement",
        help="The tax balance will be "
             "associated to this account after selecting the period in "
             "VAT statement"
    )

    # def _compute_totals_tax(self, data):
    #     """
    #     Args:
    #         data: date range, journals and registry_type
    #     Returns:
    #         A tuple: (tax_name, base, tax, deductible, undeductible)
    #
    #     """
    #     self.ensure_one()
    #     context = {
    #         'from_date': data['from_date'],
    #         'to_date': data['to_date'],
    #     }
    #     registry_type = data.get('registry_type', 'customer')
    #     if data.get('journal_ids'):
    #         context['vat_registry_journal_ids'] = data['journal_ids']
    #
    #     tax = self.env['account.tax'].with_context(context).browse(self.id)
    #     tax_name = tax._get_tax_name()
    #     if not tax.children_tax_ids:
    #         base_balance = tax.base_balance
    #         balance = tax.balance
    #         if registry_type == 'supplier':
    #             base_balance = -base_balance
    #             balance = -balance
    #         if not tax.account_id:
    #             deductible = 0
    #             undeductible = balance
    #         else:
    #             deductible = balance
    #             undeductible = 0
    #         # end if
    #
    #         return (
    #             tax_name, base_balance, balance, deductible, undeductible
    #         )
    #     else:
    #         base_balance = tax.base_balance
    #
    #         tax_balance = 0
    #         deductible = 0
    #         undeductible = 0
    #         for child in tax.children_tax_ids:
    #             child_balance = child.balance
    #             if (
    #                 (
    #                     data['registry_type'] == 'customer' and
    #                     child.cee_type == 'sale'
    #                 ) or
    #                 (
    #                     data['registry_type'] == 'supplier' and
    #                     child.cee_type == 'purchase'
    #                 )
    #             ):
    #                 # Prendo la parte di competenza di ogni registro e lo
    #                 # sommo sempre
    #                 child_balance = child_balance
    #
    #             elif child.cee_type:
    #                 continue
    #
    #             tax_balance += child_balance
    #             if child.account_id:
    #                 deductible += child_balance
    #             else:
    #                 undeductible += child_balance
    #         if registry_type == 'supplier':
    #             base_balance = -base_balance
    #             tax_balance = -tax_balance
    #             deductible = -deductible
    #             undeductible = -undeductible
    #         return (
    #             tax_name, base_balance, tax_balance, deductible, undeductible
    #         )

