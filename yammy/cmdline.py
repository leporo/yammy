#!/usr/bin/env python
from os import path, walk
from argparse import ArgumentParser

from yammy import yammy_to_html, VERSION


class Yammy2Html(object):

    def parse_arguments(self):
        parser = ArgumentParser(description='Yammy template preprocessor '
                                            'command-line utility v.%s.'
                                           % VERSION)
        parser.add_argument('yammy_templates', metavar='source', nargs='+',
                            help='a Yammy template file name or '
                                 'a name of a directory containing '
                                 'Yammy templates')
        parser.add_argument('--dest', dest='dest', default=False,
                            help='output directory (defaults to the '
                                 'yammy template\s directory)')
        parser.add_argument('--ext', metavar='ext', dest='dest_ext',
                            default='.html',
                            help='output file extension (defaults to .html)')
        parser.add_argument('--debug', action="store_true", dest='debug',
                            default=False,
                            help='keep the number of lines in output file '
                                 'the same as in the source')
        return parser.parse_args()

    def process_template(self, yammy_template, yammy_root_dir=None):
        if self.args.dest:
            mid_dir = yammy_template.replace(yammy_root_dir, '', 1)
            mid_dir = path.dirname(mid_dir)
            dest_dir = path.join(self.args.dest, mid_dir)
        else:
            dest_dir = yammy_root_dir or path.dirname(yammy_template)

        tpl_basename = path.basename(yammy_template)
        tpl_ext = path.splitext(tpl_basename)[0] + self.args.dest_ext
        dest_file_name = path.join(dest_dir, tpl_ext)

        print(('{} --> {}'.format(yammy_template, dest_file_name)))
        yammy_to_html(yammy_template, dest_file_name,
                      keep_line_numbers=self.args.debug)

    def run(self):
        self.args = args = self.parse_arguments()
        for yammy_template in args.yammy_templates:
            if path.isdir(yammy_template):
                for dirpath, _, filenames in walk(yammy_template):
                    for filename in filenames:
                        if filename.lower().endswith(('ymy', 'yammy')):
                            self.process_template(
                                    path.join(dirpath, filename),
                                    yammy_root_dir=yammy_template,
                                    )
            else:
                self.process_template(
                        yammy_template,
                        yammy_root_dir=path.dirname(yammy_template),
                        )


def main():
    Yammy2Html().run()


if __name__ == "__main__":
    main()
