=======================
sphinxcontrib-blockdiag
=======================

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
