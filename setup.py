# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requires = ['blockdiag>=1.5.0', 'Sphinx>=2.0']

setup(
    name='sphinxcontrib-blockdiag',
    version='3.0.0',
    url='https://github.com/blockdiag/sphinxcontrib-blockdiag',
    license='BSD',
    author='Takeshi KOMIYA',
    author_email='i.tkomiya@gmail.com',
    description='Sphinx "blockdiag" extension',
    long_description=open("README.rst").read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
