# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_refund_journal = fields.Boolean(string='Registro per note di credito')
    hide_refund = fields.Boolean(compute='_compute_refund', store=True)

    # Link al campo inserito in configurazione, è necessario per i domain dinamici sui journal
    config_enable_credit_note_registrations = fields.Boolean(
        related='company_id.enable_credit_note_registrations'
    )

    @api.onchange('refund_sequence', 'is_refund_journal')
    def _onchange_refund(self):
        if self.is_refund_journal and self.refund_sequence:

            # Restore previous state
            # (using update instead of write because we are working on an in memory pseudo-record)
            self.update({
                'is_refund_journal': self._origin.is_refund_journal,
                'refund_sequence': self._origin.refund_sequence
            })

            # Notify the user of the error
            return {'warning': {
                'title': 'Warning',
                'message': (
                    'Puoi selezionare solo uno tra `Registro per note di credito` '
                    'e `Sequenza per note di credito`. Verranno ripristinati i '
                    'valori originali.'
                )
            }}

    @api.depends('company_id.enable_credit_note_registrations')
    def _compute_refund(self):
        for journal in self:
            journal.hide_refund = not self.env.user.company_id.enable_credit_note_registrations
