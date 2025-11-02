# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

from odoo.addons.l10n_it_ade.bindings import fatturapa_v_1_2


class WizardLinkToInvoice(models.TransientModel):
    _name = "wizard.link.to.invoice"
    _description = "Link e-bill to bill"

    wizard_id = fields.Many2one(
        comodel_name='wizard.link.to.invoice',
    )
    invoice_id = fields.Many2one("account.invoice", string="Bill", required=True)

    def log_inconsistency(self, message):
        inconsistencies = self.env.context.get("inconsistencies", "")
        if inconsistencies:
            inconsistencies += "\n"
        inconsistencies += message
        # we can't set
        # self = self.with_context(inconsistencies=inconsistencies)
        # because self is a locale variable.
        # We use __dict__ to modify attributes of self
        self.__dict__.update(
            self.with_context(inconsistencies=inconsistencies).__dict__
        )

    def get_invoice_obj(self, fatturapa_attachment):
        xml_string = fatturapa_attachment.get_xml_string()
        if xml_string:
            return fatturapa_v_1_2.CreateFromDocument(xml_string)
        return False

    def invoiceUpdate(
        self, invoice, fatt, fatturapa_attachment, FatturaBody, partner_id, wizard
    ):
        invoice_model = self.env["account.invoice"]
        # self.env["account.invoice.line"]
        # self.env["italy.ade.invoice.type"]
        # self.env["fatturapa.related_document_type"]
        # # WelfareFundLineModel = self.env['welfare.fund.data.line']
        # self.env["faturapa.activity.progress"]
        # self.env["fatturapa.related_ddt"]
        # self.env["fatturapa.payment.data"]
        # self.env["fatturapa.payment_term"]
        # self.env["faturapa.summary.data"]
        (
            invoice_data,
            company,
            partner,
            wt_found,
            inconsistencies,
        ) = invoice_model.xml_get_header_data(
            self, fatt, fatturapa_attachment, FatturaBody, partner_id
        )
        if inconsistencies:
            self.log_inconsistency(inconsistencies)
        invoice.write(invoice_data)
        invoice.set_einvoice_data(FatturaBody)
        wizard.set_e_invoice_lines(FatturaBody, self.invoice_id)
        wizard.set_summary_data(FatturaBody, self.invoice_id)
        wizard.set_delivery_data(FatturaBody, self.invoice_id)
        wizard.set_payments_data(
            FatturaBody, self.invoice_id, partner, self.invoice_id.company_id)
        invoice.set_vendor_bill_date(FatturaBody)

    @api.multi
    def link(self):
        self.ensure_one()
        if not self.invoice_id:
            return True
        fatturapa_attachment_ids = self.env.context.get("active_ids", False)
        if len(fatturapa_attachment_ids) != 1:
            raise UserError(_("You can select only one XML file to link."))
        # fatturapa_attachment = self.wizard_id.attachment_id
        import_wiz = self.env['wizard.import.fatturapa'].with_context(
            active_ids=fatturapa_attachment_ids,
            linked_invoice=self.invoice_id,
        ).new({"e_invoice_detail_level": "2"})
        import_wiz.importFatturaPA()
        self.invoice_id.fatturapa_attachment_in_id = fatturapa_attachment_ids[0]
        fatturapa_attachment_model = self.env["fatturapa.attachment.in"]
        partner_model = self.env["res.partner"]
        for fatturapa_attachment_id in fatturapa_attachment_ids:
            fatturapa_attachment = fatturapa_attachment_model.browse(
                fatturapa_attachment_id
            )
            fatt = fatturapa_attachment.get_invoice_obj()
            if not fatt:
                raise UserError(
                    _("Cannot link an attachment that could not be parsed.\n"
                      "Please fix the parsing error first, then try again."))

            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            # 1.2
            partner_id = partner_model.getPartnerBase(cedentePrestatore, fatturapa=self)
            for FatturaBody in fatt.FatturaElettronicaBody:
                # reset inconsistencies
                self.__dict__.update(self.with_context(inconsistencies="").__dict__)
                # Variabiles to make code quite equal to import fatturapa
                self.invoiceUpdate(
                    self.invoice_id,
                    fatt,
                    fatturapa_attachment,
                    FatturaBody,
                    partner_id,
                    import_wiz,
                )
        return {
            "view_type": "form",
            "name": "Electronic Bills",
            "view_mode": "tree,form",
            "res_model": "account.invoice",
            "type": "ir.actions.act_window",
            "domain": [("id", "in", [self.invoice_id.id])],
        }
