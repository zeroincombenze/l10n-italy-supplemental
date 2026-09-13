#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from python_plus import _u

from odoo import SUPERUSER_ID, api

OVERDUE_MSG = """Gentile cliente,

le nostre scritture contabili evidenziano alcune fatture ancora aperte.

Per favore, controllate l'estratto conto riportato qui sotto e se coincide \
con la Vostra contabilità, \
Vi chiediamo di procedere con il pagamento tramite bonifico bancario al seguente IBAN:

%(bank)s

Se avete già provveduto al pagamento, Vi ringraziamo per averlo fatto e \
potete considerate nulla la presente.

Se avete qualche dubbio non esitate a contattarci al nostro numero %(phone)s.

Grazie per averci scelto e per la Vostra collaborazione.

Cordiali Saluti

"""


def update_template_ref(cr):
    """Set the default values for various entities. This function is called by
    migrate and post-install processes; both processes supply cr param.

    Args:
        cr (obj): sql cursor

    Returns:
        None

    NOTE: this only fixes up this module's *own* default/demo records
    (the multireport.style/template rows it ships, its own header/footer
    QWeb views, its own report actions). It does NOT -- and cannot,
    generically -- repair pre-existing user data created under an older
    major version whose `header_id`/`footer_id`/`report_id` (all
    Many2one to ir.ui.view/ir.actions.report) point at database ids that
    no longer resolve to the same views/actions after a multi-version
    jump. That is a real, separate data-reconciliation concern for
    whatever database this module gets installed against; see the
    migration report for details.
    """

    def set_vals(obj, def_vals):
        vals = {}
        for name in (
            "template_sale_order",
            "template_stock_picking",
            "template_stock_picking_package_preparation",
            "template_account_invoice",
            "template_purchase_order",
        ):
            if not getattr(obj, name):
                vals[name] = def_vals[name]
        return vals

    env = api.Environment(cr, SUPERUSER_ID, {})
    mr_style_model = env["multireport.style"]
    def_vals = {
        "template_sale_order": env.ref("base_multireport.mr_t_saleorder").id,
        "template_stock_picking": env.ref("base_multireport.mr_t_picking").id,
        "template_stock_picking_package_preparation": env.ref(
            "base_multireport.mr_t_ddt"
        ).id,
        "template_account_invoice": env.ref("base_multireport.mr_t_invoice").id,
        "template_purchase_order": env.ref("base_multireport.mr_t_purchaseorder").id,
    }
    domain = [("origin", "!=", "odoo")]
    for mr_style in mr_style_model.search(domain):
        vals = set_vals(mr_style, def_vals)
        if vals:
            mr_style.write(vals)

    # ir.actions.report.xml was renamed to ir.actions.report at 10.0;
    # account.invoice was merged into account.move at 13.0;
    # stock.picking.package.preparation was renamed to stock.delivery.note
    # by l10n_it_delivery_note.
    ir_report_model = env["ir.actions.report"]
    vals = {"template": False}
    domain = [
        (
            "model",
            "in",
            (
                "sale.order",
                "stock.picking",
                "stock.delivery.note",
                "account.move",
                "purchase.order",
            ),
        )
    ]
    for ir_report in ir_report_model.search(domain):
        ir_report.write(vals)

    vals = {}
    ir_view_model = env["ir.ui.view"]
    domain = [("key", "=", "base_multireport.external_layout_header")]
    ids = ir_view_model.search(domain)
    if len(ids) == 1:
        vals["header_id"] = ids[0].id
    domain = [("key", "=", "base_multireport.external_layout_footer")]
    ids = ir_view_model.search(domain)
    if len(ids) == 1:
        vals["footer_id"] = ids[0].id
    if vals:
        mr_template_model = env["multireport.template"]
        for mr_template in mr_template_model.search([]):
            mr_template.write(vals)

    rules_model = env["multireport.selection.rules"]
    for rule in rules_model.search([]):
        if rule.action == "report":
            rule.write(
                {
                    "report_id": {
                        "sale.order": env.ref("base_multireport.report_saleorder").id,
                        "account.invoice": env.ref(
                            "base_multireport.account_invoice_report_duplicate_main"
                        ).id,
                        "account.move": env.ref(
                            "base_multireport.account_invoice_report_duplicate_main"
                        ).id,
                    }.get(rule.model_name, rule.report_id.id)
                }
            )

    mr_style_odoo = env.ref("base_multireport.mr_style_odoo").id
    company_model = env["res.company"]
    vals = {"report_model_style": mr_style_odoo}
    # `overdue_msg` no longer exists on res.company at 18.0 (the
    # payment-reminder feature it fed was reworked); guard defensively
    # rather than assume it is still there.
    if "overdue_msg" in company_model._fields:
        for company in company_model.search([]):
            if "Dear Sir/Madam," in (company.overdue_msg or ""):
                params = {
                    "bank": company.bank_ids[0].acc_number if company.bank_ids else "",
                    "phone": company.phone,
                }
                vals["overdue_msg"] = _u(OVERDUE_MSG.replace("\\\n", "")) % _u(params)
            elif "overdue_msg" in vals:
                del vals["overdue_msg"]
            try:
                company.with_context({"lang": "en_US"}).write(vals)
            except IOError:
                pass
    else:
        for company in company_model.search([]):
            company.write(vals)


def update_template_ref_post(env):
    update_template_ref(env.cr)
