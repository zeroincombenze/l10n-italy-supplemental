# -*- coding: utf-8 -*-
import csv
import logging
import os

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def load_data_xlsx(env):
    tot = bonus = 0
    with open(
        os.path.join(os.path.dirname(__file__), "post-migrate.csv"), "rb"
    ) as csv_fd:
        csv_obj = csv.DictReader(csv_fd, fieldnames=[], restkey="undef_name")
        hdr_read = False
        for row in csv_obj:
            if not hdr_read:
                csv_obj.fieldnames = row["undef_name"]
                hdr_read = True
                continue
            if row["Database"] == env.cr.dbname:
                tot, bonus = row["Totale Fatture"], row.get("More", 0)
                break
        csv_fd.close()
    return tot, bonus


def update_voucher(cr):
    """Update bought invoices"""
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        channel_model = env["italy.ade.sender"]
        for channel in channel_model.search([]):
            if not channel.client_id or "shs-av@evolve.srl" not in channel.client_id:
                continue
            tot, bonus = load_data_xlsx(env)
            channel.write(
                {
                    "max_invoices_ctr": tot,
                    "bonus_invoices_ctr": bonus,
                    "used_invoices_ctr": 0,
                }
            )


def migrate(cr, version):
    if not version:
        return
    update_voucher(cr)
