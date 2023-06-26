# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later
# (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
import base64
import xlwt
import io
from odoo import api, fields, models
from ..models import spreadsheet_config as scg

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class WizardBalanceExportXls(models.TransientModel):
    _name = "wizard.balance.export.xls"
    _description = "Export balance xls"

    file_export = fields.Binary('File xls', readonly=True)
    name = fields.Char('File Name', readonly=True, default='bilancio.xls')


class WizardBalanceOppositeExportXls(models.TransientModel):
    _name = "wizard.balance.opposite.export.xls"
    _description = "Export balance xls"

    file_export = fields.Binary('File xls', readonly=True)
    name = fields.Char('File Name', readonly=True, default='bilancio.xls')
    file_type = fields.Selection(
        [
            ("parted", "Suddiviso (un foglio per sezione)"),
            ("all", "Unico"),
        ],
        required=True,
        string='Tipo di xls',
        default='parted'
    )

    def generate(self):
        active_id = self._context.get('active_id')
        if self.file_type == 'parted':
            self._generate_opposite_parted_xls(active_id)
        else:
            self._generate_opposite_all_xls(active_id)

        model_data_obj = self.env['ir.model.data']
        view_rec = model_data_obj.get_object_reference(
            'l10n_it_balance',
            'wizard_generate_balance_opposite_xls_exit'
        )
        view_id = view_rec and view_rec[1] or False

        return {
            'name': 'File generato xls',
            'view_type': 'form',
            'view_id': view_id,
            'view_mode': 'form',
            'res_model': 'wizard.balance.opposite.export.xls',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.one
    def _generate_opposite_sheet_xls(self, balance_id):
        filename = 'bilancio_a_conti_contrapposti.xls'
        balance_domain = [('id', '=', balance_id)]
        line_domain = [('balance_id', '=', balance_id)]

        balance = self.env['italy.account.balance'].search(balance_domain)

        wb = xlwt.Workbook()
        ws = wb.add_sheet(balance.name)

        line_model = self.env['italy.account.balance.line.asset']
        row_index = 0
        ws.write(row_index, 0, 'Conto', scg.STYLE_HEADER)
        ws.write(row_index, 1, 'Descrizione', scg.STYLE_HEADER)
        ws.write(row_index, 2, 'Saldo', scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(line_domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws.write(row_index, 0, line.code, cstyle)
            ws.write(row_index, 1, line.name, cstyle)
            ws.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        line_model = self.env['italy.account.balance.line.liability']
        row_index += 1
        ws.write(row_index, 0, 'Conto', scg.STYLE_HEADER)
        ws.write(row_index, 1, 'Descrizione', scg.STYLE_HEADER)
        ws.col(1).width = scg.xlwt_get_col_width(50)
        ws.write(row_index, 2, 'Saldo', scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(line_domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws.write(row_index, 0, line.code, cstyle)
            ws.write(row_index, 1, line.name, cstyle)
            ws.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        line_model = self.env['italy.account.balance.line.expense']
        row_index += 1
        ws.write(row_index, 0, 'Conto', scg.STYLE_HEADER)
        ws.write(row_index, 1, 'Descrizione', scg.STYLE_HEADER)
        ws.col(1).width = scg.xlwt_get_col_width(50)
        ws.write(row_index, 2, 'Saldo', scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(line_domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws.write(row_index, 0, line.code, cstyle)
            ws.write(row_index, 1, line.name, cstyle)
            ws.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        line_model = self.env['italy.account.balance.line.income']
        row_index += 1
        ws.write(row_index, 0, 'Conto', scg.STYLE_HEADER)
        ws.write(row_index, 1, 'Descrizione', scg.STYLE_HEADER)
        ws.col(1).width = scg.xlwt_get_col_width(50)
        ws.write(row_index, 2, 'Saldo', scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(line_domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws.write(row_index, 0, line.code, cstyle)
            ws.write(row_index, 1, line.name, cstyle)
            ws.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        line_model = self.env['italy.account.balance.line.memorandum']
        row_index += 1
        ws.write(row_index, 0, 'Conto', scg.STYLE_HEADER)
        ws.write(row_index, 1, 'Descrizione', scg.STYLE_HEADER)
        ws.col(1).width = scg.xlwt_get_col_width(50)
        ws.write(row_index, 2, 'Saldo', scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(line_domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws.write(row_index, 0, line.code, cstyle)
            ws.write(row_index, 1, line.name, cstyle)
            ws.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        fp = io.BytesIO()
        wb.save(fp)
        data = {'file_export': base64.encodebytes(fp.getvalue()),
                'name': filename}
        self.write(data)
        fp.close()

    def _generate_opposite_parted_xls(self, balance_id):
        filename = 'bilancio_a_conti_contrapposti.xls'
        domain = [('balance_id', '=', balance_id)]

        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 4
        font0.bold = True

        style0 = xlwt.XFStyle()
        style0.font = font0

        stylefloat = xlwt.XFStyle()
        stylefloat.num_format_str = '0.00'

        al = xlwt.Alignment()
        al.horz = al.HORZ_CENTER

        stylecenter = xlwt.XFStyle()
        stylecenter.num_format_str = '@'
        stylecenter.alignment = al
        stylecenter.font = font0

        wb = xlwt.Workbook()
        ws_asset_liability = wb.add_sheet('Stato patrimoniale')

        ws_economics = wb.add_sheet('Conto economico')

        ws_memorandum = wb.add_sheet('Conti d\'ordine')

        line_model = self.env['italy.account.balance.line.asset']
        row_index = 0
        ws_asset_liability.write_merge(0, 0, 0, 6, 'Stato patrimoniale',
                                       scg.STYLE_CENTER)
        row_index += 1
        ws_asset_liability.write_merge(1, 1, 0, 2, 'Attività',
                                       scg.STYLE_CENTER)
        row_index += 1
        ws_asset_liability.write(row_index, 0, 'Conto', scg.STYLE_HEADER)
        ws_asset_liability.write(row_index, 1, 'Descrizione', scg.STYLE_HEADER)
        ws_asset_liability.col(1).width = scg.xlwt_get_col_width(50)
        ws_asset_liability.write(row_index, 2, 'Saldo', scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws_asset_liability.write(row_index, 0, line.code, cstyle)
            ws_asset_liability.write(row_index, 1, line.name, cstyle)
            ws_asset_liability.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        col_index = 4
        line_model = self.env['italy.account.balance.line.liability']

        row_index = 1
        next_cols = col_index + 2
        ws_asset_liability.write_merge(row_index, row_index, col_index,
                                       next_cols, 'Passività', scg.STYLE_CENTER)
        row_index += 1
        ws_asset_liability.write(row_index, col_index, 'Conto',
                                 scg.STYLE_HEADER)
        col_index += 1
        ws_asset_liability.write(row_index, col_index, 'Descrizione',
                                 scg.STYLE_HEADER)
        ws_asset_liability.col(col_index).width = scg.xlwt_get_col_width(50)
        col_index += 1
        ws_asset_liability.write(row_index, col_index, 'Saldo',
                                 scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            col_index = 4
            ws_asset_liability.write(row_index, col_index, line.code, cstyle)
            col_index += 1
            ws_asset_liability.write(row_index, col_index, line.name, cstyle)
            col_index += 1
            ws_asset_liability.write(row_index, col_index, line.amount_balance,
                                     cstyle)
            row_index += 1
        line_model = self.env['italy.account.balance.line.expense']
        row_index = 0
        ws_economics.write_merge(0, 0, 0, 6, 'Conto economico', scg.STYLE_CENTER)
        row_index += 1
        ws_economics.write_merge(1, 1, 0, 2, 'Costi', scg.STYLE_CENTER)
        row_index += 1
        ws_economics.write(row_index, 0, 'Conto', scg.STYLE_HEADER)
        ws_economics.write(row_index, 1, 'Descrizione', scg.STYLE_HEADER)
        ws_economics.col(1).width = scg.xlwt_get_col_width(50)

        ws_economics.write(row_index, 2, 'Saldo', scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws_economics.write(row_index, 0, line.code, cstyle)
            ws_economics.write(row_index, 1, line.name, cstyle)
            ws_economics.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        col_index = 4
        line_model = self.env['italy.account.balance.line.income']

        row_index = 1
        next_cols = col_index + 2
        ws_economics.write_merge(row_index, row_index, col_index, next_cols,
                                 'Ricavi', scg.STYLE_CENTER)
        row_index += 1
        ws_economics.write(row_index, col_index, 'Conto', scg.STYLE_HEADER)
        col_index += 1
        ws_economics.write(row_index, col_index, 'Descrizione',
                           scg.STYLE_HEADER)
        ws_economics.col(col_index).width = scg.xlwt_get_col_width(50)

        col_index += 1
        ws_economics.write(row_index, col_index, 'Saldo', scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            col_index = 4
            ws_economics.write(row_index, col_index, line.code, cstyle)
            col_index += 1
            ws_economics.write(row_index, col_index, line.name, cstyle)
            col_index += 1
            ws_economics.write(row_index, col_index, line.amount_balance,
                               cstyle)
            row_index += 1

        row_index = 0
        line_model = self.env['italy.account.balance.line.memorandum']
        ws_memorandum.write_merge(row_index, row_index, 0, 6,
                                  'Conti d\'ordine', scg.STYLE_CENTER)
        row_index += 1
        ws_memorandum.write(row_index, 0, 'Conto', scg.STYLE_HEADER)
        ws_memorandum.write(row_index, 1, 'Descrizione', scg.STYLE_HEADER)
        ws_memorandum.col(1).width = scg.xlwt_get_col_width(50)

        ws_memorandum.write(row_index, 2, 'Saldo', scg.STYLE_HEADER)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws_memorandum.write(row_index, 0, line.code, cstyle)
            ws_memorandum.write(row_index, 1, line.name, cstyle)
            ws_memorandum.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        fp = io.BytesIO()
        wb.save(fp)
        data = {'file_export': base64.encodebytes(fp.getvalue()),
                'name': filename}
        self.write(data)
        fp.close()

    @api.one
    def _generate_opposite_all_xls(self, balance_id):
        filename = 'bilancio_a_conti_contrapposti.xls'
        domain = [('balance_id', '=', balance_id)]

        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 4
        font0.bold = True

        style0 = xlwt.XFStyle()
        style0.font = font0

        stylefloat = xlwt.XFStyle()
        stylefloat.num_format_str = '0.00'

        al = xlwt.Alignment()
        al.horz = al.HORZ_CENTER

        stylecenter = xlwt.XFStyle()
        stylecenter.num_format_str = '@'
        stylecenter.alignment = al
        stylecenter.font = font0

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Bilancio a conti contrapposti')

        line_model = self.env['italy.account.balance.line.asset']
        row_index = 0
        ws.write_merge(0, 0, 0, 6, 'Stato patrimoniale', scg.STYLE_CENTER)
        row_index += 1
        ws.write_merge(1, 1, 0, 2, 'Attività', scg.STYLE_CENTER)
        row_index += 1
        ws.write(row_index, 0, 'Conto', scg.STYLE_BOLD_BLACK)
        ws.write(row_index, 1, 'Descrizione', scg.STYLE_BOLD_BLACK)
        ws.col(1).width = scg.xlwt_get_col_width(50)

        ws.write(row_index, 2, 'Saldo', scg.STYLE_BOLD_BLACK)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4

            ws.write(row_index, 0, line.code, cstyle)
            ws.write(row_index, 1, line.name, cstyle)
            ws.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        col_index = 4
        line_model = self.env['italy.account.balance.line.liability']

        row_index = 1
        next_cols = col_index + 2
        ws.write_merge(row_index, row_index, col_index,
                       next_cols, 'Passività', scg.STYLE_CENTER)
        row_index += 1
        ws.write(row_index, col_index, 'Conto', scg.STYLE_BOLD_BLACK)
        col_index += 1
        ws.write(row_index, col_index, 'Descrizione', scg.STYLE_BOLD_BLACK)
        ws.col(col_index).width = scg.xlwt_get_col_width(50)

        col_index += 1
        ws.write(row_index, col_index, 'Saldo', scg.STYLE_BOLD_BLACK)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            col_index = 4
            ws.write(row_index, col_index, line.code, cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.name, cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.amount_balance, cstyle)
            row_index += 1
        line_model = self.env['italy.account.balance.line.expense']
        row_index += 2
        ws.write_merge(row_index, row_index, 0, 6, 'Conto economico',
                       scg.STYLE_CENTER)
        row_index += 1
        account_expense_last_row = row_index
        ws.write_merge(row_index, row_index, 0, 2, 'Costi', scg.STYLE_CENTER)
        row_index += 1
        ws.write(row_index, 0, 'Conto', scg.STYLE_BOLD_BLACK)
        ws.write(row_index, 1, 'Descrizione', scg.STYLE_BOLD_BLACK)
        ws.col(1).width = scg.xlwt_get_col_width(50)
        ws.write(row_index, 2, 'Saldo', scg.STYLE_BOLD_BLACK)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws.write(row_index, 0, line.code, cstyle)
            ws.write(row_index, 1, line.name, cstyle)
            ws.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        line_model = self.env['italy.account.balance.line.income']
        row_index = account_expense_last_row
        col_index = 4
        next_cols = col_index + 2
        ws.write_merge(row_index, row_index, col_index, next_cols, 'Ricavi',
                       scg.STYLE_CENTER)
        row_index += 1
        ws.write(row_index, col_index, 'Conto', scg.STYLE_BOLD_BLACK)
        col_index += 1
        ws.write(row_index, col_index, 'Descrizione', scg.STYLE_BOLD_BLACK)
        ws.col(col_index).width = scg.xlwt_get_col_width(50)
        col_index += 1
        ws.write(row_index, col_index, 'Saldo', scg.STYLE_BOLD_BLACK)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            col_index = 4
            ws.write(row_index, col_index, line.code, cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.name, cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.amount_balance, cstyle)
            row_index += 1

        row_index += 4
        line_model = self.env['italy.account.balance.line.memorandum']
        ws.write_merge(row_index, row_index, 0, 6, 'Conti d\'ordine',
                       scg.STYLE_CENTER)
        row_index += 1
        ws.write(row_index, 0, 'Conto', scg.STYLE_BOLD_BLACK)
        ws.write(row_index, 1, 'Descrizione', scg.STYLE_BOLD_BLACK)
        ws.col(1).width = scg.xlwt_get_col_width(50)
        ws.write(row_index, 2, 'Saldo', scg.STYLE_BOLD_BLACK)
        row_index += 1
        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4
            ws.write(row_index, 0, line.code, cstyle)
            ws.write(row_index, 1, line.name, cstyle)
            ws.write(row_index, 2, line.amount_balance, cstyle)
            row_index += 1

        fp = io.BytesIO()
        wb.save(fp)
        data = {'file_export': base64.encodebytes(fp.getvalue()),
                'name': filename}
        self.write(data)
        fp.close()
