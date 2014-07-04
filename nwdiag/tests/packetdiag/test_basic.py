# -*- coding: utf-8 -*-

from ..utils import with_app


@with_app(buildername='html', srcdir='docs/packetdiag/')
def test_build_html(app):
    app.builder.build_all()


@with_app(buildername='singlehtml', srcdir='docs/packetdiag/')
def test_build_singlehtml(app):
    app.builder.build_all()


@with_app(buildername='latex', srcdir='docs/packetdiag/')
def test_build_latex(app):
    app.builder.build_all()


@with_app(buildername='epub', srcdir='docs/packetdiag/')
def test_build_epub(app):
    app.builder.build_all()


@with_app(buildername='json', srcdir='docs/packetdiag/')
def test_build_json(app):
    app.builder.build_all()
