# -*- coding: utf-8 -*-

import os
import re
from .utils import with_built_docstring
from blockdiag.utils.compat import u

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

png_config = dict(
    extensions=['sphinxcontrib.blockdiag'],
    master_doc='index',
    latex_documents=[('index', 'test.tex', u(''), u('test'), 'manual')],
)

pdf_config = dict(
    extensions=['sphinxcontrib.blockdiag'],
    master_doc='index',
    latex_documents=[('index', 'test.tex', u(''), u('test'), 'manual')],
    blockdiag_latex_image_format='PDF',
    blockdiag_fontpath='/usr/share/fonts/truetype/ipafont/ipagp.ttf',
)

pdf_config_oldstyle = dict(
    extensions=['sphinxcontrib.blockdiag'],
    master_doc='index',
    latex_documents=[('index', 'test.tex', u(''), u('test'), 'manual')],
    blockdiag_tex_image_format='PDF',
    blockdiag_fontpath='/usr/share/fonts/truetype/ipafont/ipagp.ttf',
)


class TestSphinxcontribBlockdiagLatex(unittest.TestCase):
    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_build_png_image(self, app):
        """
        .. blockdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/blockdiag-.*?.png}')

    @unittest.skipUnless(os.path.exists(pdf_config['blockdiag_fontpath']), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_built_docstring(buildername='latex', confoverrides=pdf_config)
    def test_build_pdf_image1(self, app):
        """
        .. blockdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/blockdiag-.*?.pdf}')

    @unittest.skipUnless(os.path.exists(pdf_config['blockdiag_fontpath']), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_built_docstring(buildername='latex', confoverrides=pdf_config_oldstyle)
    def test_build_pdf_image2(self, app):
        """
        .. blockdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/blockdiag-.*?.pdf}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_width_option(self, app):
        """
        .. blockdiag::
           :width: 3cm

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics\\[width=3cm\\]{.*?/blockdiag-.*?.png}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_height_option(self, app):
        """
        .. blockdiag::
           :height: 4cm

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics\\[height=4cm\\]{.*?/blockdiag-.*?.png}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_scale_option(self, app):
        """
        .. blockdiag::
           :scale: 50%

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\scalebox{0.500000}{\\\\includegraphics{.*?/blockdiag-.*?.png}}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_align_option_left(self, app):
        """
        .. blockdiag::
           :align: left

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '{\\\\includegraphics{.*?/blockdiag-.*?.png}\\\\hfill}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_align_option_center(self, app):
        """
        .. blockdiag::
           :align: center

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/blockdiag-.*?.png}\\\\hfill}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_align_option_right(self, app):
        """
        .. blockdiag::
           :align: right

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/blockdiag-.*?.png}}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_caption_option(self, app):
        """
        .. blockdiag::
           :caption: hello world

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/blockdiag-.*?.png}')

            figure = re.compile('\\\\begin{figure}\\[htbp\\]\n\\\\centering.*?'
                                '\\\\caption{hello world}\\\\end{figure}', re.DOTALL)
            self.assertRegexpMatches(source, figure)

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_caption_option_and_align_option(self, app):
        """
        .. blockdiag::
           :align: left
           :caption: hello world

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/blockdiag-.*?.png}')

            figure = re.compile('\\\\begin{figure}\\[htbp\\]\\\\begin{flushleft}.*?'
                                '\\\\caption{hello world}\\\\end{flushleft}\\\\end{figure}', re.DOTALL)
            self.assertRegexpMatches(source, figure)
