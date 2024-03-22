# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
import logging

from odoo import api, models

from odoo.addons.l10n_it_balance.wizard.generate_balance import (
    INDENTING_SPACE as INDENTING_SPACE,
    SEQ2_INCR as SEQ2_INCR,
    SEQ2_LAST as SEQ2_LAST
)

_logger = logging.getLogger(__name__)


class WizardGenerateBalance(models.TransientModel):
    _inherit = "wizard.generate.balance"

    @api.multi
    def generate_balance(self):
        active_id = self._context.get('active_id')
        wizard = self
        evaluate_accrual = wizard.evaluate_accrual
        if not evaluate_accrual:
            return super().generate_balance()

        wz_message = self.check_missing_depreciation_by_date()

        wz_id = self.env['wizard.confirm.depreciation'].create(
            {
                'wizard_id': wizard.id,
                'message': wz_message,
            }
        )

        model = 'l10n_it_balance_assets'
        wiz_view = self.env.ref(model + '.wizard_confirm_depreciation')
        if wz_message:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Conferma anomalie',
                'res_model': 'wizard.confirm.depreciation',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': wiz_view.id,
                'target': 'new',
                'res_id': wz_id.id,
                # 'key2': 'client_action_multi',
                # 'binding_model_id': model + '.model_account_move_line',
                'context': {'active_id': active_id},
            }

        self.do_generate()

    # end generate_balance

    def check_missing_depreciation_by_date(self):
        active_id = self._context.get('active_id')
        warnings = ''
        adb = self.env['asset.depreciation.balance']
        balance = self.env['italy.account.balance'].browse(active_id)
        assets = self.env['asset.asset'].search([])
        for asset in assets:
            if asset.depreciation_ids:
                for adp in asset.depreciation_ids:

                    if not adb.is_valid_appreciation(asset, adp, balance.date_to):
                        continue

                    adp_date = adp.last_depreciation_date
                    if adp_date:
                        how_many_years = balance.date_to.year - adp_date.year
                        if how_many_years > 1:
                            years = []
                            for i in range(adp_date.year + 1, balance.date_to.year):
                                years.append(str(i))
                            asset_name = asset.name
                            warnings += 'Per il bene "{bene}" l\'ultimo '.format(
                                bene=asset_name
                            )
                            warnings += 'ammortamento è stato '
                            warnings += ' effettuato in data {data} \n'.format(
                                data=adp_date.strftime("%d-%m-%Y")
                            )
                            if years:
                                warnings += 'Ammortamenti mancanti'
                                warnings += ' per gli anni: '
                                warnings += ' '.join(years) + '\n'
                    # end if
                # end for
            # end if
        # end for
        return warnings

    # check_missing_depreciation_by_date

    def do_generate(self):
        active_id = self._context.get('active_id')
        balance = self.env['italy.account.balance'].browse(active_id)
        date_end = balance.date_to
        asset_model = self.env['asset.asset']
        asset_dp_model = self.env['asset.depreciation.balance']
        asset_diff_model = self.env['asset.category.difference']

        # pulizia
        query = 'DELETE FROM asset_depreciation_balance WHERE balance_id = {}'.format(
            active_id
        )
        self.env.cr.execute(query)

        query = 'DELETE FROM asset_category_difference WHERE balance_id = {}'.format(
            active_id
        )
        self.env.cr.execute(query)

        # caricamento asset
        assets = asset_model.search([('purchase_date', '<=', date_end)])
        for asset in assets:
            asset_dp_model.load_asset_depreciations(asset, date_end, balance)
        # end for

        asset_diff_model.load_differences(self.company_id, active_id)

        return super().generate_balance()

    def write_depreciations(self, params):
        super().write_depreciations(params)
        conf = self.env['res.company'].browse(self.company_id.id)
        civilistico = conf.compute_civilistico()

        _logger.info('adding amount depreciated to balance')

        def add_line_values(line, vals):
            if 'amount_start' in vals and not vals['amount_start']:
                vals['amount_start'] = 0.0
            if self.balance_type == 'trial':
                vals['amount_debit'] += line.amount_debit
                vals['amount_credit'] += line.amount_credit
                vals['amount_balance'] = (
                    line.amount_start + vals['amount_debit'] - vals['amount_credit']
                )
            else:
                vals['amount_debit'] = vals['amount_credit'] = 0.0
                vals['amount_balance'] += line.amount_balance
            return vals

        def get_credit_account(dep_balance_rec):
            if dep_balance_rec.mode_id.indirect_depreciation:
                credit_account = dep_balance_rec.category_id.fund_account_id
            else:
                credit_account = dep_balance_rec.category_id.asset_account_id
            # end if
            return credit_account

        # end _get_credit_account

        def get_debit_account(dep_balance_rec):
            return dep_balance_rec.category_id.depreciation_account_id

        # end _get_debit_account

        # COMMON DATA
        #

        level_balance = 3
        balance_id = params['active_id']

        rows = self.env['asset.depreciation.balance'].search(
            [('balance_id', '=', balance_id), (
                'type_id', '=', civilistico)]
        )
        for adp in rows:
            credit_account_id = get_credit_account(adp)
            debit_account_id = get_debit_account(adp)

            # DEBIT DATA
            #
            line_model = self.env['italy.account.balance.line.expense']

            if debit_account_id.group_id and debit_account_id.group_id.id:
                parent_id = debit_account_id.group_id.id
            else:
                parent_id = None
            account_id = debit_account_id.id
            account_nature = debit_account_id.nature
            code = debit_account_id.code
            name = debit_account_id.name
            seq1 = self.seq1[account_nature]
            self.seq2[account_nature] += SEQ2_INCR
            seq2 = self.seq2[account_nature]

            vals_debit = {
                'nature': account_nature,
                'seq1': seq1,
                'seq2': seq2,
                'balance_id': balance_id,
                'code': code,
                'name': '{}{}'.format(INDENTING_SPACE * level_balance, name),
                'to_delete': False,
                'parent_id': parent_id,
                'account_id': account_id,
                'level_balance': level_balance,
                'amount_start': 0.0,
                'amount_debit': adp.amount_current,
                'amount_credit': 0.0,
                'amount_balance': adp.amount_current,
            }

            line = line_model.search(
                [('code', '=', code), ('balance_id', '=', balance_id)]
            )
            if line:
                vals_debit = add_line_values(line, vals_debit)
                line.write(vals_debit)
            else:
                line_model.create(vals_debit)

            # CREDIT DATA
            account_nature = credit_account_id.nature
            line_model = self.line_model[account_nature]

            if credit_account_id.group_id and credit_account_id.group_id.id:
                parent_id = credit_account_id.group_id.id
            else:
                parent_id = None

            account_id = credit_account_id.id
            code = credit_account_id.code
            name = credit_account_id.name
            seq1 = self.seq1[account_nature]
            self.seq2[account_nature] += SEQ2_INCR
            seq2 = self.seq2[account_nature]

            vals_credit = {
                'nature': account_nature,
                'seq1': seq1,
                'seq2': seq2,
                'balance_id': balance_id,
                'code': code,
                'name': '{}{}'.format(INDENTING_SPACE * level_balance, name),
                'to_delete': False,
                'parent_id': parent_id,
                'account_id': account_id,
                'level_balance': level_balance,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': adp.amount_current,
                'amount_balance': adp.amount_current,
            }

            line = line_model.search(
                [('code', '=', code), ('balance_id', '=', balance_id)]
            )

            if line:
                vals_credit = add_line_values(line, vals_credit)
                line.write(vals_credit)
            else:
                line_model.create(vals_credit)

    # end write_depreciations

    def write_L_n_P(self, params, sel=None):
        super().write_L_n_P(params, sel)
        if not self.evaluate_accrual:
            return

        lines = self.env['asset.category.difference'].search([
            ('balance_id', '=', params['active_id'])
        ])

        diff_amt_civilistico = sum(lines.mapped('amount_current_civilistico'))
        diff_amt_fiscale = sum(lines.mapped('amount_current_fiscale'))
        difference_amount_balance = sum(lines.mapped('amount_balance'))

        nature_LP = 'R' if self.seq1['R'] > self.seq1['C'] else 'C'

        amount_fpf = self.loss_profit + diff_amt_civilistico - diff_amt_fiscale

        if difference_amount_balance == 0:
            vals = self.get_balance_vals_fiscal(params, nature_LP)
        else:
            if amount_fpf > 0:
                vals = self.get_profit_vals_fiscal(
                    params, nature_LP, amount_fpf)
            else:
                vals = self.get_loss_vals_fiscal(
                    params, nature_LP, amount_fpf)
            # end if
        # end fi

        self.write_1_line(vals, sel=sel)

    def get_loss_vals_fiscal(self, params, nature, difference):
        vals = {
            'nature': nature,
            'seq1': self.seq1[nature],
            'seq2': SEQ2_LAST - 1,
            'code': '!',
            'name': '* PERDITA - FISCALE *',
            'balance_id': params['active_id'],
            'to_delete': False,
            'amount_start': 0.0,
            'amount_debit': 0.0,
            'amount_credit': 0.0,
            'level_balance': '0',
        }
        if ((self.balance_type in ('ordinary', 'opposite') and
             nature == 'R') or
                (self.balance_type not in ('ordinary', 'opposite') and
                 nature == 'C')):
            vals['amount_balance'] = -difference
        else:
            vals['amount_balance'] = difference

        return vals

    def get_profit_vals_fiscal(self, params, nature, difference):
        vals = {
            'nature': nature,
            'seq1': self.seq1[nature],
            'seq2': SEQ2_LAST - 1,
            'code': '!',
            'name': '* UTILE - FISCALE *',
            'balance_id': params['active_id'],
            'to_delete': False,
            'amount_start': 0.0,
            'amount_debit': 0.0,
            'amount_credit': 0.0,
            'level_balance': '0',
        }
        if ((self.balance_type in ('ordinary', 'opposite') and
             nature == 'R') or
                (self.balance_type not in ('ordinary', 'opposite') and
                 nature == 'C')):
            vals['amount_balance'] = -difference
        else:
            vals['amount_balance'] = difference

        return vals

    def get_balance_vals_fiscal(self, params, nature):
        vals = {
            'nature': nature,
            'seq1': self.seq1[nature],
            'code': '!',
            'name': '* TOTALE A PAREGGIO - FISCALE *',
            'balance_id': params['active_id'],
            'to_delete': False,
            'amount_start': 0.0,
            'amount_debit': 0.0,
            'amount_credit': 0.0,
            'amount_balance': 0.0,
            'level_balance': '0',
        }
        return vals
