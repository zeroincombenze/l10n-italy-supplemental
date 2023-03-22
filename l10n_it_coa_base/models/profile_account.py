# Copyright 2019-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# import datetime
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License LGPL-3 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
#

from odoo import api, fields, models
import logging
# from odoo.exceptions import UserError, Warning
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class ItalyProfileAccount(models.Model):
    _name = 'italy.profile.account'
    _description = 'Profilo contabile'

    @api.depends('coa_toplevel_len', 'coa_level2_len', 'coa_lowlevel_len')
    def _compute_len_coa(self):
        for profile in self:
            profile.coa_len = (profile.coa_toplevel_len +
                               profile.coa_level2_len +
                               profile.coa_lowlevel_len)

    def _compute_coa_fixed(self):
        self.coa_fixed = (len(self.env['account.account'].search(
            [('company_id', '=', self.company_id.id)])) > 0)

    @api.model
    def _prepayment_domain(self, nature):
        domain = ['|', ('name', 'ilike', 'prepayments'),
                  ('name', 'ilike', 'risconti')]

        types = self.env['account.account.type'].search(domain).ids
        domain = [('user_type_id', 'in', types),
                  ('nature', '=', nature)]
        return domain

    name = fields.Char('Name')
    company_id = fields.Many2one(
        'res.company', 'Azienda',
        required=True,
        help="Azienda a cui applicare questo profilo contabile",
    )
    # Deprecated
    coa_toplevel_len = fields.Integer(
        'N. di caratteri mastro',
        help='Numero di caratteri che compongono il mastro\n'
             'La lunghezza del conto è la somma delle lunghezze\n'
             'del mastro, del capoconto e del sottoconto.',
        default=2)
    # Deprecated
    coa_level2_len = fields.Integer(
        'N. di caratteri capoconto',
        help='Numero di caratteri che compongono il capoconto\n'
             'La lunghezza del conto è la somma delle lunghezze\n'
             'del mastro, del capoconto e del sottoconto.',
        default=1)
    # Deprecated
    coa_lowlevel_len = fields.Integer(
        'N. di caratteri sottoconto',
        help='Numero di caratteri che compongono il sottoconto\n'
             'La lunghezza del conto è la somma delle lunghezze\n'
             'del mastro, del capoconto e del sottoconto.',
        default=3)
    # Deprecated
    coa_len = fields.Integer(
        'N. di caratteri conto',
        help='Numero di caratteri del conto\n'
             'risultato della somma delle lunghezze\n'
             'del mastro, del capoconto e del sottoconto.',
        readonly=True,
        compute=_compute_len_coa)
    coa_fixed = fields.Boolean('Pdc fissato', compute=_compute_coa_fixed)
    coa_zero = fields.Boolean('Codici con zero', default=False)

    cutoff_active = fields.Many2one(string="Rateo attivo",
                                    comodel_name="account.account",
                                    domain=[
                                        ('nature', '=', 'A')],
                                    default='')
    cutoff_passive = fields.Many2one(string="Rateo passivo",
                                     comodel_name="account.account",
                                     domain=[
                                         ('nature', '=', 'P')],
                                     default='')
    prepayment_active = fields.Many2one(
        string="Risconto attivo",
        comodel_name="account.account",
        domain=lambda self: self._prepayment_domain('A'),
        default='')
    prepayment_passive = fields.Many2one(
        string="Risconto passivo",
        comodel_name="account.account",
        domain=[('nature', '=', 'P')],
        default='')
    invtobericeived_active = fields.Many2one(
        string="Fatture clienti da emettere",
        comodel_name="account.account",
        domain=[('nature', '=', 'A')],
        default='')
    invtobericeived_passive = fields.Many2one(
        string="Fatture fornitori da ricevere",
        domain=[('nature', '=', 'P')],
        comodel_name="account.account",
        default='')
    refundtobericeived_active = fields.Many2one(
        string="NC fornitori da ricevere",
        domain=[('nature', '=', 'A')],
        comodel_name="account.account",
        default='')
    refundtobericeived_passive = fields.Many2one(
        string="NC clienti da emettere", comodel_name="account.account",
        domain=[('nature', '=', 'P')],
        default='')
    # default_account_payable = fields.Many2one(
    #     string="Conto principale di debito", comodel_name="account.account",
    #     domain=[('internal_type', '=', 'payable')],
    #     required=True,
    #     default='')
    # default_account_receivable = fields.Many2one(
    #     string="Conto principale di credito", comodel_name="account.account",
    #     domain=[('internal_type', '=', 'receivable')],
    #     required=True,
    #     default='')

    # @api.onchange('coa_toplevel_len')
    # def onchange_toplevel(self):
    #     if self.coa_toplevel_len < 1 or self.coa_toplevel_len > 4:
    #         self.coa_toplevel_len = 2
    #
    # @api.onchange('coa_level2_len')
    # def onchange_level2(self):
    #     if self.coa_level2_len < 1 or self.coa_level2_len > 4:
    #         self.coa_level2_len = 1
    #
    # @api.onchange('coa_lowlevel_len')
    # def onchange_lowlevel(self):
    #     if self.coa_lowlevel_len < 1 or self.coa_lowlevel_len > 4:
    #         self.coa_lowlevel_len = 3

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.search([('company_id', '=', self.company_id.id)]):
            return {
                'warning': {
                    'title': 'Azienda duplicata!',
                    'message': 'Azienda usata in altri profili'
                }
            }
