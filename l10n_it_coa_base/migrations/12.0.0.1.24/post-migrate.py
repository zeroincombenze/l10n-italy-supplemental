# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License LGPL-3 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
#
from odoo import api, SUPERUSER_ID
from odoo.addons.l10n_it_coa_base import (set_default_nature,
                                          set_default_account_nature,
                                          set_default_group_nature)
import logging
_logger = logging.getLogger(__name__)


def migrate_parent_account(cr):
    """This function migrate old parent account into account group

    Args:
        cr (obj): sql cursor

    Returns:
        None
    """
    def create_group(account, code_len):
        if account.parent_id:
            code = account.parent_id.code
        else:
            code = account.code[0: code_len]
        groups = group_model.search([('code_prefix', '=', code)])
        if not groups:
            group = group_model.create({
                'code_prefix': code,
                'name': account.name,
                'nature': account.nature,
            })
            account.write({'group_id': group.id})
        else:
            account.write({'group_id': groups[0].id})

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        company = None
        account_model = env['account.account']
        group_model = env['account.group']
        account_ids = []
        code_len = 2
        # 1st round: manage top level accounts
        for account in account_model.search([('parent_id', '=', False)]):
            if account.company_id != company:
                company = account.company_id
                profile = company.account_profile_id
                code_len = profile.coa_toplevel_len if profile else 2
            account_ids.append(account.id)
            create_group(account, code_len)
        # 2nd round: manage 2nd level accounts
        for account in account_model.search(
                [('parent_id', 'in', account_ids)]):
            if account.company_id != company:
                company = account.company_id
                profile = company.account_profile_id
                code_len = profile.coa_toplevel_len if profile else 2
            create_group(account, code_len)
        # 3th round: manage low level accounts
        for account in account_model.search([('is_parent', '=', False)]):
            if account.company_id != company:
                company = account.company_id
                profile = company.account_profile_id
                code_len = profile.coa_toplevel_len if profile else 2
            create_group(account, code_len)
        # Now deprecated upper levels
        for account in account_model.search([('is_parent', '=', True)]):
            account.write({'deprecated': True})


def migrate(cr, version):
    if not version:
        return
    set_default_nature(cr)
    set_default_account_nature(cr)
    set_default_group_nature(cr)
    migrate_parent_account(cr)
