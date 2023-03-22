# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import api, models
from odoo.tools.misc import formatLang


class AccountPaymentOrderReportFinancing(models.AbstractModel):
    _name = 'report.account_banking_invoice_financing.print_apo_main_ita'
    _description = 'Custom technical model for printing payment order'

    @api.model
    def _get_bank_account_name(self, partner_bank):
        if partner_bank:
            name = ''
            if partner_bank.bank_name:
                name = '%s: ' % partner_bank.bank_id.name
            if partner_bank.acc_number:
                name = '%s %s' % (name, partner_bank.acc_number)
                if partner_bank.bank_bic:
                    name = '%s - ' % (name)
            if partner_bank.bank_bic:
                name = '%s BIC %s' % (name, partner_bank.bank_bic)
            return name
        else:
            return False

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.payment.order'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'account.payment.order',
            'docs': docs,
            'data': data,
            'env': self.env,
            'get_bank_account_name': self._get_bank_account_name,
            'formatLang': formatLang,
        }
