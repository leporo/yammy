from setuptools import setup, find_packages

version = '0.3'

setup(name='yammy',
      version=version,
      description="Yammy: A better way to create a Django/Jinja template",
      long_description="Yammy is not a template engine. "
                       "It does not handle expressions or condition blocks. "
                       "It just provides with a simplier way to create "
                       "and maintain an HTML template.",
      classifiers=[],
      keywords='templates html django python',
      author='quasinerd',
      author_email='',
      url='https://bitbucket.org/quasinerd/yammy',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
