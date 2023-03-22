# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo.tests.common import TransactionCase


class TestAlwaysTrue(TransactionCase):
    def setUp(self):
        super(TestAlwaysTrue, self).setUp()
        # set invoice
        # self.journal_sale = self.env['account.journal'].search([
        #     ('type', '=', 'sale')])[0]
        # self.invoice_model = self.env['account.invoice']
        # self.invoice_line_model = self.env['account.invoice.line']
        #
        # self.partner_id = self.env['res.partner'].create({
        #     'name': 'Fortest Partner'
        # })
        # self.payment_term = False
        #
        # # product ???
        # self.product = self.env.ref("product.product_product_4")
        #
        # self.currency_eur_id = self.env.ref("base.EUR").id
        #
        # self.account_receivable = self.env['account.account'].search([
        #     ('user_type_id', '=',
        #      self.env.ref('account.data_account_type_receivable').id)], limit=1)
        #
        # self.inv = self.create_invoice(
        #     self, amount=100, currency_id=self.currency_eur_id,
        #     partner=self.partner_id.id)

    def test_always_true(self):
        test = True
        self.assertEqual(test, True)
