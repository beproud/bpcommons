#!/usr/bin/env python
#:coding=utf-8:

from setuptools import setup, find_packages

setup(
    name='beproud.django.commons',
    version='0.34',
    description='Common utilities for Django',
    author='BeProud Inc.',
    author_email='ian@beproud.jp',
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
        'Django>=1.2',
        'zenhan>=0.4',
        # 'bputils>=0.34'
    ],
    test_suite='tests.main',
    zip_safe=False,
)
