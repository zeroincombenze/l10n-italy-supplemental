# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import hashlib
import json
import logging
import os
import re
from base64 import b64decode, b64encode
from datetime import datetime, timedelta

import pytz
import requests
from Crypto.Cipher import AES
from lxml import etree
from os0 import os0
from pkcs7 import PKCS7Encoder

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.base.ir.ir_mail_server import MailDeliveryException

_logger = logging.getLogger(__name__)

RESPONSE_MAIL_REGEX = (
    "[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}_[A-Z]{2}_" "[a-zA-Z0-9]{,3}"
)

evolve_stato_mapping = {
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


def text2html(text):
    return text.replace("<", "&lt;").replace(">", "&gt;")


def map_response(state):
    res = evolve_stato_mapping.get(state)
    if not res:
        if re.match(
                "^(inviat[oiae]|in attesa di|importato|controlli .*validazione)",
                state, re.I):
            res = "sent"
        elif re.match(
                "^(il documento non |notific[ahe]+ .*scart[oiae]|errore)",
                state, re.I):
            res = "rejected"
        elif re.match(
                "^(ricevut[ae] .*mancata|notific[ahe]+ .*decorrenza)",
                state, re.I):
            res = "recipient_error"
        elif re.match(
                "^notifica .*esito.*rifiutat",
                state, re.I):
            res = "discarted"
        elif re.match(
                "^notifica .*esito.*accettat",
                state, re.I):
            res = "accepted"
        else:
            res = "sender_error"
    return res


class FatturaPAAttachmentIn(models.Model):

    _inherit = "fatturapa.attachment.in"

    @api.model
    def dict_2_print(self, values):  # pragma: no cover
        def to_str(obj):
            x = str(obj)
            return x if (hasattr(obj, "len") and len(x) < 150) else "[...]"

        if isinstance(values, dict):
            return json.dumps(values, default=to_str, indent=4)
        return values

    @api.multi
    def import_xml_invoice(self):
        for company in self.env["res.company"].search([]):
            send_channel = company.einvoice_sender_id
            if not send_channel:
                _logger.error("Undefined SDI channel for company %s" % company.name)
                continue
            if not send_channel.sender_url:
                _logger.error(
                    "Undefined URL of SDI channel for company %s" % company.name
                )
                continue

            if (
                send_channel.max_invoices_ctr > 0
                and send_channel.used_invoices_ctr == 0
            ):
                # Get used invoices
                send_channel.count_xml_invoice()
                self.env.cr.commit()  # pylint: disable=invalid-commit

            headers = Evolve.header(send_channel)
            url = os.path.join(send_channel.sender_url, "Cerca")
            archive_in = int(send_channel.param2) if send_channel.param2 else 2
            domain_mode = int(send_channel.param4) if send_channel.param4 else 0
            last_demand = send_channel.param5

            data = {
                "IdAzienda": int(send_channel.sender_company_id),
                "IdArchivio": archive_in,
                "Filtri": [],
            }
            if 0 < domain_mode <= 60:
                limit_date = (
                    datetime.now() - timedelta(days=domain_mode)
                ).strftime("%Y-%m-%dT%H:%M:%S")
                data["Filtri"] = [
                    {
                        "NomeCampo": "DataRicezione",
                        "Criterio": ">",
                        "FromValue": limit_date,
                    }
                ]
            elif 0 > domain_mode >= -60:
                limit_date = (
                    datetime.now() + timedelta(days=domain_mode)
                ).strftime("%Y-%m-%dT%H:%M:%S")
                data["Filtri"] = [
                    {
                        "NomeCampo": "DataFattura",
                        "Criterio": ">",
                        "FromValue": limit_date,
                    }
                ]
            elif domain_mode == 0:
                if last_demand:
                    last_dt = datetime.strptime(last_demand, "%Y-%m-%dT%H:%M:%S")
                if (
                        last_demand
                        and last_dt.day == datetime.now().day
                        and last_dt.month == datetime.now().month
                ):
                    limit_date = last_demand
                else:
                    limit_date = (datetime.now()
                                  - timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:%S")
                data["Filtri"] = [
                    {
                        "NomeCampo": "DataDownload",
                        "Criterio": "nullo",
                    },
                    {
                        "NomeCampo": "DataRicezione",
                        "Criterio": ">",
                        "FromValue": limit_date,
                    },
                ]
            _logger.info(json.dumps(data, ensure_ascii=False))

            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(data, ensure_ascii=False)
                )
            except BaseException:
                _logger.error("request.post FAILED for company %s" % company.name)
                continue
            if not (200 <= response.status_code < 300):
                _logger.error("FAILED request.post: %s" % response.status_code)
                continue

            last_demand = (datetime.now()
                           - timedelta(seconds=3600)).strftime("%Y-%m-%dT%H:%M:%S")
            send_channel.write({"param5": last_demand})

            try:
                documenti = response.json()
                if documenti["EsitoChiamata"] > 0:
                    _logger.info(response.text.replace(r"\r\n", "\n"))
                    continue
            except BaseException:
                continue

            for value in documenti["Documenti"]:
                documento = Evolve.parse_documento(value)
                try:
                    self.import_xml_invoice_single(documento, send_channel, headers)
                except BaseException:
                    break

    # Import singolo documento
    def import_xml_invoice_single(self, documento, send_channel, headers):

        attach_model = self.env["fatturapa.attachment.in"]
        data_ricezione = documento["DataRicezione"]
        # attachments = attach_model.search([("uid", "=", documento["Uid"])])
        # if len(attachments) > 0:
        #     attachments[0].write({"e_invoice_received_date": data_ricezione})
        #     return
        archive = int(send_channel.param2) if send_channel.param2 else 2

        data = {
            "Documento": {
                "IdAzienda": int(send_channel.sender_company_id),
                "IdArchivio": archive,
                "CampiDinamici": [{"Nome": "Uid", "Valore": documento["Uid"]}],
            },
            "Recupera": 2,
        }

        url = os.path.join(send_channel.sender_url, "Recupera")

        _logger.info(json.dumps(data, ensure_ascii=False))

        try:
            response = requests.post(
                url, headers=headers, data=json.dumps(data, ensure_ascii=False)
            )
        except BaseException:
            _logger.error("request.post FAILED")
            return
        if not (200 <= response.status_code < 300):
            _logger.error("FAILED request.post: %s" % response.status_code)
            return

        try:
            documenti = response.json()
            if documenti["EsitoChiamata"] > 0:
                _logger.info(response.text.replace(r"\r\n", "\n"))
                return
        except BaseException:
            _logger.error(response.text.replace(r"\r\n", "\n"))
            return

        documento = Evolve.parse_documento(documenti["Documenti"][0])

        # Recupero il file xml
        for file in documenti["Files"]:
            if file["Nome"] == documento["NomeFile"]:
                filein = file
                break

        attach_vals = {
            "name": filein["Nome"],
            "e_invoice_received_date": data_ricezione,
            "datas_fname": filein["Nome"],
            "datas": filein["Bytes"],
            "uid": documento["Uid"],
        }

        if attach_vals["name"].endswith(".p7m"):
            search_domain = [
                "|",
                ("name", "=", attach_vals["name"]),
                ("name", "=", attach_vals["name"][: -4]),
                ("uid", "=", attach_vals["uid"])
            ]
        else:
            search_domain = [
                ("name", "=", attach_vals["name"]),
                ("uid", "=", attach_vals["uid"])
            ]

        if attach_model.search(search_domain):
            return

        try:
            attach_model.create(attach_vals)
            send_channel.incr_invoice_counter()
        except BaseException as e:
            _logger.error("Error <%s> creating XML attachment" % e)


class FatturaPAAttachmentOut(models.Model):

    _inherit = "fatturapa.attachment.out"

    state = fields.Selection(
        [
            ("ready", "Ready to Send"),
            ("sent", "Sent"),
            ("sender_error", "Sender Error"),
            ("recipient_error", "Recipient Error"),
            ("rejected", "Rejected"),
            ("validated", "Delivered"),
            ("accepted", "Accepted"),
            ("discarted", "Discarted by PA"),
        ],
        string="State",
        default="ready",
    )

    last_sdi_response = fields.Html(
        string="Last Response from Exchange System",
        default="No response yet",
        readonly=True,
    )
    sending_date = fields.Datetime("Sent Date", readonly=True)
    delivered_date = fields.Datetime("Delivered Date", readonly=True)
    sending_user = fields.Many2one("res.users", "Sending User", readonly=True)

    @api.model
    def dict_2_print(self, values):  # pragma: no cover
        def to_str(obj):
            x = str(obj)
            return x if (hasattr(obj, "len") and len(x) < 150) else "[...]"

        if isinstance(values, dict):
            return json.dumps(values, default=to_str, indent=4)
        return values

    @api.multi
    def parse_pec_response(self, message_dict):
        message_dict["model"] = self._name
        message_dict["res_id"] = 0

        regex = re.compile(RESPONSE_MAIL_REGEX)
        attachments = [x for x in message_dict["attachments"] if regex.match(x.fname)]

        for attachment in attachments:
            response_name = attachment.fname
            message_type = response_name.split("_")[2]
            if attachment.fname.lower().endswith(".zip"):
                # not implemented, case of AT, todo
                continue
            root = etree.fromstring(attachment.content)
            file_name = root.find("NomeFile")
            fatturapa_attachment_out = False

            if file_name is not None:
                file_name = file_name.text
                fatturapa_attachment_out = self.search(
                    [
                        "|",
                        ("datas_fname", "=", file_name),
                        ("datas_fname", "=", file_name.replace(".p7m", "")),
                    ]
                )
                if len(fatturapa_attachment_out) > 1:
                    _logger.info("More than 1 out invoice found for incoming" "message")
                    fatturapa_attachment_out = fatturapa_attachment_out[0]
                if not fatturapa_attachment_out:
                    if message_type == "MT":  # Metadati
                        # out invoice not found, so it is an incoming invoice
                        return message_dict
                    else:
                        _logger.error(
                            "Error: FatturaPA {} not found.".format(file_name)
                        )
                        # TODO Send a mail warning
                        return message_dict

            if fatturapa_attachment_out:
                id_sdi = root.find("IdentificativoSdI")
                receipt_dt = root.find("DataOraRicezione")
                message_id = root.find("MessageId")
                id_sdi = id_sdi.text if id_sdi is not None else False
                receipt_dt = receipt_dt.text if receipt_dt is not None else False
                message_id = message_id.text if message_id is not None else False
                if message_type == "NS":  # 2A. Notifica di Scarto
                    error_list = root.find("ListaErrori")
                    error_str = ""
                    for error in error_list:
                        error_str += "\n[%s] %s %s" % (
                            error.find("Codice").text
                            if error.find("Codice") is not None
                            else "",
                            error.find("Descrizione").text
                            if error.find("Descrizione") is not None
                            else "",
                            error.find("Suggerimento").text
                            if error.find("Suggerimento") is not None
                            else "",
                        )
                    fatturapa_attachment_out.write(
                        {
                            "state": "sender_error",
                            "last_sdi_response": "SdI ID: {}; "
                            "Message ID: {}; Receipt date: {}; "
                            "Error: {}".format(
                                id_sdi, message_id, receipt_dt, error_str
                            ),
                        }
                    )
                elif message_type == "MC":  # 3A. Mancata consegna
                    missed_delivery_note = root.find("Descrizione").text
                    fatturapa_attachment_out.write(
                        {
                            "state": "recipient_error",
                            "last_sdi_response": "SdI ID: {}; "
                            "Message ID: {}; Receipt date: {}; "
                            "Missed delivery note: {}".format(
                                id_sdi, message_id, receipt_dt, missed_delivery_note
                            ),
                        }
                    )
                elif message_type == "RC":  # 3B. Ricevuta di Consegna
                    delivery_dt = root.find("DataOraConsegna").text
                    fatturapa_attachment_out.write(
                        {
                            "state": "validated",
                            "delivered_date": fields.Datetime.now(),
                            "last_sdi_response": "SdI ID: {}; "
                            "Message ID: {}; Receipt date: {}; "
                            "Delivery date: {}".format(
                                id_sdi, message_id, receipt_dt, delivery_dt
                            ),
                        }
                    )
                elif message_type == "NE":  # 4A. Notifica Esito per PA
                    esito_committente = root.find("EsitoCommittente")
                    if esito_committente is not None:
                        # more than one esito?
                        esito = esito_committente.find("Esito")
                        if esito is not None:
                            if esito.text == "EC01":
                                state = "validated"
                            elif esito.text == "EC02":
                                state = "rejected"
                            fatturapa_attachment_out.write(
                                {
                                    "state": state,
                                    "last_sdi_response": "SdI ID: {}; "
                                    "Message ID: {}; Response: {}; ".format(
                                        id_sdi, message_id, esito.text
                                    ),
                                }
                            )
                elif message_type == "DT":  # 5. Decorrenza Termini per PA
                    description = root.find("Descrizione")
                    if description is not None:
                        fatturapa_attachment_out.write(
                            {
                                "state": "validated",
                                "last_sdi_response": "SdI ID: {}; "
                                "Message ID: {}; Receipt date: {}; "
                                "Description: {}".format(
                                    id_sdi, message_id, receipt_dt, description.text
                                ),
                            }
                        )
                # not implemented - todo
                elif message_type == "AT":  # 6. Avvenuta Trasmissione per PA
                    description = root.find("Descrizione")
                    if description is not None:
                        fatturapa_attachment_out.write(
                            {
                                "state": "validated",
                                "last_sdi_response": (
                                    "SdI ID: {}; Message ID: {}; "
                                    "Receipt date: {};"
                                    " Description: {}"
                                ).format(
                                    id_sdi, message_id, receipt_dt, description.text
                                ),
                            }
                        )

                message_dict["res_id"] = fatturapa_attachment_out.id
        return message_dict

    @api.model
    def get_send_channel(self):
        company = False
        send_channel = False
        for invoice in self.out_invoice_ids:
            company = invoice.company_id
            break
        if company:
            send_channel = company.einvoice_sender_id
        if send_channel is False:
            _logger.error("Undefined SDI channel")
        return send_channel

    @api.model
    def primitive_json_send(self, send_channel, req, archive, action, attachment=None):
        if send_channel.trace:
            _logger.info(
                ">>> primitive_json_send(%s,%s,%s,%s)" % (
                    send_channel, self.dict_2_print(req), archive, action)
            )
        if "Documento" in req:
            req["Documento"]["IdAzienda"] = int(send_channel.sender_company_id)
            req["Documento"]["IdArchivio"] = archive
        else:
            req["IdAzienda"] = int(send_channel.sender_company_id)
            req["IdArchivio"] = archive
        headers = Evolve.header(send_channel)
        url = os.path.join(send_channel.sender_url, action)
        if send_channel.trace:
            _logger.info(
                ">>> requests.post(%s,headers=%s,req)" % (
                    url, self.dict_2_print(headers))
            )
        try:
            response = requests.post(
                url, headers=headers, data=json.dumps(req, ensure_ascii=False)
            )
        except BaseException:
            errmsg = "<p>requests.post() FAILED!</p>"
            if send_channel.trace:
                _logger.info(">>> %s" % errmsg)
            if attachment:
                attachment.state = "sender_error"
            if send_channel.trace:
                _logger.info(">>> requests.post() FAILED!")
            return False, errmsg
        if not (200 <= response.status_code < 300):
            errmsg = "<p>request.post FAILED: %s</p>" % response.status_code
            _logger.error(errmsg)
            if attachment:
                attachment.state = "sender_error"
                attachment.last_sdi_response = errmsg
            if send_channel.trace:
                _logger.info(">>> requests.post() -> %s!" % response.status_code)
            return False, errmsg
        try:
            data = response.json()
            errmsg = ""
            for item in ("ErrorStack", "ErrorInnerExceptions", "ErrorMessage"):
                if item in data:
                    errmsg += '<p>%s = "%s"</p>' % (item, data[item])
            if send_channel.trace:
                _logger.info(">>> response.json()=\n%s\n" % errmsg or data)
            if data["EsitoChiamata"] > 0:
                # Store response even if not trace enabled
                errmsg = response.text.replace(r"\r\n", "\n")
                if not send_channel.trace:
                    _logger.info(errmsg)
                if attachment:
                    attachment.state = "sender_error"
                    errmsg = errmsg.replace("\n", "</p><p>")
                    if errmsg.endswith("<p>"):
                        errmsg = errmsg[:-3]
                    attachment.last_sdi_response = "<p>%s" % errmsg
                if send_channel.trace:
                    _logger.info(">>> requests.post().esito_chiamata -> %s!"
                                 % data["EsitoChiamata"])
                return False, errmsg
        except BaseException:
            errmsg = "<p>response.json() FAILED!</p>"
            if send_channel.trace:
                _logger.info(">>> %s" % errmsg)
            if attachment:
                attachment.state = "sender_error"
            if send_channel.trace:
                _logger.info(">>> requests.post() FAILED!")
            return False, errmsg
        if send_channel.trace:
            _logger.info(">>> requests.post() -> %s" % self.dict_2_print(data))
        return data, False

    def analyze_data_list(self, att, data, errmsg, documenti, store_mesg=None):
        # att_state = att.state
        last_ix = -1
        if not Evolve.has_document(data):
            # No invoice got from server
            limit_date = (datetime.now() - timedelta(days=1)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if not att.sending_date or (
                att.sending_date and att.sending_date < limit_date
            ):
                # Invoice not sent or sent before today: set to ready
                att_state = "ready"
            else:
                # Invoice sent but no detected in server: it is a sender error
                att_state = "sender_error"
                if store_mesg:
                    if errmsg:
                        att.last_sdi_response = "<p>%s</p><p>%s</p><p>%s</p>" % (
                            "ERRORE DI COMUNICAZIONE!",
                            errmsg,
                            "Ricontrollare più tardi.",
                        )
                    else:
                        att.last_sdi_response = "<p>%s</p><p>%s</p>" % (
                            "IN ATTESA DI RISPOSTA!",
                            "Fattura inviata, ricontrollare più tardi.",
                        )
        else:
            # Got invoices sent before
            if len(documenti) == 0:
                # False response! No data, it is a sender error
                att_state = "sender_error"
                if store_mesg:
                    att.last_sdi_response = "<p>%s</p><p>%s</p>" % (
                        "CONTROLLI DI VALIDAZIONE!",
                        "Ricontrollare più tardi.",
                    )
            else:
                # Got one or more invoices
                last_date = "2019-01-01T00:00:00"
                valid_ix = -1
                for ii, doc in enumerate(documenti):
                    data_caricamento = doc.get("DataCaricamento", doc["DataFattura"])
                    if map_response(Evolve.document_state(doc)) == "accepted":
                        # PA final workflow: accepted
                        # last_date = data_caricamento
                        last_ix = ii
                        break
                    elif data_caricamento > last_date:
                        last_date = data_caricamento
                        if "Fattura duplicata" not in doc.get("Note", ""):
                            last_ix = ii
                    if map_response(Evolve.document_state(doc)) == "validated":
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
                    and map_response(Evolve.document_state(
                        documenti[last_ix])) in ("sender_error", "sent", "rejected")
                ):
                    # Final workflow for No PA subjects
                    last_ix = valid_ix
                att_state = map_response(Evolve.document_state(documenti[last_ix]))
                limit_date = (datetime.now() - timedelta(days=5)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if (
                    att_state == "sent"
                    and att.sending_date
                    and att.sending_date < limit_date
                ):
                    # Invoice sent since too much time: it is an error
                    att_state = "sender_error"
                if att_state == "recipient_error":
                    delivered_date = datetime.strptime(
                        documenti[last_ix]["DataFattura"], "%Y-%m-%dT%H:%M:%S"
                    ) + timedelta(days=32)
                    if (
                        last_ix == valid_ix
                        or delivered_date < datetime.today()
                    ):
                        # Invoice sent for a long time w/o error: it is ok
                        att_state = "validated"
                if att_state in ("sender_error", "validated"):
                    if store_mesg:
                        att.last_sdi_response = "<div>%s</div>\n" % (
                            text2html(documenti[last_ix].get("Note", ""))
                        )
                else:
                    # Found valid sent invoice: get specific state
                    att_state = map_response(Evolve.document_state(documenti[last_ix]))
        att.state = att_state
        return att, last_ix

    def build_history(self, documenti, valid_ix):
        line_fmt = ""
        for _ii in range(11):
            line_fmt += "<td>%s</td>"
        row_fmt = "<tr>" + line_fmt + "</tr>\n"
        history = (
            "<p>%s</p>\n<p>"
            '<table border="2px" cellpadding="2px" style="padding: 5px;">'
            + row_fmt.replace("td", "th")
        ) % (
            datetime.now(),
            "Data Caricamento",
            "Stato Invio SdI",
            "Tipo Documento",
            "Mittente",
            "Destinatario",
            "Dest. PartitaIva",
            "Data Fattura",
            "UID",
            "Valuta",
            "Imponibile",
            "Note",
        )
        for ii, doc in enumerate(documenti):
            history += row_fmt % (
                doc.get("DataCaricamento", ""),
                "<strong>%s</strong>" % Evolve.document_state(doc)
                if ii == valid_ix
                else Evolve.document_state(doc),
                doc.get("TipoDocumento", ""),
                doc.get("Mittente", ""),
                doc.get("Destinatario", ""),
                doc.get("DestinatarioPartitaIva", ""),
                doc.get("DataFattura", "")[:10],
                doc.get("Uid", ""),
                doc.get("Valuta", ""),
                doc.get("Imponibile", ""),
                "<strong>%s</strong>" % text2html(doc.get("Note", ""))
                if ii != valid_ix
                else text2html(doc.get("Note", "")),
            )
        history += "</table></p>"
        return history

    @api.multi
    def send_verify_via_json(self, send_channel, invoice):
        for att in self:
            data, errmsg, documenti = self.search_via_json(
                send_channel, invoice, full_info=True
            )
            att, last_ix = self.analyze_data_list(
                att, data, errmsg, documenti, store_mesg=True
            )
            if not documenti:
                continue
            att.last_sdi_response = self.build_history(documenti, last_ix)

    @api.multi
    def send_verify_via_pec(self, send_channel, invoice):
        pass

    @api.multi
    def send_verify(self):
        send_channel = self.get_send_channel()
        if send_channel is False:
            raise UserError(_("Undefined SDI channel"))

        invoice = self.out_invoice_ids
        if len(invoice) > 1:
            raise UserError(_("Multiple invoice to one xml"))

        if send_channel.method == "JSON":
            return self.send_verify_via_json(send_channel, invoice)
        elif send_channel.method == "PEC":
            return self.send_verify_via_pec(send_channel, invoice)
        else:
            raise UserError(_("Unsupported sending method"))

    @api.multi
    def send_verify_all(self):
        # Recupero tutte le fatture in modalita send
        date_limit_no_pa = (datetime.now() - timedelta(days=30)).strftime(
            "%Y-%m-%d"
        )
        date_limit_pa = (datetime.now() - timedelta(days=150)).strftime(
            "%Y-%m-%d"
        )
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
        for attachment in attachments:
            attachment.send_verify()
            # commit every table to avoid too big transaction
            self.env.cr.commit()  # pylint: disable=invalid-commit

    @api.multi
    def reset_to_ready(self):
        for att in self:
            if att.state in ("validated", "accepted"):
                raise UserError(_("You can not reset files in 'Delivered' state."))
            att.state = "ready"

    @api.multi
    def set_to_delivered(self):
        for att in self:
            if att.state != "recipient_error":
                raise UserError(
                    _("You can not reset files in 'recipient_error' state.")
                )
            att.state = "validated"

    @api.model
    def search_via_json(self, send_channel, invoice, full_info=None):
        def merge(documenti, documenti2):
            for doc in documenti:
                for doc2 in documenti2:
                    if doc["Uid"] == doc2.get("Uid"):
                        for nm in ["DataCaricamento", "Note", "StatoInvioSdi"]:
                            if nm in doc2:
                                doc[nm] = doc2[nm]
                        break
            for doc2 in documenti2:
                if not doc2.get("Uid") or doc2["Uid"] not in [
                    x.get("Uid") for x in documenti
                ]:
                    documenti.append(doc2)
            return documenti

        if send_channel.trace:
            _logger.info(
                ">>> search_via_json(%s,%s)" % (send_channel, invoice.number)
            )

        archive_out = int(send_channel.param1) if send_channel.param1 else 1
        archive_in = int(send_channel.param2) if send_channel.param2 else 2
        archive_sent = int(send_channel.param3) if send_channel.param3 else 3
        if send_channel.trace:
            _logger.info(
                ">>> remote_archive_sent/in/out=%s,%s,%s" % (
                    archive_sent, archive_in, archive_out)
            )
        request = {
            "Filtri": [
                {
                    "NomeCampo": "NumeroFattura",
                    "Criterio": "=",
                    "FromValue": invoice.number,
                }
            ]
        }
        documenti = []
        if invoice.fiscal_document_type_id.code in ('TD17', 'TD18', 'TD19'):
            data, errmsg = self.primitive_json_send(
                send_channel, request, archive_in, "Cerca"
            )
        else:
            data, errmsg = self.primitive_json_send(
                send_channel, request, archive_out, "Cerca"
            )
        if Evolve.has_document(data) and data["EsitoChiamata"] == 0 and not errmsg:
            documenti = Evolve.document_list(data["Documenti"])
            if invoice.fiscal_document_type_id.code in ('TD17', 'TD18', 'TD19'):
                documenti[0]['TD'] = invoice.fiscal_document_type_id.code
            if full_info:
                data2, errmsg = self.primitive_json_send(
                    send_channel, request, archive_sent, "Cerca"
                )
                if (
                    Evolve.has_document(data2)
                    and data2["EsitoChiamata"] == 0
                    and not errmsg
                ):
                    documenti = merge(
                        documenti, Evolve.document_list(data2["Documenti"])
                    )
        else:
            data, errmsg = self.primitive_json_send(
                send_channel, request, archive_sent, "Cerca"
            )
            if Evolve.has_document(data) and data["EsitoChiamata"] == 0 and not errmsg:
                documenti = Evolve.document_list(data["Documenti"])
        return data, errmsg, documenti

    @api.multi
    def send_via_json(self, send_channel):
        if send_channel.trace:
            _logger.info(
                ">>> send_via_json(%s)" % (send_channel.name)
            )
        # Recupero i dati della fattura
        invoice = self.out_invoice_ids
        if len(invoice) > 1:
            raise UserError(_("Multiple invoice to one xml"))

        archive_sent = int(send_channel.param3) if send_channel.param3 else 3
        for att in self:
            data, errmsg, documenti = self.search_via_json(send_channel, invoice)
            att, last_ix = self.analyze_data_list(att, data, errmsg, documenti)
            if documenti and att.state in (
                "validated",
                "accepted",
                "sent",
                "recipient_error",
            ):
                att.last_sdi_response = self.build_history(documenti, last_ix)
                continue

            bytes = att.datas
            xml = b64decode(bytes)
            sha256 = hashlib.sha256()
            sha256.update(xml)
            request = {
                "Files": [
                    {
                        "Bytes": bytes,
                        "MimeType": "text/xml",
                        "Nome": att.name,
                        "Extension": "XML",
                        "Hash": sha256.hexdigest(),
                    }
                ],
                "Documento": {
                    "Visible": True,
                    "CampiDinamici": [
                        {
                            "Nome": "NumeroFattura",
                            "Valore": invoice.number,
                            "CriterioPredefinito": "=",
                        },
                        {
                            "Nome": "DataFattura",
                            "Valore": invoice.date,
                            "CriterioPredefinito": "=",
                        },
                    ],
                },
            }
            data, errmsg = self.primitive_json_send(
                send_channel, request, archive_sent, "Salva", attachment=att
            )

            if data and data["EsitoChiamata"] == 0:
                stato = Evolve.parse_documento(data["Documenti"][-1])
                if stato["StatoInvioSdi"]:
                    att.state = map_response(stato["StatoInvioSdi"])
                    att.sending_date = fields.Datetime.now()
                    att.sending_user = self.env.user.id
                    att.last_sdi_response = "Fattura Importata"
                    send_channel.incr_invoice_counter()
                    return True
                else:
                    if send_channel.trace:
                        _logger.info(">>>     response.json() failed: not imported!")
                    att.state = "sender_error"
                    att.last_sdi_response = "ERRORE IMPORTAZIONE FATTTURA"
            else:
                if send_channel.trace:
                    _logger.info(">>>     response.json() failed: esito != 0!")
                att.state = "sender_error"
                att.last_sdi_response = "ERRORE FATTTURA NON IMPORTATA"
            return False

    @api.multi
    def send_via_pec(self, send_channel):
        if send_channel.trace:
            _logger.info(
                ">>> send_via_pec(%s)" % (send_channel.name)
            )
        self._check_fetchmail()
        for att in self:
            mail_message = self.env["mail.message"].create(
                {
                    "model": self._name,
                    "res_id": att.id,
                    "subject": att.name,
                    "body": "XML file for FatturaPA {} sent to Exchange System to "
                    "the email address {}.".format(
                        att.name, send_channel.email_exchange_system
                    ),
                    "attachment_ids": [(6, 0, att.ir_attachment_id.ids)],
                    "email_from": (send_channel.email_from_for_fatturaPA),
                    "reply_to": (send_channel.email_from_for_fatturaPA),
                    "mail_server_id": send_channel.pec_server_id.id,
                }
            )

            mail = self.env["mail.mail"].create(
                {
                    "mail_message_id": mail_message.id,
                    "body_html": mail_message.body,
                    "email_to": send_channel.email_exchange_system,
                    "headers": {"Return-Path": send_channel.email_from_for_fatturaPA},
                }
            )

            if mail:
                try:
                    mail.send(raise_exception=True)
                    att.state = "sent"
                    att.sending_date = fields.Datetime.now()
                    att.sending_user = self.env.user.id
                except MailDeliveryException as e:
                    att.state = "sender_error"
                    mail.body = e[1]

    @api.multi
    def send_einvoice(self):
        states = self.mapped("state")
        if set(states) != {"ready"}:
            raise UserError(_("You can only send 'Ready to Send' files."))
        send_channel = self.get_send_channel()
        if send_channel.trace:
            _logger.info(
                ">>> %s.send_einvoice(max=%s,meth=%s)" % (
                    send_channel.name,
                    send_channel.max_invoices_ctr,
                    send_channel.method)
            )
        if send_channel.max_invoices_ctr > 0 and send_channel.used_invoices_ctr == 0:
            # Get used invoices
            send_channel.count_xml_invoice()
            self.env.cr.commit()  # pylint: disable=invalid-commit
        if send_channel.avail_invoices_ctr < 0:
            raise UserError(
                _("You cannot send invoices. Please buy a new invoices pack!")
            )
        if send_channel.method == "JSON":
            result = self.send_via_json(send_channel)
            if (
                send_channel.avail_invoices_ctr <= 20
                or send_channel.avail_invoices_ctr in (500, 250, 100, 50)
            ):
                return {
                    "name": "Import result",
                    "type": "ir.actions.act_window",
                    "res_model": "italy.ade.sender",
                    "view_type": "form",
                    "view_mode": "form",
                    "res_id": send_channel.id,
                    "target": "new",
                    "view_id": self.env.ref(
                        "l10n_it_einvoice_send2sdi.view_available_invoices"
                    ).id,
                    "domain": [("id", "=", send_channel.id)],
                }
            return result

        elif send_channel.method == "PEC":
            return self.send_via_pec(send_channel)
        else:
            raise UserError(_("Unsupported sending method"))

    @api.multi
    def send_all_xml_invoices(self):
        for einvoice in self.search([("state", "=", "ready")]):
            einvoice.send_einvoice()
            # commit every table to avoid too big transaction
            self.env.cr.commit()  # pylint: disable=invalid-commit

    @api.multi
    def unlink(self):
        for att in self:
            if att.state not in ("ready", "rejected", "discarted"):
                raise UserError(_("You can only delete 'ready to send' files."))
        return super(FatturaPAAttachmentOut, self).unlink()

    @api.model
    def _check_fetchmail(self):
        server = self.env["fetchmail.server"].search(
            [
                ("is_fatturapa_pec", "=", True),
            ]
        )
        if not server:
            raise UserError(_("No incoming PEC server found. Please configure it."))


class Evolve:
    @staticmethod
    def has_document(data):
        if data and data["EsitoChiamata"] == 0:
            return len(data["Documenti"]) > 0
        return False

    @staticmethod
    def document_list(data):
        res = []
        for doc in data:
            documento = Evolve.parse_documento(doc)
            res.append(documento)
        return res

    @staticmethod
    def document_state(documento):
        if documento.get('TD') in ('TD17', 'TD18', 'TD19'):
            return "Ricevuta di ritorno"
        elif "StatoFattura" in documento:
            return documento["StatoFattura"]
        elif "StatoInvioSdi" in documento:
            return documento["StatoInvioSdi"]
        return "ERRORE SCONOSCIUTO"

    @staticmethod
    def documenti_by_state(data):
        res = {}
        for doc in data["Documenti"]:
            documento = Evolve.parse_documento(doc)
            if documento["StatoFattura"] not in res:
                res[documento["StatoFattura"]] = []
            res[documento["StatoFattura"]].append(documento)
        return res

    @staticmethod
    def parse_documento(data):
        res = {}
        for campodinamico in data["CampiDinamici"]:
            res[campodinamico["Nome"]] = campodinamico["Valore"]
        return res

    @staticmethod
    def header(send_channel):
        if send_channel is False or not send_channel.client_key:
            return False
        now = datetime.now(pytz.timezone("Europe/Rome")).strftime(
            "%Y-%m-%d %H.%M.%S"
        )
        aes = AES.new(
            os0.b(send_channel.client_key),
            AES.MODE_CBC,
            os0.b(send_channel.client_key[:16]),
        )
        pad_text = PKCS7Encoder().encode(now)
        headers = {
            "Content-Type": "application/json",
            "From": send_channel.client_id,
            "Authorization": "Bearer " + b64encode(aes.encrypt(pad_text)),
        }
        # _logger.info(headers)
        return headers
