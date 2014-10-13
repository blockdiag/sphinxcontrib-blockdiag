import os
import re
import json
from time import mktime
from urllib2 import urlopen
from email.utils import parsedate
from docutils import nodes
from docutils.parsers.rst.directives.images import Image, Figure
from sphinx.util.osutil import ensuredir


class Cacoo(object):
    def __init__(self, apikey):
        self.apikey = apikey

    def get_image_info(self, diagramid):
        URLBASE = "https://cacoo.com/api/v1/diagrams/%s.json?apiKey=%s"
        diagramid = re.sub('[#-].*', '', diagramid)  # remove sheetid
        url = URLBASE % (diagramid, self.apikey)
        return json.loads(urlopen(url).read())

    def get_last_modified(self, diagramid):
        image_info = self.get_image_info(diagramid)
        return mktime(parsedate(image_info['updated']))

    def get_image(self, diagramid):
        URLBASE = "https://cacoo.com/api/v1/diagrams/%s.png?apiKey=%s"
        diagramid = diagramid.replace('#', '-')
        url = URLBASE % (diagramid, self.apikey)
        return urlopen(url)


class cacoo_image(nodes.General, nodes.Element):
    def to_image(self, builder):
        if builder.format == 'html':
            reldir = "_images"
            outdir = os.path.join(builder.outdir, '_images')
        else:
            reldir = ""
            outdir = builder.outdir

        try:
            cacoo = Cacoo(builder.config.cacoo_apikey)
            last_modified = cacoo.get_last_modified(self['diagramid'])

            filename = "cacoo-%s.png" % self['diagramid'].replace('#', '-')
            path = os.path.join(outdir, filename)
            if not os.path.exists(path) or os.stat(path).st_mtime < last_modified:
                ensuredir(outdir)
                with open(path, 'wb') as fd:
                    fd.write(cacoo.get_image(self['diagramid']).read())
                os.utime(path, (last_modified, last_modified))
        except Exception as exc:
            builder.warn('Fail to download cacoo image: %s (check your cacoo_apikey or diagramid)' % exc)
            return nodes.Text('')

        relfn = os.path.join(reldir, filename)
        image_node = nodes.image(candidates={'*': relfn}, **self.attributes)
        image_node['uri'] = relfn

        return image_node


class CacooImage(Image):
    def run(self):
        result = super(CacooImage, self).run()
        if isinstance(result[0], nodes.image):
            image = cacoo_image(diagramid=self.arguments[0],
                                **result[0].attributes)
            result[0] = image
        else:
            for node in result[0].traverse(nodes.image):
                image = cacoo_image(diagramid=self.arguments[0],
                                    **node.attributes)
                node.replace_self(image)

        return result


class CacooFigure(Figure):
    def run(self):
        result = super(CacooFigure, self).run()
        for node in result[0].traverse(nodes.image):
            image = cacoo_image(diagramid=self.arguments[0],
                                **node.attributes)
            node.replace_self(image)

        return result


def on_doctree_resolved(app, doctree, docname):
    for cacoo in doctree.traverse(cacoo_image):
        image_node = cacoo.to_image(app.builder)
        cacoo.replace_self(image_node)


def setup(app):
    app.add_node(cacoo_image)
    app.add_directive('cacoo-image', CacooImage)
    app.add_directive('cacoo-figure', CacooFigure)
    app.connect('doctree-resolved', on_doctree_resolved)

    app.add_config_value('cacoo_apikey', None, 'html')
