#!/usr/bin/env python

from setuptools import setup

setup(
    name='draughtsman',
    version='0.1.0',
    description='API Blueprint Parser for Python',
    url='https://github.com/kylef/draughtsman',
    packages=['draughtsman'],
    author='Kyle Fuller',
    author_email='kyle@fuller.li',
    license='BSD',
    install_requires=('cffi', 'refract==0.3.0'),
    classifiers=(
      'Development Status :: 5 - Production/Stable',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'License :: OSI Approved :: BSD License',
    )
)
