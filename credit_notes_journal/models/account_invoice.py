from odoo import models, fields, api
from odoo.addons.account.models.account_invoice import TYPE2JOURNAL, TYPE2REFUND
from odoo.exceptions import UserError

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    I_TYPE_2_J_TYPE = {
        'out_invoice': ['sale'],
        'out_refund': ['sale'],
        'in_refund': ['purchase'],
        'in_invoice': ['purchase']
    }

    @api.model
    def _default_journal(self):

        context = self.env.context

        default_journal_id = context.get('default_journal_id', False)

        if default_journal_id:
            # Return the default journal set in the context if any
            selected_journal = self.env['account.journal'].browse(default_journal_id)

        else:
            company = self.env['res.company'].browse(context.get('company_id', self.env.user.company_id.id))
            currency_id = context.get('default_currency_id') or company.currency_id.id

            inv_type = context.get('inv_type', context.get('type', 'out_invoice'))
            inv_types = inv_type if isinstance(inv_type, list) else [inv_type]

            is_refund = 'in_refund' in inv_types or 'out_refund' in inv_types

            # Building domain clauses
            d_clause_journal_type = [('type', 'in', [TYPE2JOURNAL[ty] for ty in inv_types if ty in TYPE2JOURNAL])]

            d_clause_company = [('company_id', '=', company.id)]

            d_clause_currency = [('currency_id', '=', currency_id)]
            if currency_id == company.currency_id.id:
                d_clause_currency = ['|', ('currency_id', '=', False)] + d_clause_currency
            # end if

            if is_refund and company.enable_credit_note_registrations:
                d_clause_credit_note_journal = ['|', ('refund_sequence', '=', True), ('is_refund_journal', '=', True)]
            else:
                d_clause_credit_note_journal = []
            # end if

            # Retrieving journals
            journal_with_currency = self.env['account.journal'].search(
                d_clause_journal_type + d_clause_company + d_clause_credit_note_journal + d_clause_currency,
                limit=1
            )
            journal_no_currency = self.env['account.journal'].search(
                d_clause_journal_type + d_clause_company + d_clause_credit_note_journal,
                limit=1
            )

            # Selecting journal
            if journal_with_currency:
                selected_journal = journal_with_currency
            else:
                selected_journal = journal_no_currency
            # end if
        # end if
        if not selected_journal:
            raise UserError('You have to select a default journal!')
        return selected_journal

    # end _default_journal

    @api.model
    def create(self, vals):
        inv_type = vals.get('type', False)
        if inv_type and inv_type in ('out_refund', 'in_refund'):
            self = self.with_context(inv_type=inv_type)
            journal = self._default_journal()
            vals['journal_id'] = journal.id
        return super(AccountInvoice, self).create(vals)

    journal_id = fields.Many2one(
        comodel_name='account.journal',
        default=_default_journal,
        domain="""[
            '&',
                '&',
                    ('type', 'in',
                        {
                            'out_invoice': ['sale'],
                            'out_refund': ['sale'],
                            'in_refund': ['purchase'],
                            'in_invoice': ['purchase'],
                        }.get(type, [])
                    ),
                    ('company_id', '=', company_id),
                '|',
                    {
                        'out_refund': ('type', '=', False),
                        'in_refund': ('type', '=', False),
                    }.get(type, (1, '=', 1)),
                    '|',
                        ('config_enable_credit_note_registrations', '=', False),
                        '|',
                            ('refund_sequence', '=', True),
                            ('is_refund_journal', '=', True),
        ]"""
    )
# end AccountInvoice
