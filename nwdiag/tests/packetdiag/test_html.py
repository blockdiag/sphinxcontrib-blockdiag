# -*- coding: utf-8 -*-

import os
import re
from ..utils import with_built_docstring

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

png_config = dict(
    extensions=['sphinxcontrib.packetdiag'],
    master_doc='index',
)

svg_config = dict(
    extensions=['sphinxcontrib.packetdiag'],
    master_doc='index',
    packetdiag_html_image_format='SVG',
)


class TestSphinxcontribPacketdiagHTML(unittest.TestCase):
    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_build_png_image(self, app):
        """
        .. packetdiag::

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><img .*? src=".*?.png" .*?/></div>')

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_width_option_on_png(self, app):
        """
        .. packetdiag::
           :width: 88

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="80.0" src="\\1" width="88.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_height_option_on_png(self, app):
        """
        .. packetdiag::
           :height: 80

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="80.0" src="\\1" width="88.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_width_option_and_height_option_on_png(self, app):
        """
        .. packetdiag::
           :width: 100
           :height: 200

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="200.0" src="\\1" width="100.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_scale_option_on_png(self, app):
        """
        .. packetdiag::
           :scale: 25%

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="40.0" src="\\1" width="44.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_width_option_and_scale_option_on_png(self, app):
        """
        .. packetdiag::
           :width: 88
           :scale: 25%

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="20.0" src="\\1" width="22.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_align_option_on_png(self, app):
        """
        .. packetdiag::
           :align: center

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div align="center" class="align-center"><img .*? /></div>')

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_align_option_and_width_option_on_png(self, app):
        """
        .. packetdiag::
           :align: center
           :width: 88

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div align="center" class="align-center">'
                                              '<a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="80.0" src="\\1" width="88.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_name_option_on_png(self, app):
        """
        .. packetdiag::
           :name: target

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><img .*? id="target" src=".*?" .*? /></div>')

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_name_option_and_width_option_on_png(self, app):
        """
        .. packetdiag::
           :name: target
           :width: 88

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<img height="80.0" id="target" src="\\1" width="88.0" /></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_href_and_scale_option_on_png(self, app):
        """
        .. packetdiag::
           :scale: 50%

           * A [href = 'http://blockdiag.com/'];
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                              '<map name="(map_\d+)">'
                                              '<area shape="rect" coords="32.0,40.0,44.0,60.0" '
                                              'href="http://blockdiag.com/"></map>'
                                              '<img .*? src="\\1" usemap="#\\2" .*?/></a></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_reftarget_in_href_on_png1(self, app):
        """
        .. _target:

        heading2
        ---------

        .. packetdiag::

           * A [href = ':ref:`target`'];
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><map name="(map_\d+)">'
                                              '<area shape="rect" coords="64.0,80.0,88.0,120.0" href="#target"></map>'
                                              '<img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_reftarget_in_href_on_png2(self, app):
        """
        .. _hello world:

        heading2
        ---------

        .. packetdiag::

           * A [href = ':ref:`hello world`'];
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><map name="(map_\d+)">'
                                              '<area shape="rect" coords="64.0,80.0,88.0,120.0" href="#hello-world">'
                                              '</map><img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_built_docstring(buildername='html', confoverrides=png_config)
    def test_missing_reftarget_in_href_on_png(self, app):
        """
        .. packetdiag::

           * A [href = ':ref:`unknown_target`'];
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, ('<div><img .*? src=".*?.png" .*?/></div>'))
            self.assertIn('undefined label: unknown_target',
                          app.builder.warn.call_args_list[0][0][0])

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_build_svg_image(self, app):
        """
        .. packetdiag::

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_on_svg(self, app):
        """
        .. packetdiag::
           :width: 88

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="80.0" viewBox="0 0 176 160" width="88.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_height_option_on_svg(self, app):
        """
        .. packetdiag::
           :height: 80

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="80.0" viewBox="0 0 176 160" width="88.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_and_height_option_on_svg(self, app):
        """
        .. packetdiag::
           :width: 100
           :height: 200

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="200.0" viewBox="0 0 176 160" width="100.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_scale_option_on_svg(self, app):
        """
        .. packetdiag::
           :scale: 25%

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="40.0" viewBox="0 0 176 160" width="44.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_width_option_and_scale_option_on_svg(self, app):
        """
        .. packetdiag::
           :width: 88
           :scale: 25%

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><svg height="20.0" viewBox="0 0 176 160" width="22.0" .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_align_option_on_svg(self, app):
        """
        .. packetdiag::
           :align: center

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div align="center" class="align-center"><svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_name_option_on_svg(self, app):
        """
        .. packetdiag::
           :name: target

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<div><span id="target"></span><svg .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_reftarget_in_href_on_svg1(self, app):
        """
        .. _target:

        heading2
        ---------

        .. packetdiag::

           * A [href = ':ref:`target`'];
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<a xlink:href="#target">\\n\\s*<rect .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_reftarget_in_href_on_svg2(self, app):
        """
        .. _hello world:

        heading2
        ---------

        .. packetdiag::

           * A [href = ':ref:`hello world`'];
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>')

    @with_built_docstring(buildername='html', confoverrides=svg_config)
    def test_missing_reftarget_in_href_on_svg(self, app):
        """
        .. packetdiag::

           * A [href = ':ref:`unknown_target`'];
           * B
        """
        filename = os.path.join(app.outdir, 'index.html')
        with open(filename) as fd:
            source = fd.read()
            if sys.version_info < (3, 0):
                self.assertNotRegexpMatches(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>')
            else:
                self.assertNotRegex(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>')
            self.assertIn('undefined label: unknown_target',
                          app.builder.warn.call_args_list[0][0][0])
