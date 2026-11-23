This module enables user to delete a payment record.
Payment record cannot be remove if account entry has received the sequence number.
This module reset the field "move_name" before unlink().

**Warning!** This action leaves a hole in journal entries sequence.
This issue is forbidden in some countries.
