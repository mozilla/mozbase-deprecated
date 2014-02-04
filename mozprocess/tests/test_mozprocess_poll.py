#!/usr/bin/env python

import os
import unittest
import proctest
import mozinfo
from mozprocess import processhandler

here = os.path.dirname(os.path.abspath(__file__))

class ProcTestPoll(proctest.ProcTest):
    """ Class to test process poll """

    def test_process_poll_before_run(self):
        """Process is not started, and poll() is called"""

        p = processhandler.ProcessHandler([self.python, self.proclaunch,
                                          "process_normal_finish_python.ini"],
                                          cwd=here)
        self.assertRaises(AttributeError, p.poll)

    def test_process_poll_while_running(self):
        """Process is started, and poll() is called"""

        p = processhandler.ProcessHandler([self.python, self.proclaunch,
                                          "process_normal_finish_python.ini"],
                                          cwd=here)
        p.run()
        returncode = p.poll()

        self.assertEqual(returncode, None)

        detected, output = proctest.check_for_process(self.proclaunch)
        self.determine_status(detected,
                              output,
                              returncode,
                              p.didTimeout,
                              True)
        p.kill()

    @unittest.skip('Bug 967782 - Calling poll() after kill() should not return None')
    def test_process_poll_after_run(self):
        """Process is killed, and poll() is called"""

        p = processhandler.ProcessHandler([self.python, self.proclaunch,
                                          "process_normal_finish_python.ini"],
                                          cwd=here)
        p.run()
        p.kill()
        returncode = p.poll()

        self.assertNotIn(returncode, [None, 0])

        detected, output = proctest.check_for_process(self.proclaunch)
        self.determine_status(detected,
                              output,
                              returncode,
                              p.didTimeout)

if __name__ == '__main__':
    unittest.main()
