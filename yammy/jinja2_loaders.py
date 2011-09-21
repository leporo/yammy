from jinja2.loaders import FileSystemLoader, PackageLoader

from translator import yammy_to_html_string


class YammyLoaderMixin(object):
    
    def get_html_source(self, get_source, environment, template):
        contents, filename, uptodate = get_source(environment, template) 
        if filename.endswith('.ymy') or filename.endswith('.yammy'):
            contents = yammy_to_html_string(contents)
        return contents, filename, uptodate


class YammyFileSystemLoader(FileSystemLoader, YammyLoaderMixin):

    def get_source(self, environment, template):
        return self.get_html_source(super(YammyFileSystemLoader, self).get_source, environment, template)


class YammyPackageLoader(PackageLoader, YammyLoaderMixin):

    def get_source(self, environment, template):
        return self.get_html_source(super(YammyPackageLoader, self).get_source, environment, template)
