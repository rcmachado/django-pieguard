#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import pieguard


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = pieguard.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-pieguard',
    version=version,
    description=('django-pieguard is a simple authorization class for tastypie'
                 ' that uses django-guardian to handle object permissions.'),
    long_description=readme + '\n\n' + history,
    author='Rodrigo Machado',
    author_email='rcmachado@gmail.com',
    url='https://github.com/rcmachado/django-pieguard',
    packages=[
        'pieguard',
    ],
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    tests_require=parse_requirements('requirements-test.txt'),
    license="MIT",
    zip_safe=False,
    keywords='django-pieguard',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests.runtests.runtests',
)
