# Copyright (c) 2021
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import pytz
import datetime as dt

from odoo import fields, models, _
from odoo.exceptions import UserError


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    def get_prefix_suffix_by_date(self, date):

        def _interpolate(s, d):
            return (s % d) if s else ''

        def _interpolation_dict(datetime_obj):
            now = range_date = effective_date = datetime_obj

            if self._context.get('ir_sequence_date'):
                effective_date = fields.Datetime.from_string(
                    self._context.get('ir_sequence_date'))

            if self._context.get('ir_sequence_date_range'):
                range_date = fields.Datetime.from_string(
                    self._context.get('ir_sequence_date_range'))

            sequences = {
                'year': '%Y',
                'month': '%m',
                'day': '%d',
                'y': '%y',
                'doy': '%j',
                'woy': '%W',
                'weekday': '%w',
                'h24': '%H',
                'h12': '%I',
                'min': '%M',
                'sec': '%S'
            }
            res = {}
            for key, format in sequences.items():
                res[key] = effective_date.strftime(format)
                res['range_' + key] = range_date.strftime(format)
                res['current_' + key] = now.strftime(format)

            return res

        date_time_obj = dt.datetime.strptime(date, '%Y-%m-%d')
        timezone = pytz.timezone(self._context.get('tz') or 'UTC')
        timezone_date_time_obj = timezone.localize(date_time_obj)

        d = _interpolation_dict(timezone_date_time_obj)
        try:
            interpolated_prefix = _interpolate(self.prefix, d)
            interpolated_suffix = _interpolate(self.suffix, d)
        except ValueError:
            raise UserError(_('Invalid prefix or suffix '
                              'for sequence \'%s\'') % (
                self.get('name')))
        return interpolated_prefix, interpolated_suffix


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_number_from_alpha(self):
        if self.state == 'draft':
            raise UserError('Conversione da alfanumerico numero ad intero non '
                            'permessa se la registrazione si trova in bozza.')

        if self.journal_id:
            value_number = self.name
            journal_seq, domain = self._get_seq_number_next_stuff()
            interpolate_pref, interpolate_postf = \
                journal_seq.get_prefix_suffix_by_date(
                    fields.Date.to_string(self.date)
                )

            if interpolate_postf in self.name:
                value_number = value_number.replace(interpolate_postf, '')
            # end if

            if interpolate_pref in self.name:
                value_number = value_number.replace(interpolate_pref, '')
            # end if

            return int(value_number)
        # end if
        return False

    def _get_seq_number_next_stuff(self):
        self.ensure_one()
        journal_sequence = self.journal_id.sequence_id
        if self.journal_id.refund_sequence:
            domain = [('type', '=', self.type)]
            journal_sequence = self.type in ['in_refund', 'out_refund'] and self.journal_id.refund_sequence_id or self.journal_id.sequence_id
        elif self.type in ['in_invoice', 'in_refund']:
            domain = [('type', 'in', ['in_invoice', 'in_refund'])]
        else:
            domain = [('type', 'in', ['out_invoice', 'out_refund'])]
        if self.id:
            domain += [('id', '<>', self.id)]
        domain += [('journal_id', '=', self.journal_id.id), ('state', 'not in', ['draft', 'cancel'])]
        return journal_sequence, domain

