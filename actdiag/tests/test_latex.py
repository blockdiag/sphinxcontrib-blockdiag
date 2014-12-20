# -*- coding: utf-8 -*-

import os
import re
from sphinx_testing import with_app
from blockdiag.utils.compat import u

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

actdiag_fontpath = '/usr/share/fonts/truetype/ipafont/ipagp.ttf'
with_png_app = with_app(srcdir='tests/docs/basic',
                        buildername='latex',
                        write_docstring=True,
                        confoverrides={
                            'latex_documents': [('index', 'test.tex', u(''), u('test'), 'manual')],
                        })
with_pdf_app = with_app(srcdir='tests/docs/basic',
                        buildername='latex',
                        write_docstring=True,
                        confoverrides={
                            'latex_documents': [('index', 'test.tex', u(''), u('test'), 'manual')],
                            'actdiag_latex_image_format': 'PDF',
                            'actdiag_fontpath': actdiag_fontpath,
                        })
with_oldpdf_app = with_app(srcdir='tests/docs/basic',
                           buildername='latex',
                           write_docstring=True,
                           confoverrides={
                               'latex_documents': [('index', 'test.tex', u(''), u('test'), 'manual')],
                               'actdiag_tex_image_format': 'PDF',
                               'actdiag_fontpath': actdiag_fontpath,
                           })


class TestSphinxcontribActdiagLatex(unittest.TestCase):
    @with_png_app
    def test_build_png_image(self, app, status, warning):
        """
        .. actdiag::

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/actdiag-.*?.png}')

    @unittest.skipUnless(os.path.exists(actdiag_fontpath), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_pdf_app
    def test_build_pdf_image1(self, app, status, warning):
        """
        .. actdiag::

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/actdiag-.*?.pdf}')

    @unittest.skipUnless(os.path.exists(actdiag_fontpath), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_oldpdf_app
    def test_build_pdf_image2(self, app, status, warning):
        """
        .. actdiag::

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/actdiag-.*?.pdf}')

    @with_png_app
    def test_width_option(self, app, status, warning):
        """
        .. actdiag::
           :width: 3cm

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics\\[width=3cm\\]{.*?/latex/actdiag-.*?.png}')

    @with_png_app
    def test_height_option(self, app, status, warning):
        """
        .. actdiag::
           :height: 4cm

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics\\[height=4cm\\]{.*?/latex/actdiag-.*?.png}')

    @with_png_app
    def test_scale_option(self, app, status, warning):
        """
        .. actdiag::
           :scale: 50%

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\scalebox{0.500000}{\\\\includegraphics{.*?/latex/actdiag-.*?.png}}')

    @with_png_app
    def test_align_option_left(self, app, status, warning):
        """
        .. actdiag::
           :align: left

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '{\\\\includegraphics{.*?/latex/actdiag-.*?.png}\\\\hfill}')

    @with_png_app
    def test_align_option_center(self, app, status, warning):
        """
        .. actdiag::
           :align: center

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/latex/actdiag-.*?.png}\\\\hfill}')

    @with_png_app
    def test_align_option_right(self, app, status, warning):
        """
        .. actdiag::
           :align: right

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/latex/actdiag-.*?.png}}')

    @with_png_app
    def test_caption_option(self, app, status, warning):
        """
        .. actdiag::
           :caption: hello world

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/actdiag-.*?.png}')

        figure = re.compile('\\\\begin{figure}\\[htbp\\]\n\\\\centering.*?'
                            '\\\\caption{hello world}\\\\end{figure}', re.DOTALL)
        self.assertRegexpMatches(source, figure)

    @with_png_app
    def test_caption_option_and_align_option(self, app, status, warning):
        """
        .. actdiag::
           :align: left
           :caption: hello world

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/actdiag-.*?.png}')

        figure = re.compile('\\\\begin{figure}\\[htbp\\]\\\\begin{flushleft}.*?'
                            '\\\\caption{hello world}\\\\end{flushleft}\\\\end{figure}', re.DOTALL)
        self.assertRegexpMatches(source, figure)

    @with_png_app
    def test_href(self, app, status, warning):
        """
        .. actdiag::

           A -> B;
           A [href=":ref:`target`"];
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/actdiag-.*?.png}')
