#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from python_plus import _u
from odoo import models, fields, _


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'


    def gopher_configure_fiscalpos(self, html_txt=None):

        html = ''
        if html_txt:
            html += html_txt(_('Configure fiscal position'), 'h3')
            html += html_txt('', 'table')
            html += html_txt('', 'tr')
            html += html_txt(_('Name'), 'td')
            html += html_txt(_('Action'), 'td')
            html += html_txt('', '/tr')

        fiscalpos_model = self.env['account.fiscal.position']
        for fiscalpos in fiscalpos_model.search([]):
            actioned = ''
            for tax_line in fiscalpos.tax_ids:
                if not tax_line.tax_src_id or not tax_line.tax_dest_id:
                    actioned = 'Different tax companies'
                elif (tax_line.tax_src_id.type_tax_use !=
                      tax_line.tax_dest_id.type_tax_use):
                    actioned = 'Different tax uses'
                if (hasattr(fiscalpos, 'rc_type') and
                       getattr(fiscalpos, 'rc_type') and
                        tax_line.tax_dest_id.rc_type != getattr(
                            fiscalpos, 'rc_type')):
                    actioned = 'Invalid RC type for target tax'
                elif (hasattr(fiscalpos, 'split_payment') and
                      getattr(fiscalpos, 'split_payment')):
                    if tax_line.tax_dest_id.payability != 'S':
                        actioned = 'Invalid SP flag for target tax'
                else:
                    if (hasattr(fiscalpos, 'rc_type') and
                            not getattr(fiscalpos, 'rc_type') and
                            tax_line.tax_dest_id.rc_type):
                        actioned = 'RC tax for no RC fiscal position'
                    elif (hasattr(fiscalpos, 'payability') and
                          tax_line.tax_dest_id.payability == 'S'):
                        actioned = 'SP tax for no SP fiscal position'
            if actioned and html_txt:
                html += html_txt('', 'tr')
                html += html_txt(fiscalpos.name, 'td')
                html += html_txt(actioned, 'td')
                html += html_txt('', '/tr')
        if html_txt:
            html += html_txt('', '/table')
        return html
