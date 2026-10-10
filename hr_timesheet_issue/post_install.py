# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, api


def set_other_partner(cr):
    """Set the other partner on analytic line

    Args:
        cr (obj): sql cursor

    Returns:
        None
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        analytic_line_model = env["account.analytic.line"]
        if not analytic_line_model.search([("other_partner_id", "!=", False)], limit=1):
            env.cr.execute(
                "SELECT id FROM hr_timesheet_sheet_sheet WHERE state='confirm'"
            )
            confirm = [x[0] for x in env.cr.fetchall()]
            env.cr.execute(
                "SELECT id FROM hr_timesheet_sheet_sheet WHERE state='done'"
            )
            done = [x[0] for x in env.cr.fetchall()]
            if confirm:
                env.cr.execute(
                    "UPDATE hr_timesheet_sheet_sheet SET state='draft' WHERE id in %s"
                    % str(confirm).replace("[", "(").replace("]", ")")
                )
            if done:
                env.cr.execute(
                    "UPDATE hr_timesheet_sheet_sheet SET state='draft' WHERE id in %s"
                    % str(done).replace("[", "(").replace("]", ")")
                )
            for line in analytic_line_model.search([]):
                line.write({})
            if confirm:
                env.cr.execute(
                    ("UPDATE hr_timesheet_sheet_sheet SET state='confirm'"
                     " WHERE id in %s")
                    % str(confirm).replace("[", "(").replace("]", ")")
                )
            if done:
                env.cr.execute(
                    "UPDATE hr_timesheet_sheet_sheet SET state='done' WHERE id in %s"
                    % str(done).replace("[", "(").replace("]", ")")
                )


def set_other_partner_post(cr, registry):
    set_other_partner(cr)
