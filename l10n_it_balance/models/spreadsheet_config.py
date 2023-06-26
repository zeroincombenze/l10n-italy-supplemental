# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later
# (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

import xlwt

font_name = 'Arial'

MAIN_STYLE = xlwt.XFStyle()
font = xlwt.Font()
font.name = font_name
MAIN_STYLE.font = font
MAIN_STYLE.num_format_str = '#,##0.00'

STYLE_HEADER = xlwt.XFStyle()
font0 = xlwt.Font()
font0.name = font_name
font0.colour_index = 4
font0.bold = True
STYLE_HEADER.font = font0

STYLE_FLOAT = xlwt.XFStyle()
STYLE_FLOAT.num_format_str = '#,##0.00'

STYLE_LEVEL_ZERO = xlwt.XFStyle()
font_level_zero = xlwt.Font()
font_level_zero.name = font_name
font_level_zero.colour_index = xlwt.Style.colour_map['ocean_blue']
STYLE_LEVEL_ZERO.font = font_level_zero
STYLE_LEVEL_ZERO.num_format_str = '#,##0.00'

STYLE_LEVEL_1 = xlwt.XFStyle()
font_level_1 = xlwt.Font()
font_level_1.name = font_name
font_level_1.colour_index = xlwt.Style.colour_map['violet']
STYLE_LEVEL_1.font = font_level_1
STYLE_LEVEL_1.num_format_str = '#,##0.00'

STYLE_LEVEL_2 = xlwt.XFStyle()
font_level_2 = xlwt.Font()
font_level_2.name = font_name
font_level_2.colour_index = xlwt.Style.colour_map['green']
STYLE_LEVEL_2.font = font_level_2
STYLE_LEVEL_2.num_format_str = '#,##0.00'

STYLE_LEVEL_4 = xlwt.XFStyle()
font_level_4 = xlwt.Font()
font_level_4.name = font_name
font_level_4.colour_index = xlwt.Style.colour_map['red']
STYLE_LEVEL_4.font = font_level_4
STYLE_LEVEL_4.num_format_str = '#,##0.00'

al = xlwt.Alignment()
al.horz = al.HORZ_CENTER
STYLE_CENTER = xlwt.XFStyle()
STYLE_CENTER.num_format_str = '@'
STYLE_CENTER.alignment = al
STYLE_CENTER.font = font0

STYLE_BOLD_BLACK = xlwt.XFStyle()
fontb = xlwt.Font()
fontb.name = font_name
fontb.colour_index = xlwt.Style.colour_map['black']
fontb.bold = True
STYLE_BOLD_BLACK.font = fontb
STYLE_BOLD_BLACK.num_format_str = '#,##0.00'

EXCEL_UNITS = 256


def xlwt_get_col_width(num_characters):
    return int((1+num_characters) * EXCEL_UNITS)
