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

nwdiag_fontpath = '/usr/share/fonts/truetype/ipafont/ipagp.ttf'
with_png_app = with_app(srcdir='tests/docs/nwdiag',
                        buildername='latex',
                        write_docstring=True,
                        confoverrides={
                            'latex_documents': [('index', 'test.tex', u(''), u('test'), 'manual')],
                        })
with_pdf_app = with_app(srcdir='tests/docs/nwdiag',
                        buildername='latex',
                        write_docstring=True,
                        confoverrides={
                            'latex_documents': [('index', 'test.tex', u(''), u('test'), 'manual')],
                            'nwdiag_latex_image_format': 'PDF',
                            'nwdiag_fontpath': nwdiag_fontpath,
                        })
with_oldpdf_app = with_app(srcdir='tests/docs/nwdiag',
                           buildername='latex',
                           write_docstring=True,
                           confoverrides={
                               'latex_documents': [('index', 'test.tex', u(''), u('test'), 'manual')],
                               'nwdiag_tex_image_format': 'PDF',
                               'nwdiag_fontpath': nwdiag_fontpath,
                           })


class TestSphinxcontribNwdiagLatex(unittest.TestCase):
    @with_png_app
    def test_build_png_image(self, app, status, warning):
        """
        .. nwdiag::

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/nwdiag-.*?.png}')

    @unittest.skipUnless(os.path.exists(nwdiag_fontpath), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_pdf_app
    def test_build_pdf_image1(self, app, status, warning):
        """
        .. nwdiag::

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/nwdiag-.*?.pdf}')

    @unittest.skipUnless(os.path.exists(nwdiag_fontpath), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_oldpdf_app
    def test_build_pdf_image2(self, app, status, warning):
        """
        .. nwdiag::

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/nwdiag-.*?.pdf}')

    @with_png_app
    def test_width_option(self, app, status, warning):
        """
        .. nwdiag::
           :width: 3cm

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics\\[width=3cm\\]{.*?/latex/nwdiag-.*?.png}')

    @with_png_app
    def test_height_option(self, app, status, warning):
        """
        .. nwdiag::
           :height: 4cm

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics\\[height=4cm\\]{.*?/latex/nwdiag-.*?.png}')

    @with_png_app
    def test_scale_option(self, app, status, warning):
        """
        .. nwdiag::
           :scale: 50%

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\scalebox{0.500000}{\\\\includegraphics{.*?/latex/nwdiag-.*?.png}}')

    @with_png_app
    def test_align_option_left(self, app, status, warning):
        """
        .. nwdiag::
           :align: left

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '{\\\\includegraphics{.*?/latex/nwdiag-.*?.png}\\\\hfill}')

    @with_png_app
    def test_align_option_center(self, app, status, warning):
        """
        .. nwdiag::
           :align: center

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/latex/nwdiag-.*?.png}\\\\hfill}')

    @with_png_app
    def test_align_option_right(self, app, status, warning):
        """
        .. nwdiag::
           :align: right

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/latex/nwdiag-.*?.png}}')

    @with_png_app
    def test_caption_option(self, app, status, warning):
        """
        .. nwdiag::
           :caption: hello world

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/nwdiag-.*?.png}')

        figure = re.compile('\\\\begin{figure}\\[htbp\\]\n\\\\centering.*?'
                            '\\\\caption{hello world}\\\\end{figure}', re.DOTALL)
        self.assertRegexpMatches(source, figure)

    @with_png_app
    def test_caption_option_and_align_option(self, app, status, warning):
        """
        .. nwdiag::
           :align: left
           :caption: hello world

           network { A; B; }
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/nwdiag-.*?.png}')

        figure = re.compile('\\\\begin{figure}\\[htbp\\]\\\\begin{flushleft}.*?'
                            '\\\\caption{hello world}\\\\end{flushleft}\\\\end{figure}', re.DOTALL)
        self.assertRegexpMatches(source, figure)

    @with_png_app
    def test_href(self, app, status, warning):
        """
        .. nwdiag::

           network { A; B; }
           A [href = ':ref:`target`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, '\\\\includegraphics{.*?/latex/nwdiag-.*?.png}')
