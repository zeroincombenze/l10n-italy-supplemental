Based on following hierarchy:

    top_record: ref="valid", comment="top"

    middle_record: ref=False, comment="middle", parent_id=top_record

    bottom_record: ref=False, comment="bottom", parent_id=middle_record

Search for ancestor with various search expressions:

    bottom_record.ancestor_value("ref") -> "Valid" (from top_record)

    bottom_record.ancestor_value("comment") -> "bottom" (from current record)

    bottom_record.ancestor_value("comment", skip_current=True) -> "middle"

    bottom_record.ancestor_value("ref", field="comment") -> "top"

    bottom_record.ancestor_value("ref", value="Valid", field="comment") -> "top"

Return a record (not only a field value):

    bottom_record.ancestor_value("ref", value="Valid", field="self") -> top_record

Return if a record is an ancestor:

    bottom_record.ancestor_value("self", value=record_top)) -> True

    bottom_record.ancestor_value("self", value=record_middle)) -> True
