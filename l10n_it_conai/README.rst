==================================================
|icon| CONAI Management/Gestione CONAI 10.0.0.1.15
==================================================

**CONAI data and amount evalutation**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/l10n_it_conai/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| This module manages the `CONAI <https://www.conai.org/> `__ data on sale order and
account invoice and show CONAI statement report to pay fee.


|it| Questo modulo gestisce i dati `CONAI <https://www.conai.org/> `__ su ordini e
fatture e mostra il rendiconto per la liqudazione CONAI da pagare.


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/l10n_it_conai/static/description/description.png


Features | Caratteristiche
--------------------------

+----------------------------------------------------------------------------+----------+------------------------------+
| Description | Descrizione                                                  | Z0incomb | Note(s)                      |
+----------------------------------------------------------------------------+----------+------------------------------+
| CONAI product category | Categorie CONAI prodotto                          | ✅       | Pre-installato, modificabile |
+----------------------------------------------------------------------------+----------+------------------------------+
| CONAI partner category | Categorie CONAI cliente                           | ✅       | Pre-installato, modificabile |
+----------------------------------------------------------------------------+----------+------------------------------+
| CONAI category in product | Categoria principale del prodotto              | ✅       |                              |
+----------------------------------------------------------------------------+----------+------------------------------+
| CONAI 2nd category in product | Seconda categoria del prodotto             | ✅       | Richiede impostazione peso   |
+----------------------------------------------------------------------------+----------+------------------------------+
| CONAI 2nd category weight in product | Peso 2da categoria del prodotto     | ✅       |                              |
+----------------------------------------------------------------------------+----------+------------------------------+
| Automatic CONAI amount evaluation | Calcolo automatico degli importi CONAI | ✅       |                              |
+----------------------------------------------------------------------------+----------+------------------------------+
| Manual CONAI amount update | Modifica manuale degli importi CONAI          | ✅       |                              |
+----------------------------------------------------------------------------+----------+------------------------------+
| CONAI statement | Liquidazione CONAI                                       | ✅       |                              |
+----------------------------------------------------------------------------+----------+------------------------------+



Configuration | Configurazione
------------------------------

In order to manage configuration data, user must have:

☰ Settings > Users > Users > *USER* > [Edit] > Application > Accounting > Adviser

Configuration data:

☰ Invoicing > Configuration > Settings > CONAI product

☰ Invoicing > Configuration > Accounting > CONAI configuration > CONAI product category

☰ Invoicing > Configuration > Accounting > CONAI configuration > CONAI partner category

☰ Invoicing > Sales > Sellable products > *PRODUCT* > [Edit] > CONAI category



Usage | Utilizzo
----------------

Sale orders and account invoices can be created in usual way.
CONAI amounts are evaluated on document validation.
You can update CONAI amount, setting manual flag.

CONAI statement:

☰ Invoicing > Reports > CONAI statements



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

10.0.0.1.15 (2026-03-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Manual weight in sale order / Peso manuale in righe ordini
* [QUA] Test coverage 67% (508: 168+340) [23 TestPoints] - quality rating 43 (target 100)

10.0.0.1.14 (2026-02-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [QUA] Test coverage 67% (508: 168+340) [23 TestPoints] - quality rating 43 (target 100)

10.0.0.1.13 (2025-02-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Product w/o weight / Prodotto senza peso
* [QUA] Test coverage 67% (508: 168+340) [23 TestPoints] - quality rating 48 (target 100)

10.0.0.1.12 (2024-06-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Conai excemtion 100% / Esenzione Conai 100%
* [QUA] Test coverage 67% (508: 168+340) [23 TestPoints] - quality rating 48 (target 100)

10.0.0.1.11 (2024-06-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Check for version of l10n_it_ddt to depend on
* [QUA] Test coverage 67% (505: 166+339) [23 TestPoints] - quality rating 48 (target 100)



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

* Zeroincombenze (R) <False>



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

Last Update / Ultimo aggiornamento: 2026-03-22

.. |Maturity| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
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
