
=============================================
|Zeroincombenze| l10n-italy-supplemental 12.0
=============================================
|Build Status| |Codecov Status| |license gpl| |Try Me|


.. contents::



Overview / Panoramica
=====================

|en| 

|it| N/D
Avaiable Addons / Moduli disponibili
------------------------------------

+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| Name / Nome                    | Version    | OCA Ver.   | Description / Descrizione                                                        |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| account_export                 | 12.0.10.0. | |no_check| | Export account moves                                                             |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| account_gopher                 | 12.0.10.0. | |no_check| | Configure account records                                                        |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| account_invoice_add_sale_order | 12.0.10.0. | |no_check| | Add sale order to sale account invoice                                           |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| account_invoice_import_xlsx    | 12.0.10.0. | |no_check| | Import invoice lines from Excel file                                             |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| account_invoice_last_number    | |halt|     | |no_check| | Decrement invoice sequence if unlink last invoice                                |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| account_invoice_line_report    | 12.0.10.0. | |no_check| | New views to manage invoice lines information                                    |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| account_invoice_line_view      | 12.0.10.0. | |no_check| | Adds Invoice Line menu items                                                     |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| account_invoice_renum_lines    | 12.0.10.0. | |no_check| | Sort invoice lines by sale order, DdT, sequence, id                              |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| import_account_opening         | 12.0.10.0. | |no_check| | Import account opening                                                           |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| purchase_order_line_form       | 12.0.8.0.0 | |no_check| | Purchase Order lines easy editor                                                 |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| refocus_report                 | 12.0.10.0. | |no_check| | Customized report for Refocus                                                    |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| sale_import_xlsx               | 12.0.10.0. | |no_check| | Import sale order lines from a Excel                                             |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| sale_resellers                 | 12.0.10.0. | |no_check| | Manage Sale Resellers                                                            |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| sequence_recovery_last         | 12.0.10.0. | |no_check| | Sequence Recovery                                                                |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| status_widget                  | 12.0.10.0. | |no_check| | Status Widget                                                                    |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+
| vg7_report                     | |halt|     | |no_check| | Customized report for VG7                                                        |
+--------------------------------+------------+------------+----------------------------------------------------------------------------------+



OCA comparation / Confronto con OCA
-----------------------------------


+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Description / Descrizione                                       | Zeroincombenze    | OCA            | Notes / Note                   |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Coverage / Copertura test                                       |  |Codecov Status| | |OCA Codecov|  |                                |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+



Getting started / Come iniziare
===============================

|Try Me|


Prerequisites / Prerequisiti
----------------------------


* python 3.7+
* postgresql 9.6+ (experimental 10.0+)


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
| `Zeroincombenze Tools <https://zeroincombenze-tools.readthedocs.io/>`__    |
+---------------------------------+------------------------------------------+
| Suggested deployment is:        | Posizione suggerita per l'installazione: |
+---------------------------------+------------------------------------------+
| $HOME/12.0                                                                 |
+----------------------------------------------------------------------------+

::

    cd $HOME
    # *** Tools installation & activation ***
    # Case 1: you have not installed zeroincombenze tools
    git clone https://github.com/zeroincombenze/tools.git
    cd $HOME/tools
    ./install_tools.sh -p
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -U
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository installation; OCB repository must be installed
    odoo_install_repository l10n-italy-supplemental -b 12.0 -O zero -o $HOME/12.0
    vem create $HOME/12.0/venv_odoo -O 12.0 -a "*" -DI -o $HOME/12.0



Upgrade / Aggiornamento
-----------------------


::

    cd $HOME
    # *** Tools installation & activation ***
    # Case 1: you have not installed zeroincombenze tools
    git clone https://github.com/zeroincombenze/tools.git
    cd $HOME/tools
    ./install_tools.sh -p
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -U
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository upgrade
    odoo_install_repository l10n-italy-supplemental -b 12.0 -o $HOME/12.0 -U
    vem amend $HOME/12.0/venv_odoo -o $HOME/12.0
    # Adjust following statements as per your system
    sudo systemctl restart odoo


Support / Supporto
------------------


|Zeroincombenze| This project is mainly maintained by the `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__




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


History / Cronologia
--------------------

account_gopher: 10.0.0.2.0 (2022-02-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Menu visible for account manager / Meù visibile di manager di contabilità
* [IMP] New function Reload taxes / Nuova funzione ricarica tasse
* [IMP] New function Reload CoA / Nuova funzione ricarica PdC


import_account_opening: 10.0.0.1.7 (2022-02-03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Missed some error message / In alcuni casi non si vedevamo i messaggi di errore


import_account_opening: 10.0.0.1.6 (2022-01-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Search partner by fiscal code o only name / Riceca clienti o fornitori per codice fiscale o solo nome


account_invoice_line_view: 10.0.1.0.4 (2022-01-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] ValueError: field `number` does not exist / ValueError: Il campo `number` non esiste

import_account_opening: 10.0.0.1.5 (2022-01-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Parter account from Excel file /Conto cliente/fornitore da file Excel
* [FIX] No empty entry when dry-run / No testata vuota di registrazione contabile se simulazione


import_account_opening: 10.0.0.1.4 (2021-12-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Supplier account


import_account_opening: 10.0.0.1.3 (2021-12-23)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Search like name too / Ricerca anche con nome simile
* [IMP] Search just contact / Ricerca solo contatti
* [IMP] Dry-run / Esecuzione di prova


account_gopher: 10.0.0.1.0 (2021-12-23)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Minor enhancements


import_account_opening: 10.0.0.1.0 (2021-12-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Draft code / Bozza iniziale


sale_import_xlsx: 10.0.0.0.0 (2021-11-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] First version


account_invoice_import_xlsx: 10.0.0.0.0 (2021-11-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] First version


account_gopher: 10.0.0.0.0 (2021-11-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] First version





Credits / Didascalie
====================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


----------------


|en| **zeroincombenze®** is a trademark of `SHS-AV s.r.l. <https://www.shs-av.com/>`__
which distributes and promotes ready-to-use **Odoo** on own cloud infrastructure.
`Zeroincombenze® distribution of Odoo <https://wiki.zeroincombenze.org/en/Odoo>`__
is mainly designed to cover Italian law and markeplace.

|it| **zeroincombenze®** è un marchio registrato da `SHS-AV s.r.l. <https://www.shs-av.com/>`__
che distribuisce e promuove **Odoo** pronto all'uso sulla propria infrastuttura.
La distribuzione `Zeroincombenze® <https://wiki.zeroincombenze.org/en/Odoo>`__ è progettata per le esigenze del mercato italiano.



|chat_with_us|


|


Last Update / Ultimo aggiornamento: 2022-02-07

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-red.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |Build Status| image:: https://travis-ci.org/zeroincombenze/l10n-italy-supplemental.svg?branch=12.0
    :target: https://travis-ci.com/zeroincombenze/l10n-italy-supplemental
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/zeroincombenze/l10n-italy-supplemental/badge.svg?branch=12.0
    :target: https://coveralls.io/github/zeroincombenze/l10n-italy-supplemental?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/zeroincombenze/l10n-italy-supplemental/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/zeroincombenze/l10n-italy-supplemental/branch/12.0
    :alt: Codecov
.. |Tech Doc| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-docs-12.svg
    :target: https://wiki.zeroincombenze.org/en/Odoo/12.0/dev
    :alt: Technical Documentation
.. |Help| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-help-12.svg
    :target: https://wiki.zeroincombenze.org/it/Odoo/12.0/man
    :alt: Technical Documentation
.. |Try Me| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-12.svg
    :target: https://erp12.zeroincombenze.it
    :alt: Try Me
.. |OCA Codecov| image:: https://codecov.io/gh/OCA/l10n-italy-supplemental/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/OCA/l10n-italy-supplemental/branch/12.0
    :alt: Codecov
.. |Odoo Italia Associazione| image:: https://www.odoo-italia.org/images/Immagini/Odoo%20Italia%20-%20126x56.png
   :target: https://odoo-italia.org
   :alt: Odoo Italia Associazione
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
.. |chat_with_us| image:: https://www.shs-av.com/wp-content/chat_with_us.gif
   :target: https://t.me/Assitenza_clienti_powERP


