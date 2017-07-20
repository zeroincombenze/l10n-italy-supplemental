[![Build Status](https://travis-ci.org/zeroincombenze/l10n-italy-supplemental.svg?branch=7.0)](https://travis-ci.org/zeroincombenze/l10n-italy-supplemental)
[![license agpl](https://img.shields.io/badge/licence-AGPL--3-blue.svg)](http://www.gnu.org/licenses/agpl-3.0.html)
[![Coverage Status](https://coveralls.io/repos/github/zeroincombenze/l10n-italy-supplemental/badge.svg?branch=7.0)](https://coveralls.io/github/zeroincombenze/l10n-italy-supplemental?branch=7.0)
[![codecov](https://codecov.io/gh/zeroincombenze/l10n-italy-supplemental/branch/7.0/graph/badge.svg)](https://codecov.io/gh/zeroincombenze/l10n-italy-supplemental/branch/7.0)
[![OCA_project](http://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-oca-7.svg)](https://github.com/OCA/l10n-italy-supplemental/tree/7.0)
[![Tech Doc](http://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-docs-7.svg)](http://wiki.zeroincombenze.org/en/Odoo/7.0/dev)
[![Help](http://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-help-7.svg)](http://wiki.zeroincombenze.org/en/Odoo/7.0/man/FI)
[![try it](http://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-7.svg)](http://erp7.zeroincombenze.it)


[![en](http://www.shs-av.com/wp-content/en_US.png)](http://wiki.zeroincombenze.org/it/Odoo/7.0/man)
================================================================================================

Odoo Italian Supplemental Modules

Supplemental Italian modules for odoo (formerly OpenERP) 7.0

Warning! Follow modules replace Odoo/OCA standard modules for Italian localization:
- account_banking_pain_base
- account_banking_payment_export
- account_banking_sepa_credit_transfer

ASAP we will write integration modules but for now you must replace above modules if you want to use Italina Credit Transfer.


[![it](http://www.shs-av.com/wp-content/it_IT.png)](http://wiki.zeroincombenze.org/it/Odoo/7.0/man)

Moduli Italiani aggiuntivi

Differenze rispetto localizzazione ufficiale Odoo/OCA:

- Basato su [piano dei conti](https://www.zeroincombenze.it/il-piano-dei-conti-2/) personalizzato  in [l10n-italy-supplemental](https://github.com/zeroincombenze/l10n-italy-supplemental/tree/7.0/l10n_it_fiscal)
- Basato su [codici IVA](http://wiki.zeroincombenze.org/it/Odoo/7.0/man/codici_IVA) personalizzati in [l10n-italy-supplemental](https://github.com/zeroincombenze/l10n-italy-supplemental/tree/7.0/l10n_it_fiscal)
- Classificazione [comuni italiani](http://www.shs-av.com/variazione-denominazione-comuni-italiani-2014/) aggiornata ai nuovi comuni
- [Modulo Spesometro](https://github.com/zeroincombenze/l10n-italy-supplemental/tree/7.0/l10n_it_spesometro) con auto setup per ridurre i tempi di attivazione
- [account_banking_pain_base](https://github.com/zeroincombenze/l10n-italy-supplemental/tree/7.0/account_banking_pain_base) sostituisce il relativo modulo [Odoo/OCA](https://github.com/OCA/bank-payment/tree/7.0/account_banking_pain_base)
- [account_banking_payment_export](https://github.com/zeroincombenze/l10n-italy-supplemental/tree/7.0/account_banking_payment_export) sostituisce il relativo modulo [Odoo/OCA](https://github.com/OCA/bank-payment/tree/7.0/account_banking_payment_export)
- Il modulo [account_banking_payment_export](https://github.com/zeroincombenze/l10n-italy-supplemental/tree/7.0/account_banking_payment_export) oltre ai pagamenti pubblicati esamina anche quelli non pubblicati
- [account_banking_sepa_credit_transfer](https://github.com/zeroincombenze/l10n-italy-supplemental/tree/7.0/account_banking_sepa_credit_transfer) sostituisce il relativo modulo [Odoo/OCA](https://github.com/OCA/bank-payment/tree/7.0/account_banking_sepa_credit_transfer)

- Modulo bonifici SEPA 7.0 non ancora ufficializzato in quanto per l'uso del Bonifico Sepa in Italia è provvisorimente sostitutivo del relativo modulo .

Modificheremo al più presto posssibile questi moduli per integrarli con i moduli standard ma, al momento, se volete gestire i bonifici Sepa con Odoo in Italia, dovete sostituire i moduli sopra elencati.

Le banche italiane non usano lo standard Sepa ma una variante definita del consorzio CBI.


[//]: # (copyright)

----

**Odoo** is a trademark of [Odoo S.A.](https://www.odoo.com/) (formerly OpenERP, formerly TinyERP)

**OCA**, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

**zeroincombenze®** is a trademark of [SHS-AV s.r.l.](http://www.shs-av.com/)
which distributes and promotes **Odoo** ready-to-use on its own cloud infrastructure.
[Zeroincombenze® distribution](http://wiki.zeroincombenze.org/en/Odoo)
is mainly designed for Italian law and markeplace.
Everytime, every Odoo DB and customized code can be deployed on local server too.

[//]: # (end copyright)





[![chat with us](https://www.shs-av.com/wp-content/chat_with_us.gif)](https://tawk.to/85d4f6e06e68dd4e358797643fe5ee67540e408b)
