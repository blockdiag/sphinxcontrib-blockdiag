# -*- coding: utf-8 -*-

import os
import pytest


docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'basic')


@pytest.mark.sphinx(buildername='html', srcdir=docs)
def test_build_html(app, status, warning):
    app.builder.build_all()


@pytest.mark.sphinx(buildername='singlehtml', srcdir=docs)
def test_build_singlehtml(app, status, warning):
    app.builder.build_all()


@pytest.mark.sphinx(buildername='latex', srcdir=docs)
def test_build_latex(app, status, warning):
    app.builder.build_all()


@pytest.mark.sphinx(buildername='epub', srcdir=docs)
def test_build_epub(app, status, warning):
    app.builder.build_all()


@pytest.mark.sphinx(buildername='json', srcdir=docs)
def test_build_json(app, status, warning):
    app.builder.build_all()
