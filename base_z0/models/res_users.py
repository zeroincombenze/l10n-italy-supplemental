# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        # Upstream saves the admin login URL as web.base.url. A login from
        # localhost (or a JSON-RPC script) would store a wrong public URL:
        # drop the location so upstream does not update the parameter.
        if user_agent_env and "localhost" in (
            user_agent_env.get("base_location") or ""
        ):
            user_agent_env = dict(user_agent_env)
            user_agent_env.pop("base_location")
        return super(ResUsers, cls).authenticate(
            db, login, password, user_agent_env
        )
