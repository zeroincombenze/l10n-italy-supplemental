# -*- coding: utf-8 -*-
# Copyright 2021 Marco Colombo - Phi srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import UserError

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.addons.l10n_it_ade.bindings.fatturapa_v_1_2 import (
    AltriDatiGestionaliType,
    DatiRiepilogoType,
    DettaglioLineeType,
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDettaglioLinea(self, line_no, line, body, price_precision, uom_precision):
        DettaglioLinea = super(WizardExportFatturapa, self).setDettaglioLinea(
            line_no, line, body, price_precision, uom_precision
        )

        # if line.force_dichiarazione_intento_id:
        #     dati_gestionali = AltriDatiGestionaliType(
        #         TipoDato="INTENTO",
        #         RiferimentoTesto=encode_for_export(
        #             line.force_dichiarazione_intento_id.telematic_protocol, 60
        #         ),
        #         RiferimentoData=line.force_dichiarazione_intento_id.date,
        #     )
        #     DettaglioLinea.AltriDatiGestionali.append(dati_gestionali)
        return DettaglioLinea

    def setDettaglioLinee(self, invoice, body):
        super(WizardExportFatturapa, self).setDettaglioLinee(invoice, body)
        if not invoice.lettera_intento:
            return
        if not invoice.lettera_intento_id:
            raise UserError(_("Missed Lettera di intento in invoice!"))
        # force_dichiarazione_intento_ids = invoice.lettera_intento.browse()
        line_no = 1
        for line in invoice.invoice_line_ids:
            #     if line.force_dichiarazione_intento_id:
            #         force_dichiarazione_intento_ids |= line.force_dichiarazione_intento_id
            line_no += 1
        # to_add = invoice.lettera_intento - force_dichiarazione_intento_ids
        # if not to_add:
        #     return
        DettaglioLinea = DettaglioLineeType(
            NumeroLinea=str(line_no),
            Descrizione=encode_for_export("Altre lettere d'intento", 1000),
            PrezzoUnitario="0.00",
            PrezzoTotale="0.00",
            AliquotaIVA="0.00",
            Natura="N1",
        )
        # for dec in to_add:
        dati_gestionali = AltriDatiGestionaliType(
            TipoDato="INTENTO",
            RiferimentoTesto=encode_for_export(
                invoice.lettera_intento_id.customer_autmin, 60
            ),
            RiferimentoData=invoice.lettera_intento_id.customer_date,
        )
        DettaglioLinea.AltriDatiGestionali.append(dati_gestionali)
        body.DatiBeniServizi.DettaglioLinee.append(DettaglioLinea)

    def setDatiRiepilogo(self, invoice, body):
        super(WizardExportFatturapa, self).setDatiRiepilogo(invoice, body)
        if invoice.lettera_intento:
            # force_dichiarazione_intento_ids = invoice.lettera_intento.browse()
            # for line in invoice.invoice_line_ids:
            #     if line.force_dichiarazione_intento_id:
            #         force_dichiarazione_intento_ids |= line.force_dichiarazione_intento_id
            # to_add = invoice.lettera_intento - force_dichiarazione_intento_ids
            # if not to_add:
            #     return
            riepilogo = DatiRiepilogoType(
                AliquotaIVA="0.00",
                ImponibileImporto="0.00",
                Imposta="0.00",
                Natura="N1",
                RiferimentoNormativo="Esclusa ex. Art. 15",
            )
            body.DatiBeniServizi.DatiRiepilogo.append(riepilogo)
