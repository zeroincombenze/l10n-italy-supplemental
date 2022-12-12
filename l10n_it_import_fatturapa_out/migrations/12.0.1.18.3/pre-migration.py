# Copyright 2022 SHS-AV s.r.l. <https://www.zeroincombenze.it/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    openupgrade.logged_query(
        env.cr,
        """
    ALTER TABLE fatturapa_attachment_in
        ADD COLUMN IF NOT EXISTS invoices_date character varying
    """,
    )
