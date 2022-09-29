# -*- coding: utf-8 -*-

from mock import patch

import os
import sys
import pytest


docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'basic')


@pytest.mark.sphinx(srcdir=docs)
def test_parse_error(app, status, warning):
    doc = """
.. blockdiag::

   { A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    assert 'got unexpected token:' in warning.getvalue()


@pytest.mark.sphinx(srcdir=docs, confoverrides=dict(blockdiag_html_image_format='JPG'))
def test_unknown_format_error(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    app.builder.build_all()
    assert 'unknown format: JPG' in warning.getvalue()


@pytest.mark.sphinx(srcdir=docs, confoverrides=dict(blockdiag_html_image_format='PDF'))
def test_reportlab_not_found_error(app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    try:
        # unload reportlab and make loading it impossible
        sys.modules.pop('reportlab', None)
        path = sys.path
        sys.path = []

        app.builder.build_all()

        assert 'Could not output PDF format. Install reportlab.' in warning.getvalue()
    finally:
        sys.path = path


@pytest.mark.sphinx(srcdir=docs)
@patch("blockdiag.utils.rst.nodes.blockdiag.processor.drawer.DiagramDraw")
def test_rendering_error(DiagramDraw, app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    DiagramDraw.side_effect = RuntimeError("UNKNOWN ERROR!")
    app.builder.build_all()
    assert 'UNKNOWN ERROR!' in warning.getvalue()


@pytest.mark.skipif(sys.version_info > (3, 8), reason="Failsonpython > 3.8")
@pytest.mark.sphinx(srcdir=docs)
@patch("sphinxcontrib.blockdiag.blockdiag.drawer.DiagramDraw.draw")
def test_font_settings_error(draw, app, status, warning):
    doc = """
.. blockdiag::

   A -> B;
    """
    (app.srcdir / 'index.rst').write_text(doc, encoding='utf-8')
    draw.side_effect = UnicodeEncodeError("", "", 0, 0, "")
    app.builder.build_all()
    assert 'UnicodeEncodeError caught (check your font settings)' in warning.getvalue()
