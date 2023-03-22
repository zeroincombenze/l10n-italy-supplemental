# -*- coding: utf-8 -*-
# © 2018 Nicola Gramola - Didotech srl (www.didotech.com)
# © 2019-2020 Andrei Levin - Didotech srl (www.didotech.com)

from odoo import models, fields
import platform


class CompanyConfig(models.Model):
    _inherit = "res.company"

    def _get_node(self):
        self.node = platform.node()

    sdi_username = fields.Char(string='Username', size=255)
    sdi_password = fields.Char('Password', size=50)
    sdi_storage_format = fields.Selection(
        [('xml', 'XML'), ('p7m', 'P7M')],
        'Invoice format', default='xml'
    )
    sdi_send = fields.Boolean('Send to SDI')
    sdi_node = fields.Char(
        'Node', size=64, required=True, default='some_node',
        help="To be able to send XML invoices to SDI this value should be"
             "equal to the name of the local host")
    node = fields.Char(compute=_get_node, string='Node', method=True)
    use_local_storage = fields.Boolean(string="Open documents from local storage", default=True)


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sdi_username = fields.Char(
        related='company_id.sdi_username',
        string='Username',
        readonly=False
    )
    sdi_password = fields.Char(
        related='company_id.sdi_password',
        string='Password',
        readonly=False
    )
    sdi_storage_format = fields.Selection(
        related='company_id.sdi_storage_format',
        string='Invoice format',
        readonly=False,
        default='xml'
    )
    sdi_send = fields.Boolean(
        related='company_id.sdi_send',
        string='Send to SDI',
        readonly=False
    )
    sdi_node = fields.Char(
        related='company_id.sdi_node',
        string='SDI Host',
        readonly=False,
        help="To be able to send XML invoices to SDI this value should be equal to the name of the local host"
    )
    node = fields.Char(related='company_id.node', string='Local Host', readonly=True)
    use_local_storage = fields.Boolean(
        related='company_id.use_local_storage',
        string='Open documents from local storage',
        readonly=False
    )
