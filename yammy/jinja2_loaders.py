from django.conf import settings

from jinja2.loaders import FileSystemLoader, PackageLoader

from yammy.translator import yammy_to_html_string


class YammyLoaderMixin(object):

    def get_html_source(self, get_source, environment, template):
        contents, filename, uptodate = get_source(environment, template)
        if filename.endswith(('.ymy', '.yammy')):
            contents = yammy_to_html_string(contents,
                                            keep_line_numbers=settings.DEBUG)
        return contents, filename, uptodate


class YammyFileSystemLoader(FileSystemLoader, YammyLoaderMixin):

    def get_source(self, environment, template):
        source = super(YammyFileSystemLoader, self).get_source
        return self.get_html_source(source, environment, template)


class YammyPackageLoader(PackageLoader, YammyLoaderMixin):

    def get_source(self, environment, template):
        source = super(YammyPackageLoader, self).get_source
        return self.get_html_source(source, environment, template)
