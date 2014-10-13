# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = open('README.rst').read()

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-cacoo',
    version='0.1.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-cacoo',
    license='BSD',
    author='Takeshi KOMIYA',
    author_email='i.tkomiya@gmail.com',
    description='Sphinx "cacoo" extension; embed diagram from cacoo',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
