======================================================================================
|icon| Account Banking Sepa Direct Debit ITA/SEPA Direct Debit CBI (Italia) 18.0.1.0.0
======================================================================================

**SEPA Direct Debit CBI file (Italy) for payment orders**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/18.0/account_banking_sepa_direct_debit_ita/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| Italian banks accept SEPA Direct Debit collections in the CBI format
(``CBISDDReqLogMsg``) instead of the standard ISO 20022 pain.008 file.
This module adds two payment methods to the OCA payment orders:

* **Sepa Direct Debit CORE ITA-CBI**: debits to consumers (CORE scheme)
* **Sepa Direct Debit B2B ITA-CBI**: debits to businesses (B2B scheme)

A debit payment order using one of these methods generates the CBI file,
ready to be uploaded to the home banking.

The file is created by the Python library ``fintech``.


|it| Le banche italiane accettano gli incassi SEPA Direct Debit nel formato CBI
(``CBISDDReqLogMsg``) invece del file standard ISO 20022 pain.008.
Questo modulo aggiunge due metodi di pagamento alle distinte OCA:

* **Sepa Direct Debit CORE ITA-CBI**: addebiti a consumatori (schema CORE)
* **Sepa Direct Debit B2B ITA-CBI**: addebiti a imprese (schema B2B)

Una distinta di incasso con uno di questi metodi genera il file CBI,
pronto per essere caricato sull'home banking.

Il file è creato dalla libreria Python ``fintech``.


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/18.0/account_banking_sepa_direct_debit_ita/static/description/


Configuration | Configurazione
------------------------------

* Company: set the **SEPA Creditor Identifier** and the **Initiating Party
  Identifier**, which is the CBI unique code (CUC, 8 letters or digits).
  Both can be overridden on the payment mode.
* Bank journal: add the payment method *Sepa Direct Debit CORE ITA-CBI*
  or *Sepa Direct Debit B2B ITA-CBI* to the incoming payments.
* Payment mode: create a mode with one of the methods above and the bank journal.
* Customer: the bank account needs a valid IBAN and the bank a BIC code;
  create a valid mandate with the same scheme (CORE or B2B) as the method.

If a module providing wallet accounts ("conto di portafoglio") is installed,
the main bank account of the wallet is written in the file as creditor.



Usage | Utilizzo
----------------

* Validate the customer invoices with the SDD CBI payment mode.
* *Accounting › Payments › Debit Orders*: create the order, or use
  [Add to Debit Order] on the invoices.
* Confirm the order and press [Generate Payment File]: the CBI XML file is
  attached to the order.
* Upload the file to the home banking, then press [File Successfully Uploaded].



Getting started | Primi passi
=============================

|Try Me|


Prerequisites | Prerequisiti
----------------------------

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
| $HOME/18.0 |
+----------------------------------------------------------------------------+

::

    # Odoo repository installation; OCB repository must be installed
    deploy_odoo clone -r l10n-italy-supplemental -b 18.0 -G zero -p $HOME/18.0
    # Upgrade virtual environment
    vem amend $HOME/18.0/venv_odoo



Upgrade | Aggiornamento
-----------------------

::

    deploy_odoo update -r l10n-italy-supplemental -b 18.0 -G zero -p $HOME/18.0
    vem amend $HOME/18.0/venv_odoo
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

18.0.1.0.0 (2026-10-26)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Migrated to Odoo 18.0 / Migrazione a Odoo 18.0
* [IMP] Mandate taken from the payment line / Mandato preso dalla riga di pagamento
* [IMP] Creditor id and CUC can be set on the payment mode / Codice creditore e CUC impostabili nel modo di pagamento
* [IMP] No more dependency on account_banking_common and account_banking_fintech_initializer / Non più dipendente da account_banking_common e account_banking_fintech_initializer
* [FIX] CUC code is really validated / Il codice CUC viene effettivamente validato
* [FIX] Missing BIC code is detected / Codice BIC mancante rilevato
* [FIX] Mandate scheme must match the payment method / Lo schema del mandato deve corrispondere al metodo di pagamento
* [IMP] IBAN/BIC country mismatch reported as readable error / Discordanza nazione IBAN/BIC segnalata con errore leggibile

18.0.0
~~~~~~

* [IMP] Initial commit



Credits | Ringraziamenti
========================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


Authors | Autori
----------------

* `Zeroincombenze srls <https://www.zeroincombenze.it>`__
* LibrErp enterprise network and other partners <False>



Contributors | Partecipanti
---------------------------

* `Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>`__
* `Marco Tosato <marco.tosato@didotech.com>`__
* `Fabio Giovannelli <fabio.giovannelli@didotech.com>`__



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

Last Update / Ultimo aggiornamento: 2026-10-26

.. |Maturity| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Try Me| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-18.svg
    :target: https://erp18.zeroincombenze.it
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
