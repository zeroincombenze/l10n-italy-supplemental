# -*- coding: utf-8 -*-
#
from odoo import models


class ReportVatStatementCommunication(models.AbstractModel):
    _name = "report.l10n_it_vat_statement_communication.report_vat_statement"
    #
    # @api.model
    # def render_html(self, docids, data=None):
    #     docs = self.env["comunicazione.liquidazione"].browse(docids)
    #     docargs = {
    #         "docs": docs,
    #         "env": self.env,
    #         # "quadro_vp": self._get_quadro_vp,
    #     }
    #     return self.env["report"].render(
    #         "l10n_it_vat_statement_communication.report_vat_statement_communication",
    #         docargs
    #     )
