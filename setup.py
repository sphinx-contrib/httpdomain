# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_packages


install_requires = [
    'Sphinx >= 6.0',
    'six',
]

dev_requires = test_requires = docs_requires = [
    'Flask',
    'bottle',
    'tornado',
    'pytest',
]

def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except IOError:
        pass


setup(
    name='sphinxcontrib-httpdomain',
    version='1.8.0',
    url='https://github.com/sphinx-contrib/httpdomain',
    download_url='https://pypi.org/project/sphinxcontrib-httpdomain/',
    license='BSD',
    author='Hong Minhee, Ash Berlin-Taylor',
    author_email='Hong Minhee <\x68\x6f\x6e\x67.minhee' '@' '\x67\x6d\x61\x69\x6c.com>, Ash Berlin-Taylor <ash_github@firemirror.com>',
    description='Sphinx domain for documenting HTTP APIs',
    long_description=readme(),
    zip_safe=False,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    dev_requires=dev_requires,
    docs_requires=docs_requires,
    test_requires=test_requires,
    namespace_packages=['sphinxcontrib'],
)
