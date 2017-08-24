# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp.tests.common import SingleTransactionCase
import logging

__version__ = "0.1.1"
_logger = logging.getLogger(__name__)
INIT_PARTY_ISSUE = '1234567A'
BNK_NL_BIC = 'INGBNL2A'
BNK_NL_NAME = 'ING Bank'
BNK_NL_ACC_NUMBER = 'NL08INGB0000000555'
BNK_IT_BIC = 'BCITITMM300'
BNK_IT_NAME = 'Intesa San Paolo Ag.7 MI'
BNK_IT_ACC_NUMBER = 'IT31Z0306909420615282446606'


class Test_company(SingleTransactionCase):

        def rgx(self, model):
            return self.registry(model)

        def xtbrowse(self, model, xid):
            """ Browse record for test
            """
            id = self.ref(xid)
            return self.rgx(model).browse(self.cr,
                                          self.uid,
                                          id)

        def xtwrite(self, model, xid, values):
            """ Browse and write existent record for test
            """
            obj = self.xtbrowse(model,
                                xid)
            return obj.write(values)

        def xtcreate(self, model, values):
            """ Create a new record for test
            """
            return self.rgx(model).create(self.cr,
                                          self.uid,
                                          values)

        def setup_company(self, country_code=None):
            """Setup company (may be customized for specific country)
            """
            vals = {'initiating_party_issuer': INIT_PARTY_ISSUE}
            self.company = self.xtwrite('res.company',
                                        'base.main_company',
                                        vals)
            self.currency_id = self.ref('base.EUR')
            if country_code:
                xcountry = 'base.' + country_code
            else:
                xcountry = 'base.nl'
            self.country_id = self.ref(xcountry)
            if xcountry == 'base.nl':
                vals = {
                    'name': BNK_NL_NAME,
                    'bic': BNK_NL_BIC,
                    'country': self.country_id,
                }
            elif xcountry == 'base.it':
                vals = {
                    'name': BNK_IT_NAME,
                    'bic': BNK_IT_BIC,
                    'country': self.country_id,
                }
            else:
                vals = {}
            self.bank_id = self.xtcreate('res.bank',
                                         vals)
            self.partner_id = self.ref('base.main_partner')
            self.company_id = self.ref('base.main_company')
            if xcountry == 'base.nl':
                vals = {
                    'state': 'iban',
                    'acc_number': BNK_NL_ACC_NUMBER,
                    'bank': self.bank_id,
                    'bank_bic': BNK_NL_BIC,
                    'partner_id': self.partner_id,
                    'company_id': self.company_id,
                }
            elif xcountry == 'base.it':
                vals = {
                    'state': 'iban',
                    'acc_number': BNK_IT_ACC_NUMBER,
                    'bank': self.bank_id,
                    'bank_bic': BNK_IT_BIC,
                    'partner_id': self.partner_id,
                    'company_id': self.company_id,
                }
            else:
                vals = {}
            self.partner_bank_id = self.xtcreate('res.partner.bank',
                                                 vals)
            self.rgx('res.users').write(
                self.cr, self.uid, [self.uid],
                {'company_ids': [(4, self.company_id)]})
            self.rgx('res.users').write(
                self.cr, self.uid, [self.uid],
                {'company_id': self.company_id})
            self.partner_id = self.ref('base.res_partner_2')

        def setUp(self):
            self.setup_company()

        def test_company(self):
            cr, uid = self.cr, self.uid
            data_model = self.registry('ir.model.data')
            company_model = self.registry('res.company')
            company_id = data_model.get_object_reference(cr,
                                                         uid,
                                                         'base',
                                                         'main_company')[1]
            company = company_model.browse(cr, uid, company_id)
            assert company.initiating_party_issuer == INIT_PARTY_ISSUE, \
                'Invalid party issuer'

            res = company_model.\
                _get_initiating_party_identifier(cr,
                                                 uid,
                                                 self.company_id)
            assert res == INIT_PARTY_ISSUE, \
                'Invalid party issuer'
