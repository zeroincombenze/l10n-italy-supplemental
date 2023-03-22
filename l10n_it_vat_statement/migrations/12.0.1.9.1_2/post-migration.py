import logging
_logger = logging.getLogger(__name__)


def _update_statement_type(cr):

    cr.execute("SELECT id, annual FROM account_vat_period_end_statement")

    records = cr.fetchall()
    for record in records:
        st_id = record[0]
        annual = record[1]
        statement_type = 'year' if annual else 'recur'

        sql = "update account_vat_period_end_statement set " \
              "statement_type = '{st}' where " \
              "id = {id}".format(st=statement_type, id=st_id)
        _logger.info(sql)
        cr.execute(sql)


def migrate(cr, version):
    if not version:
        _logger.warning("Does not exist any previous version for this module. "
                        "Skipping the migration...")

        return

    _update_statement_type(cr)

    _logger.info("Migration executed successfully. Exiting...")

