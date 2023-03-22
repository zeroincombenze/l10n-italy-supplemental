# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import itertools


# Descriptors for cost types stating:
# - which products are affected by this type of cost
# - in which field of the line the cost should be set
# - how to compute the sum of the cost lines
# - how to build the set of lines for this type of cost
COST_TYPES = {

    'delivery': {
        'prods': ['good'],
        'field': 'cost_delivery_amount',
        'sum': lambda l: l.price_subtotal,
        'filter': lambda l: (
                l.product_id.id and l.product_id.cost_type == 'delivery'
        ),
    },

    'packaging': {
        'prods': ['good'],
        'field': 'cost_packaging_amount',
        'sum': lambda l: l.price_subtotal,
        'filter': lambda l: (
                l.product_id.id and l.product_id.cost_type == 'packaging'
        ),
    },

    'payment': {
        'prods': ['good', 'service'],
        'field': 'cost_payment_amount',
        'sum': lambda l: l.price_subtotal,
        'filter': lambda l: (
                l.product_id.id and l.product_id.cost_type == 'payment'
        ),
    },

    'other': {
        'prods': ['good', 'service'],
        'field': 'cost_other_amount',
        'sum': lambda l: l.price_subtotal,
        'filter': lambda l: (
                l.product_id.id and l.product_id.cost_type == 'other'
        ),
    },

    'discount': {
        'prods': ['good', 'service'],
        'field': 'cost_discount_amount',
        'sum': lambda l: l.price_subtotal,
        'filter': lambda l: (
                l.product_id.id and l.product_id.cost_type == 'discount'
        ),
    },

}

# Descriptors for products types stating:
# - how to compute the sum of the product lines
# - how to build the set of lines for this type of product
PROD_TYPES = {

    'good': {
        'sum': lambda l: l.price_subtotal,
        'filter': lambda l: l.product_id.id and l.product_id.type != 'service'
    },

    'service': {
        'sum': lambda l: l.price_subtotal,
        'filter': lambda l: l.product_id.id and l.product_id.type == 'service' and not l.product_id.cost_type
    },

}


# Function to distribute costs
def ventilazione_costi(document, lines):

    # Get decimal precision to be used for roundings
    dp = document.env['decimal.precision'].precision_get('Account')

    # Products types sets and total amount for each type of product
    prods_lines = dict()
    prods_sums = dict()

    # Costs types sets and total amount for each type of cost
    costs_lines = dict()
    costs_sums = dict()

    # Compute sets and total amounts for each product type
    for prod_type, cfg in PROD_TYPES.items():
        prods_lines[prod_type] = list(filter(cfg['filter'], lines))
        prods_sums[prod_type] = sum(map(cfg['sum'], prods_lines[prod_type]))
    # end for

    # Compute sets and total amounts for each cost type
    for cost_type, cfg in COST_TYPES.items():
        costs_lines[cost_type] = list(filter(cfg['filter'], lines))
        costs_sums[cost_type] = sum(map(cfg['sum'], costs_lines[cost_type]))
    # end for

    # Assign totals to the Document
    document.total_goods_amount = prods_sums.get('good', 0.0)
    document.total_goods_n_service_amount = (
            prods_sums.get('service', 0)
            +
            prods_sums.get('good', 0)
    )

    document.total_delivery_amount = costs_sums.get(
        'delivery', document.total_delivery_amount
    )

    document.total_discount_amount = costs_sums.get(
        'discount', document.total_discount_amount
    )

    document.total_packaging_amount = costs_sums.get(
        'packaging', document.total_packaging_amount
    )

    document.total_payment_amount = costs_sums.get(
        'payment', document.total_payment_amount
    )

    document.total_other_amount = costs_sums.get(
        'other', document.total_other_amount
    )

    # Assign costs quotas to each line
    for cost_type, cfg in COST_TYPES.items():

        target_lines = list(itertools.chain.from_iterable(
            [prods_lines.get(x, []) for x in cfg['prods']]
        ))

        target_lines_sum = sum([prods_sums.get(x, 0) for x in cfg['prods']])

        # If there are target lines where to distribute
        # the costs go on with the spreading
        if target_lines_sum != 0:

            # Get the amount to be distributed
            cost = costs_sums.get(cost_type, 0)

            # Compute the cost unit to be multiplied by the
            # price_subtotal of each line
            cost_unit = cost / target_lines_sum

            # Compute the quota to be assigned to each line and
            # recompute the quota of the last line to avoid
            # mismatch between the sum of the quotas and the original
            # cost amount due tue roundings
            cost_quotas = [
                round(cost_unit * line.price_subtotal, dp)
                for line in target_lines
            ]
            cost_quotas[-1] = round(cost - sum(cost_quotas[:-1]), dp)

            # Assign the quota to each line
            for line, quota in zip(target_lines, cost_quotas):
                setattr(line, cfg['field'], quota)
            # end for

        # end if

    # end for

# end ventilazione_costi
