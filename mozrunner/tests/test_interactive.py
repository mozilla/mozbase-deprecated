#!/usr/bin/env python

import os
import threading
from time import sleep
import unittest

import mozrunnertest


class RunnerThread(threading.Thread):
    def __init__(self, runner, timeout=10):
        threading.Thread.__init__(self)
        self.runner = runner
        self.timeout = timeout

    def run(self):
        sleep(self.timeout)
        self.runner.stop()


class MozrunnerInteractiveTestCase(mozrunnertest.MozrunnerTestCase):

    def test_run_interactive(self):
        """Bug 965183: Run process in interactive mode and call wait()"""
        pid = self.runner.start(interactive=True)
        self.pids.append(pid)

        thread = RunnerThread(self.runner, 5)
        self.threads.append(thread)
        thread.start()

        # This is a blocking call. So the process should be killed by the thread
        self.runner.wait()
        thread.join()
        self.assertFalse(self.runner.is_running())

    def test_stop_interactive(self):
        """Bug 965183: Explicitely stop process in interactive mode"""
        pid = self.runner.start(interactive=True)
        self.pids.append(pid)

        self.runner.stop()
