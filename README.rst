=============================================
|Zeroincombenze| l10n-italy-supplemental 10.0
=============================================

.. contents::



Overview / Panoramica
=====================

|en| Italian supplemental Odoo modules.
This repository contains some useful addons, mainly targetted for Italian
marketplace.


|it| Moduli supplementari per localizzazione italiana Odoo.
Questo catalogo contiene moduli utitli, principalmente orientati al mercato italiano.

Avaiable Addons / Moduli disponibili
------------------------------------

+------------------------------------+------------+----------------------------------------------------------------------------------+
| Name / Nome                        | Version    | Description / Descrizione                                                        |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_bank_statement_import_xlsx | 10.0.0.1.0 | Import account bank statement from Excel                                         |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_bank_statement_liquidity   | 10.0.0.1.1 | Liquidity accounts can be reconciled bye bank statement                          |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_counterpart_ref            | 10.0.0.1.0 | Add counterpart reference in journal entries                                     |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_export                     | 10.0.0.1.0 | Export account moves                                                             |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_gopher                     | 10.0.0.2.9 | Configure account records                                                        |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_invoice_add_sale_order     | 10.0.0.1.1 | Add sale order to sale account invoice                                           |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_invoice_import_xlsx        | 10.0.0.2.0 | Import invoice from Excel file                                                   |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_invoice_last_number        | |halt|     | Decrement invoice sequence if unlink last invoice                                |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_invoice_line_report        | 10.0.1.0.0 | New views to manage invoice lines information                                    |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_invoice_line_view          | 10.0.1.0.6 | Adds Invoice Line menu items                                                     |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_invoice_renum_lines        | 10.0.0.1.1 | Sort invoice lines by sale order, DdT, sequence, id                              |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_invoice_search_more        | 10.0.0.1.0 | Search invoices by products and more                                             |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| account_tax_rounded                | 10.0.12.0. | Round taxes to comply italian laws                                               |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| assigned_bank                      | 10.0.0.1.3 | Assign internal bank to customers or supplier                                    |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| calendar_task_link                 | 10.0.0.1.1 | Add project task to calendar event                                               |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| crm_calendar_link                  | 10.0.0.1.0 | Add opportunity link to calendar event                                           |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| import_account_opening             | 10.0.0.1.7 | Import account opening                                                           |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| l10n_it_coa                        | 10.0.0.2.1 | ITA - Fiscal localization by Zeroincombenze(R)                                   |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| l10n_it_coa_minimal                | 10.0.0.1.0 | Italy - Fiscal localization by zeroincombenze(R)                                 |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| microsoft_outlook_z0               | 10.0.1.1   | Microsoft Outlook Outgoing email server                                          |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| partner_bank                       | 10.0.0.3   | Add bank account sheet in partner view like previous Odoo 10.0                   |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| prodotti_espresso                  | 10.0.1.0.6 | Ordini e fatture con prodotti espresso                                           |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| purchase_order_line_form           | 10.0.8.0.0 | Purchase Order lines easy editor                                                 |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| rectify_negative_refund            | 10.0.0.1.1 | User can rectify negative invoice or negative refund                             |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| refocus_report                     | 10.0.0.1.7 | Customized report for Refocus                                                    |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| sale_delivery_state_z0             | 10.0.1.0.0 | Show the delivery state on the sale order                                        |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| sale_import_xlsx                   | 10.0.0.1.1 | Import sale order lines from a Excel                                             |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| sale_plus                          | 10.0.0.1.0 | Operator can full invoice multiple sale orders.                                  |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| sale_resellers                     | 10.0.1.5.4 | Manage Sale Resellers                                                            |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| sequence_recovery_last             | 10.0.0.0.1 | Sequence Recovery                                                                |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| so_convert_po                      | 10.0.0.6.1 | Converting Sale Order to Purchase Order/RFQ with single button click, transfer a |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| status_widget                      | 10.0.1.0.0 | Status Widget                                                                    |
+------------------------------------+------------+----------------------------------------------------------------------------------+
| vg7_report                         | |halt|     | Customized report for VG7                                                        |
+------------------------------------+------------+----------------------------------------------------------------------------------+




Getting started / Come iniziare
===============================

|Try Me|


Prerequisites / Prerequisiti
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


Installation / Installazione
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


Upgrade / Aggiornamento
-----------------------

::

    deploy_odoo update -r l10n-italy-supplemental -b 10.0 -G zero -p $HOME/10.0
    vem amend $HOME/10.0/venv_odoo
    # Adjust following statements as per your system
    sudo systemctl restart odoo


Support / Supporto
------------------

|Zeroincombenze| This project is mainly supported by the `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__



Get involved / Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/zeroincombenze/l10n-italy-supplemental/issues>`_.

In case of trouble, please check there if your issue has already been reported.


Proposals for enhancement
-------------------------

|en| If you have a proposal to change on oh these modules, you may want to send an email to <cc@shs-av.com> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.

|it| Se hai proposte per migliorare uno dei moduli, puoi inviare una mail a <cc@shs-av.com> per un iniziale contatto.


ChangeLog History / Cronologia modifiche
----------------------------------------

account_tax_rounded: 10.0.0.1.0 (2024-06-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] First version
* [QUA] Test coverage 24% (29: 22+7) [0 TestPoints] - quality rating 15 (target 100)


sale_delivery_state_z0: 10.0.0.1.0 (2024-06-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Initial implementation: backport from 12.0
* [QUA] Test coverage 85% (34: 5+29) [0 TestPoints] - quality rating 52 (target 100)

microsoft_outlook_z0: 10.0.0.1.1 (2024-05-29)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Outlook authentication
* [QUA] Test coverage 34% (176: 116+60) [0 TestPoints] - quality rating 21 (target 100)


microsoft_outlook_z0: 10.0.0.1.0 (2024-05-22)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Initial implementation / Implementazione iniziale
* [QUA] Test coverage 34% (176: 116+60) [0 TestPoints] - quality rating 21 (target 100)



account_gopher: 10.0.0.2.9 (2024-03-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Documentation upgrade
* [IMP] New menu reconcile move / Nuovo menù riconciliazione contabile


assigned_bank: 10.0.0.1.3 (2024-03-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornamento documentazione


account_invoice_search_more: 10.0.0.1.0 (2024-01-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Initial implementation / Implementazione iniziale
* [QUA] Test coverage 100% (6: 0+6) [0 TestPoints] - quality rating 61 (target 100)

rectify_negative_refund: 10.0.0.1.1 (2023-11-22)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Recognize negativa self-invoice / Riconosciento auto-fatture negative


rectify_negative_refund: 10.0.0.1.0 (2023-10-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [NEW] Initial implementation
* [QUA] Test coverage 19% (42: 34+8) [0 TestPoints] - quality rating 5 (target 100)

account_counterpart_ref: 10.0.0.1.0 (2023-10-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Initial implementation


l10n_it_coa_minimal: 10.0.0.1.0 (2023-09-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] First release


l10n_it_coa: 10.0.0.2.11 (2023-08-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Duplicate key during installation / Chiave duplicata in installazione
* [FIX] Wrong external name for account.group / Errati identificativi account.group
* [IMP] Module name changed (l10n_it_coa -> l10n_it_coa, only Odoo 10.0)


Credits / Ringraziamenti
========================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


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


Last Update / Ultimo aggiornamento: 2024-06-11

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-red.png
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
