# Part of the l10n_it_coa module.
"""Declarative VAT configuration of the ``it_coa`` taxes.

Tax ids are the ``id`` column of ``data/template/account.tax-it_coa.csv``.
Tax grid names are the ones of the Italian tax report of Odoo core (``l10n_it``):
a leading ``+`` is the tag applied to the invoice lines, the refund lines get the
opposite sign automatically.

Grid legend (periodic VAT report):
    02    VP2   total active operations (sales base)
    03    VP3   total passive operations (purchases base)
    4v    VP4   VAT due (sales tax)
    5v    VP5   VAT deductible (purchases tax)
    ve*   annual VAT return, section VE (sales detail)
    vf*   annual VAT return, section VF (purchases detail)
    vj*   annual VAT return, section VJ (reverse charge purchases)
"""

# Tax groups: id -> accounts (account ids are the account codes)
TAX_GROUPS = {
    "tax_group_it": {
        "tax_payable_account_id": "260010",
        "tax_receivable_account_id": "153010",
        "advance_tax_payment_account_id": "153070",
    },
}

# Standard rate taxes: id -> (base tags, tax tags, tax account)
STANDARD_TAXES = {}
for _tid in ("22v", "10v", "5v", "4v", "22vINC", "10vINC", "4vINC"):
    STANDARD_TAXES[_tid] = (["+02"], ["+4v"], "260010")
for _tid in ("22a", "10a", "5a", "4a"):
    STANDARD_TAXES[_tid] = (["+03"], ["+5v"], "153010")
# Split payment (art. 17-ter): the VAT is paid by the public administration
STANDARD_TAXES["22SPv"] = (["+02", "+ve38"], [], "260060")
STANDARD_TAXES["-SP"] = ([], [], "260060")

# VAT on cash basis (art. 32-bis DL 83/2012): id -> (base tags, tax tags,
# final VAT account, transition account)
CASH_BASIS_TAXES = {
    "22s": (["+02", "+ve37_ii"], ["+4v"], "260010", "260030"),
    "22c": (["+03"], ["+5v"], "153010", "153030"),
}

# Reverse charge, purchase side (supplier invoice, VAT integration credit):
# id -> (base tags, tax tags)
REVERSE_CHARGE_PURCHASE = {
    "a17c2a": (["+03", "+vj3"], ["+5v"]),
    "a17c6a": (["+03"], ["+5v"]),
    "a17c6ata": (["+03", "+vj16"], ["+5v"]),
    "a17c6ba": (["+03", "+vj14"], ["+5v"]),
    "a17c6ca": (["+03", "+vj15"], ["+5v"]),
    "a38a": (["+03", "+vj9"], ["+5v"]),
    "a41a": (["+03"], ["+5v"]),
    "a8aa": (["+03"], ["+5v"]),
}
REVERSE_CHARGE_PURCHASE_ACCOUNT = "153050"

# Reverse charge, sale side (self-invoice, VAT integration debit). The base is
# already reported by the purchase side, so only the tax is tagged.
REVERSE_CHARGE_SALE = (
    "aa17c2v",
    "a17c2v",
    "aa17c6v",
    "a17c6v",
    "aa17c6atv",
    "a17c6atv",
    "aa17c6bv",
    "a17c6bv",
    "aa17c6cv",
    "a17c6cv",
    "aa38v",
    "aa41v",
    "aa8av",
)
REVERSE_CHARGE_SALE_TAGS = ([], ["+4v"])
REVERSE_CHARGE_SALE_ACCOUNT = "260050"

# Zero rate taxes (exempt, non taxable, excluded, ...). The tax id is the key plus
# ``v`` (sale) or ``a`` (purchase). Tuple:
# (exemption reason, law reference, sale base tags, purchase base tags)
# A ``None`` tag list means the tax of that side is not a zero rate one.
ZERO_RATE_TAXES = {
    "a17": ("N6.9", "Art. 17 DPR 633/1972", ["+02"], ["+03"]),
    "a38": ("N3.2", "Art. 38 L. 427/1993", ["+02", "+ve30_iii"], None),
    "a41": ("N3.2", "Art. 41 L. 427/1993", ["+02", "+ve30_iii"], None),
    "a7": ("N2.1", "Art. 7 DPR 633/1972", ["+ve34"], []),
    "a7t": ("N2.1", "Art. 7-ter DPR 633/1972", ["+ve34"], ["+03"]),
    "a8a": ("N3.1", "Art. 8 lett. a DPR 633/1972", ["+02", "+ve30_ii"], None),
    "a8c2": ("N3.5", "Art. 8 c. 2 DPR 633/1972", ["+02", "+ve31"], ["+03"]),
    "a9": ("N3.4", "Art. 9 DPR 633/1972", ["+02", "+ve30_v"], ["+03"]),
    "a10": ("N4", "Art. 10 DPR 633/1972", ["+02", "+ve33"], ["+03", "+vf31"]),
    "a10c5": (
        "N4",
        "Art. 10 n. 27-quinquies DPR 633/1972",
        ["+02", "+ve33"],
        ["+03", "+vf31"],
    ),
    "a15": ("N1", "Art. 15 DPR 633/1972", ["+02"], ["+03"]),
    "a1": ("N2.2", "Art. 1 DPR 633/1972", [], []),
    "a2": ("N2.2", "Art. 2 DPR 633/1972", [], []),
    "a13": ("N2.2", "Art. 13 DPR 633/1972", [], []),
    "l41a36": ("N5", "Art. 36 DL 41/1995", ["+02"], ["+03"]),
    "l41a37": ("N5", "Art. 37 DL 41/1995", ["+02"], ["+03"]),
    "l244": ("N2.2", "Art. 1 c. 96-117 L. 244/2007", [], ["+03"]),
    "l98a27": ("N2.2", "Art. 27 DL 98/2011", [], ["+03"]),
    "l190a1": ("N2.2", "Art. 1 c. 54-89 L. 190/2014", [], ["+03"]),
}

# Partially deductible VAT. Each group of the CSV is made of an ``a`` child (the
# non deductible part, a cost: no account, no grid) and a ``b`` child (the deductible
# part). The purchase base is reported once, by the ``b`` child.
PARTIAL_DEDUCTIBLE_PREFIXES = (
    "1050",
    "10a0",
    "2220",
    "2250",
    "2270",
    "2280",
    "22a0",
    "450",
    "4a0",
)
PARTIAL_DEDUCTIBLE_ACCOUNT = "153010"
PARTIAL_ZERO_REASON = ("N2.2", "Art. 19-bis1 DPR 633/1972")

# Fixes of data errors of the CSV: id -> {field: value}
TAX_FIXES = {
    # the storno of split payment is an Italian VAT tax, not a Slovak one
    "-SP": {"tax_group_id": "tax_group_it"},
}
