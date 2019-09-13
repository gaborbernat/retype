from tests.lib import assert_reapply, assert_reapply_visible


def test_missing_trailing_newline_crash() -> None:
    pyi_txt = "def f() -> None: ...\n"
    src_txt = """
    def f():
        pass"""
    expected_txt = """
    def f() -> None:
        pass
    """
    assert_reapply(pyi_txt, src_txt, expected_txt)
    assert_reapply_visible(pyi_txt, src_txt, expected_txt)
