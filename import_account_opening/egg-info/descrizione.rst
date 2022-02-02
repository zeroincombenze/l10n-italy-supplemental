Importazione apertura conti
---------------------------

Importazione apertura conti da file Excel

Il file Excel ha la seguente struttura:

.. $include example_excel.rst

Note:

* Si possono importare solo file .xlsx
* Le etichette dell'intestazione devono essere rispettate
* Impostare solo cliente o fornitore in ogni riga cliente/fornitore
* Impostare un solo importo tra "Dare" e "Avere"
* Nel caso di clienti/fornitori viene cercato per partita IVA o codice fiscale e nome simile
* Nel caso di clienti/fornitori, il codice conto, se non è inserito, è preso dall'anagrafica
* Il campo Ref è facoltativo; serve se si vuole importare per partite aperte

Si può vedere un esempio nella cartella example.