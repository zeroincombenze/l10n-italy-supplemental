# Copyright 2017-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# import datetime
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    accountbrief_ids_rel = fields.One2many(related='move_id.accountbrief_ids')
    vatbrief_ids_rel = fields.One2many(related='move_id.vatbrief_ids')

    fiscalyear_id = fields.Many2one(
        'account.fiscal.year',
        string="Esercizio contabile",
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain=[('state', '!=', 'done')],
        copy=False,
    )

    # @api.multi
    # def _check_4_inv_date(self):
    #
    #     for invoice in self:
    #         if (invoice.type in ('out_invoice', 'out_refund') or
    #                 not invoice.journal_id.enable_date):
    #             if not invoice.date_apply_balance_human:
    #                 invoice.date_apply_balance = invoice.date_invoice
    #     return True

    @api.multi
    def action_get_duedates_mgmt_view(self):
        # Obtain the ID of the view in the DB
        view_id = self.env.ref(
            'account_invoice_entry_dates.'
            'view_account_move_due_dates_mini_for_invoice'
        ).id

        move_id = self.move_id.id

        # If there is a "account.move" record related to this invoice
        # open the view to manage the due dates
        if self.move_id:
            action = {
                'type': 'ir.actions.act_window',
                'name': "Gestione scadenze",

                'res_model': 'account.move',
                'res_id': move_id,

                'view_mode': 'form',
                'view_id': view_id,

                'target': 'new',
            }

            return action

        else:
            raise UserError(
                'Per poter creare delle scadenze è necessario creare il record '
                'contabile della fattura.'
            )

        # end if

    # end get_duedates_mgmt_view

    def action_accountbrief_update(self):
        if self.move_id:
            self.move_id.action_accountbrief_update()
        else:
            raise UserError(
                'Non è possibile aggiornare la prima nota di una fattura senza'
                'movimento contabile. Validare la fattura e riprovare.'
            )
        # end if
    # end action_update_accountbrief

    def action_vatbrief_update(self):
        if self.move_id:
            self.move_id.action_vatbrief_update()
        else:
            raise UserError(
                'Non è possibile aggiornare il riepilogo IVA di una fattura'
                'senza movimento contabile. Validare la fattura e riprovare.'
            )
        # end if
    # end action_update_accountbrief

    # Non ancora implementato, da implementare quando verrà abilitato il
    # pulsante per la creazione della registrazione contabile "temporanea"
    # @api.multi
    # def action_invoice_draft_move(self):
    #     pass
    # # end action_invoice_draft_move

# end AccountInvoice
