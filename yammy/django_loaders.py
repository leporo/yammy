from django.template.loaders.filesystem import Loader as FileSystemLoader
from django.template.loaders.app_directories import Loader as PackageLoader
from django.conf import settings

from yammy.translator import yammy_to_html_string


class YammyLoaderMixin(object):

    def get_html_source(self, get_source, template_name, template_dirs):
        contents, filename = get_source(template_name, template_dirs)
        if filename.endswith(('.ymy', '.yammy')):
            contents = yammy_to_html_string(contents,
                                            keep_line_numbers=settings.DEBUG)
        return contents, filename


class YammyFileSystemLoader(FileSystemLoader, YammyLoaderMixin):
    '''
    Overrides Django FileSystemLoader and adds a Yammy template
    processing to it.

    The actual processing takes place at YammyLoaderMixin class.
    '''
    def load_template_source(self, template_name, template_dirs=None):
        source = super(YammyFileSystemLoader, self).load_template_source
        return self.get_html_source(source, template_name, template_dirs)


class YammyPackageLoader(PackageLoader, YammyLoaderMixin):
    '''
    Overrides Django PackageLoader and adds a Yammy template
    processing to it.

    The actual processing takes place at YammyLoaderMixin class.
    '''

    def load_template_source(self, template_name, template_dirs=None):
        source = super(YammyPackageLoader, self).load_template_source
        return self.get_html_source(source, template_name, template_dirs)
