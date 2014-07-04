# -*- coding: utf-8 -*-

import os
from ..utils import with_built_docstring

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

png_config = dict(
    extensions=['sphinxcontrib.nwdiag'],
    master_doc='index',
)

svg_config = dict(
    extensions=['sphinxcontrib.nwdiag'],
    master_doc='index',
    nwdiag_html_image_format='SVG',
)


class TestSphinxcontribNwdiagHTML(unittest.TestCase):
    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_build_png_image(self, app):
        """
        .. nwdiag::

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><img .*? src=".*?.png" .*?/></div>')

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_width_option_on_png(self, app):
        """
        .. nwdiag::
           :width: 228

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="150.0" src="\\1" width="228.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_height_option_on_png(self, app):
        """
        .. nwdiag::
           :height: 150

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="150.0" src="\\1" width="228.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_width_option_and_height_option_on_png(self, app):
        """
        .. nwdiag::
           :width: 100
           :height: 200

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="200.0" src="\\1" width="100.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_scale_option_on_png(self, app):
        """
        .. nwdiag::
           :scale: 25%

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="75.0" src="\\1" width="114.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_width_option_and_scale_option_on_png(self, app):
        """
        .. nwdiag::
           :width: 228
           :scale: 25%

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="37.5" src="\\1" width="57.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_align_option_on_png(self, app):
        """
        .. nwdiag::
           :align: center

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div align="center" class="align-center"><img .*? /></div>')

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_align_option_and_width_option_on_png(self, app):
        """
        .. nwdiag::
           :align: center
           :width: 228

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div align="center" class="align-center">'
                                              '<a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="150.0" src="\\1" width="228.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_name_option_on_png(self, app):
        """
        .. nwdiag::
           :name: target

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><img .*? id="target" src=".*?" .*? /></div>')

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_name_option_and_width_option_on_png(self, app):
        """
        .. nwdiag::
           :name: target
           :width: 228

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="150.0" id="target" src="\\1" width="228.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_href_and_scale_option_on_png(self, app):
        """
        .. nwdiag::
           :scale: 50%

           network { A; B; }
           A [href = 'http://blockdiag.com/'];
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<map name="(map_\d+)">'
                                              '<area shape="rect" coords="76.0,78.0,128.0,98.0" '
                                              'href="http://blockdiag.com/"></map>'
                                              '<img .*? src="\\1" usemap="#\\2" .*?/></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_reftarget_in_href_on_png(self, app):
        """
        .. _target:

        heading2
        ---------

        .. nwdiag::

           network { A; B; }
           A [href = ':ref:`target`'];
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><map name="(map_\d+)">'
                                              '<area shape="rect" coords="152.0,156.0,256.0,196.0" href="#target"></map>'
                                              '<img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_build_svg_image(self, app):
        """
        .. nwdiag::

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_on_svg(self, app):
        """
        .. nwdiag::
           :width: 228

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="150.0" viewBox="0 0 456 300" width="228.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_height_option_on_svg(self, app):
        """
        .. nwdiag::
           :height: 150

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="150.0" viewBox="0 0 456 300" width="228.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_and_height_option_on_svg(self, app):
        """
        .. nwdiag::
           :width: 100
           :height: 200

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="200.0" viewBox="0 0 456 300" width="100.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_scale_option_on_svg(self, app):
        """
        .. nwdiag::
           :scale: 25%

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="75.0" viewBox="0 0 456 300" width="114.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_and_scale_option_on_svg(self, app):
        """
        .. nwdiag::
           :width: 228
           :scale: 25%

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="37.5" viewBox="0 0 456 300" width="57.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_align_option_on_svg(self, app):
        """
        .. nwdiag::
           :align: center

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div align="center" class="align-center"><svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_name_option_on_svg(self, app):
        """
        .. nwdiag::
           :name: target

           network { A; B; }
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><span id="target"></span><svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_reftarget_in_href_on_svg(self, app):
        """
        .. _target:

        heading2
        ---------

        .. nwdiag::

           network { A; B; }
           A [href = ':ref:`target`'];
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<a xlink:href="#target">\\n\\s*<rect .*?>\\n\\s*</a>')
