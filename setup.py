# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='compressed-deque',
    version='0.1.2',
    description='Compressed Deque',
    long_description=readme,
    author='Pedro Lopes',
    url='https://github.com/lopespm/compressed-deque',
    license=license,
    py_modules=["compdeque"],
    install_requires=[],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
         'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='compressed deque zipped zlib',
)

