=====================
sphinxcontrib-actdiag
=====================

A sphinx extension for embedding activity diagram using actdiag_.

This extension enables you to insert activity diagrams into your document.
Following code is an example::

   .. actdiag::

      actdiag {
        A -> B -> C -> D;

        lane {
          A; B;
        }
        lane {
          C; D;
        }
      }

.. _actdiag: http://bitbucket.org/blockdiag/actdiag/


For more details, see `online documentation`_ at http://blockdiag.com/.

.. _online documentation: http://blockdiag.com/en/actdiag/sphinxcontrib.html
