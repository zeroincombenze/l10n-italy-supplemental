# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models
from openerp import api


RPT_ACTION = [('odoo', 'odoo'),
              ('report', 'report'),
              ('company', 'company'),
              ('customer', 'customer')]


@api.model
def _lang_get(self):
    languages = self.env['res.lang'].search([])
    return [(language.code, language.name) for language in languages]


class BaseRuleMultireport(models.Model):
    _name = "base.rule.multireport"
    _description = "Rules to select report name"

    name = fields.Char(
        'Rule Name',
        required=True,
        help="Brief name of document to print")
    model_id = fields.Many2one(
        'ir.model', 'Related Document Model',
        required=True,
        domain=[('osv_memory', '=', False)],
        help="Model to apply this rule")
    model = fields.related(
        'model_id', 'model', type="char", string='Model')
    reportname = fields.Char(
        'Internal report name',
        readonly=True,
        help="Set the report name formatted as module.reportname;"
             " i.e: 'account.report_invoice' like"
             " Odoo standard report name."
             " This field is applied if action is 'report'.")
    purpose = fields.Char(
        'Purpose',
        help="Report purpose: why, when use this report.")
    sequence = fields.Integer(
        'sequence',
        help="Rules are evaluated startin from lower sequence. "
             "Please, use values above 1000 for default rules, "
             "from 100 to 1000 for ordinary rules."
             "Sequences below 100 must be very important!")
    action = fields.Selection(
        RPT_ACTION,
        'report action',
        help="Set 'report' to get the internal report name field,"
             " 'company' to get preferred model of company (if any),"
             " 'customer' to get preferred model of customer (if any),"
             " 'odoo' to execute Odoo standard document printing.")
    journal_id = fields.Many2one(
        'account.journal',
        'If journal',
        help="Apply rule only if journal matches document;"
             " may be useful to print commercial invoices"
             " like Italian 'Fattura Accompagnatoria'.")
    partner_id = fields.Many2one(
        'res.partner',
        'If customer',
        help="Apply rule only if invoice of customer;"
             " may be useful to print specific model for customer.")
    lang = fields.Selection(
        _lang_get,
        'If language',
        help="Apply rule only if language matches customer;"
             " may be useful to print untranslated report models.")
    position_id = fields.Many2one(
        'account.fiscal.position',
        'If fiscal position',
        help="Apply rule only if fiscal position matches"
             " invoice position; may be useful to print"
             " models to satisfy some fiscal law.")
    section_id = fields.many2one(
        'crm.case.section',
        'If sales team',
        help="Apply rule only if sales team matches"
             " invoice position; may be useful to print"
             " models to customize sale documents.")
    since_date = fields.Date('From date')
    until_date = fields.Date('To date')
    active = fields.Boolean(
        'Active',
        help="Rule is evaluated only if is active.")

    @api.model
    def get_reportname(self, invoice):
        # pdb.set_trace()
        odoo_reportname_id = False
        invoice_reportname_id = invoice.invoice_reportname_id.id
        if not invoice_reportname_id:
            company_reportname_id = invoice.company_id.\
                preferred_invoice_model_id.id
            customer_reportname_id = invoice.partner_id.\
                preferred_invoice_model_id.id
            customer_lang = invoice.partner_id.lang
            customer_position_id = invoice.fiscal_position.id
            date_invoice = invoice.date_invoice
            for rule in self.search([('active', '=', True)], order='sequence'):
                # check for selection
                if rule.journal_id and \
                        rule.journal_id.id != invoice.journal_id.id:
                    continue
                elif rule.section_id and \
                        rule.section_id.id != invoice.section_id.id:
                    continue
                elif rule.partner_id and \
                        rule.partner_id.id != invoice.partner_id.id:
                    continue
                elif rule.position_id and \
                        rule.position_id.id != customer_position_id:
                    continue
                elif rule.lang and rule.lang != customer_lang:
                    continue
                elif rule.since_date and rule.since_date < date_invoice:
                    continue
                elif rule.until_date and rule.until_date > date_invoice:
                    continue
                # Valid selection, do action
                if rule.action == 'odoo':
                    invoice_reportname_id = False
                    odoo_reportname_id = rule.id
                    break
                elif rule.action == 'company' and company_reportname_id:
                    invoice_reportname_id = company_reportname_id
                    break
                elif rule.action == 'customer' and customer_reportname_id:
                    invoice_reportname_id = customer_reportname_id
                    break
                elif rule.reportname:
                    invoice_reportname_id = rule.id
                    break
        if invoice_reportname_id:
            reportname = self.browse(invoice_reportname_id).reportname
        else:
            reportname = False
            invoice_reportname_id = odoo_reportname_id
        return reportname, invoice_reportname_id
