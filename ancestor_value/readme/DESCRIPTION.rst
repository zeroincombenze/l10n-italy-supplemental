This module is not directly useful for end user.

It gives available the function ancestor_value which returns a valid ancestor with
specific field value.
This function makes available a fallback value of record through its parents.
Imagine to manage some kinds of product recognized by a special boolean value in
product category.
From product you can easily get special value from its category but if this value is
on a ascendent category you have to navigate upward tree until you find a valid value.
The function ancestor_value does this action for you on any model with parent_id field.

Example:

    product.product Alpha, categ_id -> product.category A3

    product.category A3, special = False, parent_id = A2

    product.category A2, special = False, parent_id = A1

    product.category A1, special = "Foo", parent_id = A

    product.category A, special = "Bar", parent_id = False

    product.ancestor_value("special") return "Foo" (from product.category A1)



