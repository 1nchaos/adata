# -*- coding: utf-8 -*-
"""
@desc: setup
@author: 1nchaos
@time: 2023/04/05
"""

import os

from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "adata", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r", encoding='utf-8') as f:
    readme = f.read()

requires = [
    "requests>=2.16.0",
    "pandas>=1.1.5",
    "beautifulsoup4>=4.0.2",
    "py_mini_racer>=0.6.0",
]


def setup_package():
    metadata = dict(
        name=about["__title__"],
        version=about["__version__"],
        description=about["__description__"],
        long_description=readme,
        long_description_content_type="text/markdown",
        url=about["__url__"],
        author=about["__author__"],
        author_email=about["__author_email__"],
        license=about["__license__"],
        packages=find_packages(exclude=("tests", "docs")),
        install_requires=requires,
        include_package_data=True,
        classifiers=[
            # Trove classifiers
            # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
        ],
    )

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
