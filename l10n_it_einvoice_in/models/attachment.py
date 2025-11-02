# -*- coding: utf-8 -*-

import logging
import re

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

from odoo.addons.l10n_it_ade.bindings import fatturapa_v_1_2

_logger = logging.getLogger(__name__)


class FatturaPAAttachmentIn(models.Model):
    _name = "fatturapa.attachment.in"
    _description = "E-bill import file"
    _inherits = {"ir.attachment": "ir_attachment_id"}
    _inherit = ["mail.thread"]
    _order = "id desc"

    ir_attachment_id = fields.Many2one(
        "ir.attachment", "Attachment", required=True, ondelete="cascade"
    )
    in_invoice_ids = fields.One2many(
        "account.invoice",
        "fatturapa_attachment_in_id",
        string="In Bills",
        readonly=True,
    )
    xml_supplier_id = fields.Many2one(
        "res.partner", string="Supplier", compute="_compute_xml_data", store=True
    )
    invoices_number = fields.Integer(
        "Bills Number", compute="_compute_xml_data", store=True
    )
    invoices_total = fields.Float(
        "Bills Total",
        compute="_compute_xml_data",
        store=True,
        help="If specified by supplier, total amount of the document net of "
        "any discount and including tax charged to the buyer/ordered",
    )
    registered = fields.Boolean("Registered", compute="_compute_xml_data", store=True)

    e_invoice_received_date = fields.Datetime(string="E-Bill Received Date")

    uid = fields.Char("Uid", size=255)
    date_invoice0 = fields.Date("Date Invoice", store=True, compute="_compute_xml_data")
    company_id = fields.Many2one("res.company", string="Company")

    @api.onchange("datas_fname")
    def onchange_datas_fname(self):
        if self.search([("name", "=", self.datas_fname)]):
            raise UserError(_("File %s already loaded!") % self.datas_fname)
        self.name = self.datas_fname

    def get_xml_string(self):
        if not self.ir_attachment_id:
            return False
        xml_string = self.ir_attachment_id.get_xml_string()
        xml_string = re.sub(
            '<?xml version="1.0" encoding="utf-8"[^?]*?>',
            '<?xml version="1.0" encoding="utf-8"?>',
            xml_string)
        valid_header = (
            '<p:FatturaElettronica'
            ' xmlns:p="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2"'
            ' xmlns:ds="http://www.w3.org/2000/09/xmldsig#"'
            ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            ' versione="FPR12">')
        xml_string = re.sub(
            '<p:FatturaElettronica.*v1.2.*versione="FPR12">',
            valid_header,
            xml_string)
        # xml_string = re.sub(
        #     '<ns2:FatturaElettronica [^>]+">',
        #     valid_header,
        #     xml_string)
        # xml_string = xml_string.replace(
        #     "</ns2:FatturaElettronica>",
        #     "</p:FatturaElettronica>")

        # Do not change order of parsing!!!
        for tag in (
            "RiferimentoAmministrazione",
            "IdDocumento",
            "UnitaMisura",
            "CodiceFiscale",
            "Causale",
            "NumItem",
            "DatiConvenzione",
            "DatiRicezione",
            "NumeroCivico",
            "DatiOrdineAcquisto",
            "RiferimentoTesto",
            "RiferimentoNormativo",
        ):
            token = r"<%s>[ \t\n]*</%s>" % (tag, tag)
            xml_string = re.sub(token, "", xml_string, flags=re.DOTALL)
        for tag in (
            "Descrizione",
        ):
            token = r"<%s>[ \t\n]*</%s>" % (tag, tag)
            xml_string = re.sub(
                token, r"<%s>N/D</%s>" % (tag, tag), xml_string, flags=re.DOTALL)
        ctr = 0
        for tag in (
            "NumeroDDT",
            "DataDDT",
        ):
            token = r"<%s>[ \t\n]*</%s>" % (tag, tag)
            if re.search(token, xml_string, flags=re.DOTALL):
                ctr += 1
        if ctr:
            tag = "DatiDDT"
            token = r"<%s>.*?</%s>" % (tag, tag)
            xml_string = re.sub(token, "", xml_string, flags=re.DOTALL)
        for tag in ("Data",):
            token = r"<%s>[0-9]{4}-[0-9]{2}-[0-9]{2}[^<]+?</%s>" % (tag, tag)
            x = re.search(token, xml_string)
            while x:
                new_token = "%s</%s>" % (
                    xml_string[x.start(): x.end()][: len(tag) + 12],
                    tag,
                )
                xml_string = re.sub(token, new_token, xml_string)
                x = re.search(token, xml_string)
        pattern = re.compile(r"<Email>[^<]+</Email>")
        pattern2 = re.compile(r"[^ @<]+@[\w.]+")
        ofs = 0
        x = pattern.search(xml_string, ofs)
        while x:
            x2 = pattern2.search(xml_string, x.start() + 7)
            xml_string = (
                xml_string[:x.start()]
                + "<Email>"
                + xml_string[x2.start(): x2.end()]
                + "</Email>" + xml_string[x.end():])
            ofs = x.start() + 15
            x = pattern.search(xml_string, ofs)
        return xml_string

    @api.multi
    def get_invoice_obj(self):
        self.ensure_one()
        xml_string = self.get_xml_string()
        if xml_string:
            return fatturapa_v_1_2.CreateFromDocument(xml_string)
        return False

    @api.multi
    @api.depends("ir_attachment_id.datas", "in_invoice_ids")
    def _compute_xml_data(self):
        partner_model = self.env["res.partner"]
        for att in self:
            inv_xml = att.get_invoice_obj()
            if not inv_xml:
                continue
            xml_supplier_id = partner_model.getPartnerBase(
                inv_xml.FatturaElettronicaHeader.CedentePrestatore
            )
            if xml_supplier_id < 0:
                continue
            partner_model.browse(xml_supplier_id)
            # if partner.vat == self.env.user.company_id.vat:
            #     continue
            att.xml_supplier_id = xml_supplier_id
            att.invoices_number = len(inv_xml.FatturaElettronicaBody)
            att.registered = False
            # Strange but there is some trouble during execution
            if hasattr(att, "in_invoice_ids"):
                try:
                    if att.in_invoice_ids:
                        att.date_invoice0 = att.in_invoice_ids[0].date_invoice
                        if len(att.in_invoice_ids) == att.invoices_number:
                            att.registered = True
                    att.invoices_total = 0
                    for invoice_body in inv_xml.FatturaElettronicaBody:
                        att.invoices_total += float(
                            invoice_body.DatiGenerali.DatiGeneraliDocumento.
                            ImportoTotaleDocumento
                            or 0
                        )
                        if not att.in_invoice_ids:
                            att.date_invoice0 = (
                                invoice_body.DatiGenerali.DatiGeneraliDocumento.Data
                            )
                except BaseException:
                    _logger.error("Internal error in attachment id %d" % att.id)

    @api.multi
    @api.depends("ir_attachment_id.datas", "in_invoice_ids")
    def revaluate_due_date(self):
        wizard_model = self.env["wizard.import.fatturapa"]
        for att in self:
            fatt = wizard_model.get_invoice_obj(att)
            if not fatt:
                continue
            for fattura in fatt.FatturaElettronicaBody:
                # Strange but there is some trouble during execution
                if hasattr(att, "in_invoice_ids") and att.in_invoice_ids:
                    wizard_model.set_payment_term(
                        att.in_invoice_ids[0],
                        att.in_invoice_ids[0].company_id,
                        fattura.DatiPagamento,
                    )
