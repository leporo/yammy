import jinja2

from yammy.jinja2_loaders import YammyPackageLoader, YammyFileSystemLoader

jinja2.FileSystemLoader = YammyFileSystemLoader
jinja2.PackageLoader = YammyPackageLoader

from jingo import Loader
