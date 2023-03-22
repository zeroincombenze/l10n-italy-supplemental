
=================================
|icon| Iban in stampa 12.0.1.1.33
=================================


**Impostazione iban per la stampa nei documenti**

.. |icon| image:: https://raw.githubusercontent.com/PowERP-cloud/accounting/12.0/l10n_it_iban_in_stampa/static/description/icon.png

|Maturity| |Build Status| |license opl|


.. contents::



Overview / Panoramica
=====================

|en| Accounting bank in invoice and order print


|

|it| Gestione stampa IBAN nei documenti

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
    odoo_install_repository accounting -b 12.0 -O powerp -o $HOME/12.0
    vem create $HOME/12.0/venv_odoo -O 12.0 -a "*" -DI -o $HOME/12.0

From UI: go to:

* |menu| Setting > Activate Developer mode 
* |menu| Apps > Update Apps List
* |menu| Setting > Apps |right_do| Select **l10n_it_iban_in_stampa** > Install


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
    odoo_install_repository accounting -b 12.0 -o $HOME/12.0 -U
    vem amend $HOME/12.0/venv_odoo -o $HOME/12.0
    # Adjust following statements as per your system
    sudo systemctl restart odoo

From UI: go to:

|

Support / Supporto
------------------


This module is maintained by the / Questo modulo è mantenuto dalla rete di imprese `Powerp <http://www.powerp.it/>`__

Developer companies are / I soci sviluppatori sono:

* `Didotech s.r.l. <http://www.didotech.com>`__
* `SHS-AV s.r.l. <https://www.shs-av.com/>`__


|
|

Get involved / Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/PowERP-cloud/accounting/issues>`_.

In case of trouble, please check there if your issue has already been reported.

Proposals for enhancement
-------------------------


If you have a proposal to change this module, you may want to send an email to <info@powerp.it> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.


ChangeLog History / Cronologia modifiche
----------------------------------------

12.0.1.1.33 (2022-03-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto bug su vista registrazioni contabili (campo mancante)

12.0.1.1.32 (2022-01-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato le viste per fatture e registrazioni

12.0.1.1.31 (2022-01-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Refactoring del mixin documenti e impostato mixin base in l10n-italy

12.0.1.1.30 (2022-01-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Esclusi conti di portafoglio nel campo conto aziendale

12.0.1.1.29 (2021-12-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Esposto campo IBAN azienda sempre modificabile

12.0.1.1.28 (2021-09-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] correzione vista account.move per nascondere selettivamente i campi IBAN azienda e IBAN controparte
* [FIX] corretto campo utilizzato per determinare tipo di account.move

12.0.1.1.27 (2021-09-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] gestione copia dei campi relativi all'IBAN quando viene duplicato un documento
* [FIX] corretto errore in "account_move_view.xml" in cui veniva utilizzato il campo move_type di move_type invece del campo type

12.0.1.1.26 (2021-09-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto errore di battitura in purchase_order.py

12.0.1.1.25 (2021-09-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] eliminata derivazione di ResPartnerBank da OrderMixin in quanto errata

12.0.1.1.24 (2021-09-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] eliminata "assertion False" se documento passato ai metodi di "engine" non è ne di tipo cliente (fattura cliente o sale order) ne di tipo fornitore (fattura fornitore o purchase order) perchè le account.move possono essere di tipo diverso

12.0.1.1.23 (2021-09-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] aggiunta possibilità di configurare quali banche faranno parte di quelle di default da stampare se "Tipo stampa IBAN" = "Azienda" e "Banca aziendale" non ha valore.
* [FIX] corretto errore in stampa Ordini di Vendita, spostato campo bank_2_print nel mixin base in modo che sia disponibile anche per gli ordini

12.0.1.1.22 (2021-09-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] stampa di tutti gli IBAN dei conti correnti aziendali se bank_2_print_selector assume il valore “company” e il campo company_bank_id non è valorizzato (fattura, ordine di vendita, ordine di acquisto)
* [FIX] aggiunti codici di pagamento mancanti nell'algoritmo di calcolo del tipo di IBAN da utilizzare
* [FIX] rimosso "ensure_one()" da metodi in cui non era necessario in favore di ciclo "for" sugli elementi di contenuti nel recordset "self"
* [IMP] aggiunta campo bank_4_xml in account.invoice e account.move per calcolo del campo da utilizzare nella generazione dell'XML della fattura



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

* `powERP <https://www.powerp.it>`__
* `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__
* `Didotech s.r.l. <https://www.didotech.com>`__


Contributors / Collaboratori
----------------------------

* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
* Fabio Giovannelli <fabio.giovannelli@didotech.com>
* Marco Tosato <marco.tosato@didotech.com>


Maintainer / Manutenzione
-------------------------


This module is maintained by the / Questo modulo è mantenuto dalla rete di imprese Powerp <http://www.powerp.it/>
Developer companies are / I soci sviluppatori sono:
* Didotech s.r.l. <http://www.didotech.com>
* SHS-AV s.r.l. <https://www.shs-av.com/>


|

----------------


|en| **Powerp** is an Italian enterprises network, whose mission is to develop high-level addons designed for Italian enterprise companies.

`Powerp <http://www.powerp.it/>`__ code adds new enhanced features to Italian localization and it released under `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ or `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__ licenses.

|it| `Powerp <http://www.powerp.it/>`__ è una rete di imprese italiane, nata con la missione di sviluppare moduli per le PMI.

Il codice di `Powerp <http://www.powerp.it/>`__ aggiunge caratteristiche evolute alla localizzazione italiana; il codice è rilasciato con licenze `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ e `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__

I soci fondatori sono:

* `Didotech s.r.l. <http://www.didotech.com>`__
* `SHS-AV s.r.l. <https://www.shs-av.com/>`__
* `Xplain s.r.l. <http://x-plain.it//>`__



|chat_with_us|


|

This module is part of accounting project.

Last Update / Ultimo aggiornamento: 2022-03-08

.. |Maturity| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |Build Status| image:: https://travis-ci.org/PowERP-cloud/accounting.svg?branch=12.0
    :target: https://travis-ci.com/PowERP-cloud/accounting
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/PowERP-cloud/accounting/badge.svg?branch=12.0
    :target: https://coveralls.io/github/PowERP-cloud/accounting?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/PowERP-cloud/accounting/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/PowERP-cloud/accounting/branch/12.0
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
.. |OCA Codecov| image:: https://codecov.io/gh/OCA/accounting/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/OCA/accounting/branch/12.0
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

