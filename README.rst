===================
``StringTransform``
===================

This module adds Perl-style transliterations (i.e. ``tr///`` or ``y///``) to
Python 3, as well as the ``s///`` syntax for specifying regular expression
substitutions.
::

  >>> from transform import StringTransform
  >>> st = StringTransform()
  >>> st.addOperation(r'y/A-Za-z0-9_//cd')
  >>> st.addOperation(r'y/_/ /')
  >>> st.addOperation(r'y/a-z//s')
  >>> st.addOperation(r's/([a-z]+)/"\1"/gi')
  >>> st.transform("a/foo-_-bar")
  '"afo" "bar"'
  >>> st.clear()

A ``StringTransform`` object provides these methods:

* ``addOperation`` parses a single ``s`` or ``tr``/``y`` expression and adds
  it to the instance. The separator can be any single non-alphanumeric
  character (e.g. ``tr:SEARCHLIST:REPLACEMENTLIST:``); Perl bracketing
  quotes of the form ``s[][]`` are not supported.

  Permitted flags for transliterations are ``c``, ``d``, and ``s``. They
  have the same meanings as in Perl; from the ``perlop`` man page::

       c   Complement the SEARCHLIST.
       d   Delete found but unreplaced characters.
       s   Squash duplicate replaced characters.

  Allowed substitution flags are ``a``, ``i``, ``l``, ``m``, ``s``, and
  ``x``, corresponding to the ``re.A``, ``re.I``, etc. ``compile()`` flags
  in the Python ``re`` module. Also allowed is an integer specifying the
  maximum number of replacements (the ``count`` argument to ``re.sub()``).
  In addition, the ``g`` flag can be used as a synonym for ``count = 0``
  (replace all occurrences).

* ``addSubstitution`` and ``addTransliteration`` both take 3 string
  arguments: ``SEARCH``, ``REPLACE``, and ``FLAGS``, corresponding to the
  parts of each expression. They're called by ``addOperation`` after an
  expression is split into its component parts.

  The three methods above raise ``StringTransform.ParseError`` if an
  expression is malformed.

* ``transform`` takes a string argument and performs each previously
  compiled transformation on it, in order. It returns the transformed
  string.

* ``clear`` resets the ``StringTransform`` object.


Differences
-----------

* Unlike the Perl ``tr`` operator, the number of replacements is not
  returned.

* String escapes conform to Python syntax.

* For small inputs, the initialization overhead makes ``StringTransform``
  much slower than native Perl. For larger inputs (over 1000 lines), Perl
  remains 3-5 times faster.


Author
------

David Liang (bmdavll at gmail.com)

