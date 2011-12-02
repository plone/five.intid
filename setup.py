from setuptools import setup, find_packages
import os.path

version = '1.0.3'

setup(name='five.intid',
      version=version,
      description="Zope2 support for zope.intid",
      long_description=open("README.txt").read() + "\n" +
               open(os.path.join("five", "intid", "README.txt")).read() + "\n\n" +
               open("CHANGES.txt").read(),
      classifiers=[
          "Framework :: Zope2"],
      keywords="'zope2 intid'",
      author='Whit Morris',
      author_email='whit@openplans.org',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['five'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'zope.intid',
        'zope.component',
        'zope.event',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.keyreference',
        'zope.site',
        'zope.location',
        'five.localsitemanager',
        'Zope2 >= 2.13',
        ],
      )
