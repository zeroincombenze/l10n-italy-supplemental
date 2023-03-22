##############################################################################
#
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-01-13
#    Author : Fabio Colognesi
# Copyright Didotech s.r.l. <https://www.didotech.com>
#
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#
##############################################################################
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import api, fields, models

from odoo.addons.l10n_it_costs_allocation.utils import ventilazione_costi


class AccountInvoiceIntrastat(models.Model):
    _inherit = 'account.invoice.intrastat'

    additional_qty = fields.Float(
        string="Additional Qty")


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def _prepare_intrastat_line_weight(self, product_template, res):
        """
        override private method
        check for product_id weight
        """
        super()._prepare_intrastat_line_weight(product_template, res)
        intrastat_uom_kg = self.invoice_id.company_id.intrastat_uom_kg_id
        # ...Weight compute in Kg
        # ...If Uom has the same category of kg -> Convert to Kg
        # ...Else the weight will be product weight * qty
        product_weight = product_template.weight or 0
        if self.product_id:
            product_weight = self.product_id.weight or 0
        if intrastat_uom_kg and \
                product_template.uom_id.category_id \
                == intrastat_uom_kg.category_id:
            weight_kg = self.uom_id._compute_quantity(
                qty=self.quantity,
                to_unit=intrastat_uom_kg)
        else:
            weight_kg = self.quantity * product_weight
        res.update({
            'weight_kg': weight_kg})
        return weight_kg

    @api.multi
    def _prepare_intrastat_line_amount(self, res):
        """
        override private method
        added delivery amount
        minus discount global allocation
        """
        super()._prepare_intrastat_line_amount(res)

        company_currency = self.invoice_id.company_id.currency_id
        invoice_currency = self.invoice_id.currency_id

        delivery_amount_euro = invoice_currency._convert(
            self.cost_delivery_amount,
            company_currency,
            self.invoice_id.company_id,
            fields.Date.today())

        discount_amount_euro = invoice_currency._convert(
            self.cost_discount_amount,
            company_currency,
            self.invoice_id.company_id,
            fields.Date.today())

        if discount_amount_euro > 0:
            discount_amount_euro = discount_amount_euro * -1

        amount_euro = (
                res['amount_euro'] +
                delivery_amount_euro +
                discount_amount_euro
        )

        res.update({'amount_euro': amount_euro})

    @api.multi
    def _prepare_intrastat_line_additional_units(self, company_id, intrastat_code, res, weight_kg):
        """
            Returns quantity for each product line
        """
        super(AccountInvoiceLine, self)._prepare_intrastat_line_additional_units(company_id, intrastat_code, res, weight_kg)
        res.update({
            'additional_qty': self.quantity})


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    intrastat = fields.Boolean(
        string="Subject to Intrastat",
        readonly=True,
        states={
            'draft': [
                ('readonly', False)]},
        copy=False)

    def _get_conditions_of_sale(self):
        return self.env['res.config.settings']._get_conditions_of_sale()

    sale_conditions = fields.Text(
        string='CONDITIONS OF SALE',
        default=_get_conditions_of_sale
    )

    @api.multi
    def compute_intrastat_lines(self):
        """
        override private method
        Recompute cost spreading
        """
        super().compute_intrastat_lines()
        dp_obj = self.env['decimal.precision']
        for inv in self:
            intrastat_lines = []

            # Unlink existing lines
            inv.intrastat_line_ids.unlink()

            # Recompute cost spreading before computing
            # the new intrastat lines
            ventilazione_costi(inv, inv.invoice_line_ids)

            i_line_by_code = {}
            lines_to_split = []
            for line in inv.invoice_line_ids:
                # Lines to compute
                if not line.product_id:
                    continue
                product_template = line.product_id.product_tmpl_id
                intrastat_data = product_template.get_intrastat_data()
                if 'intrastat_code_id' not in intrastat_data or \
                        intrastat_data['intrastat_type'] == 'exclude':
                    continue
                # Free lines
                if inv.company_id.intrastat_exclude_free_line \
                        and not line.price_subtotal:
                    continue
                # lines to split at the end
                if intrastat_data['intrastat_type'] == 'misc':
                    lines_to_split.append(line)
                    continue
                if not intrastat_data['intrastat_code_id']:
                    continue

                # Group by intrastat code
                intra_line = line._prepare_intrastat_line()
                i_code_id = intra_line['intrastat_code_id']
                i_code_type = intra_line['intrastat_code_type']

                if i_code_id in i_line_by_code:
                    i_line_by_code[i_code_id]['amount_currency'] += \
                        intra_line['amount_currency']
                    i_line_by_code[i_code_id]['amount_euro'] += \
                        intra_line['amount_euro']
                    i_line_by_code[i_code_id]['statistic_amount_euro'] += \
                        intra_line['statistic_amount_euro']
                    i_line_by_code[i_code_id]['weight_kg'] += \
                        intra_line['weight_kg']
                    i_line_by_code[i_code_id]['additional_units'] += \
                        intra_line['additional_units']
                    # Added product qty summarized, grouped by custom code
                    i_line_by_code[i_code_id]['additional_qty'] += \
                        intra_line['additional_qty']
                    # Added product qty summarized, grouped by custom code
                else:
                    intra_line['statement_section'] = \
                        self.env['account.invoice.intrastat'] \
                            .compute_statement_section(i_code_type, inv.type)
                    i_line_by_code[i_code_id] = intra_line

            # Split lines for intrastat with type "misc"
            if lines_to_split:
                # tot intrastat
                amount_tot_intrastat = 0
                for key, i_line in i_line_by_code.items():
                    amount_tot_intrastat += i_line['amount_currency']

                # amount to add
                for line in lines_to_split:
                    amount_to_split = amount_to_split_residual = \
                        line.price_subtotal
                    i = 0
                    for key, i_line in i_line_by_code.items():
                        i += 1
                        # competence
                        if i == len(i_line_by_code):
                            amount_competence = amount_to_split_residual
                        else:
                            amount_competence = \
                                amount_to_split * \
                                round((i_line['amount_currency'] /
                                       amount_tot_intrastat),
                                      dp_obj.precision_get('Account'))
                        # add to existing code
                        i_line['amount_currency'] += amount_competence
                        if i_line['statistic_amount_euro']:
                            i_line[
                                'statistic_amount_euro'] += amount_competence

                        amount_to_split_residual -= amount_competence

            for key, val in i_line_by_code.items():
                intrastat_lines.append((0, 0, val))
            if intrastat_lines:
                inv.intrastat_line_ids = intrastat_lines
