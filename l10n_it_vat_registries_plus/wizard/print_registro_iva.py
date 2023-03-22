# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import models, api, _
from odoo.exceptions import Warning as UserError


class WizardRegistroIva(models.TransientModel):
    _inherit = "wizard.registro.iva"

    @api.multi
    def print_registro(self):
        self.ensure_one()
        wizard = self
        if not wizard.journal_ids:
            raise UserError(_('No journals found in the current selection.\n'
                              'Please load them before to retry!'))

        move_ids = self._get_move_ids(wizard)
        # check tax in lines
        self.check_tax_amounts_by_tax_id(move_ids)

        # check move line number / date
        activate_to_check = (self.filter_date == 'date')
        if activate_to_check:

            to_check = self.check_move_ids(move_ids)

            if to_check:
                lines = []
                for warn in to_check:
                    lines.append((0, 0, warn))

                wz_id = self.env['wizard.confirm.print.journal'].create({
                    'wizard_id': wizard.id,
                    'reason_lines': lines
                })

                model = 'l10n_it_vat_registries_plus'
                wiz_view = self.env.ref(
                    model + '.wizard_confirm_print_journal'
                )
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Conferma anomalie',
                    'res_model': 'wizard.confirm.print.journal',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': wiz_view.id,
                    'target': 'new',
                    'res_id': wz_id.id,
                    'close_on_report_download': True,
                    # 'key2': 'client_action_multi',
                    # 'binding_model_id': model + '.model_account_move_line',
                    'context': {'active_id': wizard},
                }
            # end if
        # end if

        return super().print_registro()

    def check_move_ids(self, move_ids):
        to_check = []
        prev_num = False
        prev_fy = False
        is_first = True
        for move_id in move_ids:
            move = self.env['account.move'].search([('id', '=', move_id)])
            number = move.get_number_from_alpha()
            fiscal_year = move.fiscalyear_id
            if prev_fy != fiscal_year and is_first is False:
                is_first = True

            if is_first:
                is_first = False
            else:
                if prev_fy == fiscal_year:
                    if number != (prev_num + 1):
                        to_check.append({
                            'number': move.name,
                            'date_document': move.date.strftime("%d-%m-%Y"),
                            'reason': 'Errato ordinamento del numero '
                        })

            prev_num = number
            prev_fy = fiscal_year

        return to_check

    def check_tax_amounts_by_tax_id(self, account_move_list):
        for move_id in account_move_list:
            move = self.env['account.move'].browse(move_id)
            for move_line in move.line_ids:
                if not(move_line.tax_line_id or move_line.tax_ids):
                    continue
                if move_line.tax_ids and len(move_line.tax_ids) != 1:
                    raise UserError(
                        "La riga di movimento {movimento} della registrazione"
                        " {registrazione} contiene troppi codici"
                        " imponibili".format(movimento=move_line.name,
                                             registrazione=move.display_name)
                        )

    def print_registro_super(self):
        action = super().print_registro()
        action.update({'close_on_report_download': True})
        return action
