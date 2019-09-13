from tests.lib import assert_reapply, assert_reapply_raises, assert_reapply_visible


def test_missing_ann_both() -> None:
    pyi_txt = "def fun(a1) -> None: ...\n"
    src_txt = "def fun(a1) -> None: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: .pyi file is missing "
        + "annotation for 'a1' and source doesn't provide it either"
        == str(exception)
    )


def test_missing_arg() -> None:
    pyi_txt = "def fun(a1) -> None: ...\n"
    src_txt = "def fun(a2) -> None: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: .pyi file expects "
        + "argument 'a1' next but argument 'a2' found in source"
        == str(exception)
    )


def test_missing_arg2() -> None:
    pyi_txt = "def fun(a1) -> None: ...\n"
    src_txt = "def fun(*, a1) -> None: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: "
        + "missing regular argument 'a1' in source"
        == str(exception)
    )


def test_missing_arg_kwonly() -> None:
    pyi_txt = "def fun(*, a1) -> None: ...\n"
    src_txt = "def fun(a1) -> None: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: "
        + ".pyi file expects *args or keyword-only arguments in source"
        == str(exception)
    )


def test_extra_arg1() -> None:
    pyi_txt = "def fun() -> None: ...\n"
    src_txt = "def fun(a1) -> None: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: " + "extra arguments in source: a1"
        == str(exception)
    )


def test_extra_arg2() -> None:
    pyi_txt = "def fun() -> None: ...\n"
    src_txt = "def fun(a1=None) -> None: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: "
        + "extra arguments in source: a1=None"
        == str(exception)
    )


def test_extra_arg_kwonly() -> None:
    pyi_txt = "def fun() -> None: ...\n"
    src_txt = "def fun(*, a1) -> None: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: "
        + "extra arguments in source: *, a1"
        == str(exception)
    )


def test_missing_default_arg_src() -> None:
    pyi_txt = "def fun(a1=None) -> None: ...\n"
    src_txt = "def fun(a1) -> None: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: "
        + "source file does not specify default value for arg `a1` but the "
        + ".pyi file does"
        == str(exception)
    )


def test_missing_default_arg_pyi() -> None:
    pyi_txt = "def fun(a1) -> None: ...\n"
    src_txt = "def fun(a1=None) -> None: ...\n"
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert (
        "Annotation problem in function 'fun': 1:1: "
        + ".pyi file does not specify default value for arg `a1` but the "
        + "source does"
        == str(exception)
    )


def test_missing_ann_pyi() -> None:
    pyi_txt = "def fun(a1) -> None: ...\n"
    src_txt = "def fun(a1: str) -> None: ...\n"
    expected_txt = "def fun(a1: str) -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_missing_ann_src() -> None:
    pyi_txt = "def fun(a1: str) -> None: ...\n"
    src_txt = "def fun(a1) -> None: ...\n"
    expected_txt = "def fun(a1: str) -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_missing_ann_pyi_replace_any() -> None:
    pyi_txt = "def fun(a1) -> None: ...\n"
    src_txt = "def fun(a1: Any) -> None: ...\n"
    expected_txt = "def fun(a1: Any) -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, replace_any=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, replace_any=True)


def test_missing_ann_src_replace_any() -> None:
    pyi_txt = "def fun(a1: str) -> None: ...\n"
    src_txt = "def fun(a1: Any) -> None: ...\n"
    expected_txt = "def fun(a1: str) -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, replace_any=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, replace_any=True)


def test_no_args() -> None:
    pyi_txt = "def fun() -> None: ...\n"
    src_txt = "def fun() -> None: ...\n"
    expected_txt = "def fun() -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_ann() -> None:
    pyi_txt = "def fun(a1: List[Tuple[int, int]]) -> None: ...\n"
    src_txt = "def fun(a1) -> None: ...\n"
    expected_txt = "def fun(a1: List[Tuple[int, int]]) -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_ann_with_default() -> None:
    pyi_txt = "def fun(a1: List[Tuple[int, int]] = None) -> None: ...\n"
    src_txt = "def fun(a1=None) -> None: ...\n"
    expected_txt = "def fun(a1: List[Tuple[int, int]] = None) -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig1() -> None:
    pyi_txt = "def fun(a1: str, *args: str, kwonly1: int, **kwargs) -> None: ...\n"
    src_txt = "def fun(a1, *args, kwonly1=None, **kwargs) -> None: ...\n"
    expected_txt = (
        "def fun(a1: str, *args: str, kwonly1: int = None, **kwargs) -> None: ...\n"
    )  # noqa
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig2() -> None:
    pyi_txt = "def fun(a1: str, *, kwonly1: int, **kwargs) -> None: ...\n"
    src_txt = "def fun(a1, *, kwonly1=None, **kwargs) -> None: ...\n"
    expected_txt = (
        "def fun(a1: str, *, kwonly1: int = None, **kwargs) -> None: ...\n"
    )  # noqa
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig_async() -> None:
    pyi_txt = (
        "async def fun(a1: str, *args: str, kwonly1: int, **kwargs) -> None: ...\n"
    )
    src_txt = "async def fun(a1, *args, kwonly1=None, **kwargs) -> None: ...\n"
    expected_txt = "async def fun(a1: str, *args: str, kwonly1: int = None, **kwargs) -> None: ...\n"  # noqa
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig1_type_comment() -> None:
    pyi_txt = """
    def fun(a1, *args, kwonly1, **kwargs):
        # type: (str, *str, int, **Any) -> None
        ...
    """
    src_txt = "def fun(a1, *args, kwonly1=None, **kwargs) -> None: ...\n"
    expected_txt = "def fun(a1: str, *args: str, kwonly1: int = None, **kwargs: Any) -> None: ...\n"  # noqa
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig2_type_comment() -> None:
    pyi_txt = """
    def fun(a1, *, kwonly1, **kwargs):
        # type: (str, int, **Any) -> None
        ...
    """
    src_txt = "def fun(a1, *, kwonly1=None, **kwargs) -> None: ...\n"
    expected_txt = (
        "def fun(a1: str, *, kwonly1: int = None, **kwargs: Any) -> None: ...\n"
    )  # noqa
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig3_type_comment() -> None:
    pyi_txt = """
    def fun(a1):
        # type: (Union[str, bytes]) -> None
        ...
    """
    src_txt = "def fun(a1): ...\n"
    expected_txt = "def fun(a1: Union[str, bytes]) -> None: ...\n"  # noqa
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig4_type_comment() -> None:
    pyi_txt = """
    def fun(
        a1,  # type: str
        *,
        kwonly1,  # type: int
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        ...
    """
    src_txt = "def fun(a1, *, kwonly1=None, **kwargs): ...\n"
    expected_txt = (
        "def fun(a1: str, *, kwonly1: int = None, **kwargs: Any) -> None: ...\n"
    )  # noqa
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_complex_sig4_spurious_type_comment() -> None:
    pyi_txt = """
    def fun(
        a1,  # type: str
        *,
        kwonly1,  # type: int
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        ...
    """
    src_txt = """
    def fun(a1,
            *,
            kwonly1=None,  # type: int
            **kwargs
    ):
        ...
    """
    expected_txt = """
    def fun(a1: str,
            *,
            kwonly1: int = None,
            **kwargs: Any
    ) -> None:
        ...
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)


def test_missing_ann_both_incremental() -> None:
    pyi_txt = "def fun(a1) -> None: ...\n"
    src_txt = "def fun(a1) -> None: ...\n"
    expected_txt = "def fun(a1) -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, incremental=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, incremental=True)


def test_missing_ann_both_multiple_args_incremental() -> None:
    pyi_txt = "def fun(a1, a2, *a3, **a4) -> None: ...\n"
    src_txt = "def fun(a1, a2, *a3, **a4) -> None: ...\n"
    expected_txt = "def fun(a1, a2, *a3, **a4) -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, incremental=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, incremental=True)


def test_missing_ann_both_incremental_default_value_whitespace() -> None:
    pyi_txt = "def fun(a1=..., a2: int = 0) -> None: ...\n"
    src_txt = "def fun(a1=False, a2=0) -> None: ...\n"
    expected_txt = "def fun(a1=False, a2: int = 0) -> None: ...\n"
    assert_reapply(pyi_txt, src_txt, expected_txt, incremental=True)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt, incremental=True)
