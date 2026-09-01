Sul DdT il responsabile può marcare ogni riga con:

* **Dichiarata fatturata**: la riga è considerata interamente fatturata e non
  viene più selezionata quando si crea una fattura dal DdT. Va usata quando la
  merce di quella riga non deve essere addebitata, ad esempio una sostituzione
  in garanzia.

Lo stesso risultato si ottiene da codice con i metodi
``action_declare_invoiced()`` e ``action_undeclare_invoiced()`` di
``stock.picking.package.preparation.line``.

Il campo tecnico ``line_invoiced`` è memorizzato e calcolato: è vero quando
dalla riga di DdT è stata creata una riga di fattura, oppure la riga è stata
dichiarata fatturata, oppure il prodotto ha la politica *Dichiara
automaticamente fatturato*, oppure **la riga d'ordine di vendita è stata
dichiarata fatturata**. Quest'ultimo caso è lo scopo del modulo ponte: una
decisione presa sull'ordine non viene mai contraddetta dal DdT, che
altrimenti addebiterebbe al cliente quanto l'ordine dichiara già fatturato.

La dichiarazione viaggia dall'ordine al DdT e mai in senso inverso: una riga
di DdT è una delle possibili consegne di una riga d'ordine, quindi non può
decidere per essa. Quando anche l'ordine deve essere chiuso, si dichiari
fatturata la sua riga: se ne occupa `sale_order_line_qty_policy`.

A livello di DdT, lo **Stato fatturazione** riporta gli stessi tre valori che
Odoo usa per l'ordine di vendita:

* *Niente da fatturare*: il DdT non è ancora fatturabile, oppure la sua
  causale di trasporto dichiara che non è da fatturare;
* *Da fatturare*: almeno una riga deve ancora essere fatturata;
* *Interamente fatturato*: tutte le righe sono fatturate o dichiarate
  fatturate. Un DdT può essere interamente fatturato senza avere alcuna
  fattura, quando la politica dichiara fatturate tutte le sue righe.

I filtri *Da fatturare* e *Fatturato* dell'elenco dei DdT, e il filtro *Da
fatturare* dell'elenco delle righe di DdT, sono riscritti in termini di questi
campi, così un documento chiuso dalla politica non viene più proposto per la
fatturazione.

L'eliminazione di una fattura, o di una sua riga, restituisce alla
fatturazione le righe di DdT che vi erano collegate. Tali riferimenti vengono
azzerati dal database stesso, quindi nulla indicherebbe al DdT di rivalutare
le proprie righe: una riga resterebbe fatturata per sempre, non potrebbe più
essere addebitata e il suo DdT continuerebbe a risultare interamente
fatturato pur non avendo alcuna fattura.

Il riferimento alla fattura del DdT viene scritto ogni volta che tutte le
righe risultano fatturate, indipendentemente dall'esecuzione che le ha
fatturate: il modulo standard lo scrive solo quando una singola esecuzione
fattura tutte le righe, quindi una riga fatturata separatamente - o dichiarata
fatturata - lasciava il documento aperto per sempre.

Un DdT che non ha più nulla da fatturare viene saltato dalla procedura di
fatturazione anziché bloccarla. La procedura di fatturazione massiva continua
a selezionarlo, perché il suo dominio appartiene a `l10n_it_ddt`, ma ora il
DdT viene saltato invece di far fallire l'intera esecuzione. L'errore è
sollevato solo quando nessuno dei DdT selezionati ha qualcosa da fatturare.
