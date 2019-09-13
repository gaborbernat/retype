from tests.lib import assert_reapply, assert_reapply_raises, assert_reapply_visible


def test_basic() -> None:
    pyi_txt = """
    """
    src_txt = """
    class C:
        "Docstring"

        name = "Dinsdale"
        print(name)
        name = "Diinsdaalee"
    """
    expected_txt = """
    class C:
        "Docstring"

        name: str = "Dinsdale"
        print(name)
        name = "Diinsdaalee"
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_no_value() -> None:
    pyi_txt = """
    class C:
        name: str
    """
    src_txt = """
    class C:
        "Docstring"

        name: str
        print(name)
        name = "Diinsdaalee"
    """
    expected_txt = """
    class C:
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
        name: str
    """
    src_txt = """
    class C:
        "Docstring"

        if False:
            name = "Dinsdale"
            print(name)
            name = "Diinsdaalee"
    """
    expected_txt = """
    class C:
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
        name: str
    """
    src_txt = """
    class C:
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
    class C:
        name: str
        age = ...  # type: int
        likes_spam: bool
    """
    src_txt = """
    class C:
        "Docstring"

        name = "Dinsdale"
        print(name)
        if False:
            age = 100
            name = "Diinsdaalee"
    """
    expected_txt = """
    class C:
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


def test_instance_fields_no_assignment() -> None:
    pyi_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                field0.subfield1.subfield2: Tuple[int]
                field1: str
                field2 = ...  # type: int
                field3: bool
        class D:
            def __init__(a1: C, **kwargs) -> None:
                field1: float
                field2: Optional[str]
                field3: int
    """
    src_txt = """
        class C:
            def __init__(a1, *args, kwonly1) -> None:
                "Creates C."
                super().__init__()

        class D:
            def __init__(a1, **kwargs) -> None:
                "Creates D."
                super().__init__()
    """
    expected_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                "Creates C."
                field0.subfield1.subfield2: Tuple[int]
                field1: str
                field2: int
                field3: bool
                super().__init__()

        class D:
            def __init__(a1: C, **kwargs) -> None:
                "Creates D."
                field1: float
                field2: Optional[str]
                field3: int
                super().__init__()
    """
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_instance_fields_no_assignment_no_docstring() -> None:
    pyi_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                field0.subfield1.subfield2: Tuple[int]
                field1: str
                field2 = ...  # type: int
                field3: bool
        class D:
            def __init__(a1: C, **kwargs) -> None:
                field1: float
                field2: Optional[str]
                field3: int
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
                field0.subfield1.subfield2: Tuple[int]
                field1: str
                field2: int
                field3: bool
                super().__init__()

        class D:
            def __init__(a1: C, **kwargs) -> None:
                field1: float
                field2: Optional[str]
                field3: int
                super().__init__()
    """
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_instance_fields_no_assignment_docstring() -> None:
    pyi_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                field0.subfield1.subfield2: Tuple[int]
                field1: str
                field2 = ...  # type: int
                field3: bool
        class D:
            def __init__(a1: C, **kwargs) -> None:
                field1: float
                field2: Optional[str]
                field3: int
    """
    src_txt = """
        class C:
            def __init__(a1, *args, kwonly1) -> None:
                "Docstring"
                super().__init__()

        class D:
            def __init__(a1, **kwargs) -> None:
                "Docstring"
                super().__init__()
    """
    expected_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                "Docstring"
                field0.subfield1.subfield2: Tuple[int]
                field1: str
                field2: int
                field3: bool
                super().__init__()

        class D:
            def __init__(a1: C, **kwargs) -> None:
                "Docstring"
                field1: float
                field2: Optional[str]
                field3: int
                super().__init__()
    """
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_instance_fields_assignment_docstring() -> None:
    pyi_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                field0.subfield1.subfield2: Tuple[int]
                field1: str
                field2 = ...  # type: int
                field3: bool
        class D:
            def __init__(a1: C, **kwargs) -> None:
                field1: float
                field2: Optional[str]
                field3: int
    """
    src_txt = """
        class C:
            def __init__(a1, *args, kwonly1) -> None:
                "Docstring"
                super().__init__()
                field2 = 0
                field1 = a1
                print("unrelated instruction")
                field0.subfield1.subfield2 = args[field2]

        class D:
            def __init__(a1, **kwargs) -> None:
                "Docstring"
                super().__init__()
                field2 = None
    """
    expected_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                "Docstring"
                field3: bool
                super().__init__()
                field2: int = 0
                field1: str = a1
                print("unrelated instruction")
                field0.subfield1.subfield2: Tuple[int] = args[field2]

        class D:
            def __init__(a1: C, **kwargs) -> None:
                "Docstring"
                field1: float
                field3: int
                super().__init__()
                field2: Optional[str] = None
    """
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_instance_fields_assignment_no_docstring() -> None:
    pyi_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                field0.subfield1.subfield2: Tuple[int]
                field1: str
                field2 = ...  # type: int
                field3: bool
        class D:
            def __init__(a1: C, **kwargs) -> None:
                field1: float
                field2: Optional[str]
                field3: int
    """
    src_txt = """
        class C:
            def __init__(a1, *args, kwonly1) -> None:
                super().__init__()
                field2 = 0
                field1 = a1
                print("unrelated instruction")
                field0.subfield1.subfield2 = args[field2]

        class D:
            def __init__(a1, **kwargs) -> None:
                super().__init__()
                field2 = None
                field1 = ...  # type: float
    """
    expected_txt = """
        class C:
            def __init__(a1: str, *args: str, kwonly1: int) -> None:
                field3: bool
                super().__init__()
                field2: int = 0
                field1: str = a1
                print("unrelated instruction")
                field0.subfield1.subfield2: Tuple[int] = args[field2]

        class D:
            def __init__(a1: C, **kwargs) -> None:
                field3: int
                super().__init__()
                field2: Optional[str] = None
                field1: float
    """
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)
