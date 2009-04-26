from setuptools import setup, find_packages
import os.path

version = '0.4.2'

setup(name='five.intid',
      version=version,
      description="Zope2 support for zope.app.intid",
      long_description=open("README.txt").read() + "\n" +
               open(os.path.join("five", "intid", "README.txt")).read() + "\n\n" +
               open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Zope2"],
      keywords="'zope2 Five zope3 UID'",
      author='Whit Morris',
      author_email='whit@openplans.org',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['five'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'zope.component',
        'zope.event',
        'zope.interface',
        'zope.app.component',
        'zope.app.container',
        'zope.app.intid',
        'zope.app.keyreference',
        'zope.app.zapi',
        # 'Acquisition',
        # 'ZODB3',
        # 'Zope2',
        ],
      )

