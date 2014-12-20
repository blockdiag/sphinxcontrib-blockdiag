# -*- coding: utf-8 -*-

from sphinx_testing import with_app

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

with_png_app = with_app(srcdir='tests/docs/packetdiag',
                        buildername='html',
                        write_docstring=True)
with_svg_app = with_app(srcdir='tests/docs/packetdiag',
                        buildername='html',
                        write_docstring=True,
                        confoverrides={
                            'packetdiag_html_image_format': 'SVG',
                        })


class TestSphinxcontribPacketdiagHTML(unittest.TestCase):
    @with_png_app
    def test_build_png_image(self, app, status, warning):
        """
        .. packetdiag::

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><img .*? src=".*?.png" .*?/></div>')

    @with_png_app
    def test_width_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :width: 88

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="80.0" src="\\1" width="88.0" /></a></div>'))

    @with_png_app
    def test_height_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :height: 80

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="80.0" src="\\1" width="88.0" /></a></div>'))

    @with_png_app
    def test_width_option_and_height_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :width: 100
           :height: 200

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="200.0" src="\\1" width="100.0" /></a></div>'))

    @with_png_app
    def test_scale_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :scale: 25%

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="40.0" src="\\1" width="44.0" /></a></div>'))

    @with_png_app
    def test_width_option_and_scale_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :width: 88
           :scale: 25%

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="20.0" src="\\1" width="22.0" /></a></div>'))

    @with_png_app
    def test_align_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :align: center

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div align="center" class="align-center"><img .*? /></div>')

    @with_png_app
    def test_align_option_and_width_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :align: center
           :width: 88

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div align="center" class="align-center">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="80.0" src="\\1" width="88.0" /></a></div>'))

    @with_png_app
    def test_name_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :name: target

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><img .*? id="target" src=".*?" .*? /></div>')

    @with_png_app
    def test_name_option_and_width_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :name: target
           :width: 88

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="80.0" id="target" src="\\1" width="88.0" /></a></div>'))

    @with_png_app
    def test_href_and_scale_option_on_png(self, app, status, warning):
        """
        .. packetdiag::
           :scale: 50%

           * A [href = 'http://blockdiag.com/'];
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<map name="(map_\d+)">'
                                          '<area shape="rect" coords="32.0,40.0,44.0,60.0" '
                                          'href="http://blockdiag.com/"></map>'
                                          '<img .*? src="\\1" usemap="#\\2" .*?/></a></div>'))

    @with_png_app
    def test_reftarget_in_href_on_png1(self, app, status, warning):
        """
        .. _target:

        heading2
        ---------

        .. packetdiag::

           * A [href = ':ref:`target`'];
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><map name="(map_\d+)">'
                                          '<area shape="rect" coords="64.0,80.0,88.0,120.0" href="#target"></map>'
                                          '<img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_png_app
    def test_reftarget_in_href_on_png2(self, app, status, warning):
        """
        .. _hello world:

        heading2
        ---------

        .. packetdiag::

           * A [href = ':ref:`hello world`'];
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><map name="(map_\d+)">'
                                          '<area shape="rect" coords="64.0,80.0,88.0,120.0" href="#hello-world">'
                                          '</map><img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_png_app
    def test_missing_reftarget_in_href_on_png(self, app, status, warning):
        """
        .. packetdiag::

           * A [href = ':ref:`unknown_target`'];
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><img .*? src=".*?.png" .*?/></div>'))
        self.assertIn('undefined label: unknown_target', warning.getvalue())

    @with_svg_app
    def test_build_svg_image(self, app, status, warning):
        """
        .. packetdiag::

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg .*?>')

    @with_svg_app
    def test_width_option_on_svg(self, app, status, warning):
        """
        .. packetdiag::
           :width: 88

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="80.0" viewBox="0 0 176 160" width="88.0" .*?>')

    @with_svg_app
    def test_height_option_on_svg(self, app, status, warning):
        """
        .. packetdiag::
           :height: 80

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="80.0" viewBox="0 0 176 160" width="88.0" .*?>')

    @with_svg_app
    def test_width_option_and_height_option_on_svg(self, app, status, warning):
        """
        .. packetdiag::
           :width: 100
           :height: 200

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="200.0" viewBox="0 0 176 160" width="100.0" .*?>')

    @with_svg_app
    def test_scale_option_on_svg(self, app, status, warning):
        """
        .. packetdiag::
           :scale: 25%

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="40.0" viewBox="0 0 176 160" width="44.0" .*?>')

    @with_svg_app
    def test_width_option_and_scale_option_on_svg(self, app, status, warning):
        """
        .. packetdiag::
           :width: 88
           :scale: 25%

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="20.0" viewBox="0 0 176 160" width="22.0" .*?>')

    @with_svg_app
    def test_align_option_on_svg(self, app, status, warning):
        """
        .. packetdiag::
           :align: center

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div align="center" class="align-center"><svg .*?>')

    @with_svg_app
    def test_name_option_on_svg(self, app, status, warning):
        """
        .. packetdiag::
           :name: target

           * A
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><span id="target"></span><svg .*?>')

    @with_svg_app
    def test_reftarget_in_href_on_svg1(self, app, status, warning):
        """
        .. _target:

        heading2
        ---------

        .. packetdiag::

           * A [href = ':ref:`target`'];
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<a xlink:href="#target">\\n\\s*<rect .*?>')

    @with_svg_app
    def test_reftarget_in_href_on_svg2(self, app, status, warning):
        """
        .. _hello world:

        heading2
        ---------

        .. packetdiag::

           * A [href = ':ref:`hello world`'];
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>')

    @with_svg_app
    def test_missing_reftarget_in_href_on_svg(self, app, status, warning):
        """
        .. packetdiag::

           * A [href = ':ref:`unknown_target`'];
           * B
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        if sys.version_info < (3, 0):
            self.assertNotRegexpMatches(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>')
        else:
            self.assertNotRegex(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>')
        self.assertIn('undefined label: unknown_target', warning.getvalue())

    @with_svg_app
    def test_attribute_plugin_should_not_effect_to_other_diagram(self, app, status, warning):
        """
        This testcase checks that attribute plugin is unloaded correctly (and it does not effect to other diagram).

        .. packetdiag::

           plugin attributes [property];
           * A_foo [property = foo]

        .. packetdiag::

           * A_foo [property = foo]
        """
        app.builder.build_all()
        self.assertIn('Unknown attribute: FieldItem.property', warning.getvalue())
