from tests.lib import assert_reapply, assert_reapply_raises, assert_reapply_visible


def test_basic() -> None:
    pyi_txt = """
    name: str
    """
    src_txt = """
    "Docstring"

    name = "Dinsdale"
    print(name)
    name = "Diinsdaalee"
    """
    expected_txt = """
    "Docstring"

    name: str = "Dinsdale"
    print(name)
    name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_no_value() -> None:
    pyi_txt = """
    name: str
    """
    src_txt = """
    "Docstring"

    name: str
    print(name)
    name = "Diinsdaalee"
    """
    expected_txt = """
    "Docstring"

    name: str
    print(name)
    name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_default_type() -> None:
    pyi_txt = """
    name: str
    """
    src_txt = """
    "Docstring"

    if False:
        name = "Dinsdale"
        print(name)
        name = "Diinsdaalee"
    """
    expected_txt = """
    "Docstring"
    name: str
    if False:
        name = "Dinsdale"
        print(name)
        name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_type_mismatch() -> None:
    pyi_txt = """
    name: str
    """
    src_txt = """
    "Docstring"

    name: int = 0
    print(name)
    name = "Diinsdaalee"
    """
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "incompatible existing variable annotation for 'name'. "
        + "Expected: 'str', actual: 'int'"
        == str(exception)
    )


def test_complex() -> None:
    pyi_txt = """
    name: str
    age: int
    likes_spam: bool
    """
    src_txt = """
    "Docstring"

    name = "Dinsdale"
    print(name)
    if False:
        age = 100
        name = "Diinsdaalee"
    """
    expected_txt = """
    "Docstring"
    age: int
    likes_spam: bool
    name: str = "Dinsdale"
    print(name)
    if False:
        age = 100
        name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_with_imports() -> None:
    pyi_txt = """
    from typing import Optional

    name: Optional[str]
    age: int
    likes_spam: bool
    """
    src_txt = """
    "Docstring"

    import sys

    name = "Dinsdale"
    print(name)
    if False:
        age = 100
        name = "Diinsdaalee"
    """
    expected_txt = """
    "Docstring"

    import sys

    from typing import Optional
    age: int
    likes_spam: bool
    name: Optional[str] = "Dinsdale"
    print(name)
    if False:
        age = 100
        name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_alias_basic() -> None:
    pyi_txt = """
    from typing import List, Optional

    MaybeStrings = Optional[List[Optional[str]]]
    SOME_GLOBAL: int

    def fun(errors: MaybeStrings) -> None: ...
    """
    src_txt = """
    "Docstring"

    from __future__ import print_function

    import sys

    SOME_GLOBAL: int = 0

    def fun(errors):
        for error in errors:
            if not error:
                continue
            print(error, file=sys.stderr)
    """
    expected_txt = """
    "Docstring"

    from __future__ import print_function

    import sys

    from typing import List, Optional
    SOME_GLOBAL: int = 0
    MaybeStrings = Optional[List[Optional[str]]]

    def fun(errors: MaybeStrings) -> None:
        for error in errors:
            if not error:
                continue
            print(error, file=sys.stderr)
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_alias_typevar() -> None:
    pyi_txt = """
    from typing import TypeVar

    _T = TypeVar('_T', bound=str)
    SOME_GLOBAL: int

    def fun(error: _T) -> _T: ...
    """
    src_txt = """
    "Docstring"

    from __future__ import print_function

    import sys

    SOME_GLOBAL: int = 0

    def fun(error):
        return error
    """
    expected_txt = """
    "Docstring"

    from __future__ import print_function

    import sys

    from typing import TypeVar
    SOME_GLOBAL: int = 0
    _T = TypeVar('_T', bound=str)

    def fun(error: _T) -> _T:
        return error
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_alias_typevar_typing() -> None:
    pyi_txt = """
    import typing.foo.bar

    _T = typing.foo.bar.TypeVar('_T', bound=str)
    SOME_GLOBAL: int

    def fun(error: _T) -> _T: ...
    """
    src_txt = """
    "Docstring"

    import sys

    SOME_GLOBAL: int = 0

    def fun(error):
        return error
    """
    expected_txt = """
    "Docstring"

    import sys

    import typing.foo.bar
    SOME_GLOBAL: int = 0
    _T = typing.foo.bar.TypeVar('_T', bound=str)

    def fun(error: _T) -> _T:
        return error
    """
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_alias_many() -> None:
    pyi_txt = """
    from typing import TypeVar

    _T = TypeVar('_T', bound=str)
    _EitherStr = Union[str, bytes]
    _MaybeStrings = List[Optional[_EitherStr]]
    SOME_GLOBAL: int

    def fun(error: _T) -> _T: ...
    def fun2(errors: _MaybeStrings) -> None: ...
    """
    src_txt = """
    "Docstring"

    from __future__ import print_function

    import sys

    SOME_GLOBAL: int = 0

    def fun(error):
        return error

    @decorator
    def fun2(errors) -> None:
        for error in errors:
            if not error:
                continue
            print(error, file=sys.stderr)
    """
    expected_txt = """
    "Docstring"

    from __future__ import print_function

    import sys

    from typing import TypeVar
    SOME_GLOBAL: int = 0
    _T = TypeVar('_T', bound=str)

    def fun(error: _T) -> _T:
        return error

    _EitherStr = Union[str, bytes]
    _MaybeStrings = List[Optional[_EitherStr]]
    @decorator
    def fun2(errors: _MaybeStrings) -> None:
        for error in errors:
            if not error:
                continue
            print(error, file=sys.stderr)
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)
