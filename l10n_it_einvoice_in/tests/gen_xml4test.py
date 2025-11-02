#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
from random import randint
from lxml import etree

from python_plus import _b, _u, compute_date

__version__ = "10.0.1.3.35"


def progressivo(opt_args):
    return "%3.3s%02s" % (
        os.path.basename((opt_args.test_xml_fn or opt_args.real_xml_fn))
        .split(".")[0]
        .split("_")[1][-3:],
        randint(1, 99),
    )


DATA_TO_UPDATE = [
    {
        "tags": [
            "FatturaElettronicaHeader",
            "DatiTrasmissione",
            "ProgressivoInvio",
        ],
        "text": progressivo,
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "DatiTrasmissione",
            "CodiceDestinatario",
        ],
        "text": "CE961TO",
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "CessionarioCommittente",
            "DatiAnagrafici",
            "IdFiscaleIVA",
            "IdPaese",
        ],
        "text": "IT",
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "CessionarioCommittente",
            "DatiAnagrafici",
            "IdFiscaleIVA",
            "IdCodice",
        ],
        "text": "05111810015",
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "CessionarioCommittente",
            "DatiAnagrafici",
            "CodiceFiscale",
        ],
        "text": "05111810015",
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "CessionarioCommittente",
            "DatiAnagrafici",
            "Anagrafica",
            "Denominazione",
        ],
        "text": "TEST COMPANY",
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "CessionarioCommittente",
            "Sede",
            "Indirizzo",
        ],
        "text": "Via dei Matti, 0",
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "CessionarioCommittente",
            "Sede",
            "CAP",
        ],
        "text": "20080",
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "CessionarioCommittente",
            "Sede",
            "Comune",
        ],
        "text": "Ozzero",
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "CessionarioCommittente",
            "Sede",
            "Provincia",
        ],
        "text": "MI",
    },
    {
        "tags": [
            "FatturaElettronicaHeader",
            "CessionarioCommittente",
            "Sede",
            "Nazione",
        ],
        "text": "IT",
    },
    {
        "tags": [
            "FatturaElettronicaBody",
            "DatiGenerali",
            "DatiGeneraliDocumento",
            "Data",
        ],
        "date": "####-<#-99",
    },
    {
        "tags": [
            "FatturaElettronicaBody",
            "DatiGenerali",
            "DatiDDT",
            "DataDDT",
        ],
        "date": "####-<#-15",
    },
    {
        "tags": [
            "FatturaElettronicaBody",
            "DatiGenerali",
            "DatiGeneraliDocumento",
            "TipoDocumento",
        ],
        "td": "TD24",
    },
    {
        "tags": [
            "FatturaElettronicaBody",
            "DatiPagamento",
            "DettaglioPagamento",
            "DataRiferimentoTerminiPagamento",
        ],
        "date": "####-<#-99",
    },
    {
        "tags": [
            "FatturaElettronicaBody",
            "DatiPagamento",
            "DettaglioPagamento",
            "DataScadenzaPagamento",
        ],
        "date": ["####-##-99", "####-1>-99", "####-2>-99", "####-3>-99", "####-4>-99"],
        "date_shifted": [
            "####-1>-10",
            "####-2>-10",
            "####-3>-10",
            "####-4>-10",
            "####-5>-10",
        ],
    },
]
"""    <FatturaElettronicaHeader>
    <DatiTrasmissione>
        <IdTrasmittente>
            <IdPaese>IT</IdPaese>
            <IdCodice>01234560017</IdCodice>
        </IdTrasmittente>
        <ProgressivoInvio>00001</ProgressivoInvio>"""


def preserve_xml_header(source, xml_text):
    """Preserve xnl header for some tests"""
    with open(source, "r") as fd:
        header = ""
        for line in fd.read().split("\n"):
            if "<FatturaElettronicaHeader>" in line:
                break
            header += line
            header += "\n"
    if header:
        trigger = False
        for line in xml_text.split("\n"):
            if "<FatturaElettronicaHeader>" in line:
                trigger = True
            if trigger:
                header += line
                header += "\n"
        xml_text = header
    return xml_text


def find_tag(root, tag):
    item = [x for x in root if x.tag == tag]
    if item:
        return item[0]
    return None


def find_nested_tag(elem, tags):
    if len(tags) and elem is not None:
        res = []
        tag = tags.pop(0)
        for item in elem:
            if tag == item.tag:
                saved_tags = tags.copy()
                item = find_nested_tag(item, tags)
                tags = saved_tags
                if item is not None:
                    res.append(item)
        if len(res) > 1:
            elem = res
        elif len(res) == 1:
            elem = res[0]
        else:
            elem = None
    return elem


def action_value(opt_args, value):
    if callable(value):
        return value(opt_args)
    elif value in globals():
        return globals()[value]
    return value


def get_action(opt_args, action, nr):
    for item in ("text", "text_id", "date_shifted", "date", "td"):
        if not opt_args.shift_duedates and item == "date_shifted":
            continue
        if item in action:
            if isinstance(action[item], (list, tuple)):
                return item, action_value(opt_args, action[item][nr])
            return item, action_value(opt_args, action[item])
    return None, None


def convert_xml(opt_args, root):
    for action in DATA_TO_UPDATE:
        original_tags = action["tags"].copy()
        elems = find_nested_tag(root, action["tags"])
        if elems is None:
            print(
                "Warning: tag %s of %s not found!"
                % (".".join(action["tags"]), original_tags)
            )
        else:
            if opt_args.verbose:
                print("... %s" % ".".join(original_tags))
            if not isinstance(elems, (list, tuple)):
                elems = [elems]
            for nr, elem in enumerate(elems):
                todo, value = get_action(opt_args, action, nr)
                if todo == "text":
                    elem.text = value
                elif todo in ("date", "date_shifted"):
                    if opt_args.invoice_date and original_tags[-1] in (
                        "Data",
                        "DataRiferimentoTerminiPagamento",
                    ):
                        elem.text = compute_date(opt_args.invoice_date)
                    elif (
                        opt_args.due_date
                        and original_tags[-1] == "DataScadenzaPagamento"
                    ):
                        elem.text = compute_date(opt_args.due_date)
                    else:
                        elem.text = compute_date(value)
                elif todo == "td":
                    if opt_args.fiscal_document_type:
                        elem.text = opt_args.fiscal_document_type
                    else:
                        elem.text = value
    return root


def format_xml(opt_args, source, target):
    with open(source, "r") as fd:
        try:
            root = etree.XML(_b(fd.read()))
        except SyntaxError as e:
            print("%s: ***** Error %s *****" % (source, e))
            root = None
            xml_text = None
    if root is not None:
        root = convert_xml(opt_args, root)
        try:
            xml_text = _u(etree.tostring(root, pretty_print=True))
        except SyntaxError as e:
            print("%s: ***** Error %s *****" % (source, e))
            xml_text = None
    if xml_text:
        xml_text = xml_text.replace("\n\n", "\n")
        if not opt_args.format_header:
            xml_text = preserve_xml_header(source, xml_text)
        if opt_args.dry_run:
            print(xml_text)
        else:
            with open(target, "w") as fd:
                fd.write(xml_text)


def main(cli_args=None):
    cli_args = cli_args or sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Generate xml file for test based on a real XML file",
        epilog="© 2021-2023 by SHS-AV s.r.l.",
    )
    parser.add_argument(
        "-d", "--due-date", help="Date to pay: see python-plus for info"
    )
    parser.add_argument(
        "-H",
        "--format-header",
        action="store_true",
        help="Format xml header and remove wrong header",
    )
    parser.add_argument(
        "-i", "--invoice-date", help="Date to invoice: see python-plus for info"
    )
    parser.add_argument("-n", "--dry-run", dest="dry_run", action="store_true")
    parser.add_argument(
        "-s",
        "--shift-duedates",
        action="store_true",
        help="shift due date 10 days later",
    )
    parser.add_argument(
        "-t", "--fiscal-document-type", help="may be TD01, TD04, TD24 or else"
    )
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-V', '--version', action="version", version=__version__)
    parser.add_argument('real_xml_fn')
    parser.add_argument('test_xml_fn', nargs='?')
    opt_args = parser.parse_args(cli_args)
    if not os.path.isfile(opt_args.real_xml_fn):
        print('No file %s found!' % opt_args.real_xml_fn)
    format_xml(
        opt_args, opt_args.real_xml_fn, opt_args.test_xml_fn or opt_args.real_xml_fn
    )
    return 0


if __name__ == "__main__":
    exit(main())
