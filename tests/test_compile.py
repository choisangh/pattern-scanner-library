import os
import compileall


def test_compile_package():
    pkg_dir = os.path.join(os.path.dirname(__file__), '..', 'pattern_scanner')
    assert compileall.compile_dir(pkg_dir, quiet=1)
