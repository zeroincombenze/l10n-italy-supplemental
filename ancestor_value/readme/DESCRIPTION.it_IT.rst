Questo modulo non ha alcuno scopo per l'utente finale.

Rende disponibile la funzione ancestor_value che restituisce un antenato valido
con un valore di campo specifico.
Questa funzione rende disponibile un valore di fallback del record attraverso
i suoi ascendenti.
Immaginiamo di gestire alcuni tipi di prodotti riconosciuti da uno speciale valore
booleano nella categoria di prodotto.
Dal prodotto si può facilmente ottenere un valore speciale dalla sua categoria,
ma se questo valore si trova in una categoria ascendente, occorre navigare verso l'alto
nell'albero fino a trovare un valore valido.
La funzione ancestor_value esegue questa azione su qualsiasi modello dotatto di
campo parent_id.

Esempio:

    product.product Alpha, categ_id -> product.category A3

    product.category A3, special=False, parent_id=A2

    product.category A2, special=False, parent_id=A1

    product.category A1, special="Foo", parent_id=A

    product.category A, special="Bar", parent_id=False

    product.ancestor_value("special") restituisce "Foo"
