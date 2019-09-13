from tests.lib import assert_reapply, assert_reapply_raises, assert_reapply_visible


def test_basic() -> None:
    pyi_txt = """
    def fun() -> None:
        name: str
    """
    src_txt = """
    def fun():
        "Docstring"

        name = "Dinsdale"
        print(name)
        name = "Diinsdaalee"
    """
    expected_txt = """
    def fun() -> None:
        "Docstring"

        name: str = "Dinsdale"
        print(name)
        name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_basic_replace_any() -> None:
    pyi_txt = """
    def fun() -> None:
        name: str
    """
    src_txt = """
    def fun():
        "Docstring"

        name: Any = "Dinsdale"
        print(name)
        name = "Diinsdaalee"
    """
    expected_txt = """
    def fun() -> None:
        "Docstring"

        name: str = "Dinsdale"
        print(name)
        name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt, replace_any=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, replace_any=True)


def test_no_value() -> None:
    pyi_txt = """
    def fun() -> None:
        name: str
    """
    src_txt = """
    def fun():
        "Docstring"

        name: str
        print(name)
        name = "Diinsdaalee"
    """
    expected_txt = """
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
    def fun() -> None:
        name: str
    """
    src_txt = """
    def fun():
        "Docstring"

        if False:
            name = "Dinsdale"
            print(name)
            name = "Diinsdaalee"
    """
    expected_txt = """
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
    def fun() -> None:
        name: str
    """
    src_txt = """
    def fun():
        "Docstring"

        name: int = 0
        print(name)
        name = "Diinsdaalee"
    """
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 2:1: "
        + "incompatible existing variable annotation for 'name'. "
        + "Expected: 'str', actual: 'int'"
        == str(exception)
    )


def test_complex() -> None:
    pyi_txt = """
    def fun() -> None:
        name: str
        age: int
        likes_spam: bool
    """
    src_txt = """
    def fun():
        "Docstring"

        name = "Dinsdale"
        print(name)
        if False:
            age = 100
            name = "Diinsdaalee"
    """
    expected_txt = """
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


def test_complex_type() -> None:
    pyi_txt = """
    def fun() -> None:
        many_things: Union[List[int], str, 'Custom', Tuple[int, ...]]
    """
    src_txt = """
    def fun():
        "Docstring"

        many_things = []
        other_code()
    """
    expected_txt = """
    def fun() -> None:
        "Docstring"

        many_things: Union[List[int], str, 'Custom', Tuple[int, ...]] = []
        other_code()
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)
