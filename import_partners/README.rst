
========================================
|icon| Import account opening 12.0.0.1.7
========================================


.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/12.0/import_account_opening/static/description/icon.png

|Maturity| |Build Status| |Codecov Status| |license gpl| |Try Me|


.. contents::



Overview / Panoramica
=====================

|en| Account Opening Import
---------------------------

Import account opening from Excel file.

Excel file must have following structure:

+--------+---------------------+---------+-----------+----------------+------+-------+
| Codice | Nome                | Cliente | Fornitore | Partita IVA    | Dare | Avere |
+--------+---------------------+---------+-----------+----------------+------+-------+
|        | Global Trading Ltd  | 1       |           | GB250072348000 | 1000 |       |
+--------+---------------------+---------+-----------+----------------+------+-------+
|        | Rossi e Bianchi srl |         | 1         | IT05111810015  |      | 500   |
+--------+---------------------+---------+-----------+----------------+------+-------+
| 180003 | Banca               |         |           |                | 100  |       |
+--------+---------------------+---------+-----------+----------------+------+-------+



Notes:

* Please, import just xlsx files
* The labels of the header must be exactly as you see above
* Please set 1 in one of "Cliente" or "Fornitore" for partner lines
* Please set only one value in one of "Dare" "Avere"
* Partners search try to find by vat code and name
* In partner lines, account code is set by partner record if not in line
* Ref field is not required; use it if you want load amount by invoice references

You can find Excel example in example directory.

|

|it| Importazione apertura conti
--------------------------------

Importazione apertura conti da file Excel

Il file Excel ha la seguente struttura:

+--------+---------------------+---------+-----------+----------------+------+-------+
| Codice | Nome                | Cliente | Fornitore | Partita IVA    | Dare | Avere |
+--------+---------------------+---------+-----------+----------------+------+-------+
|        | Global Trading Ltd  | 1       |           | GB250072348000 | 1000 |       |
+--------+---------------------+---------+-----------+----------------+------+-------+
|        | Rossi e Bianchi srl |         | 1         | IT05111810015  |      | 500   |
+--------+---------------------+---------+-----------+----------------+------+-------+
| 180003 | Banca               |         |           |                | 100  |       |
+--------+---------------------+---------+-----------+----------------+------+-------+



Note:

* Si possono importare solo file .xlsx
* Le etichette dell'intestazione devono essere rispettate
* Impostare solo cliente o fornitore in ogni riga cliente/fornitore
* Impostare un solo importo tra "Dare" e "Avere"
* Nel caso di clienti/fornitori viene cercato per partita IVA o codice fiscale e nome simile
* Nel caso di clienti/fornitori, il codice conto, se non è inserito, è preso dall'anagrafica
* Il campo Ref è facoltativo; serve se si vuole importare per partite aperte

Si può vedere un esempio nella cartella example.

|

OCA comparation / Confronto con OCA
-----------------------------------


+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Description / Descrizione                                       | Zeroincombenze    | OCA            | Notes / Note                   |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Coverage / Copertura test                                       |  |Codecov Status| | |OCA Codecov|  |                                |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+


|
|

Getting started / Come iniziare
===============================

|Try Me|


|

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

From UI: go to:

* |menu| Setting > Activate Developer mode 
* |menu| Apps > Update Apps List
* |menu| Setting > Apps |right_do| Select **import_account_opening** > Install


|

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

From UI: go to:

|

Support / Supporto
------------------


|Zeroincombenze| This module is maintained by the `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__


|
|

Get involved / Ci mettiamo in gioco
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


ChangeLog History / Cronologia modifiche
----------------------------------------

12.0.0.1.7 (2022-02-03)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Missed some error message / In alcuni casi non si vedevamo i messaggi di errore

12.0.0.1.6 (2022-01-31)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Search partner by fiscal code o only name / Riceca clienti o fornitori per codice fiscale o solo nome

12.0.0.1.5 (2022-01-14)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Parter account from Excel file / Conto cliente/fornitore da file Excel
* [FIX] No empty entry when dry-run / No testata vuota di registrazione contabile se simulazione

12.0.0.1.4 (2021-12-30)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Supplier account

12.0.0.1.3 (2021-12-23)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Search like name too / Ricerca anche con nome simile
* [IMP] Search just contact / Ricerca solo contatti
* [IMP] Dry-run / Esecuzione di prova

12.0.0.1.0 (2021-12-04)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Draft code / Bozza iniziale


|
|

Credits / Didascalie
====================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)



|

Authors / Autori
----------------

* `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__


Contributors / Collaboratori
----------------------------

* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>


Maintainer / Manutenzione
-------------------------




|

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

This module is part of l10n-italy-supplemental project.

Last Update / Ultimo aggiornamento: 2022-02-04

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-black.png
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

