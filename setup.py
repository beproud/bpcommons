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
    url='http://www.beproud.jp/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data=True,
    packages=find_packages(),
    namespace_packages=['beproud', 'beproud.django'],
    install_requires=[
        'Django>=1.8',
        'zenhan>=0.4',
        # 'bputils>=0.34'
    ],
    test_suite='tests.main',
    zip_safe=False,
)
