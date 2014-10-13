sphinxcontrib-astah
====================
This package contains the astah Sphinx extension.

This extension enable you to embed diagrams by astah_ .
Following code is sample::

  .. astah-image:: [filename]

  .. astah-figure:: [filename]

     caption of figure

.. _astah: http://astah.change-vision.com/

Setting
=======

Install
-------

::

   $ pip install sphinxcontrib-astah


This extension uses astah from commandline. You need to setup astah and Java package.


Configure Sphinx
----------------

Add ``sphinxcontrib.astah`` to ``extensions`` at `conf.py`::

   extensions += ['sphinxcontrib.astah']

And set your API key to ``astah_command_path``::

   astah_command_path = '/path/to/astah-command.sh'


Directive
=========

`.. astah-image:: [filename]`

  This directive insert a diagram into the document.
  If your diagram has multiple sheets, specify sheetid after ``#``.

  Examples::

    .. astah-image:: my-diagram.asta

    .. astah-image:: my-diagram.asta#class-diagram

  Options are same as `image directive`_ .

`.. astah-figure:: [filename]`

  This directive insert a diagram and its caption into the document.

  Examples::

    .. astah-figure:: my-diagram.asta

       Structure of this system

  Options are same as `figure directive`_ .

.. _image directive: http://docutils.sourceforge.net/docs/ref/rst/directives.html#image
.. _figure directive: http://docutils.sourceforge.net/docs/ref/rst/directives.html#figure

Configuration Options
======================

astah_command_path

  path to astah-command.sh (or astah-command.bat)


Repository
==========

This code is hosted by Bitbucket.

  http://bitbucket.org/birkenfeld/sphinx-contrib/
