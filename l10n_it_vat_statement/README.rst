
==================================================
|icon| ITA - Liquidazione IVA evoluta 12.0.1.9.1_2
==================================================


**Allow to create the "VAT Statement".**

.. |icon| image:: https://raw.githubusercontent.com/PowERP-cloud/l10n-italy/12.0/l10n_it_vat_statement/static/description/icon.png

|Maturity| |Build Status| |license opl|


.. contents::



Overview / Panoramica
=====================

|en| This module evaluates VAT to pay (or on credit).

Previous debit or credit amount is read from previous VAT statement, according
to its payments status.


|

|it| Versamento Iva periodica

::

    Cosa è:

Modulo per calcolare l'importo IVA da pagare (o a credito) sia per i contribuenti
mensili che trimestrali.
L'importo del versamento deve essere dichiarato per via telemativa con il modello F24 (non gestito da questo modulo).

L'IVA è calcolata dalle registrazioni contabili inerenti i registri IVA.
Inoltre viene sottratto l’eventuale credito d’imposta del periodo precedente (o l’eventuale debito inferiore a 25,82€).
Il risultato finale delle operazioni può essere un importo:

    * debito, da versare all'erario, se pari o superiore a 25,82 euro (altrimenti si riporta in aumento per il periodo successivo)
    * credito, da computare in detrazione nel periodo successivo.

L'IVA è determinata dalla data di applicazione dell'IVA, se installato il modulo account_invoice_entry_dates

::

    Destinatari:

Tutti i soggetti passivi IVA in regime non forfettario

::

    Normativa e prassi:

* `Articolo 23 del  DPR n. 633/72 - Registrazione fatture emesse <https://www.gazzettaufficiale.it/eli/id/1972/11/11/072U0633/sg>`__
* `Articolo 25 del  DPR n. 633/72 - Registrazione fatture degli acquisti <https://www.gazzettaufficiale.it/eli/id/1972/11/11/072U0633/sg>`__
* Articolo 39 del DPR n. 633/72 - Della tenuta e conservazione dei registri

Normativa non supportata da questo software:

* Articolo 24 del DPR n. 633/72) - Registrazione dei corrispettivi


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
    odoo_install_repository l10n-italy -b 12.0 -O powerp -o $HOME/12.0
    vem create $HOME/12.0/venv_odoo -O 12.0 -a "*" -DI -o $HOME/12.0

From UI: go to:

* |menu| Setting > Activate Developer mode 
* |menu| Apps > Update Apps List
* |menu| Setting > Apps |right_do| Select **l10n_it_vat_statement** > Install


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
    odoo_install_repository l10n-italy -b 12.0 -o $HOME/12.0 -U
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
<https://github.com/PowERP-cloud/l10n-italy/issues>`_.

In case of trouble, please check there if your issue has already been reported.

Proposals for enhancement
-------------------------


If you have a proposal to change this module, you may want to send an email to <info@powerp.it> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.


ChangeLog History / Cronologia modifiche
----------------------------------------

12.0.1.9.1_2 (2021-12-27)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Inserito migrations per aggiornamento valori pregressi

12.0.1.9.1_1 (2021-12-24)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring campi per liquidazioine EU-OSS

12.0.1.9.1 (2021-10-01)
~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring campo date_apply_vat rimosso e spostato in modulo common

12.0.1.9.0 (2021-09-30)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Refactoring funzione di calcolo delle tasse (spostata in apposito modulo l10n_it_vat_common)

12.0.1.8.13 (2021-09-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimozione statement_credit_group_line da it.po perchè impediva caricamento della lingua IT

12.0.1.8.12 (2021-09-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato stampa liquidazione e fix bugs

12.0.1.8.11 (2021-09-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato filtro per i movimenti contabili dell'iva

12.0.1.8.10 (2021-09-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Inserito i totali nella visualizzazione e nella stampa

12.0.1.8.9 (2021-09-08)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto il comportamento con i codici iva di EU OSS

12.0.1.8.8 (2021-07-22)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato il model delle righe tasse di debito con campo deducibile

12.0.1.8.7 (2021-07-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato il model delle righe tasse di debito con campo deducibile

12.0.1.8.6 (2021-07-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato il template



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
* Marco Tosato <marco.tosato@didotech.com>
* Fabio Giovannelli <fabio.giovannelli@didotech.com>


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

This module is part of l10n-italy project.

Last Update / Ultimo aggiornamento: 2021-12-27

.. |Maturity| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |Build Status| image:: https://travis-ci.org/PowERP-cloud/l10n-italy.svg?branch=12.0
    :target: https://travis-ci.com/PowERP-cloud/l10n-italy
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/PowERP-cloud/l10n-italy/badge.svg?branch=12.0
    :target: https://coveralls.io/github/PowERP-cloud/l10n-italy?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/PowERP-cloud/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/PowERP-cloud/l10n-italy/branch/12.0
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
.. |OCA Codecov| image:: https://codecov.io/gh/OCA/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/OCA/l10n-italy/branch/12.0
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

