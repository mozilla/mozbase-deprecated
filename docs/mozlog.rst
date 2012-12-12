:mod:`mozlog` --- Easy, configurable and uniform logging
========================================================

Mozlog is a python package intended to simplify and standardize logs
in the Mozilla universe. It wraps around python's logging module and
adds some additional functionality.

.. automodule:: mozlog
    :members: getLogger

.. autoclass:: MozLogger
    :members: testStart, testEnd, testPass, testFail, testKnownFail

Examples
--------

Log to stdout::

    import mozlog
    log = mozlog.getLogger('MODULE_NAME')
    log.setLevel(mozlog.INFO)
    log.info('This message will be printed to stdout')
    log.debug('This won't')
    log.testPass('A test has passed')
    mozlog.shutdown()

Log to a file::

    import mozlog
    log = mozlog.getLogger('MODULE_NAME', 'path/to/log/file')
    log.warning('Careful!')
    log.testKnownFail('We know the cause for this failure')
    mozlog.shutdown()

.. _logging: http://docs.python.org/library/logging.html
