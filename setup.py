# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os.path

version = '1.2.6'

longdescripton = open("README.rst").read() + "\n"
longdescripton += open(os.path.join("five", "intid", "README.rst")).read()
longdescripton += "\n\n"
longdescripton += open("CHANGES.rst").read()


setup(
    name='five.intid',
    version=version,
    description="Zope support for zope.intid",
    long_description=longdescripton,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="'zope2 intid'",
    author='Whit Morris',
    author_email='whit@openplans.org',
    license='ZPL',
    url='https://github.com/plone/five.intid',
    packages=find_packages(),
    namespace_packages=['five'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Acquisition>=4.0.1',
        'setuptools',
        'zope.intid',
        'zope.component',
        'zope.event',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.keyreference',
        'zope.location',
        'five.localsitemanager',
        'Zope2 >= 2.13;python_version=="2.7"',
        'Zope >= 4;python_version>="3.6"',
    ],
)
