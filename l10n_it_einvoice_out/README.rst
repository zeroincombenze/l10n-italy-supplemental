=============================================================================================
|icon| Italian Localization - FatturaPA - Emissione/Emissione fattura elettronica 10.0.1.0.31
=============================================================================================

**E-Invoice emission**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/l10n_it_einvoice_out/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| This module allows you to generate the fatturaPA XML file version 1.2.1
which will be sent to the SdI (Exchange System by Italian Tax Authority)

`Italian e-invoice laws <https://www.agenziaentrate.gov.it/portale/normativa-prassi-e-regole-tecniche-fatture-elettroniche>`__

|warning| Read carefully note of module *l10n_it_einvoice_base* before install this module


|it| Questo modulo permette di generare il file xml della fatturaPA versione 1.2.1
da trasmettere al sistema di interscambio SdI.


Destinatari
~~~~~~~~~~~

Il modulo è destinato a tutte le aziende che dal 2019 emettono fattura elettronica

Normativa
~~~~~~~~~

Le leggi inerenti la fattura elettronica sono numerose. Potete consultare
la `normativa fattura elettronica <https://www.agenziaentrate.gov.it/portale/normativa-prassi-e-regole-tecniche-fatture-elettroniche>`__

Per maggiori info leggere le informazioni relative al modulo *l10n_it_einvoice_base*


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/l10n_it_einvoice_out/static/description/description.png


Features | Caratteristiche
--------------------------

+--------------------------------------+----------+----------------------------------------------+
| Feature / Funzione                   |  Status  | Notes / Note                                 |
+--------------------------------------+----------+----------------------------------------------+
| Emissione FatturaPA                  | |check|  | Genera file .xml versione 1.2.1              |
+--------------------------------------+----------+----------------------------------------------+
| Emissione Fattura B2B                | |check|  | Genera file .xml versione 1.2.1              |
+--------------------------------------+----------+----------------------------------------------+
| Emissione Fattura a privato senza PI | |check|  | Genera file .xml versione 1.2.1              |
+--------------------------------------+----------+----------------------------------------------+
| E-fattura a rappresentante fiscale   | |check|  | Genera file .xml versione 1.2.1              |
+--------------------------------------+----------+----------------------------------------------+
| E-fattura a stabile organizzazione   | |check|  | Genera file .xml versione 1.2.1              |
+--------------------------------------+----------+----------------------------------------------+
| Dati azienda da fattura              | |check|  |                                              |
+--------------------------------------+----------+----------------------------------------------+
| Controllo dati durante inserimento   | |check|  |                                              |
+--------------------------------------+----------+----------------------------------------------+



Certifications | Certificazioni
-------------------------------

+----------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------------+----------------------------------------------+
| Logo                 | Ente/Certificato                                                                                                                                                                                                  | Data inizio   | Da fine      | Note                                         |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------------+----------------------------------------------+
| |xml\_schema|        | `ISO + Agenzia delle Entrate <http://www.agenziaentrate.gov.it/wps/content/Nsilib/Nsi/Strumenti/Specifiche+tecniche/Specifiche+tecniche+comunicazioni/Fatture+e+corrispettivi+ST/>`__                             | 01-06-2017    | 31-12-2025   | Validazione contro schema xml                |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------------+----------------------------------------------+
| |FatturaPA|          | `FatturaPA <https://www.agenziaentrate.gov.it/wps/content/Nsilib/Nsi/Schede/Comunicazioni/Fatture+e+corrispettivi/Fatture+e+corrispettivi+ST/ST+invio+di+fatturazione+elettronica/?page=schedecomunicazioni/>`__  | 01-06-2017    | 31-12-2025   | Controllo tramite sito Agenzia delle Entrate |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------------+----------------------------------------------+



Configuration | Configurazione
------------------------------

☰  Configuration > Configuration > Invoicing > Fattura PA

☰  Invoicing > Configuration > Tax > Tax > Set Nature

☰  Invoicing > Configuration > Management > Payment Terms

☰  Invoicing > Customers > Customers > Set data

☰  Invoicing > Configuration > Invoicing > Fiscal Positions

Read only:

☰  Invoicing > Configuration > Invoicing > IRS definition > Tax natue

☰  Invoicing > Configuration > Invoicing > IRS definition > Invoice type



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

10.0.1.0.31 (2025-11-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Riconoscimento auto-fattura da tipo documento fiscale
* [QUA] Test coverage 64% (777: 279+498) [87 TestPoints] - quality rating 48 (target 100)

10.0.1.0.30 (2025-10-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Segnalazione immediata di cliente non soggetto a fattura elettronica
* [QUA] Test coverage 64% (777: 279+498) [87 TestPoints] - quality rating 48 (target 100)

10.0.1.0.29 (2024-11-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Predispozione emisisone ritenuta d'acconto (richiede modulo supplementare)
* [QUA] Test coverage 64% (776: 279+497) [87 TestPoints] - quality rating 57 (target 100)

10.0.1.0.28 (2024-06-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] SP Refund / Nota credito SP
* [QUA] Test coverage 64% (767: 279+488) [87 TestPoints] - quality rating 57 (target 100)

10.0.1.0.27 (2024-02-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Self e-invoice management - Emissione auto-fatture
* [QUA] Test coverage 64% (762: 276+486) [87 TestPoints] - quality rating 57 (target 100)



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



Acknowledges | Riconoscimenti
-----------------------------

* `Agile Business Group sagl <https://www.agilebg.com>`__
* `Innoviu Srl <http://www.innoviu.com>`__
* `Odoo Italia Network <https://www.odoo-italia.net>`__
* `Davide Corio <davide.corio@agilebg.com>`__
* `Roberto Onnis <roberto.onnis@innoviu.com>`__
* `Lorenzo Battistini <lorenzo.battistini@agilebg.com>`__
* `Alessio Gerace <alessio.gerace@agilebg.com>`__



Translations by | Traduzioni a cura di
--------------------------------------

* `Sergio Zanchetta <https://github.com/primes2h>`__
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

Last Update / Ultimo aggiornamento: 2025-11-13

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
