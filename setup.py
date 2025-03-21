from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "2.0.1"

long_description = (
    f"{Path('README.rst').read_text()}\n"
    f"{(Path('five') / 'intid' / 'README.rst').read_text()}\n"
    f"{Path('CHANGES.rst').read_text()}\n"
)

setup(
    name="five.intid",
    version=version,
    description="Zope support for zope.intid",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="'zope2 intid'",
    author="Whit Morris",
    author_email="whit@openplans.org",
    license="ZPL",
    url="https://github.com/plone/five.intid",
    packages=find_packages(),
    namespace_packages=["five"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "AccessControl",
        "Acquisition>=4.0.1",
        "Products.CMFCore",
        "ZODB",
        "Zope",
        "five.localsitemanager",
        "persistent",
        "setuptools",
        "zope.intid",
        "zope.component",
        "zope.event",
        "zope.interface",
        "zope.lifecycleevent",
        "zope.keyreference",
        "zope.location",
    ],
)
