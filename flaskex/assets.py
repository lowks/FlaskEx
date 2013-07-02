from webassets.filter import Filter
from webassets.exceptions import FilterError
from webassets import Bundle
from subprocess import Popen, PIPE
from glob2 import glob
from os import path


class IcedCoffeescript(Filter):
    name = 'icedcoffeescript'
    max_debug_level = None

    def output(self, _in, out, **kw):
        args = ['iced', '-sp', '--runtime', 'inline']
        proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate(_in.read().encode('utf-8'))
        if proc.returncode != 0:
            raise FilterError(
                (
                    'iced: subprocess had error: stderr=%s, ' +
                    'stdout=%s, returncode=%s'
                ) % (stderr, stdout, proc.returncode)
            )
        elif stderr:
            print("coffeescript filter has warnings:", stderr)
        out.write(stdout.decode('utf-8'))

    @classmethod
    def bundles(cls, *sources):
        li = []
        for i in sources:
            li.append(
                Bundle(
                    "js/%s.iced" % i, output="built/%s.js" % i, filters=[cls]
                )
            )
        return Bundle(*li)


def find_all_images(app):
    return tuple(glob(path.join(app.static_folder, 'img', '*')))