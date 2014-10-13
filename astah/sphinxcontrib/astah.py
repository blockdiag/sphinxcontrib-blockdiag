import os
import subprocess
from glob import glob
from hashlib import sha1
from tempfile import mkdtemp
from shutil import copyfile, rmtree
from docutils import nodes
from docutils.parsers.rst.directives.images import Image, Figure
from sphinx.util.osutil import ensuredir


def find_astah_command(builder):
    if builder.config.astah_command_path:
        return builder.config.astah_command_path

    patterns = ['/Applications/astah*/astah-command.sh']  # Mac OS X
    for pattern in patterns:
        for path in glob(pattern):
            if os.path.exists(path):
                return path

    builder.warn('astah-command.sh (or .bat) not found. set astah_command_path in your conf.py')
    return None


class astah_image(nodes.General, nodes.Element):
    def convert_to(self, path, builder):
        try:
            tmpdir = mkdtemp()

            astah_command = find_astah_command(builder)
            astah_args = [astah_command, '-image', 'all', '-f', self['filename'], '-o', tmpdir]
            if astah_command is None:
                return False

            ensuredir(os.path.dirname(path))
            retcode = subprocess.call(astah_args)
            if retcode != 0:
                builder.warn('Fail to convert astah image (exitcode: %s)' % retcode)
                return False

            dirname = os.path.splitext(os.path.basename(self['filename']))[0]
            imagedir = os.path.join(tmpdir, dirname)
            if self['sheet']:
                image_path = os.path.join(imagedir, self['sheet'] + '.png')
            else:
                image_path = os.path.join(imagedir, os.listdir(imagedir)[0])  # first item in dir

            if os.path.exists(image_path):
                copyfile(image_path, path)
                return True
            else:
                builder.warn('Fail to convert astah image: unknown sheet [%s]' % self['sheet'])
                return False
        except Exception as exc:
            builder.warn('Fail to convert astah image: %s' % exc)
            return False
        finally:
            rmtree(tmpdir, ignore_errors=True)

    def to_image(self, builder):
        if builder.format == 'html':
            reldir = "_images"
            outdir = os.path.join(builder.outdir, '_images')
        else:
            reldir = ""
            outdir = builder.outdir

        hashed = sha1((self['filename'] + self['sheet']).encode('utf-8')).hexdigest()
        filename = "astah-%s.png" % hashed
        path = os.path.join(outdir, filename)
        last_modified = os.stat(self['filename']).st_mtime

        if not os.path.exists(path) or os.stat(path).st_mtime < last_modified:
            ret = self.convert_to(path, builder=builder)
            if ret:
                os.utime(path, (last_modified, last_modified))
            else:
                return nodes.Text('')

        relfn = os.path.join(reldir, filename)
        image_node = nodes.image(candidates={'*': relfn}, **self.attributes)
        image_node['uri'] = relfn

        return image_node


class AstahImage(Image):
    def run(self):
        result = super(AstahImage, self).run()
        if '#' in self.arguments[0]:
            filename, sheet = self.arguments[0].split('#', 1)
        else:
            filename = self.arguments[0]
            sheet = ''

        if not os.path.exists(filename):
            raise self.warning('astah file not found: %s' % filename)

        if isinstance(result[0], nodes.image):
            image = astah_image(filename=filename, sheet=sheet,
                                **result[0].attributes)
            result[0] = image
        else:
            for node in result[0].traverse(nodes.image):
                image = astah_image(filename=filename, sheet=sheet,
                                    **node.attributes)
                node.replace_self(image)

        return result


class AstahFigure(Figure):
    def run(self):
        result = super(AstahFigure, self).run()
        if '#' in self.arguments[0]:
            filename, sheet = self.arguments[0].split('#', 1)
        else:
            filename = self.arguments[0]
            sheet = ''

        if not os.path.exists(filename):
            raise self.warning('astah file not found: %s' % filename)

        for node in result[0].traverse(nodes.image):
            image = astah_image(filename=filename, sheet=sheet,
                                **node.attributes)
            node.replace_self(image)

        return result


def on_doctree_resolved(app, doctree, docname):
    for astah in doctree.traverse(astah_image):
        image_node = astah.to_image(app.builder)
        astah.replace_self(image_node)


def setup(app):
    app.add_node(astah_image)
    app.add_directive('astah-image', AstahImage)
    app.add_directive('astah-figure', AstahFigure)
    app.connect('doctree-resolved', on_doctree_resolved)

    app.add_config_value('astah_command_path', None, 'html')
