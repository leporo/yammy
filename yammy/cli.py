from argparse import ArgumentParser
from sys import stdin, stdout
import os

from yammy.translator import yammy_to_html_string


def make_parser():
    parser = ArgumentParser(description='yammy to html conversor')
    parser.add_argument('-i', '--input-file', type=str, metavar='FILE')
    parser.add_argument('-d', '--input-dir', type=str, metavar='DIRECTORY',
            help='only *.yammy or *.ymy named files are processed')
    return parser


def html_extension(filename):
    return os.path.splitext(filename)[0] + '.html'


def cli(args):
    conversion = {}

    if args.input_dir:
        assert os.path.isdir(args.input_dir), '-d option arg must be a directory'
        for path, _, files in os.walk(args.input_dir):
            for f in files:
                if f.endswith(('yammy', 'ymy')):
                    in_file = os.path.join(path, f)
                    out_file = html_extension(in_file)
                    conversion[open(in_file, 'r')] = open(out_file, 'w')
    elif args.input_file:
        out_file = html_extension(args.input_file)
        conversion[open(args.input_file, 'r')] = open(out_file, 'w')
    else:
        conversion[stdin] = stdout

    for in_file, out_file in conversion.items():
        out_file.write(yammy_to_html_string(in_file.read()))
        out_file.close()


def main():
    parser = make_parser()
    args = parser.parse_args()
    cli(args)

if __name__ == '__main__':
    main()
