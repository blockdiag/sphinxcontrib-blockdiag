=======================
sphinxcontrib-blockdiag
=======================

.. image:: https://travis-ci.org/blockdiag/sphinxcontrib-blockdiag.svg?branch=master
   :target: https://travis-ci.org/blockdiag/sphinxcontrib-blockdiag

.. image:: https://coveralls.io/repos/blockdiag/sphinxcontrib-blockdiag/badge.png?branch=master
   :target: https://coveralls.io/r/blockdiag/sphinxcontrib-blockdiag?branch=master

.. image:: https://codeclimate.com/github/blockdiag/sphinxcontrib-blockdiag/badges/gpa.svg
   :target: https://codeclimate.com/github/blockdiag/sphinxcontrib-blockdiag

A sphinx extension for embedding block diagram using blockdiag_.

This extension enables you to insert block diagrams into your document.
Following code is an example::

   .. blockdiag::

      diagram {
        A -> B -> C;
             B -> D;
      }

.. _blockdiag: http://bitbucket.org/blockdiag/blockdiag/


For more details, see `online documentation`_ at http://blockdiag.com/.

.. _online documentation: http://blockdiag.com/en/blockdiag/sphinxcontrib.html
