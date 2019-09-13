from tests.lib import assert_reapply, assert_reapply_raises, assert_reapply_visible


def test_basic() -> None:
    pyi_txt = """
    class C:
        def fun() -> None:
            name = ...  # type: str
            age = ...  # type: int
    """
    src_txt = """
    class C:
        def fun():
            "Docstring"

            name = "Dinsdale"
            age = 47
            print(name, age)
            name = "Diinsdaalee"
    """
    expected_txt = """
    class C:
        def fun() -> None:
            "Docstring"

            name: str = "Dinsdale"
            age: int = 47
            print(name, age)
            name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_no_value() -> None:
    pyi_txt = """
    class C:
        def fun() -> None:
            name = ...  # type: str
    """
    src_txt = """
    class C:
        def fun():
            "Docstring"

            name: str
            print(name)
            name = "Diinsdaalee"
    """
    expected_txt = """
    class C:
        def fun() -> None:
            "Docstring"

            name: str
            print(name)
            name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_no_value_type_comment() -> None:
    pyi_txt = """
    class C:
        def fun() -> None:
            name = ...  # type: str
    """
    src_txt = """
    class C:
        def fun():
            "Docstring"

            name = ...  # type: str
            print(name)
            name = "Diinsdaalee"
    """
    expected_txt = """
    class C:
        def fun() -> None:
            "Docstring"

            name: str
            print(name)
            name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_default_type() -> None:
    pyi_txt = """
    class C:
        def fun() -> None:
            name = ...  # type: str
    """
    src_txt = """
    class C:
        def fun():
            "Docstring"

            if False:
                name = "Dinsdale"
                print(name)
                name = "Diinsdaalee"
    """
    expected_txt = """
    class C:
        def fun() -> None:
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
    class C:
        def fun() -> None:
            name = ...  # type: str
    """
    src_txt = """
    class C:
        def fun():
            "Docstring"

            name: int = 0
            print(name)
            name = "Diinsdaalee"
    """
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 3:1: "
        + "incompatible existing variable annotation for 'name'. "
        + "Expected: 'str', actual: 'int'"
        == str(exception)
    )


def test_complex() -> None:
    pyi_txt = """
    class C:
        def fun() -> None:
            name = ...  # type: str
            age = ...  # type: int
            likes_spam = ...  # type: bool
    """
    src_txt = """
    class C:
        def fun():
            "Docstring"

            name = "Dinsdale"
            print(name)
            if False:
                age = 100
                name = "Diinsdaalee"
    """
    expected_txt = """
    class C:
        def fun() -> None:
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
