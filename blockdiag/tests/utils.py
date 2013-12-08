# -*- coding: utf-8 -*-

import os
import sys
import shutil
import tempfile
from functools import wraps
from sphinx.application import Sphinx

testdir = os.path.dirname(__file__)


class TestApp(Sphinx):
    def __init__(self, srcdir, buildername='html', confoverrides=None):
        # source settings
        if srcdir is None:
            raise RuntimeError("no srcdir parameter. it should be specified.")
        elif not srcdir.startswith('/'):
            srcdir = os.path.join(testdir, srcdir)

        confdir = srcdir

        # _build/ directory setings
        self.builddir = tempfile.mkdtemp()
        outdir = os.path.join(self.builddir, str(buildername))
        doctreedir = os.path.join(self.builddir, 'doctrees')

        if not os.path.isdir(doctreedir):
            os.makedirs(doctreedir)

        # misc settings
        if confoverrides is None:
            confoverrides = {}

        status = sys.stdout
        warning = sys.stdout

        Sphinx.__init__(self, srcdir, confdir, outdir, doctreedir,
                        buildername, confoverrides, status, warning)

    def cleanup(self, doctrees=False):
        shutil.rmtree(self.builddir, True)


def with_app(*args, **kwargs):
    def testcase(func):
        @wraps(func)
        def decorator(*args2, **kwargs2):
            app = None
            try:
                app = TestApp(*args, **kwargs)
                func(app, *args2, **kwargs2)
            finally:
                if app:
                    app.cleanup()
        return decorator

    return testcase
