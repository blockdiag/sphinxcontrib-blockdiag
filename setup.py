# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the blockdiag Sphinx extension.

.. _Sphinx: http://sphinx.pocoo.org/
.. _blockdiag: http://blockdiag.com/en/blockdiag/

This extension enable you to insert block diagrams in your Sphinx document.
Following code is sample::

   .. blockdiag::

      diagram {
        A -> B -> C;
             B -> D;
      }


This module needs blockdiag_.
'''

requires = ['blockdiag>=1.4.1', 'Sphinx>=0.6', 'setuptools']

setup(
    name='sphinxcontrib-blockdiag',
    version='1.4.3',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-blockdiag',
    license='BSD',
    author='Takeshi Komiya',
    author_email='i.tkomiya@gmail.com',
    description='Sphinx "blockdiag" extension',
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
