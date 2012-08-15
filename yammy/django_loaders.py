from os.path import splitext

from django.template.loaders.filesystem import Loader as FileSystemLoader
from django.template.loaders.app_directories import Loader as PackageLoader

from yammy.translator import yammy_to_html_string


class YammyLoaderMixin(object):

    def get_html_source(self, get_source, template_name, template_dirs):
        contents, filename = get_source(template_name, template_dirs)
        if splitext(filename)[1] in ['.ymy', '.yammy']:
            contents = yammy_to_html_string(contents)
        return contents, filename


class YammyFileSystemLoader(FileSystemLoader, YammyLoaderMixin):

    def load_template_source(self, template_name, template_dirs=None):
        source = super(YammyFileSystemLoader, self).load_template_source
        return self.get_html_source(source, template_name, template_dirs)


class YammyPackageLoader(PackageLoader, YammyLoaderMixin):

    def load_template_source(self, environment, template):
        source = super(YammyPackageLoader, self).load_template_source
        return self.get_html_source(source, template_name, template_dirs)
