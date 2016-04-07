# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Alessandro Camilli (a.camilli@yahoo.it)
#    Copyright (C) 2014
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import os.path
import os
import csv
import ConfigParser
import re


class partner_update_wizard(osv.TransientModel):

    _name = "wizard.spesometro.default"

    _columns = {

        'state': fields.selection([('step1', 'step1'), ('step2', 'step2')]),
        'log1': fields.text('Log1'),
        'log2': fields.text('Log2')
    }

    _defaults = {
        'state': 'step1'
    }

    def setting_default(self, cr, uid, ids, context=None):
        d = {
            "partner_utility": "vodafone.*,.*telecom.*,wind.*,.*h3g.*,"
                               "enel.*,eni.*,edison.*,iren.*"
        }
        cfg_obj = ConfigParser.SafeConfigParser(d)
        cfg_fn = "wiz_default.conf"
        cfg_ffn = os.path.abspath(os.path.join(__file__, '../../conf', cfg_fn))
        cfg_obj.read(cfg_ffn)

        user = self.pool.get('res.users').browse(cr, uid, uid)

        log2 = u""
        tax_code_obj = self.pool.get('account.tax.code')
        csv.register_dialect('csv', delimiter=',',
                             quotechar='\"',
                             quoting=csv.QUOTE_MINIMAL)
        csv_fn = "account.tax.code.csv"
        csv_ffn = os.path.abspath(os.path.join(__file__, '../../conf', csv_fn))
        ffound = False
        try:
            csv_fd = open(csv_ffn, 'rb')
            ffound = True
        except:
            pass
        if ffound:
            csv_obj = csv.DictReader(
                csv_fd, fieldnames=[], restkey='undef_name', dialect='csv')
            hdr_read = False
            for row in csv_obj:
                if not hdr_read:
                    csv_obj.fieldnames = row['undef_name']
                    hdr_read = True
                    continue
                tax_code_search = [('company_id.id', '=', user.company_id.id),
                                   ('code', '=', row['code'])]
                tax_code_ids = tax_code_obj.search(cr, uid, tax_code_search)
                for tax_code_id in self.pool.get('account.tax.code').\
                        browse(cr, uid, tax_code_ids):
                    if int(row['spesometro_escludi']) != 0:
                        vals = {'spesometro_escludi': True}
                        tlog = "escluso"
                    else:
                        vals = {'spesometro_escludi': False}
                        tlog = "In dichiarazione"
                    log2 += u"Tax {0}->{1}\n".format(tax_code_id.code, tlog)
                    id_upd = [tax_code_id.id]
                    tax_code_obj.write(cr, uid, id_upd, vals)
            csv_fd.close()

        sect = "partner"
        if not cfg_obj.has_section(sect):
            cfg_obj.add_section(sect)
        partner_regex = cfg_obj.get(sect, "partner_utility").split(',')

        log1 = u""
        log1 += u"Attenzione!" + \
                " I fornitori utility devono essere esclusi manualmente\n\n"
        italy = self.pool.get('res.country').search(
            cr, uid, [('code', '=', 'IT')])
        partner_obj = self.pool.get('res.partner')
        partner_search = [('company_id.id', '=', user.company_id.id),
                          '|',
                          ('customer', '=', True),
                          ('supplier', '=', True)]
        partner_ids = partner_obj.search(
            cr, uid, partner_search, context=context)
        for partner_id in self.pool.get('res.partner').browse(cr,
                                                              uid,
                                                              partner_ids):
            utility = False
            for regex in partner_regex:
                if re.match(regex, partner_id.name.lower()):
                    utility = True
            if partner_id.country_id:
                partner_country = partner_id.country_id.id
            elif partner_id.vat:
                country_code = partner_id.vat[0:2].upper()
                partner_country = self.pool.get('res.country').\
                    search(cr, uid, [('code', '=', country_code)])
            else:
                partner_country = italy[0]
            vals = {}
            country_id = self.pool.get('res.country').browse(
                cr, uid, partner_country)
            if utility:
                vals = {'spesometro_escludi': True}
                log1 += u"{0}->Escluso utility\n".format(partner_id.name)
            elif partner_country == italy[0]:
                vals = {'spesometro_escludi': False,
                        'spesometro_operazione': "FA"}
                log1 += u"{0}->FA\n".format(partner_id.name)
            elif country_id.inue:
                vals = {'spesometro_escludi': True}
                partner_id.partner_spesometro_escludi = True
                log1 += u"{0}->Escluso (UE)\n".format(partner_id.name)
            elif country_id.blacklist:
                vals = {'spesometro_escludi': True,
                        'spesometro_operazione': "BL1"}
                log1 += u"{0}->Blacklist\n".format(partner_id.name)
            else:
                vals = {'spesometro_escludi': True}
                log1 += u"{0}->Escluso (extraUE)\n".format(partner_id.name)
            if len(vals):
                id_upd = [partner_id.id]
                partner_obj.write(cr, uid, id_upd, vals)

        self.write(cr, uid, ids, {'state': 'step2',
                                  'log1': log1, 'log2': log2})
        wiz = self.browse(cr, uid, ids, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.spesometro.default',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz[0].id,
            'views': [(False, 'form')],
            'target': 'new',
            'context': context,
        }
