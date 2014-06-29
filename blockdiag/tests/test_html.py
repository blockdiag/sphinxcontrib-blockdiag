# -*- coding: utf-8 -*-

import os
import re
from .utils import with_built_docstring

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

png_config = dict(
    extensions=['sphinxcontrib.blockdiag'],
    master_doc='index',
)

svg_config = dict(
    extensions=['sphinxcontrib.blockdiag'],
    master_doc='index',
    blockdiag_html_image_format='SVG',
)


class TestSphinxcontribBlockdiagHTML(unittest.TestCase):
    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_build_png_image(self, app):
        """
        .. blockdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<img src=".*?.png.*?/>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_build_svg_image(self, app):
        """
        .. blockdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_on_svg(self, app):
        """
        .. blockdiag::
           :width: 224

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<svg height="60.0" viewBox="0 0 448 120" width="224.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_height_option_on_svg(self, app):
        """
        .. blockdiag::
           :height: 240

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<svg height="240.0" viewBox="0 0 448 120" width="896.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_and_height_option_on_svg(self, app):
        """
        .. blockdiag::
           :width: 100
           :height: 200

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<svg height="200.0" viewBox="0 0 448 120" width="100.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_scale_option_on_svg(self, app):
        """
        .. blockdiag::
           :scale: 25%

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<svg height="30.0" viewBox="0 0 448 120" width="112.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_and_scale_option_on_svg(self, app):
        """
        .. blockdiag::
           :width: 28
           :scale: 25%

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<svg height="1.875" viewBox="0 0 448 120" width="7.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_align_option_on_svg(self, app):
        """
        .. blockdiag::
           :align: center

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div align="center" class="align-center"><svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_name_option_on_svg(self, app):
        """
        .. blockdiag::
           :name: target

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<span id="target"></span><svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_reftarget_in_href_on_svg(self, app):
        """
        .. _target:

        heading2
        ---------

        .. blockdiag::

           A -> B;
           A [href = ':ref:`target`'];
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<a xlink:href="#target">\\n\\s*<rect .*?>\\n\\s*</a>')
