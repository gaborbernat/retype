from retype import _type_comment_re


def assert_match(input: str, *, type: str, nl: str) -> None:
    m = _type_comment_re.match(input)
    assert m is not None
    if m is not None:
        assert m.group("type") == type
        assert m.group("nl") == nl


def assert_no_match(input: str) -> None:
    m = _type_comment_re.match(input)
    assert m is None


def test_ignore() -> None:
    assert_no_match("# type:ignore")
    assert_no_match("# type: ignore")
    assert_no_match("# type: ignore\n")
    assert_no_match("# type: ignore ")
    assert_no_match("# type: ignore \n")


def test_ignore_with_comment() -> None:
    assert_no_match("# type: ignore#wut")
    assert_no_match("# type: ignore#wut\n")
    assert_no_match("# type: ignore#wut ")
    assert_no_match("# type: ignore#wut \n")
    assert_no_match("# type: ignore #wut \n")
    assert_no_match("# type: ignore # wut \n")
    assert_no_match("# type: ignore  # wut \n")
    assert_no_match("# type: ignore    # wut \n")


def test_no_whitespace_after_colon() -> None:
    assert_match("# type:int", type="int", nl="")
    assert_match("# type:int\n", type="int", nl="\n")
    assert_match("  # type:int\n", type="int", nl="\n")
    assert_match("# type:int  \n", type="int", nl="\n")
    assert_match("  # type:int  \n", type="int", nl="\n")


def test_simple_type() -> None:
    assert_match("# type: int", type="int", nl="")
    assert_match("# type: int\n", type="int", nl="\n")
    assert_match("  # type: int\n", type="int", nl="\n")
    assert_match("# type: int  \n", type="int", nl="\n")
    assert_match("  # type: int  \n", type="int", nl="\n")


def test_simple_type_with_comment() -> None:
    assert_match("# type: int#wut", type="int", nl="#wut")
    assert_match("# type: int#wut\n", type="int", nl="#wut\n")
    assert_match("  # type: int#wut\n", type="int", nl="#wut\n")
    assert_match("# type: int  #wut\n", type="int", nl="#wut\n")
    assert_match("  # type: int  # wut \n", type="int", nl="# wut \n")


def test_complex_type() -> None:
    assert_match(
        "# type: Dict[str, Union[str, int, None]]",
        type="Dict[str, Union[str, int, None]]",
        nl="",
    )
    assert_match(
        "# type: Dict[str, Union[str, int, None]]\n",
        type="Dict[str, Union[str, int, None]]",
        nl="\n",
    )
    assert_match(
        "  # type: Dict[str, Union[str, int, None]]\n",
        type="Dict[str, Union[str, int, None]]",
        nl="\n",
    )
    assert_match(
        "# type: Dict[str, Union[str, int, None]]  \n",
        type="Dict[str, Union[str, int, None]]",
        nl="\n",
    )
    assert_match(
        "  # type: Dict[str, Union[str, int, None]]  \n",
        type="Dict[str, Union[str, int, None]]",
        nl="\n",
    )
