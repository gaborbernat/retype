from tests.lib import assert_reapply, assert_reapply_raises, assert_reapply_visible


def test_basic() -> None:
    pyi_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None: ...
    """
    src_txt = """
        class C:
            def __init__(a1, *args, kwonly1) -> None:
                super().__init__()
    """
    expected_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                super().__init__()
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)


def test_two_classes() -> None:
    pyi_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None: ...
        class D:
            def __init__(a1: C, **kwargs) -> None: ...
    """
    src_txt = """
        class C:
            def __init__(a1, *args, kwonly1) -> None:
                super().__init__()

        class D:
            def __init__(a1, **kwargs) -> None:
                super().__init__()
    """
    expected_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                super().__init__()

        class D:
            def __init__(a1: C, **kwargs) -> None:
                super().__init__()
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)


def test_function() -> None:
    pyi_txt = """
        class C:
            def method(a1: str, *args: str, kwonly1: int) -> None: ...
    """
    src_txt = """
        def method(a1, *args, kwonly1):
            print("I am not a method")

        class C:
            def method(a1, *args, kwonly1) -> None:
                print("I am a method!")
    """
    expected_txt = """
        def method(a1, *args, kwonly1):
            print("I am not a method")

        class C:
            def method(a1: str, *args: str, kwonly1: int) -> None:
                print("I am a method!")
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)


def test_missing_class() -> None:
    pyi_txt = """
        class C:
            def method(a1: str, *args: str, kwonly1: int) -> None: ...
    """
    src_txt = """
        def method(a1, *args, kwonly1):
            print("I am not a method")
    """
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert "Class 'C' not found in source." == str(exception)


def test_staticmethod() -> None:
    pyi_txt = """
        class C:
            @yeah.what.aboutThis()
            @staticmethod
            def method(a1, *args: str, kwonly1: int) -> None: ...
    """
    src_txt = """
        class C:
            @whatAboutThis()
            @yeah
            @staticmethod
            def method(a1, *args, kwonly1) -> None:
                print("I am a staticmethod, don't use me!")
    """
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'method': 6:1: .pyi file is "
        + "missing annotation for 'a1' and source doesn't provide it either"
        == str(exception)
    )


def test_decorator_mismatch() -> None:
    pyi_txt = """
        class C:
            @yeah.what.aboutThis()
            @staticmethod
            def method(a1, *args: str, kwonly1: int) -> None: ...
    """
    src_txt = """
        class C:
            @classmethod
            def method(cls, a1, *args, kwonly1) -> None:
                print("I am a staticmethod, don't use me!")
    """
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Incompatible method kind for 'method': 4:1: Expected: "
        + "staticmethod, actual: classmethod"
        == str(exception)
    )


def test_decorator_mismatch2() -> None:
    pyi_txt = """
        class C:
            @staticmethod
            def method(a1, *args: str, kwonly1: int) -> None: ...
    """
    src_txt = """
        class C:
            @this.isnt.a.staticmethod
            def method(a1, *args, kwonly1) -> None:
                print("I am a fake staticmethod, don't use me!")
    """
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Incompatible method kind for 'method': 4:1: Expected: "
        + "staticmethod, actual: instancemethod"
        == str(exception)
    )


def test_decorator_mismatch3() -> None:
    pyi_txt = """
        class C:
            @this.isnt.a.staticmethod
            def method(a1, *args: str, kwonly1: int) -> None: ...
    """
    src_txt = """
        class C:
            @staticmethod
            def method(a1, *args, kwonly1) -> None:
                print("I am a staticmethod, don't use me!")
    """
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Incompatible method kind for 'method': 4:1: Expected: "
        + "instancemethod, actual: staticmethod"
        == str(exception)
    )


def test_complex_sig1_type_comment() -> None:
    pyi_txt = """
    class C:
        @staticmethod
        def fun(a1, *args, kwonly1, **kwargs):
            # type: (str, *str, int, **Any) -> None
            ...
    """
    src_txt = """
    class C:
        @staticmethod
        def fun(a1, *args, kwonly1=None, **kwargs):
            ...
    """
    expected_txt = """
    class C:
        @staticmethod
        def fun(a1: str, *args: str, kwonly1: int = None, **kwargs: Any) -> None:
            ...
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig2_type_comment() -> None:
    pyi_txt = """
    class C:
        def fun(a1, *, kwonly1, **kwargs):
            # type: (str, int, **Any) -> None
            ...
    """
    src_txt = """
    class C:
        def fun(a1, *, kwonly1=None, **kwargs):
            ...
    """
    expected_txt = """
    class C:
        def fun(a1: str, *, kwonly1: int = None, **kwargs: Any) -> None:
            ...
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig3_type_comment() -> None:
    pyi_txt = """
    class C:
        @staticmethod
        def fun(a1):
            # type: (Union[str, bytes]) -> None
            ...
    """
    src_txt = """
    class C:
        @staticmethod
        def fun(a1):
            ...
    """
    expected_txt = """
    class C:
        @staticmethod
        def fun(a1: Union[str, bytes]) -> None:
            ...
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig4_type_comment() -> None:
    pyi_txt = """
    class C:
        @classmethod
        def fun(cls, a1):
            # type: (Union[str, bytes]) -> None
            ...
    """
    src_txt = """
    class C:
        @classmethod
        def fun(cls, a1):
            ...
    """
    expected_txt = """
    class C:
        @classmethod
        def fun(cls, a1: Union[str, bytes]) -> None:
            ...
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig5_type_comment() -> None:
    pyi_txt = """
    class C:
        @classmethod
        def fun(cls, a1):
            # type: (Type['C'], Union[str, bytes]) -> None
            ...
    """
    src_txt = """
    class C:
        @classmethod
        def fun(cls, a1):
            ...
    """
    expected_txt = """
    class C:
        @classmethod
        def fun(cls: Type['C'], a1: Union[str, bytes]) -> None:
            ...
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)
