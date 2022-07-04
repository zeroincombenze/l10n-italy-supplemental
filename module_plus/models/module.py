# -*- coding: utf-8 -*-
import os
import ast
from odoo import api, models, tools, service


class BaseModuleUpdate(models.TransientModel):
    _inherit = "base.module.update"

    def read_manifest_file(self, manifest_path):
        try:
            manifest = ast.literal_eval(open(manifest_path).read())
        except (ImportError, IOError, SyntaxError):
            pass
        return manifest

    @api.multi
    def update_module(self):
        need_restart = False
        module_model = self.env["ir.module.module"]
        for addons_path in tools.config['addons_path'].split(','):
            addons_path = os.path.abspath(tools.ustr(addons_path.strip()))
            if os.path.isdir(os.path.join(addons_path, ".git")):
                # TODO> Use package GitRun
                os.system("cd %s; git stash" % addons_path)
                os.system("cd %s; git pull" % addons_path)
                for path in os.listdir(addons_path):
                    manifest_path = os.path.abspath(
                        os.path.join(addons_path, path, "__manifest__.py"))
                    if not os.path.isfile(manifest_path):
                        continue
                    manifest = self.read_manifest_file(manifest_path)
                    version = manifest.get("version")
                    if not version.startswith("10.0"):
                        version = "10.0.%s" % version
                    modules = module_model.search(
                        [("name", "=", os.path.basename(path))])
                    if modules:
                        cur_version = modules[0].latest_version
                        if cur_version and not cur_version.startswith("10.0"):
                            cur_version = "10.0.%s" % cur_version
                        if cur_version != version:
                            modules[0].published_version = version
                            if modules[0].state == "installed":
                                modules[0].state = "to upgrade"
                                need_restart = True
                if need_restart:
                    self.cr.commit()
                    service.server.restart()
                    return {
                        "type": "ir.actions.client",
                        "tag": "home",
                        "params": {"wait": True},
                    }
        return super(BaseModuleUpdate, self).update_module()
