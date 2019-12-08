# -*- coding: utf-8 -*-

import os
import re
from sphinx_testing import with_app
from blockdiag.utils.compat import u

import unittest

CR = "\r?\n"

blockdiag_fontpath = '/usr/share/fonts/truetype/ipafont/ipagp.ttf'
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
                            'blockdiag_latex_image_format': 'PDF',
                            'blockdiag_fontpath': blockdiag_fontpath,
                        })
with_oldpdf_app = with_app(srcdir='tests/docs/basic',
                           buildername='latex',
                           write_docstring=True,
                           confoverrides={
                               'latex_documents': [('index', 'test.tex', u(''), u('test'), 'manual')],
                               'blockdiag_tex_image_format': 'PDF',
                               'blockdiag_fontpath': blockdiag_fontpath,
                           })


class TestSphinxcontribBlockdiagLatex(unittest.TestCase):
    @with_png_app
    def test_build_png_image(self, app, status, warning):
        """
        .. blockdiag::

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, r'\\sphinxincludegraphics{{blockdiag-.*?}.png}')

    @unittest.skipUnless(os.path.exists(blockdiag_fontpath), "TrueType font not found")
    @with_pdf_app
    def test_build_pdf_image1(self, app, status, warning):
        """
        .. blockdiag::

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, r'\\sphinxincludegraphics{{blockdiag-.*?}.pdf}')

    @unittest.skipUnless(os.path.exists(blockdiag_fontpath), "TrueType font not found")
    @with_oldpdf_app
    def test_build_pdf_image2(self, app, status, warning):
        """
        .. blockdiag::

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, r'\\sphinxincludegraphics{{blockdiag-.*?}.pdf}')

    @with_png_app
    def test_width_option(self, app, status, warning):
        """
        .. blockdiag::
           :width: 3cm

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, r'\\sphinxincludegraphics\[width=3cm\]{{blockdiag-.*?}.png}')

    @with_png_app
    def test_height_option(self, app, status, warning):
        """
        .. blockdiag::
           :height: 4cm

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, r'\\sphinxincludegraphics\[height=4cm\]{{blockdiag-.*?}.png}')

    @with_png_app
    def test_scale_option(self, app, status, warning):
        """
        .. blockdiag::
           :scale: 50%

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, r'\\sphinxincludegraphics\[scale=0.5\]{{blockdiag-.*?}.png}')

    @with_png_app
    def test_align_option_left(self, app, status, warning):
        """
        .. blockdiag::
           :align: left

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source,
                                 (r'{\\sphinxincludegraphics{{blockdiag-.*?}.png}'
                                  r'\\hspace\*{\\fill}}'))

    @with_png_app
    def test_align_option_center(self, app, status, warning):
        """
        .. blockdiag::
           :align: center

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source,
                                 (r'{\\hspace\*{\\fill}'
                                  r'\\sphinxincludegraphics{{blockdiag-.*?}.png}'
                                  r'\\hspace\*{\\fill}}'))

    @with_png_app
    def test_align_option_right(self, app, status, warning):
        """
        .. blockdiag::
           :align: right

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source,
                                 (r'{\\hspace\*{\\fill}'
                                  r'\\sphinxincludegraphics{{blockdiag-.*?}.png}}'))

    @with_png_app
    def test_caption_option(self, app, status, warning):
        """
        .. blockdiag::
           :caption: hello world

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')

        figure = re.compile((r'\\begin{figure}\[htbp\]' + CR +
                             r'\\centering' + CR +
                             r'\\capstart' + CR + CR +
                             r'\\noindent\\sphinxincludegraphics{{blockdiag-.*?}.png}' + CR +
                             r'\\caption{hello world}\\label{\\detokenize{index:id1}}\\end{figure}'),
                            re.DOTALL)
        self.assertRegexpMatches(source, figure)

    @with_png_app
    def test_caption_option_and_align_option(self, app, status, warning):
        """
        .. blockdiag::
           :align: left
           :caption: hello world

           A -> B;
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')

        figure = re.compile((r'\\begin{wrapfigure}{l}{0pt}' + CR +
                             r'\\centering' + CR +
                             r'\\noindent\\sphinxincludegraphics{{blockdiag-.*?}.png}' + CR +
                             r'\\caption{hello world}\\label{\\detokenize{index:id1}}\\end{wrapfigure}'),
                            re.DOTALL)
        self.assertRegexpMatches(source, figure)

    @with_png_app
    def test_href(self, app, status, warning):
        """
        .. blockdiag::

           A -> B;
           A [href = ':ref:`target`'];
        """
        app.builder.build_all()
        source = (app.outdir / 'test.tex').read_text(encoding='utf-8')
        self.assertRegexpMatches(source, r'\\sphinxincludegraphics{{blockdiag-.*?}.png}')
