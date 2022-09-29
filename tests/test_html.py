# -*- coding: utf-8 -*-

import re
import os
import pytest


docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'basic')
subdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'subdir')


with_png_app = pytest.mark.sphinx(srcdir=docs, buildername='html')
with_svg_app = pytest.mark.sphinx(srcdir=docs,
                                  buildername='html',
                                  confoverrides={
                                      'blockdiag_html_image_format': 'SVG'
                                  })


@with_png_app
def test_build_png_image(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<div class="align-default"><img .*? src="_images/.*?.png" .*?/></div>', source)


@pytest.mark.sphinx(srcdir=subdir, buildername='html')
def test_build_png_image_in_subdir(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'subdir' / 'index.html').read_text(encoding='utf-8')
    assert re.search(r'<div class="align-default"><img .*? src="../_images/.*?.png" .*?/></div>', source)


@with_png_app
def test_width_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :width: 224

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<a class="reference internal image-reference" href="(.*?.png)">'
                      '<img height="60.0" src="\\1" width="224.0" /></a></div>'), source)


@with_png_app
def test_height_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :height: 240

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<a class="reference internal image-reference" href="(.*?.png)">'
                      '<img height="240.0" src="\\1" width="896.0" /></a></div>'), source)


@with_png_app
def test_width_option_and_height_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :width: 100
   :height: 200

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text()
    assert re.search(('<div class="align-default">'
                      '<a class="reference internal image-reference" href="(.*?.png)">'
                      '<img height="200.0" src="\\1" width="100.0" /></a></div>'), source)


@with_png_app
def test_scale_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :scale: 25%

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<a class="reference internal image-reference" href="(.*?.png)">'
                      '<img height="30.0" src="\\1" width="112.0" /></a></div>'), source)


@with_png_app
def test_width_option_and_scale_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :width: 28
   :scale: 25%

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<a class="reference internal image-reference" href="(.*?.png)">'
                      '<img height="1.875" src="\\1" width="7.0" /></a></div>'), source)


@with_png_app
def test_align_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :align: center

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<div class="align-center"><img .*? /></div>', source)


@with_png_app
def test_align_option_and_width_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :align: center
   :width: 224

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-center">'
                      '<a class="reference internal image-reference" href="(.*?.png)">'
                      '<img height="60.0" src="\\1" width="224.0" /></a></div>'), source)


@with_png_app
def test_name_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :name: target

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<div class="align-default"><img .*? id="target" src=".*?" .*? /></div>', source)


@with_png_app
def test_name_option_and_width_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :name: target
   :width: 224

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<a class="reference internal image-reference" href="(.*?.png)">'
                      '<img height="60.0" id="target" src="\\1" width="224.0" /></a></div>'), source)


@with_png_app
def test_href_and_scale_option_on_png(app, status, warning):
    doc = """
.. blockdiag::
   :scale: 50%

   A -> B;
   A [href = 'http://blockdiag.com/'];
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<a class="reference internal image-reference" href="(.*?.png)">'
                      '<map name="(map_\\d+)">'
                      '<area shape="rect" coords="32.0,20.0,96.0,40.0" '
                      'href="http://blockdiag.com/"></map>'
                      '<img .*? src="\\1" usemap="#\\2" .*?/></a></div>'), source)


@with_png_app
def test_reftarget_in_href_on_png1(app, status, warning):
    doc = """
.. _target:

heading2
---------

.. blockdiag::

   A -> B;
   A [href = ':ref:`target`'];
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default"><map name="(map_\\d+)">'
                      '<area shape="rect" coords="64.0,40.0,192.0,80.0" href="#target"></map>'
                      '<img .*? src=".*?.png" usemap="#\\1" .*?/></div>'), source)


@with_png_app
def test_reftarget_in_href_on_png2(app, status, warning):
    doc = """
.. _hello world:

heading2
---------

.. blockdiag::

   A -> B;
   A [href = ':ref:`hello world`'];
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default"><map name="(map_\\d+)">'
                      '<area shape="rect" coords="64.0,40.0,192.0,80.0" href="#hello-world">'
                      '</map><img .*? src=".*?.png" usemap="#\\1" .*?/></div>'), source)


@with_png_app
def test_missing_reftarget_in_href_on_png(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
   A [href = ':ref:`unknown_target`'];
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<div class="align-default"><img .*? src=".*?.png" .*?/></div>', source)
    assert 'undefined label: unknown_target' in warning.getvalue()


@pytest.mark.sphinx(srcdir=docs, confoverrides={'blockdiag_html_image_format': 'SVG'})
def test_build_svg_image(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<div class="align-default"><svg .*?>', source)


@with_svg_app
def test_width_option_on_svg(app, status, warning):
    doc = """
.. blockdiag::
   :width: 224

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<svg height="60.0" viewBox="0 0 448 120" width="224.0" .*?>'), source)


@with_svg_app
def test_height_option_on_svg(app, status, warning):
    doc = """
.. blockdiag::
   :height: 240

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<svg height="240.0" viewBox="0 0 448 120" width="896.0" .*?>'), source)


@with_svg_app
def test_width_option_and_height_option_on_svg(app, status, warning):
    doc = """
.. blockdiag::
   :width: 100
   :height: 200

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<svg height="200.0" viewBox="0 0 448 120" width="100.0" .*?>'), source)


@with_svg_app
def test_scale_option_on_svg(app, status, warning):
    doc = """
.. blockdiag::
   :scale: 25%

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<svg height="30.0" viewBox="0 0 448 120" width="112.0" .*?>'), source)


@with_svg_app
def test_width_option_and_scale_option_on_svg(app, status, warning):
    doc = """
.. blockdiag::
   :width: 28
   :scale: 25%

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search(('<div class="align-default">'
                      '<svg height="1.875" viewBox="0 0 448 120" width="7.0" .*?>'), source)


@with_svg_app
def test_align_option_on_svg(app, status, warning):
    doc = """
.. blockdiag::
   :align: center

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<div class="align-center"><svg .*?>', source)


@with_svg_app
def test_name_option_on_svg(app, status, warning):
    doc = """
.. blockdiag::
   :name: target

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<div class="align-default"><span id="target"></span><svg .*?>', source)


@with_svg_app
def test_reftarget_in_href_on_svg1(app, status, warning):
    doc = """
.. _target:

heading2
---------

.. blockdiag::

   A -> B;
   A [href = ':ref:`target`'];
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<a xlink:href="#target">\\n\\s*<rect .*?>\\n\\s*</a>', source)


@with_svg_app
def test_reftarget_in_href_on_svg2(app, status, warning):
    doc = """
.. _hello world:

heading2
---------

.. blockdiag::

   A -> B;
   A [href = ':ref:`hello world`'];
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<a xlink:href="#hello-world">\\n\\s*<rect .*?>\\n\\s*</a>', source)


@with_svg_app
def test_missing_reftarget_in_href_on_svg(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
   A [href = ':ref:`unknown_target`'];
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert not re.search('<a xlink:href="#hello-world">\\n\\s*<rect .*?>\\n\\s*</a>', source)
    assert 'undefined label: unknown_target' in warning.getvalue()


@with_svg_app
def test_autoclass_should_not_effect_to_other_diagram(app, status, warning):
    doc = """
This testcase checks that autoclass plugin is unloaded correctly (and it does not effect to other diagram).

.. blockdiag::

   plugin autoclass;
   class foo [color = red];
   A_foo;

.. blockdiag::

   class foo [color = red];
   A_foo;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'index.html').read_text(encoding='utf-8')
    assert re.search('<text[^>]+>A_foo</text>', source)  # 2nd diagram has a node labeled 'A_foo'.
