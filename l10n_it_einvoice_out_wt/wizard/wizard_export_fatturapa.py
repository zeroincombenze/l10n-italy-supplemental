# -*- coding: utf-8 -*-
from odoo import models
from odoo.tools.float_utils import float_round
from odoo.addons.l10n_it_ade.bindings.fatturapa_v_1_2 import DatiRitenutaType


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    WT_TAX_CODE = {"inps": "RT03", "enasarco": "RT04", "enpam": "RT05", "other": "RT06"}

    def getWithholdingType(self, wt_types, partner):
        if wt_types == "ritenuta":
            if partner.is_company:
                withholding_type = "RT02"
            else:
                withholding_type = "RT01"
        else:
            withholding_type = self.WT_TAX_CODE[wt_types]
        return withholding_type

    def setDatiRitenuta(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiRitenuta(invoice, body)
        wt_lines_to_write = invoice.withholding_tax_line_ids.filtered(
            lambda x: x.withholding_tax_id.wt_types in ("ritenuta", "other")
        )
        for wt in wt_lines_to_write:
            body.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta.append(
                DatiRitenutaType(
                    TipoRitenuta=self.getWithholdingType(
                        wt.withholding_tax_id.wt_types,
                        invoice.partner_id),
                    ImportoRitenuta="%.2f" % float_round(wt.tax, 2),
                    AliquotaRitenuta="%.2f" % float_round(
                        wt.tax_coeff * 100, 2),
                    CausalePagamento=wt.withholding_tax_id.causale_pagamento_id.code,
                )
            )
        return res
