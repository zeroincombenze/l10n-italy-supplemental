
import odoo.tests.common as common


class TestMakeInvoice(common.TransactionCase):

    def setUp(self):
        super(TestMakeInvoice, self).setUp()

        self.partner = self.env.ref('base.res_partner_1')

        self.sequence = self.env['ir.sequence'].create({
            'name': 'Test Sales Order',
            'code': 'sale.order',
            'prefix': 'TSO',
            'padding': 3,
        })

        self.journal = self.env['account.journal'].search(
            [('type', '=', 'sale')], limit=1)

        self.warehouse = self.env.ref('stock.stock_warehouse_shop0')

        self.immediate_payment = self.env.ref(
            'account.account_payment_term_immediate')
        self.sale_pricelist = self.env.ref('product.list0')

        self.free_carrier = self.env.ref('account.incoterm_FCA')

        self.sale_type = self.env['sale.order.type'].create({
            'name': 'Test Sale Order Type',
            'sequence_id': self.sequence.id,
            'journal_id': self.journal.id,
            'warehouse_id': self.warehouse.id,
            'picking_policy': 'one',
            'payment_term_id': self.immediate_payment.id,
            'pricelist_id': self.sale_pricelist.id,
            'incoterm_id': self.free_carrier.id,
        })

    def test_invoice_journal_percentage(self):
        journal_sale = self.env['account.journal'].create({
            'name': 'Sale Journal - Test',
            'code': 'AJ-SALE',
            'type': 'sale',
            'company_id': self.env.user.company_id.id,
        })

        account_income = self.env['account.account'].create({
            'code': 'NC1112', 'name':
            'Sale - Test Account',
            'user_type_id': 13
        })

        order, line = self._create_order()

        context = {
            'active_model': 'sale.order',
            'active_ids': [order.id],
            'active_id': order.id,
            'default_journal_id': journal_sale.id,
        }

        order.action_confirm()
        amount = 100
        payment = self.env['sale.advance.payment.inv'].with_context(
            context).create(
            {'advance_payment_method': 'fixed', 'amount': amount,
             'deposit_account_id': account_income.id})

        invoice = payment._create_invoice(order, line, amount)
        self.assertEqual(invoice.sale_type_id.id, order.type_id.id)

    def test_invoice_journal_fixed(self):
        journal_sale = self.env['account.journal'].create({
            'name': 'Sale Journal - Test',
            'code': 'AJ-SALE',
            'type': 'sale',
            'company_id': self.env.user.company_id.id,
        })

        account_income = self.env['account.account'].create({
            'code': 'NC1112', 'name':
            'Sale - Test Account',
            'user_type_id': 13
        })

        order, line = self._create_order()

        context = {
            'active_model': 'sale.order',
            'active_ids': [order.id],
            'active_id': order.id,
            'default_journal_id': journal_sale.id,
        }

        order.action_confirm()
        amount = 50
        payment = self.env['sale.advance.payment.inv'].with_context(
            context).create(
            {'advance_payment_method': 'percentage', 'amount': amount,
             'deposit_account_id': account_income.id})

        invoice = payment._create_invoice(order, line, amount)
        self.assertEqual(invoice.sale_type_id.id, order.type_id.id)

    def _create_order(self):
        # create product
        product_order = self.env['product.product'].create({
            'name': 'Cost-plus Contract',
            'categ_id': self.env.ref('product.product_category_5').id,
            'standard_price': 200.0,
            'list_price': 180.0,
            'type': 'service',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'uom_po_id': self.env.ref('uom.product_uom_unit').id,
            'default_code': 'SERV_DEL',
            'invoice_policy': 'delivery',
        })

        pricelist = self.env['product.pricelist'].create({
            'name': 'EU pricelist',
            'active': True,
            'currency_id': self.env.ref('base.EUR').id,
            'company_id': self.env.user.company_id.id,
        })

        so = self.env['sale.order'].with_context(tracking_disable=True)

        sale_order = so.create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'pricelist_id': pricelist.id,
            'type_id': self.sale_type.id,
        })

        line = self.env['sale.order.line'].create({
            'name': product_order.name,
            'product_id': product_order.id,
            'product_uom_qty': 2,
            'product_uom': product_order.uom_id.id,
            'price_unit': product_order.list_price,
            'order_id': sale_order.id,
            'tax_id': False,
        })

        return sale_order, line
