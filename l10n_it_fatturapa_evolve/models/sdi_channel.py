#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import os
from datetime import datetime
import logging
import json
import hashlib
import pytz
import requests
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder

from python_plus import _b

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class SdIChannel(models.Model):
    _inherit = 'sdi.channel'

    channel_type = fields.Selection(
        selection_add=[
            ("evolve", "Evolve (Web service)"),
        ],
    )
    client_id = fields.Char(
        "Client ID",
        help="Assigned by Evolve"
    )
    client_key = fields.Char(
        "Client Key",
        help="Assigned by Evolve"
    )
    client_company_id = fields.Integer(
        "Company ID of client",
        help="Assigned by Evolve"
    )
    sender_url = fields.Char(
        "Sender URL",
        help="Assigned by Evolve"
    )
    exchange_hub = fields.Char(
        "Exchange Hub IP",
        help="Supplied by Evolve"
    )
    archive_sent = fields.Integer(
        "Archive # to send",
        default=3,
        help="Archive ID to send invoices (usually is 3)"
    )
    archive_out = fields.Integer(
        "Archive # sent",
        default=1,
        help="Archive ID with sent invoices (usually is 1)"
    )
    archive_in = fields.Integer(
        "Archive # to receive",
        default=2,
        help="Archive ID with received invoices (usually is 2)"
    )
    capture_days = fields.Integer(
        "# days for search",
        default=60,
        help="Search for purchase invoices in # days (usually is 60)"
    )

    def is_self_invoice(self, invoice):
        return invoice.fiscal_document_type_id.code in ('TD17', 'TD18', 'TD19')

    @api.model
    def evolve_header(self):
        now = datetime.now(pytz.timezone("Europe/Rome")).strftime(
            "%Y-%m-%d %H.%M.%S"
        )
        aes = AES.new(
            _b(self.client_key),
            AES.MODE_CBC,
            _b(self.client_key[:16]),
        )
        pad_text = PKCS7Encoder().encode(now)
        header = {
            "Content-Type": "application/json",
            "From": self.client_id,
            "Authorization": b"Bearer " + b64encode(aes.encrypt(pad_text)),
        }
        return header

    @api.model
    def evolve_documenti(self, archive):
        return {
            "IdAzienda": self.client_company_id,
            "IdArchivio": archive,
        }

    @api.model
    def add_domain(self, request, domain):
        if  "Filtri" not in request:
            request["Filtri"] = []
        request["Filtri"].append({
            "NomeCampo": domain[0],
            "Criterio": domain[1],
            "FromValue": domain[2],
        })

    @api.model
    def add_document(self, request, invoice):
        if  "Documento" not in request:
            request["Documento"] = {}
            request["Documento"]["Visible"] = True
            request["Documento"]["CampiDinamici"] = []
        request["Documento"]["CampiDinamici"].append({
            "Nome": "NumeroFattura",
            "CriterioPredefinito": "=",
            "Valore": invoice.number,
        })
        request["Documento"]["CampiDinamici"].append({
            "Nome": "DataFattura",
            "CriterioPredefinito": "=",
            "Valore": str(invoice.date),
        })

    @api.model
    def add_attachment(self, request, attachment):
        if "Files" not in request:
            request["Files"] = []
        bytes = attachment.datas.decode()
        sha256 = hashlib.sha256()
        sha256.update(b64decode(bytes))
        request["Files"].append({
            "Bytes": bytes,
            "MimeType": "text/xml",
            "Nome": attachment.name,
            "Extension": "XML",
            "Hash": sha256.hexdigest(),
        })

    @api.model
    def evolve_request(
            self, action, archive, domain=None, invoice=None, attachment=None):
        """Send a request to Evolve"""
        data = {}
        errmsg = ""
        header = self.evolve_header()
        request = {}
        if domain:
            self.add_domain(request, domain)
        if invoice:
            self.add_document(request, invoice)
        if attachment:
            self.add_attachment(request, attachment)
        for key, val in self.evolve_documenti(archive).items():
            if "Documento" in request:
                request["Documento"][key] = val
            else:
                request[key] = val
        url = os.path.join(self.sender_url, action)
        try:
            response = requests.post(
                url, headers=header, data=json.dumps(request, ensure_ascii=False)
            )
        except requests.exceptions.RequestException as e:
            errmsg = e.message
        if not (200 <= response.status_code < 300):
            errmsg = "http error %s: '%s'" % (response.status_code, response.text)
        if not errmsg:
            data = response.json()
            for item in ("ErrorStack", "ErrorInnerExceptions", "ErrorMessage"):
                if item in data:
                    errmsg = "%s='%s'" % (item, data[item])
            if data["EsitoChiamata"] == 2:
                errmsg = "Errore di autenticazione:" + "\n" + errmsg
            elif data["EsitoChiamata"] and not errmsg:
                errmsg = (data.get("ErrorMessage") or "Errore generico") + "\n" + errmsg
        if errmsg:
            _logger.warning("Evolve.%s -> <<<%s>>>" % (action, errmsg))
        return data, -data.get("EsitoChiamata", 99), errmsg

    @api.model
    def evolve_search_by_number(self, invoice):
        """Search for invoice in sent archive"""
        archive = self.archive_in if self.is_self_invoice(invoice) else self.archive_out
        data, sts, errmsg = self.evolve_request(
            "Cerca",
            archive,
            domain=["NumeroFattura", "=", invoice.number,]
        )
        return sts == 0 and data.get("Documenti", [])

    @api.model
    def evolve_send_invoice(self, invoice, att):
        """Send invoice to Evolve sent archive"""
        data, sts, errmsg = self.evolve_request(
            "Salva",
            self.archive_sent,
            invoice=invoice,
            attachment=att,
        )
        return sts == 0

    def send_via_evolve(self, attachment_out_ids):
        """Override this method to send the attachments to the web service."""
        # self.client_company_id = 97   # debug
        if (
            not self.client_id
            or not self.client_key
            or not self.client_company_id
            or not self.sender_url
            or not self.exchange_hub
        ):
            raise UserError(_("SDI channel %s non configured" % self.name))
        for att in attachment_out_ids:
            for invoice in att.out_invoice_ids:
                found = self.evolve_search_by_number(invoice)
                # found = False   # debug
                if found:
                    continue
                sts =self.evolve_send_invoice(invoice, att)
                if sts:
                    break
