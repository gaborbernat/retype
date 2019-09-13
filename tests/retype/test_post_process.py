from tests.lib import assert_reapply, assert_reapply_visible


def test_straddling_variable_comments() -> None:
    pyi_txt = """
    def f(s: str) -> str: ...

    class C:
        def g() -> Iterator[Dict[int, str]]: ...
    """
    src_txt = """
    import sys

    def f(s):
        if s:
            l = []  # type: List[str]
            for elem in l:
                s += elem
        return s

    class C:
        def g():
            for i in range(10):
                result = {}  # type: Dict[int, str]
                result[i] = f(str(i))
                yield result
    """
    expected_txt = """
    import sys

    def f(s: str) -> str:
        if s:
            l: List[str] = []
            for elem in l:
                s += elem
        return s

    class C:
        def g() -> Iterator[Dict[int, str]]:
            for i in range(10):
                result: Dict[int, str] = {}
                result[i] = f(str(i))
                yield result
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_straddling_function_signature_type_comments1() -> None:
    pyi_txt = """
    class C:
        def f() -> Callable[[int, int], str]: ...
    """
    src_txt = """
    import sys

    class C:
        def f():
            def g(row, column):
                # type: (int1, int2) -> str
                return chessboard[row][column]
            return g
    """
    expected_txt = """
    import sys

    class C:
        def f() -> Callable[[int, int], str]:
            def g(row: int1, column: int2) -> str:
                return chessboard[row][column]
            return g
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_straddling_function_signature_type_comments2() -> None:
    pyi_txt = """
    class C:
        def f() -> Callable[[int, int], str]: ...
    """
    src_txt = """
    import sys

    class C:
        def f():
            @some_decorator
            def g(row, column):
                # type: (int1, int2) -> str
                return chessboard[row][column]
            return g
    """
    expected_txt = """
    import sys

    class C:
        def f() -> Callable[[int, int], str]:
            @some_decorator
            def g(row: int1, column: int2) -> str:
                return chessboard[row][column]
            return g
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_straddling_function_signature_type_comments3() -> None:
    pyi_txt = """
    class C:
        def f() -> Callable[[int, int], str]: ...
    """
    src_txt = """
    import sys

    class C:
        def f():
            def g(row, # type: int1
                  column, # type: int2  # with a further comment
            ):
                # type: (...) -> str
                return chessboard[row][column]
            return g
    """
    expected_txt = """
    import sys

    class C:
        def f() -> Callable[[int, int], str]:
            def g(row: int1,
                  column: int2  # with a further comment
            ) -> str:
                return chessboard[row][column]
            return g
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_straddling_function_signature_type_ignore() -> None:
    pyi_txt = """
    class C:
        def f() -> Callable[[int, int], str]: ...
    """
    src_txt = """
    import sys

    class C:
        def f():
            x = Foo.get(user_id)  # type: ignore  # comment
            y = []  # type: List[int]  # comment
            def g(row, # type: int1
                  column, # type: ignore
            ):
                # type: ignore
                return chessboard[row][column]
            return g
    """
    expected_txt = """
    import sys

    class C:
        def f() -> Callable[[int, int], str]:
            x = Foo.get(user_id)  # type: ignore  # comment
            y: List[int] = []  # comment
            def g(row, # type: int1
                  column, # type: ignore
            ):
                # type: ignore
                return chessboard[row][column]
            return g
    """
    # NOTE: `# type: int1` is not applied either because of the missing
    # return value type comment.
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)
