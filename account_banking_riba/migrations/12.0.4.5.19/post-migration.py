# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging

_logger = logging.getLogger(__name__)


def _update_move_lines(cr):
    cr.execute(
        "SELECT id, company_bank_id"
        " FROM public.account_move_line"
        " where company_bank_id is not null"
        " and payment_method in ("
        " select id from account_payment_method where "
        " code like 'riba_cbi')"
        " and company_bank_id in ("
        " select id from res_partner_bank where "
        " company_id = 1 and partner_id = 1"
        " and (bank_is_wallet is null or bank_is_wallet = 'false'))"
    )

    records = cr.fetchall()
    for record in records:
        line_id = record[0]
        company_bank_id = record[1]
        sql_bank = (
            "select id from res_partner_bank where company_id = 1 "
            "and partner_id = 1 and  bank_is_wallet = 'true' "
            "and bank_main_bank_account_id = {cp_id}".format(cp_id=company_bank_id)
        )
        cr.execute(sql_bank)
        res = cr.fetchone()
        if res:
            bank_id = res[0]
            sql = (
                "update account_move_line set company_bank_id = {bank_id} "
                "where id = {mvl_id}".format(bank_id=bank_id, mvl_id=line_id)
            )
            _logger.info(sql)
            cr.execute(sql)


def migrate(cr, version):
    if not version:
        _logger.warning(
            "Does not exist any previous version for this module. "
            "Skipping the migration..."
        )

        return

    _update_move_lines(cr)

    _logger.info("Migration executed successfully. Exiting...")
