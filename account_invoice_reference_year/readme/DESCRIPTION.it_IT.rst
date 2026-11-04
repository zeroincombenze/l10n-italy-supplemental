Quando una fattura o nota di credito fornitore viene convalidata, Odoo standard
la rifiuta se esiste un'altra fattura/nota di credito dello stesso fornitore con
lo stesso riferimento, qualunque sia la data.

I fornitori italiani ricominciano la numerazione delle fatture ogni anno, quindi
lo stesso numero si ripete ogni anno. Questo modulo considera duplicato il
riferimento fornitore solo se presente nello **stesso anno solare** della data
fattura. Se la data fattura è vuota, viene usato l'anno corrente.
