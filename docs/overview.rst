Overview
========

Motivation
----------

In the course of writing automated tests at Mozilla, we found that
the same tasks needed to be performed occurred over and over, no
matter what the specific nature of what we were testing.

To help us from writing the same code over and over, we created
libraries embodying the "best practices" for performing these tasks.

Getting information on the system we're testing
-----------------------------------------------

It's often necessary to get some information about the system we're
testing, for example to turn on or off some platform specific
behaviour.

:doc:`mozinfo`

Managing list of tests to run (and when to run them)
----------------------------------------------------

We don't always want to run all tests, all the time. Sometimes a test
may be broken, in other cases we only want to run a test on a specific
platform or build of Mozilla. To handle these cases (and more), we
created a python library to create and use test manifests, which can
codify all this information.

:doc:`manifestdestiny`

Setting up and running the browser/program
------------------------------------------

Activities under this domain include installing the software, creating
a profile (a set of configuration settings), running a program in a
controlled environment such that it can be shut down safely, and
correctly handling the case where the system crashes.

:doc:`mozprofile`

:doc:`mozcrash`

Logging and reporting
---------------------

Ideally output between different types of testing system should be as
uniform as possible, as well as making it easy to make things more or
less verbose. We created some libraries to make doing this easy.

:doc:`mozlog`

Serving up content to be consumed by the browser
------------------------------------------------

I know, right? ANOTHER Python HTTP server? In all seriousness, we
weren't able to find anything out there that was fast enough, flexible
enough, and easy-to-use enough for our needs. So we created our own.

:doc:`mozhttpd`

