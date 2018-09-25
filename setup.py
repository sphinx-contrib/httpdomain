# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_packages


requires = [
    'Sphinx >= 1.5',
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
    version='1.7.0',
    url='https://github.com/sphinx-contrib/httpdomain',
    download_url='https://pypi.org/project/sphinxcontrib-httpdomain/',
    license='BSD',
    author='Hong Minhee',
    author_email='\x68\x6f\x6e\x67.minhee' '@' '\x67\x6d\x61\x69\x6c.com',
    description='Sphinx domain for documenting HTTP APIs',
    long_description=readme(),
    zip_safe=False,
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
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
