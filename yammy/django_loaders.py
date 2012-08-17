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

    def load_template_source(self, template_name, template_dirs=None):
        source = super(YammyPackageLoader, self).load_template_source
        return self.get_html_source(source, template_name, template_dirs)


class YammyTemplateMiddleware(object):
    """Renders Yammy templates ending in '.yammy' to HTML on the fly"""

    def process_template_response(self, request, response):
        template_name = response.resolve_template(response.template_name).name
        if template_name.endswith(('.yammy', 'ymy')):
            response.render()
            content = yammy_to_html_string(response.rendered_content)
            response._set_content(content)
        return response
