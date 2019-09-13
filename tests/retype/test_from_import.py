from typing import Optional

from tests.lib import assert_reapply

IMPORT = "from y import x"


def _test_matched(matched: str, expected: Optional[str] = None) -> None:
    pyi = f"{IMPORT}\n"
    src = f"{matched}\n"
    expected = f"{expected if expected is not None else matched}\n"
    assert_reapply(pyi, src, expected)


def _test_unmatched(unmatched: str) -> None:
    pyi = f"{IMPORT}\n"
    src = f"{unmatched}\n"
    expected = f"{unmatched}\n{IMPORT}\n"
    assert_reapply(pyi, src, expected)


def test_matched1() -> None:
    _test_matched("from y import x as x")


def test_matched2() -> None:
    _test_matched("from y import z, y, x")


def test_matched3() -> None:
    _test_matched("from y import z as y, x")


def test_unmatched1() -> None:
    _test_unmatched("from y import y as x")


def test_unmatched2() -> None:
    _test_unmatched("from y import x as y")


def test_unmatched3() -> None:
    _test_unmatched("from .y import x")


def test_unmatched4() -> None:
    _test_unmatched("import y.x")


def test_unmatched5() -> None:
    _test_unmatched("import y")


def test_unmatched6() -> None:
    _test_unmatched("from . import x")


def test_unmatched7() -> None:
    _test_unmatched("from .y import x")


def test_unmatched8() -> None:
    _test_unmatched("import x")
