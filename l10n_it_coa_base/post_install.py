# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
#
from odoo import api, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


def set_default_nature(cr):
    """Set the default nature of account type. This function is called by
    migrate and post-install processes; both processes supply cr param.

    Args:
        cr (obj): sql cursor

    Returns:
        None
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        type_model = env['account.account.type']
        for query, nature in (
                (['|',
                  ('type', '=', 'receivable'),
                  ('internal_group', '=', 'asset')], 'A'),
                (['|',
                  ('type', '=', 'payable'),
                  ('internal_group', 'in', ('liability', 'equity'))], 'P'),
                (['|',
                  ('name', 'ilike', '%prepayments%'),
                  ('name', 'ilike', '%risconti%')], 'A'),
                ([('internal_group', '=', 'expense')], 'C'),
                ([('internal_group', '=', 'income')], 'R'),
                ([('name', '=', 'Memorandum')], 'O'),
        ):
            type_model.search(query).write({'nature': nature})
        for query, nature, alt_nature in (
                ([('type', '=', 'liquidity')], 'P', 'A'),
                ([('name', '=', 'Current Year Earnings')], 'R', 'C'),
        ):
            type_model.search(query).write(
                {'nature': nature, 'alt_nature': alt_nature})
        _logger.info("Migration set_default:nature terminated.")


def set_default_account_nature(cr):
    """Set the default nature of account account. This function is called by
    migrate and post-install processes; both processes supply cr param.

    Args:
        cr (obj): sql cursor

    Returns:
        None
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        type_model = env['account.account.type']
        account_model = env['account.account']
        for acc_type in type_model.search([]):
            account_model.search(
                [('user_type_id', '=', acc_type.id)]).write(
                {'nature': acc_type.nature})


def set_default_group_nature(cr):
    """Set the default nature of account group. This function is called by
    migrate and post-install processes; both processes supply cr param.

    Args:
        cr (obj): sql cursor

    Returns:
        None
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        account_model = env['account.account']
        group_model = env['account.group']
        for group in group_model.search([]):
            account = account_model.search(
                [('group_id', '=', group.id)], limit=1)
            group.write({'nature': account.nature})
        for group in group_model.search([('nature', '=', False)]):
            child = group_model.search(
                [('parent_id', '=', group.id)], limit=1)
            group.write({'nature': child.nature})


def migrate_negative_balance(cr):
    """This function set negative = 'invert' if account.type has 2 natures.
    This function is called by migrate and post-install processes;
    both processes supply cr param.

    Args:
        cr (obj): sql cursor

    Returns:
        None
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        account_model = env['account.account']
        for acc in account_model.search([]):
            if (acc.user_type_id.alt_nature and
                    acc.user_type_id.nature != acc.user_type_id.alt_nature):
                acc.write({'negative_balance': 'invert'})


def set_default_nature_post(cr, registry):
    set_default_nature(cr)
    set_default_account_nature(cr)
    set_default_group_nature(cr)
    migrate_negative_balance(cr)
