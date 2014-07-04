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
    extensions=['sphinxcontrib.seqdiag'],
    master_doc='index',
    latex_documents=[('index', 'test.tex', u(''), u('test'), 'manual')],
)

pdf_config = dict(
    extensions=['sphinxcontrib.seqdiag'],
    master_doc='index',
    latex_documents=[('index', 'test.tex', u(''), u('test'), 'manual')],
    seqdiag_latex_image_format='PDF',
    seqdiag_fontpath='/usr/share/fonts/truetype/ipafont/ipagp.ttf',
)

pdf_config_oldstyle = dict(
    extensions=['sphinxcontrib.seqdiag'],
    master_doc='index',
    latex_documents=[('index', 'test.tex', u(''), u('test'), 'manual')],
    seqdiag_tex_image_format='PDF',
    seqdiag_fontpath='/usr/share/fonts/truetype/ipafont/ipagp.ttf',
)


class TestSphinxcontribSeqdiagLatex(unittest.TestCase):
    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_build_png_image(self, app):
        """
        .. seqdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/seqdiag-.*?.png}')

    @unittest.skipUnless(os.path.exists(pdf_config['seqdiag_fontpath']), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_built_docstring(buildername='latex', confoverrides=pdf_config)
    def test_build_pdf_image1(self, app):
        """
        .. seqdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/seqdiag-.*?.pdf}')

    @unittest.skipUnless(os.path.exists(pdf_config['seqdiag_fontpath']), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_built_docstring(buildername='latex', confoverrides=pdf_config_oldstyle)
    def test_build_pdf_image2(self, app):
        """
        .. seqdiag::

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/seqdiag-.*?.pdf}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_width_option(self, app):
        """
        .. seqdiag::
           :width: 3cm

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics\\[width=3cm\\]{.*?/seqdiag-.*?.png}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_height_option(self, app):
        """
        .. seqdiag::
           :height: 4cm

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics\\[height=4cm\\]{.*?/seqdiag-.*?.png}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_scale_option(self, app):
        """
        .. seqdiag::
           :scale: 50%

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\scalebox{0.500000}{\\\\includegraphics{.*?/seqdiag-.*?.png}}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_align_option_left(self, app):
        """
        .. seqdiag::
           :align: left

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '{\\\\includegraphics{.*?/seqdiag-.*?.png}\\\\hfill}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_align_option_center(self, app):
        """
        .. seqdiag::
           :align: center

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/seqdiag-.*?.png}\\\\hfill}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_align_option_right(self, app):
        """
        .. seqdiag::
           :align: right

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/seqdiag-.*?.png}}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_caption_option(self, app):
        """
        .. seqdiag::
           :caption: hello world

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/seqdiag-.*?.png}')

            figure = re.compile('\\\\begin{figure}\\[htbp\\]\n\\\\centering.*?'
                                '\\\\caption{hello world}\\\\end{figure}', re.DOTALL)
            self.assertRegexpMatches(source, figure)

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_caption_option_and_align_option(self, app):
        """
        .. seqdiag::
           :align: left
           :caption: hello world

           A -> B;
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/seqdiag-.*?.png}')

            figure = re.compile('\\\\begin{figure}\\[htbp\\]\\\\begin{flushleft}.*?'
                                '\\\\caption{hello world}\\\\end{flushleft}\\\\end{figure}', re.DOTALL)
            self.assertRegexpMatches(source, figure)
