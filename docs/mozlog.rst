mozlog
======

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
