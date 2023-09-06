
======================================
|icon| Account validations 12.0.1.9.30
======================================

**Account validation for Italian Localization**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/12.0/l10n_it_validations/static/description/icon.png


.. contents::



Overview / Panoramica
=====================

|en| Check on account move and invoices.

|

|it| Controlli contabili

Gestione controlli contabili


|

Getting started / Primi passi
=============================

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
    ./install_tools.sh -pT
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -UT
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository installation; OCB repository must be installed
    deploy_odoo clone -r l10n-italy-supplemental -b 12.0 -G zero -p $HOME/12.0
    # Upgrade virtual environment
    vem amend $HOME/12.0/venv_odoo

From UI: go to:

* |menu| Setting > Activate Developer mode
* |menu| Apps > Update Apps List
* |menu| Setting > Apps |right_do| Select **l10n_it_validations** > Install


|

Upgrade / Aggiornamento
-----------------------


::

    cd $HOME
    # *** Tools installation & activation ***
    # Case 1: you have not installed zeroincombenze tools
    git clone https://github.com/zeroincombenze/tools.git
    cd $HOME/tools
    ./install_tools.sh -pT
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -UT
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository upgrade
    deploy_odoo update -r l10n-italy-supplemental -b 12.0 -G zero -p $HOME/12.0
    vem amend $HOME/12.0/venv_odoo
    # Adjust following statements as per your system
    sudo systemctl restart odoo

From UI: go to:

* |menu| Setting > Activate Developer mode
* |menu| Apps > Update Apps List
* |menu| Setting > Apps |right_do| Select **l10n_it_validations** > Update


|

Support / Supporto
------------------


|Zeroincombenze| This module is supported by the `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__


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

12.0.1.9.30 (2023-09-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Ignore partner check on closing records / Controllo nomitavo disabilitato per opearazioni di chiusura/apertura
* [IMP] Removed old code about is_parent flag / Rimosso vecchio codice inutile
* [QUA] Test coverage 25% (423: 317+106) 

12.0.1.9.29 (2023-02-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Validation error on self invoice in prior year / Errata segnalazione di errore per auto-fatture anno preceente

12.0.1.9.28 (2022-09-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Module dependency
* [FIX] Crash rc_self_invoice_id

12.0.1.9.27 (2022-09-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Avoid validation on date when reverse charge invoice self / Gestita validazione della data contabile se ha autofattura

12.0.1.9.27 (2022-07-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Avoid validation on date when reverse charge self from SDI / Gestita validazione della data contabile se autofattura dallo SDI

12.0.1.9.26 (2022-04-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] No set date=date_invoice if rev_charge / Non imposta date=date_invoice in RC

12.0.1.9.24 (2021-10-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimosso controllo data documento se non è fattura o nota di credito

12.0.1.9.24 (2021-06-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Verifica write con anno fiscale assente in validazione

12.0.1.8.23 (2021-03-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Verifica anno fiscale assente in validazione

12.0.1.8.21 (2021-03-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Gestione anno fiscale in write e create

12.0.1.8.20 (2021-03-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato controllo data di registrazione su tipo vendite

12.0.1.8.19 (2021-03-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato controllo data di registrazione su tipo vendite

12.0.1.8.18 (2021-03-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato controllo data fattura fornitore

12.0.1.8.17 (2021-02-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] No check data bilancio

12.0.1.8.16 (2021-02-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Update validation

12.0.1.8.15 (2020-12-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Sostituito campo con _13 e aggiornato dipendenze

12.0.1.8.14 (2020-11-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Campo date_apply_vat spostato in l10n_it_statement

12.0.1.8.13 (2020-11-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Removed checks in date invoice

12.0.1.8.12 (2020-10-27)
~~~~~~~~~~~~~~~~~~~~~~~~
* [FIX] Removed checks in account move

12.0.1.8.11 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~
* [MOD] spostato campo "fiscal_year_id" da modulo "l10n_it_validations" a "account_invoice_entry_dates"
* [FIX] No constraints se stato bozza o annullata

12.0.1.8.10 (2020-10-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] No constraints se stato bozza o annullata

12.0.1.8.9 (2020-09-29)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimosse definizioni dei campi e commentato controllo su termini di pagamento

12.0.1.8.8 (2020-09-10)
~~~~~~~~~~~~~~~~~~~~~~~

* Patch per validazione fatture: ATTENZIONE Da approfondire

12.0.1.8.8 (2020-09-10)
~~~~~~~~~~~~~~~~~~~~~~~

* Patch per validazione fatture: ATTENZIONE Da approfondire


12.0.1.8.7 (2020-09-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [REF] AXI - 133 Account move lines mandatory / Avviso bloccante per registrazione senza linee


12.0.1.7.7 (2020-09-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI - 133 Account move lines mandatory / Avviso bloccante per registrazione senza linee


12.0.1.6.7 (2020-09-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Invoice date mandatory in view / Data fattura per clenti e fornitori viene resa obbligatoria sulla vista


12.0.1.6.6 (2020-09-01)
~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] modificate etichette dei campi data


12.0.0.6.5 (2020-08-26)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Invoice date mandatory for invoices and credit notes / Data fattura obbligatoria per fatture e note di credito

12.0.0.6.4 (2020-08-26)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] filter on journal / Filtro del registro sul tipo di movimento

12.0.0.6.3 (2020-08-25)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] check partner enabled / Verifica sul conto e messaggio di errore se manca il partner

12.0.0.5.3 (2020-08-21)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] type readonly if account.move has lines / Il campo type è reso readonly se ha almeno una registrazione

12.0.0.4.2 (2020-08-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] AXI-113 Gestito i default e il cambio del tipo

12.0.0.3.2 (2020-08-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Reso obbligatorio il campo "tipo" per account.move / Set field "type" as required for account.move

12.0.0.2.2 (2020-08-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Journal changed by type / Registro aggiornato da tipo documento


12.0.0.2.1 (2020-08-03)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added type file in account move / Aggiunto campo tipo in registrazione contabile
* [IMP] Date invoice naming 13.0


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

* `LibrERP enterprise network <https://www.librerp.it>`__
* `SHS-AV s.r.l. <https://www.zeroincombenze.it>`__
* `Didotech s.r.l. <https://www.didotech.com>`__

Contributors / Contributi da
----------------------------

* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
* Marco Tosato <marco.tosato@didotech.com>
* Fabio Giovannelli <fabio.giovannelli@didotech.com>

Maintainer / Manutenzione
-------------------------

LibrERP enterprise network <https://www.librerp.it>

|

----------------


|en| **zeroincombenze®** is a trademark of `SHS-AV s.r.l. <https://www.shs-av.com/>`__
which distributes and promotes ready-to-use **Odoo** on own cloud infrastructure.
`Zeroincombenze® distribution of Odoo <https://www.zeroincombenze.it/>`__
is mainly designed to cover Italian law and markeplace.

|it| **zeroincombenze®** è un marchio registrato da `SHS-AV s.r.l. <https://www.shs-av.com/>`__
che distribuisce e promuove **Odoo** pronto all'uso sulla propria infrastuttura.
La distribuzione `Zeroincombenze® <https://www.zeroincombenze.it/>`__ è progettata per le esigenze del mercato italiano.


|

This module is part of l10n-italy-supplemental project.

Last Update / Ultimo aggiornamento: 2023-09-06

.. |Maturity| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
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


