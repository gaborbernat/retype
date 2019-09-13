from tests.lib import assert_reapply_raises


def test_print_stmt_crash() -> None:
    pyi_txt = "def f() -> None: ...\n"
    src_txt = """
    import sys

    def f():
        print >>sys.stderr, "Nope"  # funnily, this parses just fine.
        print "This", "will", "fail", "to", "parse"
    """
    exception = assert_reapply_raises(pyi_txt, src_txt, ValueError)
    assert 'Cannot parse: 6:10:     print "This", "will", "fail", "to", "parse"' == str(
        exception
    )
