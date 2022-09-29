# -*- coding: utf-8 -*-

import os
import re

import unittest
import pytest

docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'basic')

CR = "\r?\n"

blockdiag_fontpath = '/usr/share/fonts/truetype/ipafont/ipagp.ttf'
with_png_app = pytest.mark.sphinx(srcdir=docs,
                                  buildername='latex',
                                  confoverrides={
                                      'latex_documents': [('index', 'test.tex', '', 'test', 'manual')],
                                  })
with_pdf_app = pytest.mark.sphinx(srcdir=docs,
                                  buildername='latex',
                                  confoverrides={
                                      'latex_documents': [('index', 'test.tex', '', 'test', 'manual')],
                                      'blockdiag_latex_image_format': 'PDF',
                                      'blockdiag_fontpath': blockdiag_fontpath,
                                  })
with_oldpdf_app = pytest.mark.sphinx(srcdir=docs,
                                     buildername='latex',
                                     confoverrides={
                                         'latex_documents': [('index', 'test.tex', '', 'test', 'manual')],
                                         'blockdiag_tex_image_format': 'PDF',
                                         'blockdiag_fontpath': blockdiag_fontpath,
                                     })


@with_png_app
def test_build_png_image(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search(r'\\sphinxincludegraphics{{blockdiag-.*?}.png}', source)


@unittest.skipUnless(os.path.exists(blockdiag_fontpath), "TrueType font not found")
@with_pdf_app
def test_build_pdf_image1(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search(r'\\sphinxincludegraphics{{blockdiag-.*?}.pdf}', source)


@unittest.skipUnless(os.path.exists(blockdiag_fontpath), "TrueType font not found")
@with_oldpdf_app
def test_build_pdf_image2(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search(r'\\sphinxincludegraphics{{blockdiag-.*?}.pdf}', source)


@with_png_app
def test_width_option(app, status, warning):
    doc = """
.. blockdiag::
   :width: 3cm

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search(r'\\sphinxincludegraphics\[width=3cm\]{{blockdiag-.*?}.png}', source)


@with_png_app
def test_height_option(app, status, warning):
    doc = """
.. blockdiag::
   :height: 4cm

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search(r'\\sphinxincludegraphics\[height=4cm\]{{blockdiag-.*?}.png}', source)


@with_png_app
def test_scale_option(app, status, warning):
    doc = """
.. blockdiag::
   :scale: 50%

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search(r'\\sphinxincludegraphics\[scale=0.5\]{{blockdiag-.*?}.png}', source)


@with_png_app
def test_align_option_left(app, status, warning):
    doc = """
.. blockdiag::
   :align: left

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search((r'{\\sphinxincludegraphics{{blockdiag-.*?}.png}'
                      r'\\hspace\*{\\fill}}'), source)


@with_png_app
def test_align_option_center(app, status, warning):
    doc = """
.. blockdiag::
   :align: center

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search((r'{\\hspace\*{\\fill}'
                      r'\\sphinxincludegraphics{{blockdiag-.*?}.png}'
                      r'\\hspace\*{\\fill}}'), source)


@with_png_app
def test_align_option_right(app, status, warning):
    doc = """
.. blockdiag::
   :align: right

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search((r'{\\hspace\*{\\fill}'
                      r'\\sphinxincludegraphics{{blockdiag-.*?}.png}}'), source)


@with_png_app
def test_caption_option(app, status, warning):
    doc = """
.. blockdiag::
   :caption: hello world

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')

    figure = re.compile((r'\\begin{figure}\[htbp\]' + CR +
                         r'\\centering' + CR +
                         r'\\capstart' + CR + CR +
                         r'\\noindent\\sphinxincludegraphics{{blockdiag-.*?}.png}' + CR +
                         r'\\caption{hello world}\\label{\\detokenize{index:id1}}\\end{figure}'),
                        re.DOTALL)
    assert re.search(figure, source)


@with_png_app
def test_caption_option_and_align_option(app, status, warning):
    doc = """
.. blockdiag::
   :align: left
   :caption: hello world

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')

    figure = re.compile((r'\\begin{wrapfigure}{l}{0pt}' + CR +
                         r'\\centering' + CR +
                         r'\\noindent\\sphinxincludegraphics{{blockdiag-.*?}.png}' + CR +
                         r'\\caption{hello world}\\label{\\detokenize{index:id1}}\\end{wrapfigure}'),
                        re.DOTALL)
    assert re.search(figure, source)


@with_png_app
def test_href(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
   A [href = ':ref:`target`'];
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
    assert re.search(r'\\sphinxincludegraphics{{blockdiag-.*?}.png}', source)
