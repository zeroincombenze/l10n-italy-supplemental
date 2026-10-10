========================================================
|icon| IPA Code (IndicePA)/l10n_it_fiscal_ipa 10.0.1.1.2
========================================================

**IPA Code and Destination Code in Partner Record**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy/10.0/l10n_it_fiscal_ipa/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| This module adds IPA (IndicePA) code and Recipient Code fields to partner,
used by Italian Electronic Invoice.

http://www.indicepa.gov.it


|it| Questo modulo permette l'inserimento del codice IPA (IndicePA) e del Codice Destinatario
nell'anagrafica cliente.

Questi dati sono indispensabili per la gestione della Fattura Elettronica B2B e
per la FatturaPA.

http://www.indicepa.gov.it


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy/10.0/l10n_it_fiscal_ipa/static/description/


Features | Caratteristiche
--------------------------

Features / Funzioni
-------------------

+-------------------------------------------------+----------+----------------------------------------------+
| Feature / Funzione                              |  Status  | Notes / Note                                 |
+-------------------------------------------------+----------+----------------------------------------------+
| Parter: IPA Code / Codice IPA                   | |check|  | Per FatturaPA                                |
+-------------------------------------------------+----------+----------------------------------------------+
| Partner: Recipient Code / Codice Destinatario   | |check|  | EInvoice / Per Fattura Elettronica B2B       |
+-------------------------------------------------+----------+----------------------------------------------+



OCA comparation | Confronto con OCA
-----------------------------------

+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| Description / Descrizione            | Odoo Italia                   | OCA               | Notes / Note                   |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| Validation checks / Validazioni      | |check|                       | |no_check|        |                                |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| Partner view / Vista cliente         | This Module                   | This Module       | Different layout               |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| IPA Code                             | This Module                   | This Module       |                                |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| Recipient Code / Codice Destinatario | This Module                   | l10n_it_fatturapa | |warning| Different deployment |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| Is PA / Pubbblica Amministrazione?   | This Module                   | l10n_it_fatturapa | |warning| Different deployment |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| EInvoice / Soggetto Fattura E.       | This Module                   | l10n_it_fatturapa | |warning| Different deployment |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| EORI Code / Codice EORI              | This Module                   | l10n_it_fatturapa | |warning| Different deployment |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| License Code / Codice Licenza        | This Module                   | l10n_it_fatturapa | |warning| Different deployment |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+
| PEC                                  | PEC destinatario o PEC legale | PEC destinatario  | |warning| Different deployment |
+--------------------------------------+-------------------------------+-------------------+--------------------------------+



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
    deploy_odoo clone -r l10n-italy -b 10.0 -G zero -p $HOME/10.0
    # Upgrade virtual environment
    vem amend $HOME/10.0/venv_odoo



Upgrade | Aggiornamento
-----------------------

::

    deploy_odoo update -r l10n-italy -b 10.0 -G zero -p $HOME/10.0
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
<https://github.com/zeroincombenze/l10n-italy/issues>`_.

In case of trouble, please check there if your issue has already been reported.



Proposals for enhancement
-------------------------

|en| If you have a proposal to change this module, you may want to send an email to <cc@shs-av.com> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.

|it| Se hai proposte per migliorare questo modulo, puoi inviare una mail a <cc@shs-av.com> per un iniziale contatto.



ChangeLog History | Cronologia modifiche
----------------------------------------

10.0.1.1.2 (2022-06-08)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Account Reference / Riferimento amministrativo

10.0.1.1.1 (2019-09-26)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Foreign customer w/o vat / I clienti esteri senza P.IVA ne CF se cod.destinatario = 'XXXXXXX'



Credits | Ringraziamenti
========================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


Authors | Autori
----------------

* `KTec S.r.l. <https://www.ktec.it>`__
* `Odoo Community Association (OCA) <https://odoo-community.org>`__
* `Associazione Odoo Italia <https://www.odoo-italia.org>`__
* `Agile Business Group sagl <https://www.agilebg.com>`__
* `SHS-AV s.r.l. <https://www.zeroincombenze.it>`__



Contributors | Partecipanti
---------------------------

* `Luigi Di Naro <luigi.dinaro@ktec.it>`__
* `Alex Comba <alex.comba@agilebg.com>`__
* `Lorenzo Battistini <lorenzo.battistini@agilebg.com>`__
* `Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>`__
* Translations by / Traduzioni a cura di <False>
* -------------------------------------- <False>
* `Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>`__



Translations by | Traduzioni a cura di
--------------------------------------

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

This module is part of l10n-italy project.

Last Update / Ultimo aggiornamento: 2024-06-06

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
