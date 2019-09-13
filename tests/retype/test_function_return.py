from tests.lib import assert_reapply, assert_reapply_raises, assert_reapply_visible


def test_missing_return_value_both() -> None:
    pyi_txt = "def fun(): ...\n"
    src_txt = "def fun(): ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: .pyi file is missing "
        + "return value and source doesn't provide it either"
        == str(exception)
    )


def test_missing_return_value_pyi() -> None:
    pyi_txt = "def fun(): ...\n"
    src_txt = "def fun() -> None: ...\n"
    expected_txt = "def fun() -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_missing_return_value_src() -> None:
    pyi_txt = "def fun() -> None: ...\n"
    src_txt = "def fun(): ...\n"
    expected_txt = "def fun() -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_return_value() -> None:
    pyi_txt = "def fun() -> List[Tuple[int, int]]: ...\n"
    src_txt = "def fun(): ...\n"
    expected_txt = "def fun() -> List[Tuple[int, int]]: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_return_value2() -> None:
    pyi_txt = "def fun() -> List[Tuple[Callable[[], Any], ...]]: ...\n"
    src_txt = "def fun(): ...\n"
    expected_txt = "def fun() -> List[Tuple[Callable[[], Any], ...]]: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_return_value3() -> None:
    pyi_txt = "def fun() -> List[Callable[[str, int, 'Custom'], Any]]: ...\n"
    src_txt = "def fun(): ...\n"
    expected_txt = "def fun() -> List[Callable[[str, int, 'Custom'], Any]]: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_mismatched_return_value() -> None:
    pyi_txt = "def fun() -> List[Tuple[int, int]]: ...\n"
    src_txt = "def fun() -> List[int]: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: incompatible existing "
        + "return value. Expected: 'List[Tuple[int, int]]', actual: 'List[int]'"
        == str(exception)
    )


def test_complex_return_value_type_comment() -> None:
    pyi_txt = """
    def fun():
        # type: () -> List[Callable[[str, int, 'Custom'], Any]]
        ...
    """
    src_txt = """
    def fun():
        ...
    """
    expected_txt = """
    def fun() -> List[Callable[[str, int, 'Custom'], Any]]:
        ...
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_return_value_spurious_type_comment() -> None:
    pyi_txt = """
    def fun():
        # type: () -> List[Callable[[str, int, 'Custom'], Any]]
        ...
    """
    src_txt = """
    def fun():
        # type: () -> List[Callable[[str, int, 'Custom'], Any]]
        ...
    """
    expected_txt = """
    def fun() -> List[Callable[[str, int, 'Custom'], Any]]:
        ...
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_missing_return_value_both_incremental() -> None:
    pyi_txt = "def fun(): ...\n"
    src_txt = "def fun(): ...\n"
    expected_txt = "def fun(): ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, incremental=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, incremental=True)


def test_missing_return_value_pyi_incremental() -> None:
    pyi_txt = "def fun(): ...\n"
    src_txt = "def fun() -> None: ...\n"
    expected_txt = "def fun() -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, incremental=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, incremental=True)


def test_missing_return_value_src_incremental() -> None:
    pyi_txt = "def fun() -> None: ...\n"
    src_txt = "def fun(): ...\n"
    expected_txt = "def fun() -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, incremental=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, incremental=True)


def test_any_return_value_src_no_replace_any() -> None:
    pyi_txt = "def fun() -> None: ...\n"
    src_txt = "def fun() -> Any: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: incompatible existing "
        + "return value. Expected: 'None', actual: 'Any'"
        == str(exception)
    )


def test_any_return_value_src_replace_any() -> None:
    pyi_txt = "def fun() -> None: ...\n"
    src_txt = "def fun() -> Any: ...\n"
    expected_txt = "def fun() -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, replace_any=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, replace_any=True)


def test_any_return_value_missing_pyi_src_replace_any() -> None:
    pyi_txt = "def fun(): ...\n"
    src_txt = "def fun() -> Any: ...\n"
    expected_txt = "def fun() -> Any: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, replace_any=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, replace_any=True)
