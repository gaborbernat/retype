from textwrap import dedent

from typed_ast import ast3

from retype import serialize_attribute


def test_serialize_attribute() -> None:
    src_txt = "a.b.c"
    expected = "a.b.c"

    src = ast3.parse(dedent(src_txt))
    assert isinstance(src, ast3.Module)
    attr_expr = src.body[0]
    assert serialize_attribute(attr_expr) == expected


def test_serialize_name() -> None:
    src_txt = "just_a_flat_name"
    expected = "just_a_flat_name"

    src = ast3.parse(dedent(src_txt))
    assert isinstance(src, ast3.Module)
    attr_expr = src.body[0]
    assert serialize_attribute(attr_expr) == expected
