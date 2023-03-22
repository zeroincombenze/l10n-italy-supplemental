##############################################################################
#
# Copyright Didotech s.r.l. <https://www.didotech.com>
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-01-09
#    Author : Fabio Colognesi
#
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#
##############################################################################
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import fields, models

DEFAULT_MSG = "La merce viaggia a rischio e pericolo del Committente e anche " \
              "se venduta franco destino gli eventuali reclami per avarie " \
              "di viaggio o manomissioni debbono essere rivolti al Vettore. " \
              "Trascorsi otto giorni dal ricevimento della merce non sono " \
              "ammessi reclami per nessuna ragione o causa. " \
              "Il cliente conferma, sotto la sua responsabilità, " \
              "l'esattezza dell'indicazione del nome e dell'indirizzo. " \
              "- Art. 21 D.P.R. 26/10/1972 n. 633. In caso di ritardato " \
              "pagamento alla scadenza saranno applicati gli interessi di " \
              "mora al tasso bancario corrente. " \
              "- Legge 27/12/2017 n.205 Fatturazione Elettronica La presente" \
              " fattura in formato cartaceo non è utilizzabile ai fini " \
              "fiscali. Il documento valido è quello in formato elettronico " \
              "reso disponibile dal " \
              "Sistema di interscambio (SDI)."


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    setup_invoice_bottom_message = fields.Char(
        string='Invoice bottom message',
        default=DEFAULT_MSG, translate=True,
        config_parameter='account.invoice.bottom_message')

    def _get_conditions_of_sale(self):
        message = self.env["ir.config_parameter"].sudo().get_param(
            "account.invoice.bottom_message")
        return message
