
from odoo.addons.account_common_mixin.engine.compute_iban import (
    get_company_bank_account, get_counterparty_bank_account
)

from ..engine.compute_iban import (
    get_bank_2_print
)


from odoo import api, fields
from odoo.addons.account_common_mixin.models.mixin_base import BaseMixin


class PrintMixin(BaseMixin):

    bank_2_print_selector = fields.Selection(
        string='Tipo stampa IBAN',
        selection=[
            ('ni', 'Non indicato'),
            ('partner', 'Partner'),
            ('company', 'Azienda'),
        ],
        default=False,
        copy=True,
    )

    bank_2_print = fields.One2many(
        string='Banca da utilizzare in stampa / XML',
        comodel_name='res.partner.bank',
        readonly=True,
        compute='_compute_bank_2_print',
    )

    @api.multi
    def adapt_document(self):
        """Must be implemented by subclass"""
        self.ensure_one()
        raise NotImplemented()
    # end adapt_document

    @api.onchange('bank_2_print_selector')
    def _iban_onchange_bank_2_print_selector(self):

        if not self._must_process_event('_iban_onchange_bank_2_print_selector'):

            # Change the partner bank domain
            domain_filters = self._get_domains()
            return domain_filters

        # end if

    # end _iban_onchange_bank_2_print_selector

    @api.multi
    def _compute_bank_2_print(self):

        for doc in self:

            if not doc.bank_2_print_selector:
                doc.bank_2_print = False
            elif doc.bank_2_print_selector == 'ni':
                doc.bank_2_print = False
            elif doc.bank_2_print_selector == 'partner':
                doc.bank_2_print = doc.counterparty_bank_id
            elif doc.bank_2_print_selector == 'company':

                if doc.company_bank_id.id:
                    # Campo company_bank_id ha un valore: stampo quello
                    doc.bank_2_print = doc.company_bank_id
                else:
                    # Campo company_bank_id NON ha un valore: stampo tutte le banche dell'azienda
                    bank_model = self.env['res.partner.bank']
                    company_p = doc.company_id.partner_id
                    company_banks = bank_model.search(
                        [
                            ('partner_id', '=', company_p.id),
                            ('part_of_default_banks_2_print', '=', True)
                        ]
                    )
                    doc.bank_2_print = company_banks
            else:
                assert False
            # end if
        # end for

    # end _compute_bank_2_print

    @api.multi
    def _get_domains(self):

        self.ensure_one()

        counterparty_p = self.partner_id
        company_p = self.company_id.partner_id

        # Change the partner bank domain
        domain_filters = {
            'domain': {
                'counterparty_bank_id': [
                    ('partner_id', '=', counterparty_p.parent_id.id or counterparty_p.id)
                ],
                'company_bank_id': [
                    ('partner_id', '=', company_p.id),
                    ('bank_is_wallet', '=', False)
                ],
            },
        }

        return domain_filters
    # end _get_domains

    @api.multi
    def _update_iban(self):

        super()._update_iban()

        for doc in self:

            # Specify the type of "doc" variable so PyCharm stops
            # complaining about calling a protected method
            doc: PrintMixin

            # Update bank_to_print
            doc.bank_2_print_selector = get_bank_2_print(doc)

            # Update company bank and counterparty bank
            doc.company_bank_id = get_company_bank_account(doc)
            doc.counterparty_bank_id = get_counterparty_bank_account(doc)

        # end for

    # end _update_iban

    # def _must_process_event(self, event_name):
    #     """
    #         Skip the first "on_chage" event if
    #         'from_purchase_order_change'is set in context
    #     """
    #
    #     ctx = self.env.context
    #     skipped_flag_name = event_name + 'SKIPPED'
    #
    #     from_po = ctx.get('from_purchase_order_change')
    #     first_skipped = ctx.get(skipped_flag_name)
    #
    #     if from_po and not first_skipped:
    #         ctx[skipped_flag_name] = True
    #         return True
    #     else:
    #         return False
    #     # end if
    # # end _must_skip_event

# end BaseMixin


class OrderMixin(PrintMixin):
    pass
# end OrderMixin


class AccountMixin(PrintMixin):

    bank_4_xml = fields.Many2one(
        string='Banca da utilizzare in stampa / XML',
        comodel_name='res.partner.bank',
        readonly=True,
        compute='_compute_bank_4_xml',
    )

    @api.multi
    def _compute_bank_4_xml(self):

        for doc in self:

            if not doc.bank_2_print_selector:
                doc.bank_4_xml = False
            elif doc.bank_2_print_selector == 'ni':
                doc.bank_4_xml = False
            elif doc.bank_2_print_selector == 'partner':
                doc.bank_4_xml = doc.counterparty_bank_id
            elif doc.bank_2_print_selector == 'company':
                doc.bank_4_xml = doc.company_bank_id
            else:
                assert False
            # end if
        # end for

    # end _compute_bank_4_xml

    @api.multi
    def _update_iban(self):

        super()._update_iban()

        for doc in self:

            # Specify the type of "doc" variable so PyCharm stops
            # complaining about calling a protected method
            doc: AccountMixin

            # Update partner_bank_id
            doc._update_partner_bank_id()

        # end for

    # end _update_iban

    # @api.onchange('company_bank_id')
    # def _iban_onchange_company_bank_id(self):
    #
    #     if not self._must_process_event('_iban_onchange_company_bank_id'):
    #         self._update_partner_bank_id()
    #     # end if
    #
    # # end _onchange_partner_id

    # @api.onchange('counterparty_bank_id')
    # def _iban_onchange_counterparty_bank_id(self):
    #
    #     if not self._must_process_event('_iban_onchange_counterparty_bank_id'):
    #         self._update_partner_bank_id()
    #     # end if
    #
    # # end _onchange_partner_id

    @api.multi
    def _update_partner_bank_id(self):

        super()._update_partner_bank_id()
        # for doc in self:
        #
        #     doc: AccountMixin
        #
        #     comp_bnk = doc.company_bank_id
        #     ctpt_bnk = doc.counterparty_bank_id
        #
        #     # Update partner_bank_id
        #     if doc._get_doc_type() in ('out_invoice', 'out_refund') and comp_bnk:
        #         doc.partner_bank_id = comp_bnk
        #     elif doc._get_doc_type() in ('in_invoice', 'in_refund') and ctpt_bnk:
        #         doc.partner_bank_id = ctpt_bnk
        #     # end if
        # # end for

    # end _update_partner_bank_id

    @api.multi
    def _get_doc_type(self):
        """Must be implemented by subclass"""
        self.ensure_one()
        raise NotImplemented()
    # end _get_doc_type

# end FunctionsMixin
