================================================================
|icon| base_rule_multireport/Multi modelli di stampa 10.0.0.2.33
================================================================

**Manage document multiple reports**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/base_multireport/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| Install this module if you wish to wish customize your report printing.

The module is built on follow concepts:

* You can customize order, invoice and delivery documents
* Module does not disable standard Odoo report: you can use them whenever you want
* You can use this module as base for your custom report module
* Configuration parameters are organized as a hierarchical tree


|it| Installate questo modulo se volete personalizzare i modelli di stampa.

Il modulo è costruito sui seguenti concetti:

* Personalizza ordini, fatture e documenti di trasporto
* Il modulo non disabilita i modelli standard di Odoo, che potete utilizzare in qualsiasi momento
* Potete usare questo modulo come base per un vostro modulo di personalizzazione stampe
* I parametri di configurazione sono organizzati tramite albero gerarchico


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/base_multireport/static/description/description.png


Features | Caratteristiche
--------------------------

+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Feature / Funzione                                                                      | Notes / Note                                                                                              |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Print original Odoo reports / Stampa modelli originali di Odoo                          | Style configuration = Odoo/Configurazione a livello di stile = Odoo                                       |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Header line-up: logo and slogan / Intestazione solo logo e slogan                       |                                                                                                           |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Header line-up: logo and company data / Intestazione solo logo e dati azienda           | Company data shifted up / Dati aziende spostati in alto                                                   |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Header line-up: logo and customized data / Intestazione solo logo e dati personalizzati | You can use macroes to retriebe company data / Disponibili macro per caricare dati aziendali              |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Header with only wide logo / Intestazione solo logo largo                               | Logo with company data / Logo con i dati dell'azienda                                                     |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Header without data / No intestazione                                                   | Use preprinted paper / Utilizzo su carta intestata                                                        |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Custom footer / Piede personalizzato                                                    | You can use macroes to retriebe company data / Disponibili macro per caricare dati aziendali              |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Optional separation line / Linea di separazione opzionale                               |                                                                                                           |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Address mode / Modo stampa indirizzo                                                    | Print 2 addresses or only the specific one / Stampa doppio indirizzo o solo specifico                     |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Print product code / Stampa codice prodotto                                             |                                                                                                           |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Print description without code / Stampa descrizione senza codice                        | Extract code from description / Estrapola il codice dalla descrizione                                     |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Configurable documents / Documenti configurabili:                                       | Sale order, Delivery document, Invoice, Purchase order / Ordine cliente, DdT, Fattura, Ordine a fornitore |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Watermark / Filigrana                                                                   | High quality report / Stampa di alta qualità                                                              |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Ending page / Pagina finale                                                             | Ending page with commercial info / Pagina finale con informazioni commerciali                             |
+-----------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+



Usage | Utilizzo
----------------

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

+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| Name                       | Description                                        | Notes / Example                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| address_mode               | Which addresses are printed                        | Only invoices, order and deliveires                                                             |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| bottom_text                | Text to print at the bottom of the document        |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| code                       | Product code                                       |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| code_mode                  | Print code in document body                        | <t t-set="code_mode" t-value="report.get_report_attrib('code_mode',o,doc_opts)"/>               |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| company                    | Company of current document                        | Set by external layout                                                                          |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| company_partner            | Company partner of current document                | Set by external layout                                                                          |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| datetime                   | Python datetime instance                           | Only in render by Odoo core                                                                     |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| ddt_ref_text               | Text at every change of delivery document          |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| debug                      | Session in developer mode                          | Only in render by Odoo core                                                                     |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| description_mode           | Print code in document body                        | <t t-set="description_mode" t-value="report.get_report_attrib('description_mode',o,doc_opts)"/> |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc                        | Current document which is printing                 | Set by module. External layout set 'o' to compatibility with Odoo reports                       |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc_ids                    | Document object Id(s)                              | Set by Odoo core                                                                                |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc_model                  | Document model                                     | It is the same of use doc_opts.model                                                            |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc_opts                   | Document parametes                                 |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc_opts.model             | Document model                                     | Same as doc_model, set by Odoo core                                                             |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc_opts.paperformat_id    | ID to paperformat                                  | Only invoices, order and deliveires                                                             |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc_opts.report_name       | Report Name                                        |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc_style                  | Style parameteres                                  |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc_style.name             | Name of Style                                      |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| doc_style.origin           | `Report Identity` (see below)                      |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| docs                       | Document objects list                              | Set by Odoo core                                                                                |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| env                        | Environment                                        | Only in render by Odoo core                                                                     |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| footer_mode                | How to print footer                                |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| header_mode                | How to print header                                |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| l                          | Current invoice line when printing                 | Alias used only in invoice print                                                                |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| logo style                 | Html logo style                                    | Default is “max-height: 45px                                                                    | ” |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| o                          | Current invoice which is printing                  | Alias used in invoice print set by external layout                                              |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| order_ref_text             | Text at every change of order reference            |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| payment_term_position      | Payment data position                              | Only invoices, order and deliveries                                                             |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| pdf_ending_page            | Default Ending Page for this report                |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| pdf_ending_page_expression | Default Ending Page for this report                |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| pdf_watermark              | Default watermark for this report                  |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| pdf_watermark_expression   | Default watermark for this report                  |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| relativedelta              | relativedelta.docutils.relativedelta.relativedelta | Only in render by Odoo core                                                                     |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| report                     | Document report class                              | Only invoices, order and deliveires                                                             |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| report.get_report_attrib   | Get specific fallback value                        | <div t-if="report.get_report_attrib('header_mode',o,doc_opts)"> .. </div>.                      |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| res_company                | Default company                                    | Set by Odoo report module                                                                       |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| res_company                | Company of current document                        | Set by Odoo core                                                                                |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| style                      | Current `Report Identity` (see below)              |                                                                                                 |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| time                       | Python time instance                               | No invoices, orders and deliveries                                                              |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+
| xmlid                      | External identifier of current report              | Only in render by Odoo core                                                                     |   |
+----------------------------+----------------------------------------------------+-------------------------------------------------------------------------------------------------+---+



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



Getting started | Primi passi
=============================

|Try Me|


Prerequisites | Prerequisiti
----------------------------

* python 2.7+ (best 2.7.5+)
* postgresql 9.2+ (best 9.5)

::

    cd $HOME
    # Follow statements activate deployment, installation and upgrade tools
    cd $HOME
    [[ ! -d ./tools ]] && git clone https://github.com/zeroincombenze/tools.git
    cd ./tools
    ./install_tools.sh -pUT
    source $HOME/devel/activate_tools



Installation | Installazione
----------------------------

+---------------------------------+------------------------------------------+
| |en|                            | |it|                                     |
+---------------------------------+------------------------------------------+
| These instructions are just an  | Istruzioni di esempio valide solo per    |
| example; use on Linux CentOS 7+ | distribuzioni Linux CentOS 7+,           |
| Ubuntu 14+ and Debian 8+        | Ubuntu 14+ e Debian 8+                   |
|                                 |                                          |
| Installation is built with:     | L'installazione è costruita con:         |
+---------------------------------+------------------------------------------+
| `Zeroincombenze Tools <https://zeroincombenze-tools.readthedocs.io/>`__ |
+---------------------------------+------------------------------------------+
| Suggested deployment is:        | Posizione suggerita per l'installazione: |
+---------------------------------+------------------------------------------+
| $HOME/10.0 |
+----------------------------------------------------------------------------+

::

    # Odoo repository installation; OCB repository must be installed
    deploy_odoo clone -r l10n-italy-supplemental -b 10.0 -G zero -p $HOME/10.0
    # Upgrade virtual environment
    vem amend $HOME/10.0/venv_odoo



Upgrade | Aggiornamento
-----------------------

::

    deploy_odoo update -r l10n-italy-supplemental -b 10.0 -G zero -p $HOME/10.0
    vem amend $HOME/10.0/venv_odoo
    # Adjust following statements as per your system
    sudo systemctl restart odoo



Support | Supporto
------------------

|Zeroincombenze| This module is supported by the `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__



Get involved | Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/zeroincombenze/l10n-italy-supplemental/issues>`_.

In case of trouble, please check there if your issue has already been reported.



Proposals for enhancement
-------------------------

|en| If you have a proposal to change this module, you may want to send an email to <cc@shs-av.com> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.

|it| Se hai proposte per migliorare questo modulo, puoi inviare una mail a <cc@shs-av.com> per un iniziale contatto.



ChangeLog History | Cronologia modifiche
----------------------------------------

10.0.0.2.33 (2025-07-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Requested date in sale order line (requires sale_order_line_date)
* [QUA] Test coverage 80% (524: 106+418) [13 TestPoints] - quality rating 47 (target 100)

10.0.0.2.32 (2024-02-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Picking: no delivery note / No note consegna in prelievo
* [QUA] Test coverage 39% (650: 395+255)

10.0.0.2.31 (2024-02-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Picking: net weight, delivery note / Peso netto, note consegna in prelievo
* [QUA] Test coverage 39% (650: 395+255)

10.0.0.2.30 (2024-02-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] New custom report picking / Nuova stampa prelievo personalizzato
* [QUA] Test coverage 39% (650: 395+255)

10.0.0.2.29 (2024-01-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] New custom report picking slip
* [QUA] Test coverage 39% (650: 395+255)

10.0.0.2.29 (2024-01-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Sometimes, some random reports fall in crash
* [FIX] Purchase order, sometime status was not recognized
* [IMP] New custom report delivery slip
* [QUA] Test coverage 39% (650: 395+255)



Credits | Ringraziamenti
========================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


Authors | Autori
----------------

* `SHS-AV s.r.l. <https://www.zeroincombenze.it>`__



Contributors | Partecipanti
---------------------------

* `Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>`__



Maintainer | Manutenzione
-------------------------

* `Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>`__



----------------

|en| **zeroincombenze®** is a trademark of `SHS-AV s.r.l. <https://www.shs-av.com/>`__
which distributes and promotes ready-to-use **Odoo** on own cloud infrastructure.
`Zeroincombenze® distribution of Odoo <https://www.zeroincombenze.it/>`__
is mainly designed to cover Italian law and markeplace.

|it| **zeroincombenze®** è un marchio registrato da `SHS-AV s.r.l. <https://www.shs-av.com/>`__
che distribuisce e promuove **Odoo** pronto all'uso sulla propria infrastuttura.
La distribuzione `Zeroincombenze® <https://www.zeroincombenze.it/>`__ è progettata per le esigenze del mercato italiano.


|
|

This module is part of l10n-italy-supplemental project.

Last Update / Ultimo aggiornamento: 2025-07-14

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-black.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Try Me| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-10.svg
    :target: https://erp10.zeroincombenze.it
    :alt: Try Me
.. |Zeroincombenze| image:: https://avatars0.githubusercontent.com/u/6972555?s=460&v=4
   :target: https://www.zeroincombenze.it/
   :alt: Zeroincombenze
.. |en| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/en_US.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |it| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/it_IT.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/check.png
.. |no_check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/no_check.png
.. |menu| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/menu.png
.. |right_do| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/right_do.png
.. |exclamation| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/exclamation.png
.. |warning| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/warning.png
.. |same| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/same.png
.. |late| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/late.png
.. |halt| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/halt.png
.. |info| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/info.png
.. |xml_schema| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/iso/icons/xml-schema.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/iso/scope/xml-schema.md
.. |DesktopTelematico| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/DesktopTelematico.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/Desktoptelematico.md
.. |FatturaPA| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/fatturapa.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/fatturapa.md
