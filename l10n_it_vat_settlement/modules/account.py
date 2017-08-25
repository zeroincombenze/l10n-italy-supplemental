# -*- coding: utf-8 -*-
# Copyright 2017 Didotech srl (<http://www.didotech.com>)
#                Andrei Levin <andrei.levin@didotech.com>
#                Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo-Italia.org Community
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.osv import fields, orm
from openerp.tools.translate import _


class AccountVatPeriodEndStatement(orm.Model):
    _inherit = 'account.vat.period.end.statement'

    def action_cancel(self, cr, uid, ids, context=None):
        for vat_statement in self.browse(cr, uid, ids, context):
            if vat_statement:
                raise orm.except_orm(
                    _('Error!'),
                    _('You should delete VAT Settlement before deleting Vat Period End Statement')
                )
        return super(AccountVatPeriodEndStatement, self).action_cancel(cr, uid, ids, context)

    _columns = {
        'vat_settlement_attachment_id': fields.many2one(
            'account.vat.settlement.attachment',
            'VAT Settlement Export File',
            readonly=True
        )
    }

    def copy(self, cr, uid, ids, defaults, context=None):
        context = {} if context is None else context
        defaults['vat_settlement_attachment_id'] = False
        return super(AccountVatPeriodEndStatement, self).copy(
            cr, uid, ids, defaults, context)


class AccountVatSettlementAttachment(orm.Model):
    _name = "account.vat.settlement.attachment"
    _description = "Vat Settlement Export File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']

    _columns = {
        'ir_attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', required=True, ondelete="cascade"),
        'vat_statement_ids': fields.one2many(
            'account.vat.period.end.statement', 'vat_settlement_attachment_id',
            string="VAT Statements", readonly=True),
    }
