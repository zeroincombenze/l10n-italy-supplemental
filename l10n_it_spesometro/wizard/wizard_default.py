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
        'log2': fields.text('Log2'),
        'log3': fields.text('Log3')
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
        tax_code_pool = self.pool.get('account.tax.code')
        csv.register_dialect('csv', delimiter=',',
                             quotechar='\"',
                             quoting=csv.QUOTE_MINIMAL)
        csv_fn = "account.tax.code.csv"
        csv_ffn = os.path.abspath(os.path.join(__file__, '../../conf', csv_fn))
        ffound = False
        try:
            csv_fd = open(csv_ffn, 'rb')
            ffound = True
        except BaseException:
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
                tax_code_ids = tax_code_pool.search(cr, uid, tax_code_search)
                for tax_code_id in tax_code_ids:
                    tax_code_obj = tax_code_pool.\
                        browse(cr, uid, tax_code_id)
                    if int(row['spesometro_escludi']) != 0:
                        vals = {'spesometro_escludi': True}
                        tlog = "escluso"
                    else:
                        vals = {'spesometro_escludi': False}
                        tlog = "In dichiarazione"
                    log2 += u"Tax {0}->{1}\n".format(tax_code_obj.code, tlog)
                    tax_code_pool.write(cr, uid, tax_code_id, vals)
            csv_fd.close()

        log3 = u""
        account_journal_pool = self.pool.get('account.journal')
        csv.register_dialect('csv', delimiter=',',
                             quotechar='\"',
                             quoting=csv.QUOTE_MINIMAL)
        csv_fn = "account.journal.csv"
        csv_ffn = os.path.abspath(os.path.join(__file__, '../../conf', csv_fn))
        ffound = False
        try:
            csv_fd = open(csv_ffn, 'rb')
            ffound = True
        except BaseException:
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
                account_journal_search = [('company_id.id',
                                           '=',
                                           user.company_id.id),
                                          ('code', '=', row['code'])]
                account_journal_ids = account_journal_pool.\
                    search(cr, uid, account_journal_search)
                for account_journal_id in account_journal_ids:
                    account_journal_obj = account_journal_pool.\
                        browse(cr, uid, account_journal_id)
                    vals = {}
                    if int(row['spesometro_escludi']) != 0:
                        vals = {'spesometro': False}
                        tlog = "escluso"
                    elif account_journal_obj.type == "sale" or \
                            account_journal_obj.type == "sale_refund":
                        vals = {'spesometro': True,
                                'spesometro_operazione': "FA",
                                'spesometro_segno': 'attiva'}
                    elif account_journal_obj.type == "purchase" or \
                            account_journal_obj.type == "purchase_refund":
                        vals = {'spesometro': True,
                                'spesometro_operazione': "FA",
                                'spesometro_segno': 'passiva'}
                        tlog = "In dichiarazione"
                    else:
                        vals = {'spesometro': False}
                        tlog = "escluso"
                    log3 += u"Journal {0}->{1}\n".\
                        format(account_journal_obj.code, tlog)
                    if len(vals):
                        account_journal_pool.write(cr,
                                                   uid,
                                                   account_journal_id,
                                                   vals)
            csv_fd.close()

        sect = "partner"
        if not cfg_obj.has_section(sect):
            cfg_obj.add_section(sect)
        partner_regex = cfg_obj.get(sect, "partner_utility").split(',')

        log1 = u"Controllate:\n"
        log1 += u"- I sezionali\n"
        log1 += u"- Il piano dei conti imposte\n"
        log1 += u"- I clienti e fornitori\n"
        log1 += u"per eventuali correzioni di inclusione o esclusione\n"
        log1 += u"Se effettuate modifiche manuali"
        log1 += u" non eseguite più questa funzione in futuro!\n\n\n"
        italy = self.pool.get('res.country').search(
            cr, uid, [('code', '=', 'IT')])
        partner_pool = self.pool.get('res.partner')
        partner_search = [('company_id.id', '=', user.company_id.id),
                          '|',
                          ('customer', '=', True),
                          ('supplier', '=', True)]
        partner_ids = partner_pool.search(
            cr, uid, partner_search, context=context)
        for partner_id in partner_ids:
            try:
                partner_obj = partner_pool.browse(cr,
                                                  uid,
                                                  partner_id)
            except BaseException:
                continue
            utility = False
            for regex in partner_regex:
                if re.match(regex, partner_obj.name.lower()):
                    utility = True
            if partner_obj.country_id:
                partner_country = partner_obj.country_id.id
            elif partner_obj.vat:
                country_code = partner_obj.vat[0:2].upper()
                partner_country = self.pool.get('res.country').\
                    search(cr, uid, [('code', '=', country_code)])
            else:
                partner_country = italy[0]
            vals = {}
            # country_id = self.pool.get('res.country').browse(
            #     cr, uid, partner_country)
            if utility:
                vals = {'spesometro_escludi': True}
                log1 += u"{0}->Escluso utility\n".format(partner_obj.name)
            elif not partner_obj.vat and not partner_obj.fiscalcode:
                vals = {'spesometro_escludi': True}
                log1 += u"{0}->Escluso senza PI ne CF\n".\
                        format(partner_obj.name)
            elif partner_country == italy[0]:
                if partner_obj.vat and partner_obj.vat[2:3] == "9":
                    vals = {'spesometro_escludi': True}
                    log1 += u"{0}->Escluso associazione/ente\n".\
                        format(partner_obj.name)
                else:
                    vals = {'spesometro_escludi': False,
                            'spesometro_operazione': "FA"}
                    log1 += u"{0}->FA\n".format(partner_obj.name)
            # elif country_id.inue:
            #     vals = {'spesometro_escludi': True}
            #     partner_obj.partner_spesometro_escludi = True
            #     log1 += u"{0}->Escluso (UE)\n".format(partner_obj.name)
            # elif country_id.blacklist:
            #     vals = {'spesometro_escludi': True,
            #             'spesometro_operazione': "BL1"}
            #     log1 += u"{0}->Blacklist\n".format(partner_obj.name)
            else:
                vals = {'spesometro_escludi': True}
                log1 += u"{0}->Escluso (extraUE)\n".format(partner_obj.name)
            if len(vals):
                try:
                    partner_pool.write(cr, uid, partner_id, vals)
                except BaseException:
                    log1 += u"{0} **PARTITA IVA NON VALIDA**\n".format(
                        partner_obj.name)

        self.write(cr, uid, ids, {'state': 'step2',
                                  'log1': log1,
                                  'log2': log2,
                                  'log3': log3})
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
