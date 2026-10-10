=======================================================================
|icon| Comunicazione periodica IVA/l10n_it_vat_communication 10.0.0.2.4
=======================================================================

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy/10.0/l10n_it_vat_communication/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| Generate xml file for sending to Agenzia delle Entrate, kwnown as Spesometro.


|it| Gestisce la Comunicazione periodica IVA con l'elenco delle fatture emesse e
ricevute e genera il file da inviare all'Agenzia delle Entrate.
Questo obbligo è conosciuto anche come Spesometro light 2018 e sostistuisce i
precedenti obblighi chiamati Spesometro e Spesometro 2017.

::

    Destinatari:

Tutti i soggetti IVA (con partita IVA)

::

    Normativa e prassi:

* `Art. 21 D.L. n. 78/2010 <https://www.gazzettaufficiale.it/gunewsletter/dettaglio.jsp?service=1&datagu=2010-05-31&task=dettaglio&numgu=125&redaz=010G0101&tmstp=1275551085053>`__
* `Art. 4 D.L. n. 193/2016 <https://www.gazzettaufficiale.it/eli/id/2016/10/24/16G00209/sg>`__
* `Art. 1ter D.L. n. 148/2017 <https://www.gazzettaufficiale.it/eli/id/2017/12/05/17A08254/SG>`__
* `Provvedimenti Agenzia delle entrate del 27 marzo 2017, numero 58793 <https://www.agenziaentrate.gov.it/wps/wcm/connect/4e22d9ab-2bbd-4e3f-9e60-a9a8cbf70232/PROVVEDIMENTO+PROT.+58793+DEL+27+MARZO+2017.pdf?MOD=AJPERES&CACHEID=4e22d9ab-2bbd-4e3f-9e60-a9a8cbf70232>`__
* `Info Agenzia delle Entrate <https://www.agenziaentrate.gov.it/wps/content/Nsilib/Nsi/Schede/Comunicazioni/Dati+Fatture+%28c.d.+nuovo+spesometro%29/Scheda+informativa+Dati+Fatture+c.d.+nuovo+spesometro/?page=schedecomunicazioni>`__

Note fiscali da circolare Agenzia delle Entrate su tipo documento fiscale:

* Le autofatture, per fatture non ricevute dopo 4 mesi, rif. art. 6 c.8 D.Lgs 471/97, (codice TD20) sono inserite nella comunicazione.
* Le autofatture da reverse charge nazionale (codice TD01) non sono inserite nello spesometro. Marcare il registro sezionale come registro con e-fatture.
* Le autofatture da reverse charge estero (codice TD01) non sono inserite nello spesometro. La relativa fattura d'acquisto è inserita nell'"esterometro". Marcare il registro sezionale come registro con e-fatture

|

Il software permette di operare in modalità 2017 per rigenerare eventuali file
in formato 2017. Per eseguire questa funzione, prima di avviare Odoo eseguire
la seguente istruzione:

::

     export SPESOMETRO_VERSION=2.0


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy/10.0/l10n_it_vat_communication/static/description/


Features | Caratteristiche
--------------------------

+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Feature / Funzione                                | Status     | Notes / Note                                                        |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Fatture clienti e fornitori detraibili            | |check|    | Fatture ordinarie                                                   |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Fatture fornitori indetraibili                    | |check|    | Tutte le percentuali di indetraibilità                              |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Fatture a privati senza Partita IVA               | |check|    | Necessario codice fiscale                                           |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Fatture semplificata                              | |check|    | Per clienti senza PI ne CF                                          |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Fatture senza IVA                                 | |check|    | Fatture esenti, NI, escluse, eccetera                               |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Escludi importi Fuori Campo IVA                   | |check|    | Totale fattura in Comunicazione può essere diverso da registrazione |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Controlla CAP e provincia Italia in comunicazione | |check|    | Da nazione, oppure da partita IVA oppure Italia                     |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Converti CF no Italia in comunicazione            | |check|    | Da nazione, oppure da partita IVA oppure Italia                     |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Controlli dati anagrafici                         | |check|    | Controlli Agenzia Entrate                                           |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Conversione utf-8                                 | |check|    | Lo Spesometro 2017 richiedeva ISO-Latin1                            |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| IVA differita                                     | |check|    | Da codice imposte                                                   |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| IVA da split-payment                              | |check|    | Da codice imposte                                                   |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Ignora autofatture                                | |check|    | Esclusione tramite sezionale                                        |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Ignora corrispettivi                              | |check|    | Esclusione tramite sezionale                                        |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Ignora avvisi di parcella                         | |check|    | Esclusione tramite sezionale                                        |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Identificazione Reverse Charge                    | |check|    | Da codice imposte                                                   |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Fatture vendita UE                                | |check|    | Inserite in spesometro                                              |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Fatture vendita extra-UE                          | |check|    | Inserite in spesometro                                              |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Fatture acq. intra-UE beni                        | |no_check| | In fase di rilascio                                                 |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Fatture acq. intra-UE servizi                     | |check|    | Tutte le fatture EU (provvisoriamente)                              |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Rettifica dichiarazione                           | |no_check| | In fase di rilascio                                                 |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Nomenclatura del file                             | |check|    |                                                                     |
+---------------------------------------------------+------------+---------------------------------------------------------------------+
| Dimensioni del file                               | |no_check| | Nessuna verifica anche futura                                       |
+---------------------------------------------------+------------+---------------------------------------------------------------------+



Certifications | Certificazioni
-------------------------------

+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+------------+-----------------------------------------------------------+
| Logo                | Ente/Certificato                                                                                                                                                                                              | Data inizio | Da fine    | Note                                                      |
+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+------------+-----------------------------------------------------------+
| |xml\_schema|       | `ISO + Agenzia delle Entrate <http://www.agenziaentrate.gov.it/wps/content/Nsilib/Nsi/Strumenti/Specifiche+tecniche/Specifiche+tecniche+comunicazioni/Fatture+e+corrispettivi+ST/>`__                         | 01-10-2017  | 31-12-2018 | Validazione contro schema xml                             |
+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+------------+-----------------------------------------------------------+
| |DesktopTelematico| | `Desktop telematico <http://www.agenziaentrate.gov.it/wps/content/nsilib/nsi/schede/comunicazioni/dati+fatture+%28c.d.+nuovo+spesometro%29/software+di+controllo+dati+fatture+%28c.d.+nuovo+spesometro%29>`__ | 01-03-2018  | 31-12-2018 | Controllo tramite s/w Agenzia delle Entrate               |
+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+------------+-----------------------------------------------------------+
| |FatturaPA|         | `FatturaPA <http://www.agenziaentrate.gov.it/wps/content/Nsilib/Nsi/Strumenti/Specifiche+tecniche/Specifiche+tecniche+comunicazioni/Fatture+e+corrispettivi+ST/>`__                                           | 05-10-2017  | 31-12-2018 | File accettati da portale fatturaPA Agenzia delle Entrate |
+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+------------+-----------------------------------------------------------+



Usage | Utilizzo
----------------

* |menu| Contabilità > Configurazione > Sezionali > Sezionali :point_right: Impostare sezionali autofatture
* |menu| Contabilità > Configurazione > Imposte > Imposte :point_right: Impostare natura codici IVA
* |menu| Contabilità > Clienti > Clienti :point_right: Impostare nazione, partita IVA, codice fiscale e Cognome/nome
* |menu| Contabilità > Fornitori > Fornitori :point_right: Impostare nazione, partita IVA, codice fiscale e Cognome/nome
* |menu| Contabilità > Elaborazione periodica > Fine periodo > Comunicazione :point_right: Gestione Comunicazione e scarico file xml



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



Known issues | Roadmap
----------------------

|en| Please, do not mix the following OCA Italy and OIA module.

|it| Si consiglia di non mescolare moduli OCA Italia e moduli OIA.

* This module replaces l10n_it_base of OCA distribution.
* Do not use l10n_it_split_payment module of OCA distribution
* Do not use l10n_it_reverse_charge of OCA distribution



Proposals for enhancement
-------------------------

|en| If you have a proposal to change this module, you may want to send an email to <cc@shs-av.com> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.

|it| Se hai proposte per migliorare questo modulo, puoi inviare una mail a <cc@shs-av.com> per un iniziale contatto.



ChangeLog History | Cronologia modifiche
----------------------------------------

10.0.0.2.4 (2022-06-30)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Tax nature_id renamed

10.0.0.2.3 (2022-06-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Fiscal document type renamed



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

* `Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>`__



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
