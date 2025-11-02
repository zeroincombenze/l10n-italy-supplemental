# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import fields, models


class ItalyEinvoiceSender(models.Model):
    _name = "italy.ade.sender"
    _description = "E-Invoice Sender Channel"

    name = fields.Char(
        "Sender Channel Name",
        required=True,
        help="Give a unique name for Sender Channel",
    )
    method = fields.Selection(
        [
            ("NO", "Nessun Invio"),
            ("PEC", "Tramite PEC"),
            ("FTP", "Tramite FTP"),
            ("JSON", "Tramite JSON"),
        ],
        "SDI channel",
        help="Sending Method",
    )
    company_id = fields.Many2one(
        "res.company",
        "Company",
        help="Set company, if specific company channel",
    )
    client_id = fields.Char("Client ID", help="Client ID assigned by 3th Party Sender")
    client_key = fields.Char(
        "Client key", help="Client key assigned by 3th Party Sender"
    )
    sender_url = fields.Char("Sender url", help="3th Party Sender URL to connect")
    sender_company_id = fields.Char(
        "Company ID", help="Company Identification assigned by 3th Party Sender"
    )
    hub_ip_addr = fields.Char("Hub IP Address", help="IP Address to connect")
    email_from_for_fatturaPA = fields.Char(
        string="Sender Email Address", help="PEC of sender"
    )
    email_exchange_system = fields.Char(
        string="Exchange System Email Address", help="E-mail to use when method is PEC"
    )
    pec_server_id = fields.Many2one(
        "ir.mail_server",
        string="Pec mail server",
        required=False,
        domain=[("is_fatturapa_pec", "=", True)],
    )
    active = fields.Boolean(string="Active", default=True)
    trace = fields.Boolean(
        string="Trace",
        default=False,
        help="Trace data in log. Warning! Use this feature with caution; "
        "all sent data will be recorded in the log file."
        "This feature must be used only to debug handshake",
    )
    param1 = fields.Char(
        string="Custom value 1",
        help="Custom value to issue for communication, if required",
    )
    param2 = fields.Char(
        string="Custom value 2",
        help="Custom value to issue for communication, if required",
    )
    param3 = fields.Char(
        string="Custom value 3",
        help="Custom value to issue for communication, if required",
    )
    param4 = fields.Char(
        string="Custom value 4",
        help="Custom value to issue for communication, if required",
    )
    param5 = fields.Char(
        string="Custom value 5",
        help="Custom value to issue for communication, if required",
    )
    param6 = fields.Char(
        string="Custom value 6",
        help="Custom value to issue for communication, if required",
    )
