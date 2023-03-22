# Copyright (c) 2021
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo.tests.common import TransactionCase

TEST_VAT_UPPER = 'IT234567891'


class TestPivaCase(TransactionCase):

    def setUp(self):
        super(TestPivaCase, self).setUp()
        self.partner_model = self.env['res.partner']

    def test_capitalize_first_n_second_empty(self):
        """
        check if parameter is empty string
        """
        partner = self._create_partner()
        partner.vat = partner._capitalize_first_n_second('')
        self.assertTrue(partner.vat == '')

    def test_capitalize_first_n_second_len2chars(self):
        """
        check if parameter is minus the 3 characters
        """
        partner = self._create_partner()
        partner.vat = partner._capitalize_first_n_second('12')
        self.assertTrue(partner.vat == '12')

    def test_create_partner(self):
        """
        check create method
        """
        partner = self.partner_model.create({
            'vat': 'it234567891',
            'company_type': 'company',
            'name': 'Test PIVA',
        })
        self.assertEqual(partner.vat, TEST_VAT_UPPER)

    def test_modify_partner(self):
        """
        check write method
        """
        partner = self._create_partner()

        partner.write({
            'vat': 'it234567891',
        })
        self.assertEqual(partner.vat, TEST_VAT_UPPER)

    def test_onchange_vat(self):
        """
        check on_change vat
        """

        partner = self._create_partner()
        partner.vat = 'it234567891'
        partner.onchange_vat()
        self.assertEqual(partner.vat, TEST_VAT_UPPER)

        # testing duplicate VAT
        # browse partner esistente
        partner_in = self.env.ref('base.res_partner_1')
        # cambiare la vat con quella precedente
        partner_in.vat = 'it234567891'
        # chiamare onchange
        res = partner_in.onchange_vat()
        self.assertIn('warning', res)

    def _create_partner(self):
        """
        helper build a partner
        """
        partner = self.partner_model.create({
            'vat': 'it234567891',
            'company_type': 'company',
            'name': 'Test PIVA',
        })
        return partner
