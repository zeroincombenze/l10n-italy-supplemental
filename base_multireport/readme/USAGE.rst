This module gives a lot of pretty features to print nice reports.

Inside every report it is possible check for some characteristics and/or add some values.
The value of every parameter is evaluate in fallback way.
The fallback path is:

1. Valid value (not null and not space) in report (model ir_action_report_xml)
2. Valid value (not null and not space) in template of report (model multireport.template), if declared
3. Valid value (not null and not space) in specific document style (model multireport.style)
4. Value in default document style (model multireport.style)
5. For some parameters, for historical reason, value may be load from other sources (i.e. custom footer)

In report the fallback function is report.get_report_attrib(PARAM,o,doc_opts), where param is parameter to get value.

Report may load specific value if declare field as follow:

* If field name beginning with `doc_opts`, value is from the specific report which is printing.
* If Field name beginning with `doc_style`, value is from the style of the company.

Warning! If report get value directly from report or style, can get a None value and result may be unexpected.

Look at follow table for details:

.. $include usage_detail.rst

`Report Identity`

Report Identity is used to select standard Odoo reports or customized reports.
If value is 'Odoo' all customization is disabled and original Odoo reports are printed.
It is only an attribute of company style.

|

`Header mode`

This parameter, named `header_mode` set how the header is printed.
May be one of 'standard', 'logo', 'only_logo', 'line-up', 'line-up2', 'line-up3', 'line-up4', 'line-up5', 'line-up6', 'no_header'

* standard: standard Odoo header is printed
* logo: only the wide logo is printed which must contain company informations; separation line after logo
* only_logo: only the wide logo is printed which must contain company informations; no separation line is printed
* line-up:  logo and slogan, separation line but no company data
* line-up2:  logo and slogan but no separation line neither company data
* line-up3:  logo and company data and separation line; no slogan
* line-up4:  logo and company data; no separation line neither slogan
* line-up5:  logo and custom data and separation line; no slogan
* line-up6:  logo and custom data; no separation line neither slogan
* no_header: no header is printed; used on pre-printed paper

|

`Footer mode`

This parameter, name `footer_mode` set how the footer is printed.
May be one of 'standard', 'auto', 'custom', 'no_footer'

* standard: standard Odoo footer is printed; may be as 'auto' or as 'custom' based on company.custom_footer field
* auto: footer is printed with company data
* custom: user data is printed in footer (like Odoo custom footer)
* no_footer: no footer is printed; anyway pages are printed

|

`Address mode`

This parameter, named `address_mode` set how the partner address is printed.
May be on of 'standard', 'only_one'.

* standard: standard Odoo behavior; id shipping and invoice addresses are different, both of them are printed
* only_on: just the specific address is printed; specific is shipping address on delivery document, invoice addres on invoice document

|

`Payment Term Position`

This parameter, named `payment_term_position` set where the payment datas (payment term, due date and payment term notes) are printed.
May be one of 'odoo', 'auto', 'header', 'header_no_iban', 'footer', 'footer_no_iban', 'footer_notes', 'none'

* odoo: standard Odoo behavior; payment term on header, payment term notes on footer
* auto: when due payment is whole in one date, all datas are printed on header otherwise on footer
* header: all the payment datas are printed on header
* header_no_iban: like "header" but without IBAN
* footer: all the payment data are printed on footer
* footer_no_iban: like "footer" but without IBAN
* footer_notes: just payment term notes in footer
* none: no any payment data is printed


|

`Print code`

This parameter, name `code_mode` manage the printing of product code in document lines.
May be one of: 'print', 'no_print'

* noprint: standard Odoo behavior
* print: print a column with code in body of documents

|

`Print description`

This parameter, name `description_mode` manage the printing of description in document lines.
May be one of: 'as_is', 'line1', 'nocode', 'nocode1'

* as_is: that is the default value; it means description is printed as is, without manipulations
* line1: only the 1st line of description is printed
* nocode: product code (text between [brackets]) is removed
* nocode1: same of line1 + nocode

|

`Order reference text`

This parameter, named `order_ref_text` contains the text to print before every line of document body when order changes.
May be used following macroes:

%(client_order_ref)s => Customer reference of order
%(order_name)s => Sale order number
%(date_order)s => Sale order date

i.e. "Order #: %(order_name)s - Your ref: %(client_order_ref)s"'

|

`DdT reference text`

This parameter, named `ddt_ref_text` contains the text to print before every line of document body when delivery document changes.
May be used following macroes:

%(ddt_number)s => Delivery document number
%(date_ddt)s => Delivery document date
%(date_done)s => Delivery date

'i.e. "Ddt #: %(ddt_number)s of %(date_ddt)s"'

|

`Delivery Date`

In sale order you can print Delivery Date of every line. This feature requires the sale_order_line_date
module installed.

|

`Custom Header`

This parameter, named `custom_header` contains the html code to print when header_mode is set to line_up5 or line_up6.
May be used following macroes:

%(banks)s => IBAN of company
%(city)s => City of company
%(email)s => e-mail of company
%(fax)s
%(mobile)s
%(name)s
%(phone)s
%(street)s
%(street2)s
%(vat)s
%(website)s
%(zip)s
%(codice_destinatario)s (solo se installato modulo fattura elettronica)
%(fatturapa_rea_capital)s (solo se installato modulo fattura elettronica)
%(fatturapa_rea_number)s (solo se installato modulo fattura elettronica)
%(fatturapa_rea_office)s (solo se installato modulo fattura elettronica)
%(fiscalcode)s (solo se installato modulo codice fiscale)
%(ipa_code)s (solo se installato modulo codice ipa)

|

In xml report it is also possible test the existence of a field. The should be as follow:

`
<div t-if="'some_field' in docs[0]">FOUND SOME FIELD</div>
<div t-if="'some_field' not in docs[0]">NOT FOUND SOME FIELD</div>
`
