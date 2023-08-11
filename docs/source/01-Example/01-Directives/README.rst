Directives
==============================================================================


Admonition
------------------------------------------------------------------------------
.. note::

    This is note

.. admonition:: Look ma! A custom title.

   It looks different though.

.. admonition:: Another Custom Title
   :class: note

   Maaa! I made it look the same by setting the class.

.. note::

   You can nest admonitions.

   .. warning::

      But you really should not.

      .. danger::

         It's distracting.

      And can be confusing for the user to understand.

   And, honestly, looks weird.


Badge
------------------------------------------------------------------------------
:bdg:`plain badge`

:bdg-primary:`primary`, :bdg-primary-line:`primary-line`

:bdg-secondary:`secondary`, :bdg-secondary-line:`secondary-line`

:bdg-success:`success`, :bdg-success-line:`success-line`

:bdg-info:`info`, :bdg-info-line:`info-line`

:bdg-warning:`warning`, :bdg-warning-line:`warning-line`

:bdg-danger:`danger`, :bdg-danger-line:`danger-line`

:bdg-light:`light`, :bdg-light-line:`light-line`

:bdg-dark:`dark`, :bdg-dark-line:`dark-line`


Dropdown
------------------------------------------------------------------------------
.. dropdown::

    Dropdown content

.. dropdown:: Dropdown title

    Dropdown content

.. dropdown:: Open dropdown
    :open:

    Dropdown content


Card
------------------------------------------------------------------------------
.. card:: Card Title

    Card content

.. card:: Card Title

    Header
    ^^^
    Card content
    +++
    Footer


Button
------------------------------------------------------------------------------
.. button-link:: https://example.com

.. button-link:: https://example.com

    Button text

.. button-link:: https://example.com
    :color: primary
    :shadow:

.. button-link:: https://example.com
    :color: primary
    :outline:

.. button-link:: https://example.com
    :color: secondary
    :expand:
