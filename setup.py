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
    long_description_content_type='text/x-rst',
    author='BeProud Inc.',
    author_email='project@beproud.jp',
    license='BSD',
    url='http://www.beproud.jp/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data=True,
    packages=find_packages(),
    namespace_packages=['beproud', 'beproud.django'],
    install_requires=[
        'Django>=2.2',
    ],
    test_suite='tests.main',
    zip_safe=False,
)
