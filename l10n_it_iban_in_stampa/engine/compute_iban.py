
from odoo.addons.account_common_mixin.engine.compute_iban import (
    get_company_bank_account, get_counterparty_bank_account, is_client_doc,
    is_supplier_doc
)


def get_bank_2_print(document):

    value = None
    adapted_doc = document.adapt_document()

    if adapted_doc['fatturapa_pm_id'] and adapted_doc['fatturapa_pm_id'].code:

        code = adapted_doc['fatturapa_pm_id'].code

        if is_client_doc(adapted_doc):
            if code in ('MP09', 'MP10', 'MP11', 'MP12', 'MP16', 'MP17', 'MP19', 'MP20', 'MP21'):
                value = 'partner'
            # end if

            if (
                adapted_doc['type'] in ('out_invoice', 'sale_order')
                and
                code in ('MP05', 'MP07', 'MP08', 'MP13', 'MP18')
            ):
                value = 'company'
            # end if

            if (
                adapted_doc['type'] == 'out_refund'
                and
                code in ('MP05', 'MP07', 'MP08', 'MP13', 'MP18')
            ):
                value = 'partner'
            # end if

        elif is_supplier_doc(adapted_doc):
            if code in ('MP11', 'MP12', 'MP16', 'MP17', 'MP19', 'MP20', 'MP21'):
                value = 'company'
            # end if

            if (
                adapted_doc['type'] in ('in_invoice', 'purchase_order')
                and
                code in ('MP05', 'MP07', 'MP08', 'MP13', 'MP18')
            ):
                value = 'partner'
            # end if

            if (
                adapted_doc['type'] == 'in_refund'
                and
                code in ('MP05', 'MP07', 'MP08', 'MP13', 'MP18')
            ):
                value = 'company'
            # end if

        else:
            value = None
        # end if

    # end if

    return value
# end get_bank_2_print

