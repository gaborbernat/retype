from textwrap import dedent

import pytest
from typed_ast import ast3

from retype import ReApplyFlags, fix_remaining_type_comments, lib2to3_parse, reapply_all


def assert_reapply(
    pyi_txt, src_txt, expected_txt, *, incremental=False, replace_any=False
):
    src = _reapply(incremental, pyi_txt, replace_any, src_txt)
    expected = lib2to3_parse(dedent(expected_txt))
    assert expected == src, f"\n{expected!r} != \n{src!r}"


def assert_reapply_visible(
    pyi_txt, src_txt, expected_txt, *, incremental=False, replace_any=False
):
    src = _reapply(incremental, pyi_txt, replace_any, src_txt)
    expected = lib2to3_parse(dedent(expected_txt))
    assert str(expected) == str(src), f"\n{str(expected)!r} != \n{str(src)!r}"


def assert_reapply_raises(
    pyi_txt, src_txt, expected_exception, *, incremental=False, replace_any=False
):
    with pytest.raises(expected_exception) as ctx:
        _reapply(incremental, pyi_txt, replace_any, src_txt)
    return ctx.value


def _reapply(incremental, pyi_txt, replace_any, src_txt):
    pyi = ast3.parse(dedent(pyi_txt))
    src = lib2to3_parse(dedent(src_txt))
    assert isinstance(pyi, ast3.Module)
    flags = ReApplyFlags(replace_any=replace_any, incremental=incremental)
    reapply_all(pyi.body, src, flags)
    fix_remaining_type_comments(src, flags)
    return src
