# Copyright 2019-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def inv_line_characteristic_hashcode(self, invoice_line):
        return '%s-%s-%s' % (
                super().inv_line_characteristic_hashcode(invoice_line),
                invoice_line.get('accrual_start_date', 'False'),
                invoice_line.get('accrual_end_date', 'False'),
        )

    @api.model
    def line_get_convert(self, line, part):
        """Copy from invoice to move lines"""
        res = super().line_get_convert(line, part)
        res['accrual_start_date'] = line.get('accrual_start_date', False)
        res['accrual_end_date'] = line.get('accrual_end_date', False)
        return res

    @api.model
    def invoice_line_move_line_get(self):
        """Copy from invoice line to move lines"""
        res = super().invoice_line_move_line_get()
        line_model = self.env['account.invoice.line']
        for item in res:
            invline = line_model.browse(item['invl_id'])
            item['accrual_start_date'] = invline.accrual_start_date
            item['accrual_end_date'] = invline.accrual_end_date
        return res


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    accrual_start_date = fields.Date()
    accrual_end_date = fields.Date()

    @api.model
    def get_actual_val(self, vals, name, layer=None, ttype=None):
        """Get real value from vals or from record
        @layer: 'onchange', 'create', 'write', 'validate', 'post'
        @ttype: 'company', 'company_id', 'many2one', 'id', 'date', 'datetime'
        """
        if name in vals:
            if ttype == 'date' and vals[name] and isinstance(vals[name], str):
                return datetime.datetime.strptime(
                    vals[name], '%Y-%m-%d').date()
            elif (isinstance(vals[name], int) and
                  hasattr(self, name) and
                  ttype in ('company', 'company_id', 'many2one', 'id')):
                return getattr(self, name).browse(vals[name])
            return vals[name]
        elif layer != 'create' and self and len(self) == 1:
            if ttype == 'company_id':
                if self[name]:
                    return self[name].id
                return self.env.user.company_id.id
            elif ttype == 'id':
                if self[name]:
                    return self[name].id
                return False
            else:
                return self[name]
        elif ttype == 'company_id':
            return self.env.user.company_id.id
        return False

    @api.model
    def show_error(self, vals, message, title, layer=None):
        if layer != 'onchange':
            raise UserError(message)
        warning_mess = {
            'title': title,
            'message': message
        }
        return {
            'warning': warning_mess,
            'values': vals,
        }

    @api.model
    def ret_by_layer(self, vals, layer=None):
        if layer != 'onchange':
            return vals
        return {
            'values': vals,
        }

    @api.model
    def check_n_set(self, vals, layer=None):
        accrual_start_date = self.get_actual_val(vals, 'accrual_start_date',
                                                 ttype='date', layer=layer)
        accrual_end_date = self.get_actual_val(vals, 'accrual_end_date',
                                               ttype='date', layer=layer)
        if not accrual_start_date and not accrual_end_date:
            return vals
        if not accrual_start_date and layer == 'onchange':
            return vals
        if accrual_start_date and not accrual_end_date:
            return self.show_error(vals,
                                   'Missing Accrual End Date',
                                   'Accrual dates!', layer=layer)
        if not accrual_start_date and accrual_end_date:
            return self.show_error(vals,
                                   'Missing Accrual Start Date',
                                   'Accrual dates!', layer=layer)
        if accrual_start_date > accrual_end_date:
            return self.show_error(vals,
                                   'Invalid Accrual Date',
                                   'Accrual dates!', layer=layer)
        return self.ret_by_layer(vals, layer=layer)

    @api.onchange('fiscalyear_id', 'date', 'date_invoice')
    def _onchange_date_fiscalyear_id(self):
        return self.check_n_set({}, layer='onchange')

    @api.model
    def create(self, vals):
        vals = self.check_n_set(vals, layer='create')
        return super().create(vals)

    @api.multi
    def write(self, vals):
        vals = self.check_n_set(vals, layer='write')
        super().write(vals)
