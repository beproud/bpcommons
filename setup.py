#!/usr/bin/env python
#:coding=utf-8:

from setuptools import setup, find_packages
from beproud.django.commons import VERSION


def read(filename):
    with open(filename) as f:
        return f.read()


setup(
    name='beproud.django.commons',
    version=VERSION,
    description='Common utilities for Django',
    long_description=read('README.rst') + read('ChangeLog.rst'),
    author='BeProud Inc.',
    author_email='project@beproud.jp',
    license='BSD',
    url='http://www.beproud.jp/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data=True,
    packages=find_packages(),
    namespace_packages=['beproud', 'beproud.django'],
    install_requires=[
        'Django>=1.8',
        'zenhan>=0.4',
        'six',
    ],
    test_suite='tests.main',
    zip_safe=False,
)
