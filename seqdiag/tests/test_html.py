# -*- coding: utf-8 -*-

import os
from .utils import with_built_docstring

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

png_config = dict(
    extensions=['sphinxcontrib.seqdiag'],
    master_doc='index',
)

svg_config = dict(
    extensions=['sphinxcontrib.seqdiag'],
    master_doc='index',
    seqdiag_html_image_format='SVG',
)


class TestSphinxcontribSeqdiagHTML(unittest.TestCase):
    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_build_png_image(self, app):
        """
        .. seqdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><img .*? src=".*?.png" .*?/></div>')

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_width_option_on_png(self, app):
        """
        .. seqdiag::
           :width: 224

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="97.0" src="\\1" width="224.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_height_option_on_png(self, app):
        """
        .. seqdiag::
           :height: 97

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="97.0" src="\\1" width="224.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_width_option_and_height_option_on_png(self, app):
        """
        .. seqdiag::
           :width: 100
           :height: 200

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="200.0" src="\\1" width="100.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_scale_option_on_png(self, app):
        """
        .. seqdiag::
           :scale: 25%

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="48.5" src="\\1" width="112.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_width_option_and_scale_option_on_png(self, app):
        """
        .. seqdiag::
           :width: 28
           :scale: 25%

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="3.03125" src="\\1" width="7.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_align_option_on_png(self, app):
        """
        .. seqdiag::
           :align: center

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div align="center" class="align-center"><img .*? /></div>')

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_align_option_and_width_option_on_png(self, app):
        """
        .. seqdiag::
           :align: center
           :width: 224

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div align="center" class="align-center">'
                                              '<a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="97.0" src="\\1" width="224.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_name_option_on_png(self, app):
        """
        .. seqdiag::
           :name: target

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><img .*? id="target" src=".*?" .*? /></div>')

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_name_option_and_width_option_on_png(self, app):
        """
        .. seqdiag::
           :name: target
           :width: 224

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="97.0" id="target" src="\\1" width="224.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_href_and_scale_option_on_png(self, app):
        """
        .. seqdiag::
           :scale: 50%

           A -> B;
           A [href = 'http://blockdiag.com/'];
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<map name="(map_\d+)">'
                                              '<area shape="rect" coords="32.0,20.0,96.0,40.0" '
                                              'href="http://blockdiag.com/"></map>'
                                              '<img .*? src="\\1" usemap="#\\2" .*?/></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_reftarget_in_href_on_png(self, app):
        """
        .. _target:

        heading2
        ---------

        .. seqdiag::

           A -> B;
           A [href = ':ref:`target`'];
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><map name="(map_\d+)">'
                                              '<area shape="rect" coords="64.0,40.0,192.0,80.0" href="#target"></map>'
                                              '<img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_build_svg_image(self, app):
        """
        .. seqdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_on_svg(self, app):
        """
        .. seqdiag::
           :width: 224

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="97.0" viewBox="0 0 448 194" width="224.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_height_option_on_svg(self, app):
        """
        .. seqdiag::
           :height: 97

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="97.0" viewBox="0 0 448 194" width="224.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_and_height_option_on_svg(self, app):
        """
        .. seqdiag::
           :width: 100
           :height: 200

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="200.0" viewBox="0 0 448 194" width="100.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_scale_option_on_svg(self, app):
        """
        .. seqdiag::
           :scale: 25%

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="48.5" viewBox="0 0 448 194" width="112.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_and_scale_option_on_svg(self, app):
        """
        .. seqdiag::
           :width: 28
           :scale: 25%

           A -> B;
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="3.03125" viewBox="0 0 448 194" width="7.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_align_option_on_svg(self, app):
        """
        .. seqdiag::
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
        .. seqdiag::
           :name: target

           A -> B;
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

        .. seqdiag::

           A -> B;
           A [href = ':ref:`target`'];
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<a xlink:href="#target">\\n\\s*<rect .*?>\\n\\s*</a>')
