# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_packages


requires = [
    'Sphinx >= 1.6',
    'six',
]


def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except IOError:
        pass


setup(
    name='sphinxcontrib-httpdomain',
    version='1.8.1',
    url='https://github.com/sphinx-contrib/httpdomain',
    download_url='https://pypi.org/project/sphinxcontrib-httpdomain/',
    license='BSD',
    author='Hong Minhee, Ash Berlin-Taylor',
    author_email='Hong Minhee <\x68\x6f\x6e\x67.minhee' '@' '\x67\x6d\x61\x69\x6c.com>, Ash Berlin-Taylor <ash_github@firemirror.com>',
    description='Sphinx domain for documenting HTTP APIs',
    long_description=readme(),
    zip_safe=False,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
