# -*- coding: utf-8 -*-

from mock import patch
from .utils import FakeSphinx, with_app, with_parsed
import sphinxcontrib.blockdiag
from blockdiag.utils.compat import u

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestSphinxcontribBlockdiagErrors(unittest.TestCase):
    def setUp(self):
        self.app = FakeSphinx()
        sphinxcontrib.blockdiag.setup(self.app)

    def tearDown(self):
        self.app.cleanup()

    @with_parsed()
    def test_parse_error(self, nodes):
        """
        .. blockdiag::

           { A -> B;
        """
        self.assertEqual([], nodes)

    @with_app(srcdir='docs/basic', confoverrides=dict(blockdiag_html_image_format='JPG'))
    def test_unknown_format_error(self, app, status, warning):
        app.builder.build_all()
        self.assertIn('unknown format: JPG', warning.getvalue())

    @with_app(srcdir='docs/basic', confoverrides=dict(blockdiag_html_image_format='PDF'))
    def test_reportlab_not_found_error(self, app, status, warning):
        try:
            # unload reportlab and make loading it impossible
            sys.modules.pop('reportlab', None)
            path = sys.path
            sys.path = []

            app.builder.build_all()

            self.assertIn('Could not output PDF format. Install reportlab.',
                          warning.getvalue())
        finally:
            sys.path = path

    @with_app(srcdir='docs/basic')
    @patch("blockdiag.utils.rst.nodes.blockdiag.processor.drawer.DiagramDraw")
    def test_rendering_error(self, app, status, warning, DiagramDraw):
        DiagramDraw.side_effect = RuntimeError("UNKNOWN ERROR!")
        app.builder.build_all()
        self.assertIn('UNKNOWN ERROR!', warning.getvalue())

    @with_app(srcdir='docs/basic')
    @patch("sphinxcontrib.blockdiag.blockdiag.drawer.DiagramDraw.draw")
    def test_font_settings_error(self, app, status, warning, draw):
        draw.side_effect = UnicodeEncodeError("", u(""), 0, 0, "")
        app.builder.build_all()
        self.assertIn('UnicodeEncodeError caught (check your font settings)',
                      warning.getvalue())
