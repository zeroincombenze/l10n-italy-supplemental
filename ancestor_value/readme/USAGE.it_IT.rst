Basato su seguente gerarchia:

    top_record: ref="valid", comment="top"

    middle_record: ref=False, comment="middle", parent_id=top_record

    bottom_record: ref=False, comment="bottom", parent_id=middle_record

Ricerca ascendente con varie espressioni:

    bottom_record.ancestor_value("ref") -> "Valid" (from top_record)

    bottom_record.ancestor_value("comment") -> "bottom" (from current record)

    bottom_record.ancestor_value("comment", skip_current=True) -> "middle"

    bottom_record.ancestor_value("ref", field="comment") -> "top"

    bottom_record.ancestor_value("ref", value="Valid", field="comment") -> "top"

Restituisce un record (non solo un valore di campo):

    bottom_record.ancestor_value("ref", value="Valid", field="self") -> top_record

Restituisce se un record è nella gerarchia:

    bottom_record.ancestor_value("self", value=record_top)) -> True

    bottom_record.ancestor_value("self", value=record_middle)) -> True
