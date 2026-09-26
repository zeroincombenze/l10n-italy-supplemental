# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    e_invoice_customer_product_search = fields.Selection(
        [
            ("c", "By internal code"),
            ("cn", "By code or exact name"),
            ("cndx", "By code or similar name"),
            ("n", "By exact name"),
        ],
        "Customer product search",
        help="How to search for product from sale e-invoice",
    )

    @api.model
    def search_partner_from_xml(self, partner_xml):
        """Existing partner of an e-invoice header, without creating anything.

        getPartnerBase() creates or updates the partner, which must not happen
        while computing a stored field: this is a plain read-only lookup, and
        it returns an empty recordset when nothing matches.
        """
        if not partner_xml or not getattr(partner_xml, "DatiAnagrafici", None):
            return self.browse()
        DatiAnagrafici = partner_xml.DatiAnagrafici
        IdFiscaleIVA = getattr(DatiAnagrafici, "IdFiscaleIVA", None)
        if IdFiscaleIVA:
            vat = "%s%s" % (IdFiscaleIVA.IdPaese, IdFiscaleIVA.IdCodice)
            partners = self.search([("vat", "=ilike", vat)], limit=1)
            if partners:
                return partners
        fiscalcode = getattr(DatiAnagrafici, "CodiceFiscale", None)
        if fiscalcode:
            partners = self.search([("fiscalcode", "=ilike", fiscalcode)], limit=1)
            if partners:
                return partners
        return self.browse()

    @api.model
    def getCustomerBase(self, partner_xml, fatturapa=None):
        """Get the CessionarioCommittente of a sale e-invoice as a customer.

        getPartnerBase() creates missing partners as suppliers, which is right
        for a received bill and wrong here: the flag is set afterwards, and the
        supplier one is left as it is, because the same company may be both.
        """
        partner_id = self.getPartnerBase(partner_xml, fatturapa=fatturapa)
        if partner_id > 0:
            partner = self.browse(partner_id)
            if not partner.customer:
                partner.customer = True
        return partner_id
