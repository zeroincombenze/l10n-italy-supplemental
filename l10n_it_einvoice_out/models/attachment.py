# -*- coding: utf-8 -*-
#
# Copyright 2014    - Davide Corio
# Copyright 2015-16 - Lorenzo Battistini - Agile Business Group
# Copyright 2018-19 - Odoo Italia Associazione <https://www.odoo-italia.org>
# Copyright 2018-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class FatturaPAAttachment(models.Model):
    _name = "fatturapa.attachment.out"
    _description = "E-invoice Export File"
    _inherits = {"ir.attachment": "ir_attachment_id"}
    _inherit = ["mail.thread"]
    _order = "id desc"

    ir_attachment_id = fields.Many2one(
        "ir.attachment", "Attachment", required=True, ondelete="cascade"
    )
    out_invoice_ids = fields.One2many(
        "account.invoice",
        "fatturapa_attachment_out_id",
        string="Out Invoices",
        readonly=True,
    )
    has_pdf_invoice_print = fields.Boolean(
        help="True if all the invoices have a printed "
        "report attached in the XML, False otherwise.",
        compute="_compute_has_pdf_invoice_print",
        store=True,
    )
    invoice_partner_id = fields.Many2one(
        "res.partner", string="Customer", store=True, compute="_compute_xml_data"
    )
    invoices_total = fields.Float(
        "Invoices Total", compute="_compute_xml_data", store=True
    )
    date_invoice0 = fields.Date("Date Invoice", store=True, compute="_compute_xml_data")
    invoices_number = fields.Char(
        "Invoice Number", compute="_compute_xml_data", store=True
    )

    def get_xml_string(self):
        return self.ir_attachment_id.get_xml_string()

    @api.multi
    @api.depends("out_invoice_ids")
    def _compute_xml_data(self):
        wizard_model = self.env["wizard.export.fatturapa"]
        for att in self:
            fatt = wizard_model.get_invoice_obj(att)
            fatt.FatturaElettronicaHeader.CessionarioCommittente
            partners = att.mapped("out_invoice_ids.partner_id")
            if len(partners) == 1:
                att.invoice_partner_id = partners.id
            if att.out_invoice_ids:
                att.date_invoice0 = att.out_invoice_ids[0].date_invoice
            att.invoices_total = 0
            att.invoices_number = ""
            for invoice in att.out_invoice_ids:
                att.invoices_total += invoice.amount_total
                att.invoices_number += " %s" % invoice.number

    @api.multi
    @api.constrains("datas_fname")
    def _check_datas_fname(self):
        for att in self:
            res = self.search([("datas_fname", "=", att.datas_fname)])
            if len(res) > 1:
                raise UserError(_("File %s already present.") % att.datas_fname)

    @api.multi
    @api.depends("out_invoice_ids.fatturapa_doc_attachments.is_pdf_invoice_print")
    def _compute_has_pdf_invoice_print(self):
        """Check if all the invoices related to this attachment
        have at least one attachment containing
        the PDF report of the invoice"""
        for attachment_out in self:
            for invoice in attachment_out.out_invoice_ids:
                invoice_attachments = invoice.fatturapa_doc_attachments
                if any([ia.is_pdf_invoice_print for ia in invoice_attachments]):
                    continue
                else:
                    attachment_out.has_pdf_invoice_print = False
                    break
            else:
                # We have examined all the invoices and none of them
                # has caused a break, this means all the invoices have at least
                # one attachment having is_pdf_invoice_print = True
                attachment_out.has_pdf_invoice_print = True

    @api.multi
    def write(self, vals):
        res = super(FatturaPAAttachment, self).write(vals)
        if "datas" in vals and "message_ids" not in vals:
            for attachment in self:
                attachment.message_post(
                    subject=_("E-invoice attachment changed"),
                    body=_("User %s uploaded a new e-invoice file")
                    % self.env.user.login,
                )
        return res

    @api.multi
    def unlink(self):
        for attachment_out in self:
            for invoice in attachment_out.out_invoice_ids:
                invoice.fatturapa_doc_attachments.filtered(
                    "is_pdf_invoice_print"
                ).unlink()
        return super(FatturaPAAttachment, self).unlink()


class FatturaAttachments(models.Model):
    _inherit = "fatturapa.attachments"

    is_pdf_invoice_print = fields.Boolean(
        help="This attachment contains the PDF report of the linked invoice"
    )
