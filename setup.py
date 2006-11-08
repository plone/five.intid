from setuptools import setup, find_packages
import sys, os

version = '0.1.4'

setup(name='five.intid',
      version=version,
      description="Overrides and zope2 classes to allow intid and keyreferences to work in Five",
      long_description="""\ """,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords="'zope2 Five zope3 UID'",
      author='whit',
      author_email='whit@openplans.org',
      url='http://openplans.org/projects/opencore/five-intid',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['five'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['collective.testing',],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
