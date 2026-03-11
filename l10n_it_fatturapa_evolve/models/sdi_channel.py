#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import os
from datetime import datetime, timedelta
import logging
import re
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

EVOLVE_STATO_MAPPING = {
    "Inviato": "sent",
    "Il documento è in fase di invio": "sent",
    "Inviata a Sdi": "sent",
    "In attesa di conferma dall'utente": "sent",
    "In attesa di risposta dopo aver inviato il documento": "sent",
    "Importato": "sent",
    "Controlli validazione": "sent",
    "Errore": "rejected",
    "Notifica di scarto": "rejected",
    "Il documento non può essere preso in carico": "rejected",
    "Il documento non ha superato i controlli di validazione": "rejected",
    "Ricevuta di consegna": "validated",
    "Ricevuta di ritorno": "validated",
    "Notifica di mancata consegna": "recipient_error",
    "Notifica di esito: documento rifiutato dalla PA": "discarted",
    "Notifica di esito: documento accettato": "accepted",
    "Notifica di decorrenza termini": "recipient_error",
    "ERRORE SCONOSCIUTO": "sender_error",
}


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

    def evolve_map_response(self, state):
        res = EVOLVE_STATO_MAPPING.get(state)
        if not res:
            if re.match(
                "^(inviat[oiae]|in attesa di|importato|controlli .*validazione)",
                state, re.I
            ):
                res = "sent"
            elif re.match(
                "^(il documento non |notific[ahe]+ .*scart[oiae]|errore)",
                state, re.I
            ):
                res = "rejected"
            elif re.match(
                "^(ricevut[ae] .*mancata|notific[ahe]+ .*decorrenza)",
                state, re.I
            ):
                res = "recipient_error"
            elif re.match("^notifica .*esito.*rifiutat", state, re.I):
                res = "discarted"
            elif re.match("^notifica .*esito.*accettat", state, re.I):
                res = "accepted"
            else:
                res = "sender_error"
        return res

    @api.model
    def evolve_document_response(self, documento):
        if documento.get('TD') in ('TD17', 'TD18', 'TD19'):
            return "validated"
        elif "StatoFattura" in documento:
            return self.evolve_map_response(documento["StatoFattura"])
        elif "StatoInvioSdi" in documento:
            return self.evolve_map_response(documento["StatoInvioSdi"])
        return "sender_error"

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
    def evolve_add_domain(self, request, domain):
        if "Filtri" not in request:
            request["Filtri"] = []
        request["Filtri"].append({
            "NomeCampo": domain[0],
            "Criterio": domain[1],
            "FromValue": domain[2],
        })

    @api.model
    def evolve_add_document(self, request, invoices):
        if "Documento" not in request:
            request["Documento"] = {}
            request["Documento"]["Visible"] = True
            request["Documento"]["CampiDinamici"] = []
        for invoice in invoices:
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
    def evolve_add_attachment(self, request, attachment):
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
            self, action, archive, domain=None, invoices=None, attachment=None):
        """Send a request to Evolve"""
        data = {}
        errmsg = ""
        header = self.evolve_header()
        request = {}
        if domain:
            self.evolve_add_domain(request, domain)
        if invoices:
            self.evolve_add_document(request, invoices)
        if attachment:
            self.evolve_add_attachment(request, attachment)
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
            if attachment:
                attachment.last_sdi_response = errmsg
        return data, -data.get("EsitoChiamata", 99), errmsg

    @api.model
    def evolve_search_by_number(self, invoice):
        """Search for invoice in out (or in for self invoice) archive"""
        archive = self.archive_in if self.is_self_invoice(invoice) else self.archive_out
        data, sts, errmsg = self.evolve_request(
            "Cerca",
            archive,
            domain=["NumeroFattura", "=", invoice.number]
        )
        return sts == 0 and data.get("Documenti", [])

    def evolve_check_if_sending(self, invoice):
        """Search for invoice in sent archive"""
        data, sts, errmsg = self.evolve_request(
            "Cerca",
            self.archive_sent,
            domain=["NumeroFattura", "=", invoice.number]
        )
        return sts == 0 and data.get("Documenti", [])

    @api.model
    def evolve_send_invoice(self, invoices, att):
        """Send invoice to Evolve sent archive"""
        data, sts, errmsg = self.evolve_request(
            "Salva",
            self.archive_sent,
            invoices=invoices,
            attachment=att,
        )
        return sts == 0

    @api.model
    def evolve_parse_documento(self, doc):
        res = {}
        for campodinamico in doc["CampiDinamici"]:
            res[campodinamico["Nome"]] = campodinamico["Valore"]
        return res

    @api.model
    def evolve_document_list(self, data):
        res = []
        for doc in data:
            res.append(self.evolve_parse_documento(doc))
        return res

    def send_via_evolve(self, attachment_out_ids):
        """Override this method to send the attachments to the web service."""
        if (
            not self.client_id
            or not self.client_key
            or not self.client_company_id
            or not self.sender_url
            or not self.exchange_hub
        ):
            raise UserError(_("SDI channel %s non configured" % self.name))
        for att in attachment_out_ids:
            att_state = att.state
            to_send = False
            for invoice in att.out_invoice_ids:
                if (
                    self.evolve_search_by_number(invoice)
                    or self.evolve_check_if_sending(invoice)
                ):
                    att_state = "sent"
                    continue
                to_send = True
            if to_send:
                sts = self.evolve_send_invoice(att.out_invoice_ids, att)
                att_state = "sender_error" if sts else "sent"
            if att.state != att_state:
                att.state = att_state
                att.sending_date = fields.Datetime.now()
                att.sending_user = self.env.user.id
            if to_send and sts:
                break
        return True

    @api.model
    def verify_all_notifications(self):
        date_limit_no_pa = (
            datetime.now() - timedelta(days=self.capture_days)).strftime("%Y-%m-%d")
        date_limit_pa = (
            datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
        attachments = self.env["fatturapa.attachment.out"].search(
            [
                "|",
                "|",
                ("state", "=", "sent"),
                "&",
                ("state", "in", ["recipient_error", "sender_error"]),
                ("sending_date", ">=", date_limit_no_pa),
                "&",
                ("sending_date", ">=", date_limit_pa),
                ("invoice_partner_id.is_pa", "=", True),
            ]
        )
        for att in attachments:
            att_state = att.state
            for invoice in att.out_invoice_ids:
                data = self.evolve_search_by_number(invoice)
                if not data:
                    # No invoice got from Evolve server
                    limit_date = datetime.now() - timedelta(days=1)
                    if (
                        self.evolve_check_if_sending(invoice)
                        and att.sending_date > limit_date
                    ):
                        att_state = "sent"
                        break
                    elif not att.sending_date or (
                        att.sending_date and att.sending_date < limit_date
                    ):
                        att_state = "ready"
                        att.last_sdi_response = (
                            "No riscontro da SdI, inviare nuovamente documento")
                        break
                    else:
                        # Invoice sent but no detected in server: it is a sender error
                        att_state = "sender_error"
                        att.last_sdi_response = "Documento non convalidato da SdI"
                        break
                # Got one or more invoices
                last_date = "2019-01-01T00:00:00"
                last_ix = -1
                valid_ix = -1
                documents = self.evolve_document_list(data)
                for ii, doc in enumerate(documents):
                    data_caricamento = doc.get("DataCaricamento", doc["DataFattura"])
                    if self.evolve_document_response(doc) == "accepted":
                        # PA final workflow: accepted
                        # last_date = data_caricamento
                        last_ix = ii
                        break
                    elif data_caricamento > last_date:
                        last_date = data_caricamento
                        if "Fattura duplicata" not in doc.get("Note", ""):
                            last_ix = ii
                    if self.evolve_document_response(doc) == "validated":
                        # No PA subject final workflow: validated
                        valid_ix = ii
                    elif "disponibile in consultazione nell'area riservata" in doc.get(
                        "Note", ""
                    ):
                        # Final workflow for no VAT partner
                        valid_ix = ii
                if (
                    valid_ix >= 0
                    and last_ix >= 0
                    and self.evolve_document_response(documents[last_ix]) in (
                        "sender_error", "sent", "rejected")
                ):
                    # Final workflow for No PA subjects
                    last_ix = valid_ix
                att_state = self.evolve_document_response(documents[last_ix])
                limit_date = (datetime.now() - timedelta(days=5)).strftime(
                    "%Y-%m-%d %H:%M:%S")
                if (
                    att_state == "sent"
                    and att.sending_date
                    and att.sending_date < limit_date
                ):
                    # Invoice sent since too much time: it is an error
                    att.last_sdi_response = "No riscontro da SdI da troppo tempo"
                    att_state = "sender_error"
                if att_state == "recipient_error":
                    delivered_date = datetime.strptime(
                        documents[last_ix]["DataFattura"], "%Y-%m-%dT%H:%M:%S"
                    ) + timedelta(days=32)
                    if (
                        last_ix == valid_ix
                        or delivered_date < datetime.today()
                    ):
                        # Invoice sent for a long time w/o error: it is ok
                        att_state = "validated"
                        att.last_sdi_response = "No errori da SdI da lungo tempo"
                if att_state not in ("sender_error", "validated"):
                    # Found valid sent invoice: get specific state
                    att_state = self.evolve_document_response(documents[last_ix])
            if att.state != att_state:
                att.state = att_state
