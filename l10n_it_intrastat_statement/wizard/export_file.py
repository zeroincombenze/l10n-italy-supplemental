# Copyright 2019 Simone Rubino - Agile Business Group
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License AGPL-3 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

import base64
from odoo import api, fields, models, _


class AccountIntrastatExportFile(models.TransientModel):
    _name = "account.intrastat.export.file"
    _description = "Intrastat export file"

    name = fields.Char(
        string="File Name",
        readonly=True)
    data = fields.Binary(
        string="File",
        readonly=True)
    state = fields.Selection(
        selection=[
            ('choose', "Choose"),
            ('get', "Get")],
        string="State",
        default='choose')

    @api.multi
    def act_getfile(self):
        self.ensure_one()
        statement_id = self.env.context.get('active_id')
        statement = self.env['account.intrastat.statement'].browse(
            statement_id)

        file = statement.generate_file_export()

        filename = statement._get_file_name()

        out = base64.encodebytes(file.encode())

        view = self.env['ir.model.data'].get_object_reference(
            'l10n_it_intrastat_statement',
            'wizard_account_intrastat_export_file'
        )
        view_id = view[1] or False

        self.write({'state': 'get', 'data': out, 'name': filename})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.intrastat.export.file',
            'view_mode': 'form',
            'view_type': 'form',
            'name': _('Export Intrastat File'),
            'res_id': self.id,
            'nodestroy': True,
            'view_id': [view_id],
            'target': 'new',
        }
