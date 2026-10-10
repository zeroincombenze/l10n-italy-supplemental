#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa - pylint: skip-file
# -*- coding: utf-8 -*-
#
# pyxbgen
# Agenzia delle Entrate pyxb generator
#
# This free software is released under GNU Affero GPL3
# author: Antonio M. Vigliotti - antoniomaria.vigliotti@gmail.com
# (C) 2017-2020 by SHS-AV s.r.l. - http://www.shs-av.com - info@shs-av.com
#
import os
import re
import sys
import argparse


__version__ = "10.0.0.3.6"


def wash_source(lines, kind):
    lineno = 0
    # TODO: patch fatturapa for OCA compatibility, may not work in the future
    RULES = (
        "RateType",
        "PesoType",
        "QuantitaType",
        "Amount8DecimalType",
        "Amount2DecimalType",
        "class",
        "rate_type_1",
        "rate_type_2",
        "rate_type_3",
        "rate_type_4",
        "rate_type_5",
        "rate_type_6",
    )
    RULES_START = {
        "RateType": "class RateType",
        "PesoType": "class PesoType",
        "QuantitaType": "class QuantitaType",
        "Amount8DecimalType": "class Amount8DecimalType",
        "Amount2DecimalType": "class Amount2DecimalType",
        "class": "class ",
        "follow": "    ",
        "rate_type_1": "RateType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive",
        "rate_type_3": "RateType._InitializeFacetMap(RateType._CF_maxInclusive,",
        "rate_type_5": "RateType._InitializeFacetMap(RateType._CF_pattern,",
    }
    RULES_MATCH = {
        "rate_type_2": "value_datatype=RateType, value=pyxb.binding.datatypes.decimal('100.0')",
        "rate_type_4": "RateType._CF_pattern)",
        "rate_type_6": "RateType._CF_maxInclusive)",
    }
    RULES_REPLMNT = {
        "RateType": (".decimal)", ".string)", True),
        "PesoType": (".decimal)", ".string)", True),
        "QuantitaType": (".decimal)", ".string)", True),
        "Amount8DecimalType": (".decimal)", ".string)", True),
        "Amount2DecimalType": (".decimal)", ".string)", True),
        "follow": (".decimal", ".string", 2),
        "rate_type_1": (0, "# ", 1),
        "rate_type_2": (0, "# ", 1),
        "rate_type_3": ("RateType._CF_maxInclusive,", "", 1),
        "rate_type_4": ("", "", 1),
        "rate_type_5": (-1, ")", 1),
        "rate_type_6": (0, "# ", 1),
    }
    RULES_PATCH = {
        "RateType": 1,
    }
    patch = 0
    while lineno < len(lines):
        if not lines[lineno] or not kind:
            pass
        else:
            for rule in RULES:
                if (
                    rule in RULES_START and lines[lineno].startswith(RULES_START[rule])
                ) or (
                    rule in RULES_MATCH and lines[lineno].find(RULES_MATCH[rule]) >= 0
                ):
                    if rule in RULES_REPLMNT:
                        src = RULES_REPLMNT[rule][0]
                        tgt = RULES_REPLMNT[rule][1]
                        cond = RULES_REPLMNT[rule][2]
                        if cond or patch == cond:
                            if src == 0:
                                lines[lineno] = tgt + lines[lineno]
                            elif src == -1:
                                lines[lineno] = lines[lineno][0:-1] + tgt
                            elif lines[lineno].find(src) < 0:
                                patch = 2
                            elif src == "" and tgt == "":
                                lines[lineno - 1] += lines[lineno].strip()
                                del lines[lineno]
                                lineno -= 1
                            else:
                                lines[lineno] = lines[lineno].replace(src, tgt)
                    if rule in RULES_PATCH:
                        patch = RULES_PATCH[rule]
                    else:
                        patch = 0
                    break
        lineno += 1


def robust_source(lines, file_schema):
    if file_schema:
        TXT1_FILE_SCHEMA = '"' + file_schema + '"'
        TXT2_FILE_SCHEMA = "'" + file_schema + "'"
        TXT3_FILE_SCHEMA = '"' + os.path.abspath(file_schema) + '"'
        TXT4_FILE_SCHEMA = "'" + os.path.abspath(file_schema) + "'"
    state = 0
    lineno = 0
    saved_lines = []
    lines.insert(lineno, "# flake8: noqa")
    lineno += 1
    lines.insert(lineno, "# -*- coding: utf-8 -*-")
    lineno += 1
    while lineno < len(lines):
        if state == 3:
            lines.insert(lineno, "except ImportError as err:")
            lineno += 1
            lines.insert(lineno, "    _logger.debug(err)")
            lineno += 1
            lines.insert(lineno, "")
            # lineno += 1
            # lines.insert(lineno, "SCHEMA_FILE = '%s'" % file_schema)
            lineno += 1
            lines.insert(lineno, "")
            lineno += 1
            state = 2
        if not lines[lineno]:
            if state < 2:
                del lines[lineno]
                lineno -= 1
        elif state == 0 and lines[lineno].startswith("# Generated "):
            lineno += 1
            lines.insert(
                lineno,
                "# by Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>",
            )
        elif lines[lineno] == "# -*- coding: utf-8 -*-":
            del lines[lineno]
            lineno -= 1
        elif lines[lineno][0:6] == "import":
            if lines[lineno][0:11] == "import pyxb":
                if state == 0:
                    lines.insert(lineno, "import logging")
                    lineno += 1
                    state = 1
                if state == 1:
                    saved_lines.append(lines[lineno])
                    del lines[lineno]
                    lineno -= 1
                elif state == 2:
                    lines.insert(lineno, "try:")
                    lineno += 1
                    state = 3
                if state == 3:
                    lines[lineno] = "    %s" % lines[lineno]
            elif (
                lines[lineno][0:10] == "import _cm"
                or lines[lineno][0:10] == "import _ds"
            ):
                lines[lineno] = "from . %s" % lines[lineno]
        elif state == 1:
            lines.insert(lineno, "_logger = logging.getLogger(__name__)")
            lineno += 1
            lines.insert(lineno, "try:")
            lineno += 1
            for saved_line in saved_lines:
                lines.insert(lineno, "    %s" % saved_line)
                lineno += 1
            lines.insert(lineno, "except ImportError as err:")
            lineno += 1
            lines.insert(lineno, "    _logger.debug(err)")
            lineno += 1
            lines.insert(lineno, "")
            lineno += 1
            state = 2
        elif file_schema:
            lines[lineno] = lines[lineno].replace(TXT1_FILE_SCHEMA, "SCHEMA_FILE")
            lines[lineno] = lines[lineno].replace(TXT2_FILE_SCHEMA, "SCHEMA_FILE")
            lines[lineno] = lines[lineno].replace(TXT3_FILE_SCHEMA, "SCHEMA_FILE")
            lines[lineno] = lines[lineno].replace(TXT4_FILE_SCHEMA, "SCHEMA_FILE")
        lineno += 1


def correct_future(lines):
    binding_line = ""
    lineno = 0
    state = -1
    while lineno < len(lines):
        if state < 0 and lines[lineno].find("_ImportedBinding__") >= 0:
            binding_line = lines[lineno]
            del lines[lineno]
            lineno -= 1
        elif state < 0 and lines[lineno].find("import") >= 0:
            state = lineno
        elif state >= 0 and binding_line:
            lines.insert(lineno, binding_line)
            lineno += 1
            binding_line = ""
        lineno += 1


LEX_RULES = {}


def cvt_decimal_2_str(lines, convert=None):
    schema_root = os.path.dirname(os.getcwd())
    lineno = 0
    token = ""
    class_converted = False
    while lineno < len(lines):
        if schema_root in lines[lineno]:
            lines[lineno] = lines[lineno].replace(
                "'%s" % schema_root, "'..").replace("\"%s" % schema_root, "\"..")
        if (
            lines[lineno] == ("#" * len(lines[lineno])) or
            lines[lineno] == (" " * len(lines[lineno]))
        ):
            del lines[lineno]
            continue
        x = re.match("[ ]*class[ ]+[A-Za-z0-9_]+", lines[lineno])
        if x:
            token = ""
            class_converted = False
        if token:
            t = ",%s" % token
            x = re.match(t, lines[lineno])
            if x:
                lines[lineno] = lines[lineno].replace(t, "")
            t = ", %s" % token
            x = re.match(t, lines[lineno])
            if x:
                lines[lineno] = lines[lineno].replace(t, "")
        x = re.match(r"[ ]*def[ ]+[A-Za-z0-9_]+ \(", lines[lineno])
        if x:
            lines[lineno] = lines[lineno].replace(" (", "(")
        x = re.match(r"[ ]*class[ ]+[A-Za-z0-9_]+ \(", lines[lineno])
        if x:
            lines[lineno] = lines[lineno].replace(" (", "(")
        if convert:
            # if "Amount8DecimalType" in lines[lineno]:
            #     x = None
            # else:
            x = re.match(
                r"class[ ]+[A-Za-z0-9_]+[ ]*\(.*pyxb.binding.datatypes.decimal",
                lines[lineno],
            )
            if x:
                lines[lineno] = lines[lineno].replace(
                    "datatypes.decimal", "datatypes.string"
                )
                lines.insert(
                    lineno, "# Follow decimal class updated to string"
                )
                lineno += 1
                class_converted = True
        if class_converted:
            x = re.match("^[^#].*\._?CF_maxInclusive", lines[lineno])
            if x:
                # import pdb; pdb.set_trace()
                first_lineno = lineno
                x = re.match(r"^[ ]+[A-Za-z0-9_]", lines[first_lineno])
                while x:
                    first_lineno -= 1
                    x = re.match(r"^[ ]+[A-Za-z0-9_]", lines[first_lineno])
                last_lineno = lineno + 1
                x = re.match( r"^[ ]+[A-Za-z0-9_]", lines[last_lineno])
                while x:
                    last_lineno += 1
                    x = re.match(r"^[ ]+[A-Za-z0-9_]", lines[last_lineno])
                for ix in (first_lineno, last_lineno - 1):
                    lines[ix] = "# " + lines[ix]
                lines.insert(
                    lineno,
                    "# Follow(s) line(s) are ignored because string class"
                )
                lineno += 1
        lineno += 1


def main(cli_args=None):
    cli_args = cli_args or sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Generate file to generate XML files",
        epilog="© 2017-2022 by SHS-AV s.r.l."
    )
    parser.add_argument('-3', '--python3', action='store_true')
    parser.add_argument('-S', '--dec2str', action='store_false', default=True)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-V', '--version', action="version", version=__version__)
    parser.add_argument('filepy')
    parser.add_argument('fileschema', nargs='?', default='')
    parser.add_argument('fmlist', nargs='?', default='')
    opt_args = parser.parse_args(cli_args)
    sts = 0
    try:
        with open(opt_args.filepy, "r") as fd:
            source = fd.read()
            lines = source.split("\n")
        if opt_args.python3:
            correct_future(lines)
        else:
            robust_source(lines, opt_args.fileschema)
        cvt_decimal_2_str(lines, convert=opt_args.dec2str)
        with open(opt_args.filepy, "w") as fd:
            fd.write("".join("%s\n" % l for l in lines))
    except BaseException:
        print("**** Error *****")
        sts = 1
    return sts


if __name__ == "__main__":
    exit(main())
