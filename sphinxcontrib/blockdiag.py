# -*- coding: utf-8 -*-
"""
    blockdiag.sphinx_ext
    ~~~~~~~~~~~~~~~~~~~~

    Allow blockdiag-formatted diagrams to be included in Sphinx-generated
    documents inline.

    :copyright: Copyright 2010 by Takeshi Komiya.
    :license: BSDL.
"""

from __future__ import absolute_import

import os
import re
import posixpath
import traceback
from collections import namedtuple
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from sphinx.util.osutil import ensuredir

import blockdiag
import blockdiag.parser
import blockdiag.builder
import blockdiag.drawer
import blockdiag.utils.rst.directives
from blockdiag.utils.bootstrap import detectfont
from blockdiag.utils.compat import u
from blockdiag.utils.fontmap import FontMap

# fontconfig; it will be initialized on `builder-inited` event.
fontmap = None


class Blockdiag(blockdiag.utils.rst.directives.BlockdiagDirective):
    def node2image(self, node, diagram):
        return node


def get_image_filename(self, node, format, prefix='blockdiag'):
    """
    Get path of output file.
    """
    hashkey = (node['code'] + str(node['options'])).encode('utf-8')
    fname = '%s-%s.%s' % (prefix, sha(hashkey).hexdigest(), format.lower())
    if hasattr(self.builder, 'imgpath'):
        # HTML
        relfn = posixpath.join(self.builder.imgpath, fname)
        outfn = os.path.join(self.builder.outdir, '_images', fname)
    else:
        # LaTeX
        relfn = fname
        outfn = os.path.join(self.builder.outdir, fname)

    if os.path.isfile(outfn):
        return relfn, outfn

    ensuredir(os.path.dirname(outfn))

    return relfn, outfn


def get_anchor(self, refid, fromdocname):
    for docname in self.builder.env.found_docs:
        doctree = self.builder.env.get_doctree(docname)
        for target in doctree.traverse(nodes.Targetable):
            if target.attributes.get('refid') == refid:
                targetfile = self.builder.get_relative_uri(fromdocname, docname)
                return targetfile + "#" + refid


def resolve_reference(self, href, options):
    if href is None:
        return
    pattern = re.compile(u("^:ref:`(.+?)`"), re.UNICODE)
    matched = pattern.search(href)
    if matched:
        return get_anchor(self, matched.group(1), options.get('current_docname', ''))
    else:
        return href


def create_blockdiag(self, code, format, filename, options, **kwargs):
    """
    Render blockdiag code into a PNG output file.
    """
    draw = None
    try:
        tree = blockdiag.parser.parse_string(code)
        diagram = blockdiag.builder.ScreenNodeBuilder.build(tree)
        for node in diagram.traverse_nodes():
            if node.href:
                node.href = resolve_reference(self, node.href, options)

        antialias = self.builder.config.blockdiag_antialias
        draw = blockdiag.drawer.DiagramDraw(format, diagram, filename,
                                            fontmap=fontmap, antialias=antialias, **kwargs)

    except:
        if self.builder.config.blockdiag_debug:
            traceback.print_exc()

        raise

    return draw


def render_svg(self, node):
    options = node['options']
    relfn, outfn = get_image_filename(self, node, 'SVG')

    options['current_docname'] = self.builder.current_docname
    image = create_blockdiag(self, node['code'], 'SVG', None, options, nodoctype=True)
    image.draw()

    if 'align' in options:
        self.body.append('<div align="%s" class="align-%s">' % (options['align'], options['align']))
        self.context.append('</div>\n')
    else:
        self.context.append('')

    # reftarget
    for node_id in node['ids']:
        self.body.append('<span id="%s"></span>' % node_id)

    # resize image
    size = image.pagesize().resize(**options)
    self.body.append(image.save(size))
    self.context.append('')


def create_maptag(self, image, width_ratio, height_ratio):
    href_nodes = [node for node in image.nodes if node.href]
    if not href_nodes:
        return

    self.body.append('<map name="map_%d">' % id(image))
    for node in href_nodes:
        x1, y1, x2, y2 = image.metrics.cell(node)

        x1 *= width_ratio
        x2 *= width_ratio
        y1 *= height_ratio
        y2 *= height_ratio
        areatag = '<area shape="rect" coords="%s,%s,%s,%s" href="%s">' % (x1, y1, x2, y2, node.href)
        self.body.append(areatag)

    self.body.append('</map>')


def render_dot_html(self, node, options):
    format = self.builder.config.blockdiag_html_image_format
    relfn, outfn = get_image_filename(self, node, format)

    options['current_docname'] = self.builder.current_docname
    image = create_blockdiag(self, node['code'], format, outfn, options)

    if not os.path.isfile(outfn):
        image.draw()
        image.save()

    # align
    if 'align' in node['options']:
        self.body.append('<div align="%s" class="align-%s">' % (options['align'], options['align']))
        self.context.append('</div>\n')
    else:
        self.context.append('')

    # link to original image
    if 'width' in node['options'] or 'height' in node['options'] or 'scale' in node['options']:
        self.body.append('<a class="reference internal image-reference" href="%s">' % relfn)
        self.context.append('</a>')
    else:
        self.context.append('')

    # <img> tag
    original_size = image.pagesize()
    resized = original_size.resize(**node['options'])
    img_attr = dict(src=relfn,
                    width=resized.width,
                    height=resized.height)

    if any(node.href for node in image.nodes):
        img_attr['usemap'] = "#map_%d" % id(image)

        width_ratio = float(resized.width) / original_size.width
        height_ratio = float(resized.height) / original_size.height
        create_maptag(self, image, width_ratio, height_ratio)

    if 'alt' in node['options']:
        img_attr['alt'] = node['options']['alt']

    self.body.append(self.starttag(node, 'img', '', empty=True, **img_attr))


def html_visit_blockdiag(self, node):
    try:
        image_format = get_image_format_for(self.builder)
        if image_format.upper() == 'SVG':
            render_svg(self, node)
        else:
            render_dot_html(self, node, node['options'])
    except UnicodeEncodeError:
        msg = ("blockdiag error: UnicodeEncodeError caught "
               "(check your font settings)")
        self.builder.warn(msg)
        raise nodes.SkipNode
    except Exception as exc:
        self.builder.warn('dot code %r: %s' % (node['code'], str(exc)))
        raise nodes.SkipNode


def html_depart_blockdiag(self, node):
    self.body.append(self.context.pop())
    self.body.append(self.context.pop())


def get_image_format_for(builder):
    if builder.format == 'html':
        image_format = builder.config.blockdiag_html_image_format.upper()
    elif builder.format == 'latex':
        if builder.config.blockdiag_tex_image_format:
            image_format = builder.config.blockdiag_tex_image_format.upper()
        else:
            image_format = builder.config.blockdiag_latex_image_format.upper()
    else:
        image_format = 'PNG'

    if image_format.upper() not in ('PNG', 'PDF', 'SVG'):
        raise ValueError('unknown format: %s' % image_format)

    if image_format.upper() == 'PDF':
        try:
            import reportlab  # NOQA: importing test
        except ImportError:
            raise ImportError('Could not output PDF format. Install reportlab.')

    return image_format


def on_builder_inited(self):
    # show deprecated message
    if self.builder.config.blockdiag_tex_image_format:
        self.builder.warn('blockdiag_tex_image_format is deprecated. Use blockdiag_latex_image_format.')

    # initialize fontmap
    global fontmap

    try:
        fontmappath = self.builder.config.blockdiag_fontmap
        fontmap = FontMap(fontmappath)
    except:
        fontmap = FontMap(None)

    try:
        fontpath = self.builder.config.blockdiag_fontpath
        if isinstance(fontpath, blockdiag.utils.compat.string_types):
            fontpath = [fontpath]

        if fontpath:
            config = namedtuple('Config', 'font')(fontpath)
            fontpath = detectfont(config)
            fontmap.set_default_font(fontpath)
    except:
        pass


def on_doctree_resolved(self, doctree, docname):
    if self.builder.format == 'html':
        return

    try:
        image_format = get_image_format_for(self.builder)
    except Exception as exc:
        self.builder.warn('blockdiag error: %s' % exc)
        for node in doctree.traverse(blockdiag.utils.rst.nodes.blockdiag):
            node.parent.remove(node)

        return

    for node in doctree.traverse(blockdiag.utils.rst.nodes.blockdiag):
        try:
            code = node['code']
            options = node['options']
            relfn, outfn = get_image_filename(self, node, image_format)

            image = create_blockdiag(self, code, image_format, outfn, options)
            if not os.path.isfile(outfn):
                image.draw()
                image.save()

            image = nodes.image(uri=outfn, candidates={'*': relfn}, **options)
            node.parent.replace(node, image)
        except Exception as exc:
            self.builder.warn('dot code %r: %s' % (node['code'], str(exc)))
            node.parent.remove(node)


def setup(app):
    app.add_node(blockdiag.utils.rst.nodes.blockdiag,
                 html=(html_visit_blockdiag, html_depart_blockdiag))
    app.add_directive('blockdiag', Blockdiag)
    app.add_config_value('blockdiag_fontpath', None, 'html')
    app.add_config_value('blockdiag_fontmap', None, 'html')
    app.add_config_value('blockdiag_antialias', False, 'html')
    app.add_config_value('blockdiag_debug', False, 'html')
    app.add_config_value('blockdiag_html_image_format', 'PNG', 'html')
    app.add_config_value('blockdiag_tex_image_format', None, 'html')  # backward compatibility for 1.3.1
    app.add_config_value('blockdiag_latex_image_format', 'PNG', 'html')
    app.connect("builder-inited", on_builder_inited)
    app.connect("doctree-resolved", on_doctree_resolved)
