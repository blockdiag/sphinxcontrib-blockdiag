# -*- coding: utf-8 -*-

from sphinx_testing import with_app

import unittest


with_png_app = with_app(srcdir='tests/docs/basic',
                        buildername='html',
                        write_docstring=True)
with_svg_app = with_app(srcdir='tests/docs/basic',
                        buildername='html',
                        write_docstring=True,
                        confoverrides={
                            'blockdiag_html_image_format': 'SVG'
                        })


class TestSphinxcontribBlockdiagHTML(unittest.TestCase):
    @with_png_app
    def test_build_png_image(self, app, status, warning):
        """
        .. blockdiag::

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div class="align-default"><img .*? src="_images/.*?.png" .*?/></div>')

    @with_app(srcdir='tests/docs/subdir', buildername='html', write_docstring=True)
    def test_build_png_image_in_subdir(self, app, status, warning):
        """
        .. blockdiag::

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'subdir' / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, r'<div class="align-default"><img .*? src="../_images/.*?.png" .*?/></div>')

    @with_png_app
    def test_width_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :width: 224

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="60.0" src="\\1" width="224.0" /></a></div>'))

    @with_png_app
    def test_height_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :height: 240

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="240.0" src="\\1" width="896.0" /></a></div>'))

    @with_png_app
    def test_width_option_and_height_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :width: 100
           :height: 200

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text()
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="200.0" src="\\1" width="100.0" /></a></div>'))

    @with_png_app
    def test_scale_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :scale: 25%

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="30.0" src="\\1" width="112.0" /></a></div>'))

    @with_png_app
    def test_width_option_and_scale_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :width: 28
           :scale: 25%

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="1.875" src="\\1" width="7.0" /></a></div>'))

    @with_png_app
    def test_align_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :align: center

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div class="align-center"><img .*? /></div>')

    @with_png_app
    def test_align_option_and_width_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :align: center
           :width: 224

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-center">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="60.0" src="\\1" width="224.0" /></a></div>'))

    @with_png_app
    def test_name_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :name: target

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div class="align-default"><img .*? id="target" src=".*?" .*? /></div>')

    @with_png_app
    def test_name_option_and_width_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :name: target
           :width: 224

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<img height="60.0" id="target" src="\\1" width="224.0" /></a></div>'))

    @with_png_app
    def test_href_and_scale_option_on_png(self, app, status, warning):
        """
        .. blockdiag::
           :scale: 50%

           A -> B;
           A [href = 'http://blockdiag.com/'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<a class="reference internal image-reference" href="(.*?.png)">'
                                          '<map name="(map_\\d+)">'
                                          '<area shape="rect" coords="32.0,20.0,96.0,40.0" '
                                          'href="http://blockdiag.com/"></map>'
                                          '<img .*? src="\\1" usemap="#\\2" .*?/></a></div>'))

    @with_png_app
    def test_reftarget_in_href_on_png1(self, app, status, warning):
        """
        .. _target:

        heading2
        ---------

        .. blockdiag::

           A -> B;
           A [href = ':ref:`target`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default"><map name="(map_\\d+)">'
                                          '<area shape="rect" coords="64.0,40.0,192.0,80.0" href="#target"></map>'
                                          '<img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_png_app
    def test_reftarget_in_href_on_png2(self, app, status, warning):
        """
        .. _hello world:

        heading2
        ---------

        .. blockdiag::

           A -> B;
           A [href = ':ref:`hello world`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default"><map name="(map_\\d+)">'
                                          '<area shape="rect" coords="64.0,40.0,192.0,80.0" href="#hello-world">'
                                          '</map><img .*? src=".*?.png" usemap="#\\1" .*?/></div>'))

    @with_png_app
    def test_missing_reftarget_in_href_on_png(self, app, status, warning):
        """
        .. blockdiag::

           A -> B;
           A [href = ':ref:`unknown_target`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default"><img .*? src=".*?.png" .*?/></div>'))
        self.assertIn('undefined label: unknown_target', warning.getvalue())

    @with_app(srcdir='tests/docs/basic', copy_srcdir_to_tmpdir=True,
              write_docstring=True, confoverrides={'blockdiag_html_image_format': 'SVG'})
    def test_build_svg_image(self, app, status, warning):
        """
        .. blockdiag::

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div class="align-default"><svg .*?>')

    @with_svg_app
    def test_width_option_on_svg(self, app, status, warning):
        """
        .. blockdiag::
           :width: 224

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<svg height="60.0" viewBox="0 0 448 120" width="224.0" .*?>'))

    @with_svg_app
    def test_height_option_on_svg(self, app, status, warning):
        """
        .. blockdiag::
           :height: 240

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<svg height="240.0" viewBox="0 0 448 120" width="896.0" .*?>'))

    @with_svg_app
    def test_width_option_and_height_option_on_svg(self, app, status, warning):
        """
        .. blockdiag::
           :width: 100
           :height: 200

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<svg height="200.0" viewBox="0 0 448 120" width="100.0" .*?>'))

    @with_svg_app
    def test_scale_option_on_svg(self, app, status, warning):
        """
        .. blockdiag::
           :scale: 25%

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<svg height="30.0" viewBox="0 0 448 120" width="112.0" .*?>'))

    @with_svg_app
    def test_width_option_and_scale_option_on_svg(self, app, status, warning):
        """
        .. blockdiag::
           :width: 28
           :scale: 25%

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, ('<div class="align-default">'
                                          '<svg height="1.875" viewBox="0 0 448 120" width="7.0" .*?>'))

    @with_svg_app
    def test_align_option_on_svg(self, app, status, warning):
        """
        .. blockdiag::
           :align: center

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div class="align-center"><svg .*?>')

    @with_svg_app
    def test_name_option_on_svg(self, app, status, warning):
        """
        .. blockdiag::
           :name: target

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<div class="align-default"><span id="target"></span><svg .*?>')

    @with_svg_app
    def test_reftarget_in_href_on_svg1(self, app, status, warning):
        """
        .. _target:

        heading2
        ---------

        .. blockdiag::

           A -> B;
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

        .. blockdiag::

           A -> B;
           A [href = ':ref:`hello world`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>\\n\\s*</a>')

    @with_svg_app
    def test_missing_reftarget_in_href_on_svg(self, app, status, warning):
        """
        .. blockdiag::

           A -> B;
           A [href = ':ref:`unknown_target`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertNotRegex(source, '<a xlink:href="#hello-world">\\n\\s*<rect .*?>\\n\\s*</a>')
        self.assertIn('undefined label: unknown_target', warning.getvalue())

    @with_svg_app
    def test_autoclass_should_not_effect_to_other_diagram(self, app, status, warning):
        """
        This testcase checks that autoclass plugin is unloaded correctly (and it does not effect to other diagram).

        .. blockdiag::

           plugin autoclass;
           class foo [color = red];
           A_foo;

        .. blockdiag::

           class foo [color = red];
           A_foo;
        """
        app.builder.build_all()
        source = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '<text[^>]+>A_foo</text>')  # 2nd diagram has a node labeled 'A_foo'.
