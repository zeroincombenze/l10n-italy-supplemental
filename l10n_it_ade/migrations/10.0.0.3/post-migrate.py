# -*- coding: utf-8 -*-
#
# Copyright 2016-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import re

from odoo import SUPERUSER_ID, api

# Nature(text), law number(number), law supplemental(text), \
# law section(number), law letter(text), law ref (text)
# - law supplemental -> (bis|ter|quater|quinques|sexies|septies|octies|novies)
RE_ESCL = "E[scl.]+"
RE_FC = r"(F\.?C|F[uori.]+ C[ampo.]+)( IVA )?"
RE_NSOGG = "N[on]*[. ]+S"
RE_MIN = "Contr[ib. ]+Min"
RE_NI = "N[on]*[. ]+I[mp. ]+"
RE_ESE = "Es[ente.]+"
ASSOCODES = {
    "N010100": (RE_ESCL, "15", None, None, None, None),
    "N020100": (RE_FC, "(1|17)", None, None, None, None),
    "N020101": (RE_FC, "2", None, None, None, None),
    "N020102": (RE_FC, "3", None, None, None, None),
    "N020103": (RE_FC, "4", None, None, None, None),
    "N020104": (RE_FC, "5", None, None, None, None),
    "N020201": (None, "7", "bis", None, None, None),
    "N020202": (None, "7", "ter", None, None, None),
    "N020203": (None, "7", "quater", None, None, None),
    "N020204": (None, "7", "quinquies", None, None, None),
    "N020206": (None, "7", "sexies", None, None, None),
    "N020207": (None, "7", "septies", None, None, None),
    "N020208": (None, "38", None, "5", None, r"D?\.?L.? *331"),
    "N020209": ("no.? res", "17", None, "3", None, None),
    "N020210": (None, "7", None, None, None, "19[- .,]*c[- .,]*3[- .,/]*l[etr.]*b"),
    "N020212": (RE_NSOGG, "50", "bis", "4", "[cehi .]+", r"D?\.?L.? *331"),
    "N020213": (None, "7", "octies", None, None, None),
    "N020300": (RE_NSOGG, "74", None, "[12]", None, None),
    "N020400": (RE_ESCL, "13", None, None, None, None),
    "N020501": (RE_MIN, "(1|27)", None, None, None, r"(D?\.?L.? *98|L.? *244)"),
    "N020502": ("Forf", "1", None, None, None, "L.? *190"),
    "N020601": ("Var[iazione.]?", "26", None, "3", None, None),
    "N030101": (RE_NI, "8", None, "1", "a", None),
    "N030106": (RE_NI, "8", None, "1", "b", None),
    "N030109": (RE_NI, "8", "bis", None, None, None),
    "N030110": (RE_NI, "9", None, "1", None, None),
    "N030111": (RE_NI, "72", None, None, None, None),
    "N030112": (RE_NI, "71", None, None, None, "(RSM|Marino)"),
    "N030113": (RE_NI, "71", None, None, None, "(SCV|Vaticano)"),
    "N030201": (
        RE_NI,
        "8",
        None,
        "1",
        "c",
        "(Let[tera.]+|Dich[iarzone]*)[ di]* Int[ento.]+",
    ),
    "N030202": (
        RE_NI,
        "8",
        "(bis)?",
        "2",
        None,
        "(Let[tera.]+|Dich[iarzone]*)[ di]* Int[ento.]+",
    ),
    "N030203": (
        RE_NI,
        "9",
        None,
        "2",
        None,
        "(Let[tera.]+|Dich[iarzone]*)[ di]* Int[ento.]+",
    ),
    "N030204": (
        RE_NI,
        "72",
        None,
        "1",
        None,
        "(Let[tera.]+|Dich[iarzone]*)[ di]* Int[ento.]+",
    ),
    "N030401": (RE_NI, "41", None, None, None, r"D?\.?L.? *331"),
    "N030501": (RE_NI, "38", "quater", "1", None, None),
    "N040101": (RE_ESE, "10", None, None, None, None),
    "N040102": (RE_ESE, "10", None, "[123456789]", None, None),
    "N040103": (RE_ESE, "10", None, "11", None, None),
    "N040105": (RE_ESE, "10", None, "27", None, "quinques"),
    "N050100": ("R[egime.]+[ di]+Marg", "3[67]", None, None, None, r"D?\.?L.? *41"),
    "N060101": (None, "17", None, "6", "a", "bis"),
    "N060102": (None, "74", None, "[78]", None, None),
    "N060103": (None, "17", None, "5", None, None),
    "N060104": (None, "17", None, "6", "a", None),
    "N060105": (None, "17", None, "6", "b", None),
    "N060106": (None, "17", None, "6", "c", None),
    "N060107": (None, "17", None, "6", "a", "ter"),
    "N060109": (None, "7", "bis", None, None, None),
    "N060201": (None, "7", "ter", None, None, None),
    "N060202": (None, "7", "quater", None, None, None),
    "N060203": (None, "7", "quinques", None, None, None),
    "*SP": (None, "17", "ter", None, None, None),
    "*DF": (None, "32", "bis", None, None, "83"),
    "*N6.9": (None, "17", None, "c", None, None),
}


def migrate(cr, version):
    """Set default values"""

    def search_4_tokens(
        tax_name,
        number,
        nature=None,
        bis=None,
        comma=None,
        letter=None,
        roman=None,
        law=None,
    ):
        regex = "(Oper[azione]?)?"
        if nature:
            regex += "[- (,./]?%sArt[ .]+%s" % (nature, number)
        else:
            regex += "[- (,./]?Art[ .]+%s" % number
        plus = False
        if bis:
            regex += "[- ]?%s" % bis
            plus = True
        if comma:
            regex += "[- ,.]*[nc](omma)?[- .,/]*%s" % comma
            plus = True
        if letter:
            regex += "[- ,./]*l[etr. ]*%s" % letter
            plus = True
        if roman:
            regex += "[- ,./]+%s" % roman
            plus = True
        if not plus:
            regex += "[^0-9]"
        if law:
            regex += ".*%s" % law
        if re.search(regex, tax_name, re.I):
            return True
        return False

    def set_result(tax, assosoftware, assosoftware_model, weight, res):
        res[tax.description]["wgt"] = weight
        if assosoftware == "*SP":
            res[tax.description]["axc"] = False
            res[tax.description]["nat"] = ""
            res[tax.description]["pay"] = "S"
        elif assosoftware == "*DF":
            res[tax.description]["axc"] = False
            res[tax.description]["nat"] = ""
            res[tax.description]["pay"] = "D"
        elif assosoftware.startswith("*N"):
            res[tax.description]["axc"] = False
            res[tax.description]["nat"] = assosoftware[1:]
            res[tax.description]["pay"] = ""
        else:
            assosoftware_rec = assosoftware_model.search([("code", "=", assosoftware)])
            res[tax.description]["axc"] = assosoftware
            res[tax.description]["nat"] = assosoftware_rec.nature
            res[tax.description]["pay"] = ""
            res[tax.description]["law"] = assosoftware_rec.name

    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        assosoftware_model = env["italy.ade.tax.assosoftware"]
        tax_model = env["account.tax"]
        nature_model = env["italy.ade.tax.nature"]
        env["res.company"]
        cur_company_id = False
        cur_company_pay = False
        res = {}
        for tax in tax_model.search([]):
            if tax.company_id.id != cur_company_id:
                cur_company_pay = "I"
                try:
                    env.cr.execute(
                        """select f.code from
                        res_company c,fatturapa_fiscal_position f
                        where c.fatturapa_fiscal_position_id=f.id and
                        c.id=%d"""
                        % tax.company_id.id
                    )
                    code = cr.fetchone()[0]
                    if code in ("RF16", "RF17"):
                        cur_company_pay = "D"
                except BaseException:
                    pass
                cur_company_id = tax.company_id.id
            res[tax.description] = {
                "wgt": 0,
                "nat": "",
                "pay": cur_company_pay if tax.type_tax_use == "sale" else "I",
                "amt": tax.amount,
                "des": tax.description,
                "nme": tax.name,
            }
            for assosoftware in ASSOCODES.keys():
                if search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                    bis=ASSOCODES[assosoftware][2],
                    comma=ASSOCODES[assosoftware][3],
                    letter=ASSOCODES[assosoftware][4],
                    law=ASSOCODES[assosoftware][5],
                ):
                    # Full match
                    weight = 4 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight < res[tax.description]["wgt"]:
                        continue
                    set_result(tax, assosoftware, assosoftware_model, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    bis=ASSOCODES[assosoftware][2],
                    comma=ASSOCODES[assosoftware][3],
                    letter=ASSOCODES[assosoftware][4],
                    law=ASSOCODES[assosoftware][5],
                ):
                    # match w/o nature
                    weight = 3 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight <= res[tax.description]["wgt"]:
                        continue
                    set_result(tax, assosoftware, assosoftware_model, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                    comma=ASSOCODES[assosoftware][3],
                    letter=ASSOCODES[assosoftware][4],
                    law=ASSOCODES[assosoftware][5],
                ):
                    # match w/o supplemental (bis/ter/...)
                    weight = 3 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight <= res[tax.description]["wgt"]:
                        continue
                    set_result(tax, assosoftware, assosoftware_model, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                    bis=ASSOCODES[assosoftware][2],
                    comma=ASSOCODES[assosoftware][3],
                    letter=ASSOCODES[assosoftware][4],
                ):
                    # Match w/o law reference
                    weight = 2 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight <= res[tax.description]["wgt"]:
                        continue
                    set_result(tax, assosoftware, assosoftware_model, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                    bis=ASSOCODES[assosoftware][2],
                    comma=ASSOCODES[assosoftware][3],
                ):
                    # Match w/o law ref neither law letter
                    weight = 2 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight <= res[tax.description]["wgt"]:
                        continue
                    set_result(tax, assosoftware, assosoftware_model, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                ):
                    # Finally match just nature and law number
                    weight = 1
                    if weight <= res[tax.description]["wgt"]:
                        continue
                    set_result(tax, assosoftware, assosoftware_model, weight, res)
        for item in res:
            if res[item]["wgt"] or res[item]["amt"]:
                tax = tax_model.search([("description", "=", res[item]["des"])])[0]
                vals = {}
                if res[item].get("nat"):
                    vals["kind_id"] = nature_model.search(
                        [("code", "=", res[item]["nat"])]
                    )[0].id
                elif "nat" in res[item]:
                    vals["kind_id"] = False
                if "pay" in res[item]:
                    vals["payability"] = res[item]["pay"]
                if res[item].get("axc"):
                    vals["assosoftware_id"] = assosoftware_model.search(
                        [("code", "=", res[item]["axc"])]
                    )[0].id
                elif "axc" in res[item]:
                    vals["assosoftware_id"] = False
                if "law" in res[item]:
                    vals["law_reference"] = res[item]["law"]
                tax.write(vals)
