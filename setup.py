#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.5.2'

setup(name='yammy',
      version=VERSION,
      description="Yammy: A better way to create a Django/Jinja template",
      long_description="Yammy is not a template engine. "
                       "It does not handle expressions or condition blocks. "
                       "It just provides with a simplier way to create "
                       "and maintain an HTML template.",
      classifiers=[],
      keywords='templates html django python',
      author='Vlad Glushchuk',
      author_email='high.slopes@gmail.com',
      url='https://bitbucket.org/quasinerd/yammy',
      license='GPL',
      packages=['yammy'],
      entry_points={'console_scripts': ['yammy = yammy.cmdline:main', ]}, )
