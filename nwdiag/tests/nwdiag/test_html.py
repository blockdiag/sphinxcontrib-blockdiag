# -*- coding: utf-8 -*-

from sphinx_testing import with_app

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

with_png_app = with_app(srcdir='tests/docs/nwdiag',
                        buildername='html',
                        write_docstring=True)
with_svg_app = with_app(srcdir='tests/docs/nwdiag',
                        buildername='html',
                        write_docstring=True,
                        confoverrides={
                            'nwdiag_html_image_format': 'SVG',
                        })


class TestSphinxcontribNwdiagHTML(unittest.TestCase):
    @with_png_app
    def test_build_png_image(self, app, status, warning):
        """
        .. nwdiag::

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><img .*? src=".*?.png" .*?/></div>')

    @with_png_app
    def test_width_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :width: 228

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="150.0" src="\\1" width="228.0" /></a></div>'))

    @with_png_app
    def test_height_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :height: 150

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="150.0" src="\\1" width="228.0" /></a></div>'))

    @with_png_app
    def test_width_option_and_height_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :width: 100
           :height: 200

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="200.0" src="\\1" width="100.0" /></a></div>'))

    @with_png_app
    def test_scale_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :scale: 25%

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="75.0" src="\\1" width="114.0" /></a></div>'))

    @with_png_app
    def test_width_option_and_scale_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :width: 228
           :scale: 25%

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="37.5" src="\\1" width="57.0" /></a></div>'))

    @with_png_app
    def test_align_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :align: center

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div align="center" class="align-center"><img .*? /></div>')

    @with_png_app
    def test_align_option_and_width_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :align: center
           :width: 228

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div align="center" class="align-center">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="150.0" src="\\1" width="228.0" /></a></div>'))

    @with_png_app
    def test_name_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :name: target

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><img .*? id="target" src=".*?" .*? /></div>')

    @with_png_app
    def test_name_option_and_width_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :name: target
           :width: 228

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="150.0" id="target" src="\\1" width="228.0" /></a></div>'))

    @with_png_app
    def test_href_and_scale_option_on_png(self, app, status, warning):
        """
        .. nwdiag::
           :scale: 50%

           network { A; B; }
           A [href = 'http://blockdiag.com/'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><a class="reference internal image-reference" href="(.*?.png)">'
                                          '<map name="(map_\d+)">'
                                          '<area shape="rect" coords="76.0,78.0,128.0,98.0" '
                                          'href="http://blockdiag.com/"></map>'
                                          '<img .*? src="\\1" usemap="#\\2" .*?/></a></div>'))

    @with_png_app
    def test_reftarget_in_href_on_png1(self, app, status, warning):
        """
        .. _target:

        heading2
        ---------

        .. nwdiag::

           network { A; B; }
           A [href = ':ref:`target`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><map name="(map_\d+)">'
                                          '<area shape="rect" coords="152.0,156.0,256.0,196.0" href="#target"></map>'
                                          '<img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_png_app
    def test_reftarget_in_href_on_png2(self, app, status, warning):
        """
        .. _hello world:

        heading2
        ---------

        .. nwdiag::

           network { A; B; }
           A [href = ':ref:`hello world`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><map name="(map_\d+)">'
                                          '<area shape="rect" coords="152.0,156.0,256.0,196.0" href="#hello-world">'
                                          '</map><img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_png_app
    def test_missing_reftarget_in_href_on_png(self, app, status, warning):
        """
        .. nwdiag::

           network { A; B; }
           A [href = ':ref:`unknown_target`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div><img .*? src=".*?.png" .*?/></div>'))
        self.assertIn('undefined label: unknown_target', warning.getvalue())

    @with_svg_app
    def test_build_svg_image(self, app, status, warning):
        """
        .. nwdiag::

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg .*?>')

    @with_svg_app
    def test_width_option_on_svg(self, app, status, warning):
        """
        .. nwdiag::
           :width: 228

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="150.0" viewBox="0 0 456 300" width="228.0" .*?>')

    @with_svg_app
    def test_height_option_on_svg(self, app, status, warning):
        """
        .. nwdiag::
           :height: 150

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="150.0" viewBox="0 0 456 300" width="228.0" .*?>')

    @with_svg_app
    def test_width_option_and_height_option_on_svg(self, app, status, warning):
        """
        .. nwdiag::
           :width: 100
           :height: 200

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="200.0" viewBox="0 0 456 300" width="100.0" .*?>')

    @with_svg_app
    def test_scale_option_on_svg(self, app, status, warning):
        """
        .. nwdiag::
           :scale: 25%

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="75.0" viewBox="0 0 456 300" width="114.0" .*?>')

    @with_svg_app
    def test_width_option_and_scale_option_on_svg(self, app, status, warning):
        """
        .. nwdiag::
           :width: 228
           :scale: 25%

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div><svg height="37.5" viewBox="0 0 456 300" width="57.0" .*?>')

    @with_svg_app
    def test_align_option_on_svg(self, app, status, warning):
        """
        .. nwdiag::
           :align: center

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div align="center" class="align-center"><svg .*?>')

    @with_svg_app
    def test_name_option_on_svg(self, app, status, warning):
        """
        .. nwdiag::
           :name: target

           network { A; B; }
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

        .. nwdiag::

           network { A; B; }
           A [href = ':ref:`target`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<a xlink:href="#target">\\n\\s*<rect .*?>\\n\\s*</a>')

    @with_svg_app
    def test_reftarget_in_href_on_svg2(self, app, status, warning):
        """
        .. _hello world:

        heading2
        ---------

        .. nwdiag::

           network { A; B; }
           A [href = ':ref:`hello world`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>\\n\\s*</a>')

    @with_svg_app
    def test_missing_reftarget_in_href_on_svg(self, app, status, warning):
        """
        .. nwdiag::

           network { A; B; }
           A [href = ':ref:`unknown_target`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        if sys.version_info < (3, 0):
            self.assertNotRegexpMatches(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>\\n\\s*</a>')
        else:
            self.assertNotRegex(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>\\n\\s*</a>')
        self.assertIn('undefined label: unknown_target', warning.getvalue())

    @with_svg_app
    def test_autoclass_should_not_effect_to_other_diagram(self, app, status, warning):
        """
        This testcase checks that autoclass plugin is unloaded correctly (and it does not effect to other diagram).

        .. nwdiag::

           plugin autoclass;
           class foo [color = red];
           network { A_foo; }

        .. nwdiag::

           class foo [color = red];
           network { A_foo; }
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<text[^>]+>A_foo</text>')  # 2nd diagram has a node labeled 'A_foo'.
