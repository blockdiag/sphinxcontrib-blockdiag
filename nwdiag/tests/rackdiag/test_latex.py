# -*- coding: utf-8 -*-

import os
import re
from ..utils import with_built_docstring
from blockdiag.utils.compat import u

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

png_config = dict(
    extensions=['sphinxcontrib.rackdiag'],
    master_doc='index',
    latex_documents=[('index', 'test.tex', u(''), u('test'), 'manual')],
)

pdf_config = dict(
    extensions=['sphinxcontrib.rackdiag'],
    master_doc='index',
    latex_documents=[('index', 'test.tex', u(''), u('test'), 'manual')],
    rackdiag_latex_image_format='PDF',
    rackdiag_fontpath='/usr/share/fonts/truetype/ipafont/ipagp.ttf',
)

pdf_config_oldstyle = dict(
    extensions=['sphinxcontrib.rackdiag'],
    master_doc='index',
    latex_documents=[('index', 'test.tex', u(''), u('test'), 'manual')],
    rackdiag_tex_image_format='PDF',
    rackdiag_fontpath='/usr/share/fonts/truetype/ipafont/ipagp.ttf',
)


class TestSphinxcontribRackdiagLatex(unittest.TestCase):
    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_build_png_image(self, app):
        """
        .. rackdiag::

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/rackdiag-.*?.png}')

    @unittest.skipUnless(os.path.exists(pdf_config['rackdiag_fontpath']), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_built_docstring(buildername='latex', confoverrides=pdf_config)
    def test_build_pdf_image1(self, app):
        """
        .. rackdiag::

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/rackdiag-.*?.pdf}')

    @unittest.skipUnless(os.path.exists(pdf_config['rackdiag_fontpath']), "TrueType font not found")
    @unittest.skipIf(sys.version_info[:2] == (3, 2), "reportlab does not support python 3.2")
    @with_built_docstring(buildername='latex', confoverrides=pdf_config_oldstyle)
    def test_build_pdf_image2(self, app):
        """
        .. rackdiag::

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/rackdiag-.*?.pdf}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_width_option(self, app):
        """
        .. rackdiag::
           :width: 3cm

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics\\[width=3cm\\]{.*?/rackdiag-.*?.png}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_height_option(self, app):
        """
        .. rackdiag::
           :height: 4cm

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics\\[height=4cm\\]{.*?/rackdiag-.*?.png}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_scale_option(self, app):
        """
        .. rackdiag::
           :scale: 50%

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\scalebox{0.500000}{\\\\includegraphics{.*?/rackdiag-.*?.png}}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_align_option_left(self, app):
        """
        .. rackdiag::
           :align: left

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '{\\\\includegraphics{.*?/rackdiag-.*?.png}\\\\hfill}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_align_option_center(self, app):
        """
        .. rackdiag::
           :align: center

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/rackdiag-.*?.png}\\\\hfill}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_align_option_right(self, app):
        """
        .. rackdiag::
           :align: right

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '{\\\\hfill\\\\includegraphics{.*?/rackdiag-.*?.png}}')

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_caption_option(self, app):
        """
        .. rackdiag::
           :caption: hello world

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/rackdiag-.*?.png}')

            figure = re.compile('\\\\begin{figure}\\[htbp\\]\n\\\\centering.*?'
                                '\\\\caption{hello world}\\\\end{figure}', re.DOTALL)
            self.assertRegexpMatches(source, figure)

    @with_built_docstring(buildername='latex', confoverrides=png_config)
    def test_caption_option_and_align_option(self, app):
        """
        .. rackdiag::
           :align: left
           :caption: hello world

           * A
           * B
        """
        filename = os.path.join(app.outdir, 'test.tex')
        with open(filename) as fd:
            source = fd.read()
            self.assertRegexpMatches(source, '\\\\includegraphics{.*?/rackdiag-.*?.png}')

            figure = re.compile('\\\\begin{figure}\\[htbp\\]\\\\begin{flushleft}.*?'
                                '\\\\caption{hello world}\\\\end{flushleft}\\\\end{figure}', re.DOTALL)
            self.assertRegexpMatches(source, figure)
