#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import errno
import os
import subprocess
import sys

import mozfile
from mozprocess.processhandler import ProcessHandler


def compile_executables():
    '''Function compiles all assets connected to tests'''
    here = os.path.abspath(os.path.dirname(__file__))

    executable = os.path.join(here, 'firefox.exe')
    stub_example_c = os.path.join(here, 'firefox.c')
    stub_example_rc = os.path.join(here, 'firefox.rc')
    stub_example_res = os.path.join(here, 'firefox.res')
    stub_example_obj = os.path.join(here, 'firefox.obj')

    if os.path.exists(executable):
        print "Removing existing browser stub: %s" % executable
        mozfile.remove(executable)

    commands = [
        # For browser we need to generate resource file
        # because is_installer needs to check PE Headers
        ['rc.exe', stub_example_rc],

        # And then we compile next version of browser file which
        # contains tested PE Header ('BuildID')
        ['cl.exe', stub_example_c, stub_example_res],
    ]

    for command in commands:
        print "Executing command: %s" % (' '.join(command),)
        try:
            process = ProcessHandler(command)
            process.run(timeout=20)
            returncode = process.wait()
            if returncode:
                raise subprocess.CalledProcessError(returncode, command, output)

        except OSError, e:
            if e.errno == errno.ENOENT:
                print "Missing %s" % command[0]
                print  "Visual C++ and Windows Platform SDK are required."
                sys.exit(e.errno)
            raise

    print "Removing temporary files: %s %s" % (stub_example_res, stub_example_obj)
    mozfile.remove(stub_example_res)
    mozfile.remove(stub_example_obj)


if __name__ == '__main__':
    compile_executables()
