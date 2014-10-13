# -*- coding: utf-8 -*-

from mock import patch, Mock
from ..utils import FakeSphinx, with_app, with_parsed
import sphinxcontrib.rackdiag
from blockdiag.utils.compat import u

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestSphinxcontribRackdiagErrors(unittest.TestCase):
    def setUp(self):
        self.app = FakeSphinx()
        sphinxcontrib.rackdiag.setup(self.app)

    def tearDown(self):
        self.app.cleanup()

    @with_parsed()
    def test_parse_error(self, nodes):
        """
        .. rackdiag::

           {
             * A
             * B
        """
        self.assertEqual([], nodes)

    @with_app(srcdir='docs/rackdiag', confoverrides=dict(rackdiag_html_image_format='JPG'))
    def test_unknown_format_error(self, app):
        app.builder.warn = Mock()
        app.builder.build_all()

        self.assertIn('unknown format: JPG',
                      app.builder.warn.call_args_list[0][0][0])

    @with_app(srcdir='docs/rackdiag', confoverrides=dict(rackdiag_html_image_format='PDF'))
    def test_reportlab_not_found_error(self, app):
        try:
            # unload reportlab and make loading it impossible
            sys.modules.pop('reportlab', None)
            path = sys.path
            sys.path = []

            app.builder.warn = Mock()
            app.builder.build_all()

            self.assertIn('Could not output PDF format. Install reportlab.',
                          app.builder.warn.call_args_list[0][0][0])
        finally:
            sys.path = path

    @with_app(srcdir='docs/rackdiag')
    @patch("rackdiag.utils.rst.nodes.rackdiag.processor.drawer.DiagramDraw")
    def test_rendering_error(self, app, DiagramDraw):
        DiagramDraw.side_effect = RuntimeError("UNKNOWN ERROR!")
        app.builder.warn = Mock()
        app.builder.build_all()

        self.assertIn('UNKNOWN ERROR!',
                      app.builder.warn.call_args_list[0][0][0])

    @with_app(srcdir='docs/rackdiag')
    @patch("sphinxcontrib.rackdiag.rackdiag.drawer.DiagramDraw.draw")
    def test_font_settings_error(self, app, draw):
        draw.side_effect = UnicodeEncodeError("", u(""), 0, 0, "")
        app.builder.warn = Mock()
        app.builder.build_all()

        self.assertIn('UnicodeEncodeError caught (check your font settings)',
                      app.builder.warn.call_args_list[0][0][0])
