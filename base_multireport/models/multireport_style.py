# -*- coding: utf-8 -*-
#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import _, fields, models

HELP_HEAFOO = """You can insert html code to format the field.
You can use following macro:
%(banks)s  -> Company banks      %(codice_destinatario)s
%(city)s   -> Company city       %(fatturapa_rea_capital)s
%(email)s  -> Company email      %(fatturapa_rea_capital)s
%(fax)s    -> Company fax        %(fatturapa_rea_number)s
%(name)    -> Company name       %(fatturapa_rea_office)s
%(phone)s  -> Company phone      %(fiscalcode)s
%(street)s -> Company street     %(ipa_code)s
%(street2)s-> Company street2    %(mobile)s
%(vat)s    -> Company vat
%(website)s-> Company website
%s(zip)    -> Company zip"""


class MultireportStyle(models.Model):
    _name = "multireport.style"
    _description = "Multi Report Document Style"

    name = fields.Char(
        "Name of Style", required=True, help="Give a unique name for this report style"
    )
    origin = fields.Selection(
        [("odoo", "Original Odoo Model"), ("odoo_based", "Odoo based Model")],
        "Report origin/indentity",
        required=True,
        help="Original report",
        default="odoo",
    )
    # default values
    header_mode = fields.Selection(
        [
            ("standard", "ⓞ Full Odoo Standard"),
            ("logo", "⌘ Only wide logo"),
            ("only_logo", "⌘ Only wide logo / no sep. line"),
            ("line-up", "⌘ ⌁ Line-up logo / slogan"),
            ("line-up2", "⌘ ⌁ Line-up logo / slogan / no sep. line"),
            ("line-up3", "⌘ ┅ Line-up: logo / company data"),
            ("lin3-up4", "⌘ ┅ Line-up: logo / company data / no sep. line"),
            ("line-up5", "⌘ ☷ Line-up: logo / custom_header"),
            ("line-up6", "⌘ ☷ Line-up: logo / custom header / no sep. line"),
            ("line-up25", "☷ Two lines: logo / custom_header"),
            ("line-up26", "☷ Two lines: logo / custom header / no sep. line"),
            ("no_header", "▭ No print Header"),
        ],
        "Header Print Mode",
        help="Which content is printed in document header",
        required=True,
        default="standard",
    )
    address_mode = fields.Selection(
        [
            ("standard", "Standard Invoice + Shipping"),
            ("only_one", "Only specific address"),
            ("docnum", "Doc. number & Specific address"),
        ],
        "Address Print Mode",
        help="Which addresses are printed in document header",
        required=True,
        default="standard",
    )
    logo_style = fields.Char(
        "Html logo style",
        help="Html style attribute for logo <img> tag.\n" 'i.e. "max-height: 45px;"',
        default="max-height: 45px;",
    )
    payment_term_position = fields.Selection(
        [
            ("odoo", "Odoo"),
            ("auto", "Auto"),
            ("footer", "On Footer"),
            ("footer_no_iban", "On Footer, no IBAN"),
            ("footer_notes", "On Footer, only notes"),
            ("header", "On Header"),
            ("header_no_iban", "On Header, no IBAN"),
            ("none", "None"),
        ],
        "Payment term layout position",
        help="Where Payment term and due dates are printed:\n"
        "may be Auto, None, on Footer, on Header or None\n"
        'If "auto", when due payment is whole in one date,\n'
        "all datas are printed on header otherwise on footer\n"
        'If "Odoo" print only Payment Term notes on Footer',
        default="odoo",
        required=True,
    )
    footer_mode = fields.Selection(
        [
            ("standard", "Odoo Standard"),
            ("auto", "Automatic Footer"),
            ("custom", "Customized Footer"),
            ("no_footer", "No print Footer"),
        ],
        "Footer Print Mode",
        help="Which content is printed in document footer\n"
        'If "standard", footer is printed as "auto" or "custom"\n'
        "based on company.custom_footer field (Odoo standard behavior)\n"
        'If "auto", footer is printed with automatic data\n'
        'If "custom", footer is printed from user data written\n',
        required=True,
        default="standard",
    )
    code_mode = fields.Selection(
        [
            ("noprint", "No print"),
            ("print", "Print"),
        ],
        "Print code in document line",
        help='If you choice "print", please set description mode to "nocode"',
        default="noprint",
        required=True,
    )
    description_mode = fields.Selection(
        [
            ("as_is", "As is"),
            ("line1", "Only first line"),
            ("nocode", "No code"),
            ("nocode1", "No code & Only first line"),
        ],
        "Print description in document line",
        help="Which content is printed in document line",
        default="as_is",
        required=True,
    )
    pdf_watermark = fields.Binary(
        "Watermark PDF",
        help="Upload your company letterhead PDF to form the background "
        "of every page of your reports.",
    )
    pdf_watermark_expression = fields.Char(
        "Watermark expression",
        help="An expression yielding the base64 "
        "encoded data to be used as watermark. \n"
        "You have access to variables `env` and `docs`",
    )
    pdf_ending_page = fields.Binary(
        "Ending Page PDF",
        help="Here you can upload a PDF document that contain "
        "some specific content. "
        "This document will be appended to the printed report",
    )
    pdf_ending_page_expression = fields.Char(
        "Ending Page PDF expression",
        help="An expression yielding the base64 "
        "encoded data to be used as Ending Page PDF.\n"
        "You have access to variables `env` and `docs`",
    )
    # sale.order values
    template_sale_order = fields.Many2one(
        "multireport.template", "Sale order template", help="Sale order model"
    )
    # stock.picking values
    template_stock_picking = fields.Many2one(
        "multireport.template",
        "Picking document template",
    )
    # stock.picking.package.preparation values
    template_stock_picking_package_preparation = fields.Many2one(
        "multireport.template",
        "Delivery document template",
        help="Delivery document model",
    )
    # account.invoice values
    template_account_invoice = fields.Many2one(
        "multireport.template", "Account_invoice template", help="Account invoice model"
    )
    # purchase.order values
    template_purchase_order = fields.Many2one(
        "multireport.template", "Purchase order template", help="Purchase order model"
    )
    # other values
    custom_header = fields.Html("Html custom header", help=_(HELP_HEAFOO))
    bottom_text = fields.Text(
        "Bottom text", help="Text to print in bottom area of document"
    )
    custom_footer = fields.Html("Html custom footer", help=_(HELP_HEAFOO))
