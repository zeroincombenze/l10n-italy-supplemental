# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2017-19 Lorenzo Battistini
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2017-21 Odoo Community Association (OCA) <https://odoo-community.org>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#

import base64
from odoo import api, fields, models, exceptions, _


class ComunicazioneLiquidazioneExportFile(models.TransientModel):
    _name = "comunicazione.liquidazione.export.file"
    _description = "Export VAT statement communication XML file"

    file_export = fields.Binary('File', readonly=True)
    name = fields.Char('File Name', readonly=True, default='liquidazione.xml')

    @api.multi
    def export(self):

        comunicazione_ids = self._context.get('active_ids')
        if not comunicazione_ids:
            raise exceptions.Warning(_(
                "No communication selected"
            ))
        if len(comunicazione_ids) > 1:
            raise exceptions.Warning(_(
                'You can export only 1 communication at a time'
            ))

        for wizard in self:
            for comunicazione in self.env['comunicazione.liquidazione'].\
                    browse(comunicazione_ids):
                out = base64.encodestring(comunicazione.get_export_xml())
                wizard.file_export = out
                wizard.name = "%s_LI_%s.xml" % (
                    comunicazione.declarant_fiscalcode,
                    str(comunicazione.identificativo).rjust(5, '0'))
            model_data_obj = self.env['ir.model.data']
            view_rec = model_data_obj.get_object_reference(
                'l10n_it_vat_statement_communication_plus',
                'wizard_liquidazione_export_file_exit'
            )
            view_id = view_rec and view_rec[1] or False

            return {
                'view_type': 'form',
                'view_id': [view_id],
                'view_mode': 'form',
                'res_model': 'comunicazione.liquidazione.export.file',
                'res_id': wizard.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
