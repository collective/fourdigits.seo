from setuptools import setup, find_packages
import os

version = '0.3'

setup(name='fourdigits.seo',
      version=version,
      description="Package for SEO",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Four Digits',
      author_email='info@fourdigits.nl',
      url='http://www.fourdigits.nl',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['fourdigits'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity [relations]',
          'plone.app.relationfield',
          'plone.namedfile [blobs]',
          'plone.behavior',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )
