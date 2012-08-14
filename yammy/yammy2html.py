import os
import argparse

from translator import yammy_to_html


class Yammy2Html(object):

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Translates templates.')
        parser.add_argument('yammy_templates', metavar='source', nargs='+',
                           help='yammy template file')
        parser.add_argument('--dest', dest='dest', default=False,
                           help='output directory (defaults to the yammy template\s directory)')
        parser.add_argument('--ext', metavar='ext', dest='dest_ext',
                           default='.html',
                           help='processed template extension (default is .html)')

        return parser.parse_args()

    def process_single_template(self, yammy_template, yammy_root_dir=None):
        tpl_basename = os.path.basename(yammy_template)
        if self.args.dest:
            mid_dir = yammy_template[len(yammy_root_dir):len(yammy_template) - len(tpl_basename) - 1]
            dest_dir = os.path.join(self.args.dest, mid_dir)
        else:
            dest_dir = yammy_root_dir or os.path.dirname(yammy_template)
        dest_file_name = os.path.join(dest_dir, tpl_basename.split('.')[0] + self.args.dest_ext)
        print '%s -> %s' % (yammy_template, dest_file_name)
        yammy_to_html(yammy_template, dest_file_name)

    def run(self):
        self.args = args = self.parse_arguments()
        for yammy_template in args.yammy_templates:
            if os.path.isdir(yammy_template):
                for dirpath, _, filenames in os.walk(yammy_template):
                    for filename in filenames:
                        loname = filename.lower()
                        for yammy_ext in ('.ymy', '.yammy'):
                            if loname.endswith(yammy_ext):
                                self.process_single_template(os.path.join(dirpath, filename), yammy_root_dir=yammy_template)
            else:
                self.process_single_template(yammy_template, yammy_root_dir=os.path.dirname(yammy_template))


Yammy2Html().run()
