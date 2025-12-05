# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Sale Resellers",
    "category": "Sales",
    "author": "SHS-AV s.r.l.",
    "website": "http://www.zeroincombenze.it",
    "summary": "Manage Sale Resellers",
    "version": "18.0.1.5.5",
    "description": """
Manager Sale Resellers
======================
""",
    "depends": [
        "purchase",
        "sale",
        "delivery",
        "stock_delivery",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_view.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
    ],
    "qweb": ["static/src/xml/*.xml"],
    "installable": True,
}
